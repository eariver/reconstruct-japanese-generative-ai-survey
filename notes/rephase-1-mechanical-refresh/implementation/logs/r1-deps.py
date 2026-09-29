import importlib.metadata
import sys

print("python:", sys.version)
for dist in ("pypdf", "jsonschema"):
    try:
        print(dist, importlib.metadata.version(dist))
    except Exception as exc:
        print(dist, "UNKNOWN", exc)
