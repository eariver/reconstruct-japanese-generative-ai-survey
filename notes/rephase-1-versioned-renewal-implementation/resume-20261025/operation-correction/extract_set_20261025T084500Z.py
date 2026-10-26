#!/usr/bin/env python3
import sys, json
print(json.load(open(sys.argv[1]))["set_path"])
with open(sys.argv[2], "w") as f:
    f.write(json.load(open(sys.argv[1]))["set_path"])
