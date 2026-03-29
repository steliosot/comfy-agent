from comfy_agent.job import Job, Executor
from skills.workflows.txt2img.generate_sd15_image.skill import run as generate_image


class ImageAgent:
    def run(self, prompt):
        jobs = [
            Job(generate_image, prompt=prompt),
            Job(generate_image, prompt=prompt + " cinematic lighting"),
            Job(generate_image, prompt=prompt + " sunset"),
        ]

        executor = Executor()
        return executor.run_parallel(jobs)


if __name__ == "__main__":
    agent = ImageAgent()
    results = agent.run("greek island with white houses and blue sea")
    print(results)
