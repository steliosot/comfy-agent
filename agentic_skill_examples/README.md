# Agentic Skill Examples

These examples demonstrate an agnostic reasoning layer that:

- analyzes prompt intent
- selects skill(s) with confidence scores
- executes the selected plan

Examples:

- `example_agentic_single_skill.py`: generate a Coke bottle image with one skill
- `example_agentic_generate_then_crop.py`: generate a Coke bottle and then crop to widescreen in one workflow run

## Cloud run

```bash
export COMFY_URL=http://34.30.216.121
export COMFY_AUTH_HEADER=XXXXXX

PYTHONPATH=. python3 agentic_skill_examples/example_agentic_single_skill.py
PYTHONPATH=. python3 agentic_skill_examples/example_agentic_generate_then_crop.py
```
