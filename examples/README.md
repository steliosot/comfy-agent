# Examples Index

All runnable examples are grouped under this `examples/` folder.

## Primary Folders

- `workflows_direct_dsl/`
  - Direct node-based DSL workflow examples.
- `workflows_fluent_dsl/`
  - Fluent chain-style workflow examples.
- `agents_agentic/`
  - Agnostic routing layer examples with reasoning + confidence + multi-skill planning.
- `end_to_end_pipelines/`
  - Full multi-skill pipelines (upload -> generate -> download -> video).

## Other Examples

All additional examples are grouped under `other/`:

- `other/workflows_editable/`
  - Editable workflow patterns (`clone`, `override`, `inspect`, `to_json`, YAML).
- `other/workflows_cloud_server/`
  - Cloud/Nginx examples with optional auth headers.
- `other/workflows_comfyui_imported/`
  - Python examples adapted from exported ComfyUI workflows.
- `other/workflows_comfyui_json/`
  - Raw ComfyUI JSON workflows for testing in ComfyUI directly.
  - Includes `4 WAN video clip.json` (video export via VHS).
- `other/skills_basic/`
  - Basic skill usage examples.
  - Includes dependency ops examples (`model_folder_guide`, `download_model`, `remove_model`).
  - Includes curated workflow routing examples (`match_curated_workflow`, `run_curated_workflow`).
  - Includes workflow-note link extraction example (`get_workflow_download_links`).
  - Includes execution likelihood prediction example (`predict_job_success_likelihood`).
- `other/skills_buildable/`
  - Build-first skill examples where `build(...)` returns a workflow.
  - Includes WAN 2.1 h264-mp4 animation skill examples.
- `other/agents_threaded/`
  - Threaded agent/job execution examples.

## Skills Package Layout

Skill implementations live under `skills/` and now include:

- `skill.py`
- `skill.yaml`
- `SKILL.md`
- `scripts/run.py`

Run a skill directly from CLI:

```bash
python3 skills/workflows/generate_sd15_image/scripts/run.py --args '{"prompt":"cinematic robot"}' --pretty
```
