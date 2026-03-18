# Simple Pipelining Examples

These examples mirror the existing workflows in `workflow_examples/`,
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

- `workflow_examples/` keeps the original tuple/lowercase API
- `workflow_examples_simple_pipelining/` uses the fluent chain API

`Workflow()` reads `COMFY_URL` if it is set, otherwise it defaults to
`http://127.0.0.1:8000`.
