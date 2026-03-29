from comfy_agent.job import Job, Executor
from skills.workflows.video_t2v_i2v_avatar.generate_sd15_animated_webp.skill import run as animated_webp
from skills.workflows.txt2img.generate_sd15_stelios_shoe_ad.skill import run as shoe_ad
from skills.workflows.txt2img.generate_sd15_cinematic_portrait.skill import run as portrait


class MotionComboAgent:
    def run(self):
        jobs = [
            Job(
                animated_webp,
                prompt="stylized robot walking through a rainy neon alley",
                batch_size=6,
                fps=6,
            ),
            Job(
                shoe_ad,
                prompt="cinematic advertisement for Stelios shoes in London streets",
                batch_size=24,
                fps=6,
            ),
            Job(
                portrait,
                prompt="cinematic portrait of a fashion model wearing premium shoes",
            ),
        ]

        return Executor().run_parallel(jobs)


if __name__ == "__main__":
    agent = MotionComboAgent()
    print(agent.run())
