# Examples Index

All runnable examples are grouped under this `examples/` folder.

## Workflows

- `workflows_direct_dsl/`
  - Direct node-based DSL workflow examples.
- `workflows_fluent_dsl/`
  - Fluent chain-style workflow examples.
- `workflows_editable/`
  - Editable workflow patterns (`clone`, `override`, `inspect`, `to_json`, YAML).
- `workflows_cloud_server/`
  - Cloud/Nginx examples with optional auth headers.
- `workflows_comfyui_imported/`
  - Python examples adapted from exported ComfyUI workflows.
- `workflows_comfyui_json/`
  - Raw ComfyUI JSON workflows for testing in ComfyUI directly.
  - Includes `4 WAN cat gif.json`.

## Skills

- `skills_basic/`
  - Basic skill usage examples.
- `skills_buildable/`
  - Build-first skill examples where `build(...)` returns a workflow.
  - Includes WAN 2.1 GIF skill examples.

## Agents

- `agents_threaded/`
  - Threaded agent/job execution examples.
- `agents_agentic/`
  - Agnostic routing layer examples with reasoning + confidence + multi-skill planning.
