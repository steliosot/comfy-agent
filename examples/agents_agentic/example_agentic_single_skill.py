from comfy_agent import reasoning_agentic, run_agentic

prompt = "cinematic product photo of a bottle of Coca-Cola on a kitchen counter, realistic lighting"
# prompt = "cinematic product video clip of a bottle of Coca-Cola on a kitchen counter, realistic lighting"

reasoning_agentic(prompt=prompt, print_output=True)

result = run_agentic(
    prompt=prompt,
    print_reasoning=False,
)

print(result)
