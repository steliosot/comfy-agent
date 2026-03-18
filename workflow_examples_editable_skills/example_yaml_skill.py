from comfy_agent import load_yaml_skill


wf = load_yaml_skill(
    "workflow_examples_editable_skills/generate_sd15_image.yaml",
    prompt="cinematic robot",
    negative_prompt="watermark, text",
)

wf.inspect()
wf.run()
