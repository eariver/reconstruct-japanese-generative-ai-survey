import importlib.metadata
for d in sorted(importlib.metadata.distributions(), key=lambda x: (x.metadata.get("Name") or "")):
    print(d.metadata.get("Name"), d.version)
