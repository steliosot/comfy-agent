from comfy_agent.job import Executor, Job
from skills.generate_sd15_cinematic_portrait.skill import build as build_portrait
from skills.generate_sd15_image.skill import build as build_image
from skills.generate_sd15_landscape_batch.skill import build as build_landscape


def run_overridden_portrait():
    wf = build_portrait(prompt="cinematic portrait of a futuristic courier")
    wf.override(
        {
            "ksampler.cfg": 8.5,
            "ksampler.steps": 28,
            "save.filename_prefix": "agent_portrait_override",
        }
    )
    wf.run()
    return {"status": "done", "output": "agent_portrait_override"}


def run_overridden_image():
    wf = build_image(prompt="premium product shot of luxury shoes")
    wf.override(
        {
            "ksampler.steps": 24,
            "save.filename_prefix": "agent_image_override",
        }
    )
    wf.run()
    return {"status": "done", "output": "agent_image_override"}


def run_overridden_landscape():
    wf = build_landscape(prompt="cinematic Santorini cliffs at sunset", batch_size=2)
    wf.override(
        {
            "save.filename_prefix": "agent_landscape_override",
        }
    )
    wf.run()
    return {"status": "done", "output": "agent_landscape_override"}


class BuildableOverrideAgent:
    def run(self):
        jobs = [
            Job(run_overridden_portrait),
            Job(run_overridden_image),
            Job(run_overridden_landscape),
        ]

        return Executor().run_parallel(jobs)


if __name__ == "__main__":
    agent = BuildableOverrideAgent()
    print(agent.run())
