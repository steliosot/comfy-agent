import unittest

from comfy_agent.optimizations import apply_optimization_profile, build_optimization_profile
from comfy_agent.workflow import Workflow
from unit_tests.test_helpers import mocked_comfy_api


class OptimizationProfilesTests(unittest.TestCase):
    def test_build_profile_none(self):
        profile = build_optimization_profile(mode="none")
        self.assertEqual(profile["mode"], "none")
        self.assertFalse(profile["workflow"]["cache_enabled"])
        self.assertFalse(profile["workflow"]["memoization_enabled"])
        self.assertFalse(profile["model_manager"]["enabled"])

    def test_build_profile_full_stack(self):
        profile = build_optimization_profile(mode="full_stack", cache_size=64, max_models_in_vram=2)
        self.assertTrue(profile["workflow"]["cache_enabled"])
        self.assertTrue(profile["workflow"]["memoization_enabled"])
        self.assertEqual(profile["workflow"]["cache_size"], 64)
        self.assertTrue(profile["model_manager"]["enabled"])
        self.assertEqual(profile["model_manager"]["max_models_in_vram"], 2)
        self.assertTrue(profile["attention_reuse"]["enabled"])

    def test_build_profile_attention_reuse(self):
        profile = build_optimization_profile(
            mode="attention_reuse",
            attn_reuse_threshold=0.7,
            attn_cache_device="cpu",
            attn_store_frequency=3,
            attn_reuse_layers=["cross_attention"],
        )
        self.assertEqual(profile["mode"], "attention_reuse")
        self.assertFalse(profile["workflow"]["cache_enabled"])
        self.assertFalse(profile["model_manager"]["enabled"])
        self.assertTrue(profile["attention_reuse"]["enabled"])
        self.assertEqual(profile["attention_reuse"]["threshold"], 0.7)
        self.assertEqual(profile["attention_reuse"]["store_frequency"], 3)

    def test_build_profile_attention_reuse_cpu_offload(self):
        profile = build_optimization_profile(mode="attention_reuse_cpu_offload", max_models_in_vram=2)
        self.assertEqual(profile["mode"], "attention_reuse_cpu_offload")
        self.assertTrue(profile["attention_reuse"]["enabled"])
        self.assertTrue(profile["model_manager"]["enabled"])

    def test_build_profile_attention_reuse_wan21(self):
        profile = build_optimization_profile(mode="attention_reuse_wan21")
        self.assertEqual(profile["mode"], "attention_reuse_wan21")
        self.assertTrue(profile["attention_reuse"]["enabled"])
        self.assertEqual(
            profile["attention_reuse"]["reuse_layers"],
            ["cross_attention", "temporal_attention", "transformer_attention"],
        )

    def test_build_profile_attention_reuse_wan21_cpu_offload(self):
        profile = build_optimization_profile(mode="attention_reuse_wan21_cpu_offload", max_models_in_vram=2)
        self.assertEqual(profile["mode"], "attention_reuse_wan21_cpu_offload")
        self.assertTrue(profile["attention_reuse"]["enabled"])
        self.assertTrue(profile["model_manager"]["enabled"])
        self.assertTrue(profile["model_manager"]["enable_cpu_offload"])
        self.assertEqual(profile["model_manager"]["max_models_in_vram"], 2)

    def test_apply_profile_to_workflow(self):
        profile = build_optimization_profile(mode="full_stack", cache_size=32, max_models_in_vram=3)
        with mocked_comfy_api():
            wf = Workflow()
            apply_optimization_profile(wf, profile)

        self.assertTrue(wf.cache_enabled)
        self.assertTrue(wf.memoization_enabled)
        self.assertEqual(wf.cache_size, 32)
        self.assertEqual(wf.model_manager.max_models_in_vram, 3)
        self.assertTrue(wf.attention_reuse_plugin.enabled)

    def test_build_profile_rejects_unknown_mode(self):
        with self.assertRaises(ValueError):
            build_optimization_profile(mode="not_a_mode")


if __name__ == "__main__":
    unittest.main()
