# Configuration

## Single server env

- `COMFY_URL`
- `COMFY_AUTH_HEADER` (optional)

## Multi-server env

- `COMFY_SERVERS_FILE` (default: `.comfy_servers.yaml`)

Example:

```yaml
default_server: local
servers:
  local:
    url: http://localhost:8000
    api_prefix: /api
    manager_api_prefix: /manager
  clouda:
    url: https://example.trycloudflare.com
    headers:
      X-API-Key: ${COMFY_CLOUDA_KEY}
    api_prefix: /api
    manager_api_prefix: /manager
```

## Notes

- Keep secrets out of git.
- Prefer explicit server resolution per run (`select_comfy_server`).
- Use `prepare_workflow_dependencies` before heavy workflows.
