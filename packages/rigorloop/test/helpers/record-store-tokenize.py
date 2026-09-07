"""Count controlled interaction pieces, never persist their request/response text."""
import importlib.metadata
import json
import sys
import tiktoken
version = importlib.metadata.version("tiktoken")
if version != "0.12.0":
    raise SystemExit("Expected tiktoken==0.12.0")
encoding = tiktoken.get_encoding("cl100k_base")
runs = []
for pieces in json.load(sys.stdin):
    categories = {}
    for piece in pieces:
        categories[piece["category"]] = categories.get(piece["category"], 0) + len(encoding.encode(piece["text"], disallowed_special=()))
    runs.append({"tokens": sum(categories.values()), "by_category": categories})
json.dump({"tokenizer": {"package": "tiktoken", "version": version, "encoding": "cl100k_base"}, "runs": runs}, sys.stdout)
