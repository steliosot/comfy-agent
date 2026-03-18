# Unit Tests

This folder contains unit tests for:

- core workflow behavior
- buildable skills
- agent examples
- example scripts

Run them with:

```bash
python3 -m unittest discover -s unit_tests -v
```

The tests use mocked ComfyUI API responses, so they do not require a live
ComfyUI server.
