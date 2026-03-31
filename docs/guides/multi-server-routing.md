# Multi-Server Routing

`comfy-agent` supports explicit server selection using `.comfy_servers.yaml`.

## Example config

```yaml
default_server: local
servers:
  local:
    url: http://localhost:8000
    api_prefix: /api
    manager_api_prefix: /manager
  clouda:
    url: https://your-public-url.example
    headers:
      X-API-Key: ${COMFY_CLOUDA_KEY}
    api_prefix: /api
    manager_api_prefix: /manager
```

## Resolve server per run

```bash
export COMFY_SERVERS_FILE=.comfy_servers.yaml
PYTHONPATH=. python3 skills/infra/select_comfy_server/scripts/run.py \
  --args '{"server_name":"clouda","require_ready":true}' --pretty
```

Pass resolved `server`, `headers`, `api_prefix`, and `manager_api_prefix` to target skills/workflows.

## Why explicit selection

- No hidden global mutation.
- Easier debugging per run.
- Safer for multi-tenant or mixed GPU pools.
