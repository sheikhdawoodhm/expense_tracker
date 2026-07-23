import json
import os

log_file = "/home/sheik-dawoodh/.gemini/antigravity/brain/27f11413-3cb7-4429-aa7f-052ac529aab0/.system_generated/logs/transcript_full.jsonl"
base_dir = "/home/sheik-dawoodh/Documents/projects/expense-tracking-app/backend/src"

print(f"Reading {log_file}...")
with open(log_file, "r") as f:
    for line in f:
        try:
            data = json.loads(line)
            if "tool_calls" in data:
                for tool in data["tool_calls"]:
                    if tool["function"] == "default_api:write_to_file":
                        args = tool.get("args", {})
                        if "TargetFile" in args and "CodeContent" in args:
                            path = args["TargetFile"]
                            if path.startswith(base_dir):
                                print(f"Recovering {path}...")
                                os.makedirs(os.path.dirname(path), exist_ok=True)
                                with open(path, "w") as out:
                                    out.write(args["CodeContent"])
        except Exception as e:
            pass
print("Recovery done.")
