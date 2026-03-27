# Direct DSL Examples

These examples are also skill-first for consistency with fluent examples.

Each file uses a minimal `run(...)` call from `skills/*/skill.py`, with explicit
arguments where useful.

For composable flows, see:

- `example_compose_skills_two_images.py`
- pattern: `upload_image -> generate_flux_multi_input_img2img -> download_image`
