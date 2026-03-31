# Infra Skill Catalog

Core infra skills for routing, health, dependencies, transfer, and optimization.

| Skill | Purpose | Key Inputs | Typical Output |
|---|---|---|---|
| `select_comfy_server` | Resolve named server and optional readiness | `server_name`, `require_ready` | `server`, `headers`, prefixes |
| `get_server_status` | Check server reachability/status | none | health info |
| `get_queue_status` | Inspect queue depth | none | queue stats |
| `get_progress` | Poll execution progress | `prompt_id` | progress snapshot |
| `prepare_workflow_dependencies` | Validate models/custom nodes before run | required assets | missing/ok report |
| `assess_server_resources` | Basic resource fitness hints | optional profile | recommendations |
| `download_model` | Pull model via manager API | model name/url | install result |
| `install_custom_node` | Install custom node package | repo/ref | install result |
| `remove_model` | Remove model file | model id/path | deletion result |
| `upload_image` | Upload image input | local path | uploaded file metadata |
| `download_image` | Fetch image outputs | `prompt_id`, `run_id` | saved local file(s) |
| `upload_video` | Upload video input | local path | uploaded video metadata |
| `download_video` | Fetch video outputs | `prompt_id`, `run_id` | saved local file(s) |
| `delete_image_job` | Cleanup image job history/assets | prompt/job identifiers | deletion result |
| `delete_video_job` | Cleanup video job history/assets | prompt/job identifiers | deletion result |
| `agentic_plan` | Produce executable plan of skills | goal/context | plan payload |
| `agentic_execute` | Execute planned skill chain | plan steps | per-step results |
| `configure_optimizations` | Build optimization profile | mode/options | profile snippet |

Optimization wrappers include: `optimization_none`, `optimization_cache`, `optimization_memoization`, `optimization_model_lru`, `optimization_cpu_offload`, `optimization_lazy_loading`, `optimization_attention_reuse`, plus model-specific variants.
