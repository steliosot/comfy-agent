import unittest

from comfy_agent.model_manager import ModelManager


class DummyModel:
    def __init__(self, name):
        self.name = name
        self.device = "cpu"

    def to(self, device):
        self.device = str(device)
        return self


class ModelManagerTests(unittest.TestCase):
    def test_lazy_load_only_on_first_request(self):
        calls = []

        def loader(name):
            calls.append(name)
            return DummyModel(name)

        manager = ModelManager(loader=loader)
        manager.get_model("a")
        manager.get_model("a")

        self.assertEqual(calls, ["a"])
        stats = manager.stats()
        self.assertEqual(stats["disk_loads"], 1)
        self.assertEqual(stats["vram_hits"], 1)

    def test_lru_updates_on_vram_hit(self):
        manager = ModelManager(
            max_models_in_vram=2,
            enable_cpu_offload=True,
            loader=lambda n: DummyModel(n),
        )
        manager.get_model("a")
        manager.get_model("b")
        manager.get_model("a")

        self.assertEqual(manager.stats()["vram_models"], ["b", "a"])

    def test_eviction_moves_oldest_to_cpu_when_enabled(self):
        manager = ModelManager(
            max_models_in_vram=1,
            enable_cpu_offload=True,
            loader=lambda n: DummyModel(n),
        )
        manager.get_model("a")
        manager.get_model("b")

        stats = manager.stats()
        self.assertEqual(stats["vram_models"], ["b"])
        self.assertEqual(stats["cpu_models"], ["a"])
        self.assertEqual(stats["evictions_to_cpu"], 1)

    def test_eviction_drops_model_when_cpu_offload_disabled(self):
        manager = ModelManager(
            max_models_in_vram=1,
            enable_cpu_offload=False,
            loader=lambda n: DummyModel(n),
        )
        manager.get_model("a")
        manager.get_model("b")

        stats = manager.stats()
        self.assertEqual(stats["vram_models"], ["b"])
        self.assertEqual(stats["cpu_models"], [])
        self.assertEqual(stats["evictions_dropped"], 1)

    def test_cpu_hit_moves_back_to_vram(self):
        manager = ModelManager(
            max_models_in_vram=1,
            enable_cpu_offload=True,
            loader=lambda n: DummyModel(n),
        )
        manager.get_model("a")
        manager.get_model("b")
        model = manager.get_model("a")

        stats = manager.stats()
        self.assertEqual(model.device, "cuda")
        self.assertEqual(stats["cpu_hits"], 1)
        self.assertEqual(stats["vram_models"], ["a"])

    def test_stats_include_expected_keys(self):
        manager = ModelManager(loader=lambda n: DummyModel(n))
        manager.get_model("a")
        stats = manager.stats()

        self.assertIn("requests", stats)
        self.assertIn("disk_loads", stats)
        self.assertIn("total_load_time_s", stats)
        self.assertIn("vram_models", stats)
        self.assertIn("cpu_models", stats)


if __name__ == "__main__":
    unittest.main()
