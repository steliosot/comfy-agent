from comfy_agent.job import Job, Executor
from skills.workflows.txt2img.generate_sd15_lora.skill import run as lora_image
from skills.workflows.txt2img.generate_sd15_image.skill import run as base_image
from skills.workflows.txt2img.preview_sd15_image.skill import run as preview_image


class LoraComboAgent:
    def run(self):
        jobs = [
            Job(
                lora_image,
                prompt="luxury sneaker product photo on dark studio background",
                lora="sd15/CakeStyle.safetensors",
                strength=1.0,
            ),
            Job(
                base_image,
                prompt="luxury sneaker product photo on marble pedestal",
                steps=30,
            ),
            Job(
                preview_image,
                prompt="fashion campaign portrait for a premium shoe brand",
            ),
        ]

        return Executor().run_parallel(jobs)


if __name__ == "__main__":
    agent = LoraComboAgent()
    print(agent.run())
