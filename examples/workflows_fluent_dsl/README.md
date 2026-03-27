# Fluent DSL Examples

These examples are intentionally simple and skill-first.

Each file calls a single `skills/*/skill.py` `run(...)` entrypoint (or a very small
composition chain), so users can learn one pattern and reuse it everywhere.

For composable image flows, see:

- `example_compose_skills_three_images.py`
- pattern: `upload_image -> generate_flux_multi_input_img2img -> download_image`

The compose example now uses a fluent chain wrapper as well:

```python
(
    FluentSkillComposeFlow(cfg, run_id="shared_compose_three_refs")
    .ref("woman.png")
    .ref("St-Pauls-Cathedral.png")
    .ref("hat.jpeg")
    .prompt("...")
    .stage("final")
    .run()
)
```
