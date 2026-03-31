import unittest

from comfy_agent.attention_reuse_plugin import AttentionReusePlugin, AutoModuleAttentionReuseAdapter


class DummyTensor:
    def __init__(self, name="t"):
        self.name = name
        self.detached = False
        self.device = "cuda"

    def detach(self):
        clone = DummyTensor(self.name)
        clone.detached = True
        clone.device = self.device
        return clone

    def to(self, device):
        self.device = str(device)
        return self


class DummyAdapter:
    def __init__(self, compatible=True):
        self.compatible = compatible
        self.attached = 0
        self.detached = 0

    def is_compatible(self, model_obj):
        return self.compatible and model_obj is not None

    def attach(self, model_obj, plugin_runtime):
        self.attached += 1
        self.runtime = plugin_runtime
        return {"model": model_obj}

    def detach(self, handle):
        self.detached += 1


class DummyVideoAttentionModule:
    def __init__(self):
        self.calls = 0

    def forward(self, x, **kwargs):
        self.calls += 1
        return x


class DummyVideoModel:
    def __init__(self):
        self.temporal_block_3 = DummyVideoAttentionModule()

    def named_modules(self):
        return [
            ("temporal_block_3.attention", self.temporal_block_3),
        ]


class AttentionReusePluginTests(unittest.TestCase):
    def test_store_and_reuse_respects_threshold_and_later_steps(self):
        plugin = AttentionReusePlugin()
        plugin.enable(threshold=0.6, store_frequency=2, reuse_layers=["cross_attention"], debug=False)

        # step 2/10 is below threshold -> not stored
        stored_early = plugin.store_attention(
            model_id="m1",
            layer_id="l1",
            step=2,
            total_steps=10,
            attention_kind="cross_attention",
            prompt_fingerprint="p1",
            attention_tensor=DummyTensor(),
        )
        self.assertFalse(stored_early)

        # step 8/10 and divisible by 2 -> stored
        stored_late = plugin.store_attention(
            model_id="m1",
            layer_id="l1",
            step=8,
            total_steps=10,
            attention_kind="cross_attention",
            prompt_fingerprint="p1",
            attention_tensor=DummyTensor(),
        )
        self.assertTrue(stored_late)

        # reuse on later step -> hit
        reused = plugin.load_reusable_attention(
            model_id="m1",
            layer_id="l1",
            step=10,
            total_steps=10,
            attention_kind="cross_attention",
            prompt_fingerprint="p1",
        )
        self.assertIsNotNone(reused)
        self.assertEqual(plugin.run_stats()["attn_reuse"], 1)

    def test_strict_prompt_mismatch_falls_back(self):
        plugin = AttentionReusePlugin()
        plugin.enable(threshold=0.6, store_frequency=1, reuse_layers=["cross_attention"], debug=False)

        plugin.store_attention(
            model_id="m1",
            layer_id="l1",
            step=7,
            total_steps=10,
            attention_kind="cross_attention",
            prompt_fingerprint="p1",
            attention_tensor=DummyTensor(),
        )

        reused = plugin.load_reusable_attention(
            model_id="m1",
            layer_id="l1",
            step=8,
            total_steps=10,
            attention_kind="cross_attention",
            prompt_fingerprint="other",
        )
        self.assertIsNone(reused)
        self.assertGreaterEqual(plugin.run_stats()["attn_fallback"], 1)

    def test_tensor_is_detached_and_moved_to_cache_device(self):
        plugin = AttentionReusePlugin()
        plugin.enable(threshold=0.6, cache_device="cpu", store_frequency=1, reuse_layers=["cross_attention"], debug=False)
        tensor = DummyTensor()

        plugin.store_attention(
            model_id="m1",
            layer_id="l1",
            step=7,
            total_steps=10,
            attention_kind="cross_attention",
            prompt_fingerprint="p1",
            attention_tensor=tensor,
        )

        self.assertEqual(len(plugin.cache), 1)
        cached = next(iter(plugin.cache.values())).tensor
        self.assertTrue(cached.detached)
        self.assertEqual(cached.device, "cpu")

    def test_begin_run_with_missing_adapter_is_safe_fallback(self):
        plugin = AttentionReusePlugin()
        plugin.enable(debug=False)
        plugin.begin_run({"model_id": "m1", "model_obj": object()})
        self.assertGreaterEqual(plugin.run_stats()["attn_fallback"], 1)

    def test_begin_end_run_with_compatible_adapter_attach_and_detach(self):
        plugin = AttentionReusePlugin()
        adapter = DummyAdapter(compatible=True)
        plugin.set_adapter(adapter)
        plugin.enable(debug=False)

        plugin.begin_run({"model_id": "m1", "model_obj": object()})
        plugin.end_run()

        self.assertEqual(adapter.attached, 1)
        self.assertEqual(adapter.detached, 1)

    def test_shape_and_runtime_signature_gate_reuse(self):
        plugin = AttentionReusePlugin()
        plugin.enable(threshold=0.6, store_frequency=1, reuse_layers=["cross_attention", "temporal_attention"], debug=False)
        plugin.begin_run(
            {
                "model_id": "ltx-video-2b-v0.9.5.safetensors",
                "model_obj": object(),
                "prompt_fingerprint": "p1",
                "total_steps": 10,
                "seed": 123,
                "frame_count": 49,
                "scheduler": "normal",
                "model_type": "video",
            }
        )

        plugin.store_attention(
            model_id="ltx-video-2b-v0.9.5.safetensors",
            layer_id="temporal_block_3",
            step=8,
            total_steps=10,
            attention_kind="temporal_attention",
            prompt_fingerprint="p1",
            attention_tensor=DummyTensor("t_video"),
            attention_shape=(1, 49, 64, 128),
            runtime_signature=plugin._runtime_signature(),
        )

        # shape mismatch => no reuse
        miss_shape = plugin.load_reusable_attention(
            model_id="ltx-video-2b-v0.9.5.safetensors",
            layer_id="temporal_block_3",
            step=9,
            total_steps=10,
            attention_kind="temporal_attention",
            prompt_fingerprint="p1",
            attention_shape=(1, 33, 64, 128),
            runtime_signature=plugin._runtime_signature(),
        )
        self.assertIsNone(miss_shape)

        # matching shape and runtime => reuse
        hit = plugin.load_reusable_attention(
            model_id="ltx-video-2b-v0.9.5.safetensors",
            layer_id="temporal_block_3",
            step=9,
            total_steps=10,
            attention_kind="temporal_attention",
            prompt_fingerprint="p1",
            attention_shape=(1, 49, 64, 128),
            runtime_signature=plugin._runtime_signature(),
        )
        self.assertIsNotNone(hit)

    def test_auto_adapter_patches_attention_layer_forward(self):
        plugin = AttentionReusePlugin()
        plugin.set_adapter(AutoModuleAttentionReuseAdapter())
        plugin.enable(threshold=0.6, store_frequency=1, reuse_layers=["temporal_attention"], debug=False)

        model = DummyVideoModel()
        plugin.begin_run(
            {
                "model_id": "ltx-video-2b-v0.9.5.safetensors",
                "model_obj": model,
                "prompt_fingerprint": "p_video",
                "total_steps": 10,
                "seed": 777,
                "frame_count": 49,
                "scheduler": "normal",
            }
        )
        # First call computes + stores.
        _ = model.temporal_block_3.forward(DummyTensor("tensor"), step=8)
        # Second call should reuse from cache and skip underlying call count increment.
        before = model.temporal_block_3.calls
        _ = model.temporal_block_3.forward(DummyTensor("tensor"), step=9)
        after = model.temporal_block_3.calls
        plugin.end_run()

        self.assertGreater(plugin.run_stats()["attn_store"], 0)
        self.assertGreater(plugin.run_stats()["attn_reuse"], 0)
        self.assertEqual(before, after)


if __name__ == "__main__":
    unittest.main()
