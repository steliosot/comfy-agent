from comfy_agent.job import Job, Executor
from skills.workflows.txt2img.generate_sd15_cinematic_portrait.skill import run as portrait
from skills.workflows.txt2img.generate_sd15_landscape_batch.skill import run as landscape_batch
from skills.workflows.txt2img.preview_sd15_fast_character.skill import run as fast_character_preview


class MixedStillsAgent:
    def run(self):
        jobs = [
            Job(
                portrait,
                prompt="cinematic portrait of a stylish traveler in Athens",
            ),
            Job(
                landscape_batch,
                prompt="dramatic mediterranean coastline at sunrise",
                batch_size=2,
            ),
            Job(
                fast_character_preview,
                prompt="stylized explorer character with elegant boots",
            ),
        ]

        return Executor().run_parallel(jobs)


if __name__ == "__main__":
    agent = MixedStillsAgent()
    print(agent.run())
