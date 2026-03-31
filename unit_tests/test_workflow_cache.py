import unittest

from comfy_agent.cache_utils import hash_value
from comfy_agent.workflow import Workflow
from unit_tests.test_helpers import mocked_comfy_api


class _Adapter:
    def __init__(self):
        self.attach_calls = 0
        self.detach_calls = 0

    def is_compatible(self, model_obj):
        return model_obj is not None

    def attach(self, model_obj, plugin_runtime):
        self.attach_calls += 1
        return {"model": model_obj}

    def detach(self, handle):
        self.detach_calls += 1


class WorkflowCacheTests(unittest.TestCase):
    def _build_basic(self):
        wf = Workflow()
        (
            wf
            .checkpoint("sd1.5/juggernaut_reborn.safetensors")
            .prompt("robot")
            .negative("bad")
            .latent(512, 512)
            .sample(seed=1, steps=20)
            .decode()
            .save("robot")
        )
        return wf

    def test_hash_value_is_order_independent_for_dicts(self):
        left = {"b": 2, "a": {"y": [1, 2], "x": 3}}
        right = {"a": {"x": 3, "y": [1, 2]}, "b": 2}
        self.assertEqual(hash_value(left), hash_value(right))

    def test_cache_short_circuits_identical_second_run(self):
        with mocked_comfy_api() as posted:
            wf = self._build_basic().enable_cache().enable_memoization()
            first = wf.run(target="save")
            second = wf.run(target="save")

        self.assertEqual(first.get("prompt_id"), "test-prompt")
        self.assertEqual(second.get("prompt_id"), "test-prompt")
        self.assertEqual(len(posted), 1)

    def test_cache_without_memoization_still_posts(self):
        with mocked_comfy_api() as posted:
            wf = self._build_basic().enable_cache().disable_memoization()
            wf.run(target="save")
            wf.run(target="save")

        self.assertEqual(len(posted), 2)

    def test_prompt_change_recomputes_downstream_only(self):
        with mocked_comfy_api():
            wf = self._build_basic().enable_cache()
            wf.run(target="save")
            wf.override({"prompt.text": "robot updated"})
            result = wf.run(target="save", debug=True)

        trace = result.get("execution_trace") or []
        by_node = {item["node_id"]: item["event"] for item in trace if item["event"] in {"execute", "cache_hit"}}
        self.assertEqual(by_node.get("1"), "cache_hit")  # Checkpoint
        self.assertEqual(by_node.get("2"), "execute")  # Positive prompt encode
        self.assertEqual(by_node.get("5"), "execute")  # KSampler

    def test_seed_change_recomputes_sampler_branch(self):
        with mocked_comfy_api():
            wf = self._build_basic().enable_cache()
            wf.run(target="save")
            wf.override({"ksampler.seed": 2})
            result = wf.run(target="save", debug=True)

        trace = result.get("execution_trace") or []
        by_node = {item["node_id"]: item["event"] for item in trace if item["event"] in {"execute", "cache_hit"}}
        self.assertEqual(by_node.get("1"), "cache_hit")  # Checkpoint unchanged
        self.assertEqual(by_node.get("2"), "cache_hit")  # Prompt encode unchanged
        self.assertEqual(by_node.get("5"), "execute")  # KSampler changed by seed

    def test_model_change_forces_full_recompute(self):
        with mocked_comfy_api():
            wf = self._build_basic().enable_cache()
            wf.run(target="save")
            wf.override({"checkpoint.ckpt_name": "sd1.5/other_model.safetensors"})
            result = wf.run(target="save", debug=True)

        trace = result.get("execution_trace") or []
        by_node = {item["node_id"]: item["event"] for item in trace if item["event"] in {"execute", "cache_hit"}}
        self.assertEqual(by_node.get("1"), "execute")
        self.assertEqual(by_node.get("2"), "execute")
        self.assertEqual(by_node.get("3"), "execute")
        self.assertEqual(by_node.get("5"), "execute")
        self.assertEqual(by_node.get("6"), "execute")
        self.assertEqual(by_node.get("7"), "execute")

    def test_partial_run_omits_unrelated_nodes(self):
        with mocked_comfy_api() as posted:
            wf = self._build_basic()
            wf.preview()
            wf.run(target="save")

        self.assertEqual(len(posted), 1)
        prompt = posted[0]["json"]["prompt"]
        class_types = {item["class_type"] for item in prompt.values()}
        self.assertIn("SaveImage", class_types)
        self.assertNotIn("PreviewImage", class_types)

    def test_partial_run_supports_indexed_selector(self):
        with mocked_comfy_api() as posted:
            wf = self._build_basic()
            wf.save("robot_2")
            wf.run(target="save[0]")

        prompt = posted[0]["json"]["prompt"]
        save_nodes = [node_id for node_id, item in prompt.items() if item["class_type"] == "SaveImage"]
        self.assertEqual(save_nodes, ["7"])

    def test_run_without_target_keeps_backward_compatible_full_submission(self):
        with mocked_comfy_api() as posted:
            wf = self._build_basic()
            wf.preview()
            wf.run()

        prompt = posted[0]["json"]["prompt"]
        class_types = {item["class_type"] for item in prompt.values()}
        self.assertIn("PreviewImage", class_types)
        self.assertIn("SaveImage", class_types)

    def test_execution_metrics_shape_present(self):
        with mocked_comfy_api():
            wf = self._build_basic().enable_cache()
            result = wf.run(target="save")

        metrics = result.get("execution_metrics")
        self.assertIsInstance(metrics, dict)
        self.assertIn("executed_nodes", metrics)
        self.assertIn("cache_hits", metrics)
        self.assertIn("cache_misses", metrics)
        self.assertIn("sampler_runs", metrics)

    def test_attention_reuse_toggle_does_not_break_run(self):
        with mocked_comfy_api():
            wf = self._build_basic()
            wf.enable_attention_reuse()
            result = wf.run(target="save")
            wf.disable_attention_reuse()

        self.assertIn("execution_metrics", result)
        self.assertIn("attn_fallback", result["execution_metrics"])

    def test_attention_reuse_adapter_attach_detach_is_called(self):
        with mocked_comfy_api():
            wf = self._build_basic()
            adapter = _Adapter()
            wf.set_attention_reuse_adapter(adapter)
            wf.enable_attention_reuse()
            wf.run(target="save")

        self.assertEqual(adapter.attach_calls, 1)
        self.assertEqual(adapter.detach_calls, 1)


if __name__ == "__main__":
    unittest.main()
