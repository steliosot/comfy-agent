# Agentic Skill Examples

These examples demonstrate an agnostic reasoning layer that:

- analyzes prompt intent
- selects skill(s) with confidence scores
- executes the selected plan

Examples:

- `example_agentic_single_skill.py`: generate a Coke bottle image with one skill
- `example_agentic_generate_then_crop.py`: generate a Coke bottle and then crop to widescreen in one workflow run
- `example_agentic_video_clip.py`: route to generic WAN video clip skill (`video/h264-mp4`)
- `example_reasonings_agentic.py`: reasoning-only matrix with multiple prompts
- `example_upload_crop_download.py`: upload local image -> crop skill -> download outputs
- `example_agentic_compose_two_images.py`: compose single-purpose skills with two refs
- `example_agentic_compose_three_images.py`: compose single-purpose skills with three refs

## Cloud run

```bash
export COMFY_URL=http://34.27.83.101
export COMFY_AUTH_HEADER=YOUR_AUTH_KEY
export COMFY_INPUT_DIR=tmp/inputs
export COMFY_OUTPUT_DIR=tmp/outputs
export EXAMPLE_INPUT_IMAGE=/absolute/path/to/redhead_portrait.png

PYTHONPATH=. python3 examples/agents_agentic/example_agentic_single_skill.py
PYTHONPATH=. python3 examples/agents_agentic/example_agentic_generate_then_crop.py
PYTHONPATH=. python3 examples/agents_agentic/example_agentic_video_clip.py
PYTHONPATH=. python3 examples/agents_agentic/example_reasonings_agentic.py
PYTHONPATH=. python3 examples/agents_agentic/example_upload_crop_download.py
PYTHONPATH=. python3 examples/agents_agentic/example_agentic_compose_two_images.py
PYTHONPATH=. python3 examples/agents_agentic/example_agentic_compose_three_images.py
```

Compose examples now reuse shared helper utilities in
`comfy_agent/examples_helpers.py` to keep naming and flow consistent.
