from comfy_agent import reasoning_agentic


PROMPTS = [
    "cinematic product photo of a bottle of Coca-Cola on a kitchen counter, realistic lighting",
    "generate a rusty robot and then crop it to 256x256 at x=96 y=64",
    "please crop this image to wide screen 1280x720",
    "create a cute 3D-rendered cartoon cat animation and export as video/h264-mp4",
    "make something cool",
]


for index, prompt in enumerate(PROMPTS, start=1):
    print(f"\n=== Reasoning Case {index} ===")
    print(f"Prompt: {prompt}")
    reasoning_agentic(prompt=prompt, print_output=True)
