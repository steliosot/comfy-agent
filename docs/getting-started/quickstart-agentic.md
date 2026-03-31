# Quickstart (Agentic)

All examples assume:

- `COMFY_URL` (or multi-server config) is set.
- You run from repository root.

## 1) Plan then execute

Prerequisite: core infra skills available (default in repo).

```bash
PYTHONPATH=. python3 examples/agents_agentic/example_agentic_plan_then_execute.py
```

Expected output: a plan payload followed by step execution results.

Common failure: plan chooses missing workflow dependency. Fix with preflight dependency checks.

## 2) Select server then execute

Prerequisite: `.comfy_servers.yaml` configured.

```bash
PYTHONPATH=. python3 examples/agents_agentic/example_agentic_select_server_then_execute.py
```

Expected output: selected server details and successful workflow execution.

Common failure: unknown server alias. Fix by updating `.comfy_servers.yaml`.

## 3) Slash commands flow

Prerequisite: command parser/example environment as provided by script.

```bash
PYTHONPATH=. python3 examples/agents_agentic/example_agentic_slash_commands.py
```

Expected output: slash-command style plan/execute orchestration logs.

Common failure: malformed command payload. Fix by following example command format exactly.
