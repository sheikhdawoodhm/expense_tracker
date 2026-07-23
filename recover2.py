import json
import os

log_file = "/home/sheik-dawoodh/.gemini/antigravity/brain/27f11413-3cb7-4429-aa7f-052ac529aab0/.system_generated/logs/transcript_full.jsonl"
base_dir = "/home/sheik-dawoodh/Documents/projects/expense-tracking-app/backend/src"

print(f"Reading {log_file}...")

# Keep track of file content to simulate replacements
file_states = {}

with open(log_file, "r") as f:
    for line in f:
        try:
            data = json.loads(line)
            if "tool_calls" in data:
                for tool in data["tool_calls"]:
                    # check if it is write_to_file or replace_file_content
                    # in Gemini logs, it is usually tool['function']['name'] and tool['function']['arguments']
                    # or tool['name'] and tool['args']
                    
                    func_name = tool.get("name") or tool.get("function", {}).get("name")
                    args = tool.get("args") or tool.get("arguments") or tool.get("function", {}).get("arguments")
                    
                    if not isinstance(args, dict):
                        if isinstance(args, str):
                            try:
                                args = json.loads(args)
                            except:
                                args = {}
                        else:
                            args = {}
                    
                    if not args:
                        continue
                        
                    if "write_to_file" in str(func_name):
                        target = args.get("TargetFile")
                        content = args.get("CodeContent")
                        if target and content and target.startswith(base_dir):
                            file_states[target] = content
                            
                    elif "replace_file_content" in str(func_name) or "multi_replace_file_content" in str(func_name):
                        target = args.get("TargetFile")
                        if target and target.startswith(base_dir) and target in file_states:
                            # apply replacements roughly
                            chunks = args.get("ReplacementChunks", [])
                            if "TargetContent" in args:
                                chunks.append({
                                    "TargetContent": args.get("TargetContent"),
                                    "ReplacementContent": args.get("ReplacementContent")
                                })
                            
                            for chunk in chunks:
                                tc = chunk.get("TargetContent")
                                rc = chunk.get("ReplacementContent")
                                if tc and rc:
                                    file_states[target] = file_states[target].replace(tc, rc)
        except Exception as e:
            print("Error parsing line", e)
            pass

for target, content in file_states.items():
    print(f"Recovering {target}...")
    os.makedirs(os.path.dirname(target), exist_ok=True)
    with open(target, "w") as out:
        out.write(content)
print("Recovery done.")
