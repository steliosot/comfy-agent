from comfy_agent import reasoning_agentic, run_agentic

prompt = "generate a bottle of Coca-Cola and then crop it to wide screen 1280x720"

reasoning_agentic(prompt=prompt, print_output=True)

result = run_agentic(
    prompt=prompt,
    print_reasoning=False,
)

print(result)
