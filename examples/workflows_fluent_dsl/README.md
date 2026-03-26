# Simple Pipelining Examples

These examples mirror the direct DSL workflows in `examples/workflows_direct_dsl/`,
but use the fluent chain style:

```python
from comfy_agent import Workflow

wf = Workflow()

(
    wf
    .checkpoint("model.safetensors")
    .prompt("rusty robot")
    .negative("bad quality")
    .latent(512, 512)
    .sample()
    .decode()
    .save("robot")
)

wf.run()
```

Both styles are supported:

- `examples/workflows_direct_dsl/` keeps the original tuple/lowercase API
- `examples/workflows_fluent_dsl/` uses the fluent chain API
- `example_compose_skills_three_images.py` shows fluent-style composition of
  `upload_image -> generate_flux_multi_input_img2img -> download_image`

`Workflow()` reads `COMFY_URL` if it is set, otherwise it defaults to
`http://127.0.0.1:8000`.
