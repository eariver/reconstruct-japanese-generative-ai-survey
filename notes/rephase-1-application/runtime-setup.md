# Application-review runtime

Root provisioned a task-local Linux Python **3.12.14** after the initial Python 3.10 diagnostic encountered an upstream f-string syntax incompatibility. Upstream workflows specify Python `3.12`; this closes the minor-version mismatch, not GitHub-hosted execution or platform parity.

Executed in WSL Ubuntu (no system package installation):

```sh
# Bootstrap uv with the already-captured official pip zipapp and existing isolated Python.
<workspace>/.rephase-1-inputs/integration-venv/bin/python3 \
  <workspace>/.rephase-1-inputs/pip.pyz install --target /tmp/jgas-rephase-uv uv

UV_PYTHON_INSTALL_DIR=/tmp/jgas-rephase-python UV_CACHE_DIR=/tmp/jgas-rephase-uv-cache \
  /tmp/jgas-rephase-uv/bin/uv python install 3.12 --no-bin

UV_PYTHON_INSTALL_DIR=/tmp/jgas-rephase-python UV_CACHE_DIR=/tmp/jgas-rephase-uv-cache \
  /tmp/jgas-rephase-uv/bin/uv venv --python 3.12 /tmp/jgas-rephase-application-venv

UV_CACHE_DIR=/tmp/jgas-rephase-uv-cache /tmp/jgas-rephase-uv/bin/uv pip install \
  --python /tmp/jgas-rephase-application-venv/bin/python \
  -r /tmp/jgas-rephase-application-r2/config/survey-production-v2-requirements.txt
```

Here `<workspace>` is `/mnt/d/Git/reconstruct-japanese-generative-ai-survey`. Acquisition of packages/runtime is separate from candidate test execution and uses no production repository operations.

Resolved on this run: uv `0.12.15`, CPython `3.12.14`, jsonschema `4.23.0`, pypdf `6.16.2`, attrs `26.1.0`, jsonschema-specifications `2025.9.1`, referencing `0.37.0`, rpds-py `2026.6.3`, typing-extensions `4.16.0`. The two direct dependencies match the fixed Core requirements. For exact reconstruction pin these versions; the commands above otherwise resolve current patch/transitive versions. `/tmp` runtime/cache is disposable and is not a production installation.
