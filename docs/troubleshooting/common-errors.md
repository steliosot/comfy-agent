# Common Errors

## 1) Cannot connect to server

Symptom:
- connection refused / timeout.

Fix:
- verify ComfyUI is running.
- verify `COMFY_URL`.
- if cloud, verify gateway public URL and headers.

## 2) Unauthorized / forbidden

Symptom:
- 401/403 from API nodes or gateway.

Fix:
- set valid auth header/API key.
- check key header name (`X-API-Key` for many gateways).

## 3) Missing model

Symptom:
- validation/runtime error mentioning checkpoint/vae/lora missing.

Fix:
- run `prepare_workflow_dependencies`.
- download/install model to expected Comfy model folder.

## 4) Missing custom node

Symptom:
- workflow validation fails with unknown node class.

Fix:
- install required custom node.
- restart ComfyUI and re-run.

## 5) Manager API not reachable

Symptom:
- model/node install skills fail.

Fix:
- ensure ComfyUI-Manager is installed and reachable at manager prefix.
- fallback to manual model placement if manager endpoint is unavailable.

## 6) Device/backend runtime issues

Symptom:
- backend-specific runtime errors (CUDA/MPS/ROCm).

Fix:
- test a lighter workflow first.
- reduce resolution/steps/batch.
- switch model variant or execution device.
