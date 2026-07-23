import json
import os
import glob

base_dir = "/home/sheik-dawoodh/Documents/projects/expense-tracking-app/backend/src"
brain_dir = "/home/sheik-dawoodh/.gemini/antigravity/brain"

# Find all transcript_full.jsonl files
log_files = glob.glob(f"{brain_dir}/*/.system_generated/logs/transcript_full.jsonl")

file_states = {}

for log_file in log_files:
    print(f"Reading {log_file}...")
    with open(log_file, "r") as f:
        for line in f:
            try:
                data = json.loads(line)
                if "tool_calls" in data:
                    for tool in data["tool_calls"]:
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
                            if target and content and "backend/src" in target:
                                file_states[target] = content
                                
                        elif "replace_file_content" in str(func_name) or "multi_replace_file_content" in str(func_name):
                            target = args.get("TargetFile")
                            if target and "backend/src" in target and target in file_states:
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
                pass

print(f"Found {len(file_states)} files.")
for target, content in file_states.items():
    print(f"Recovering {target}...")
    os.makedirs(os.path.dirname(target), exist_ok=True)
    with open(target, "w") as out:
        out.write(content)
print("Recovery done.")
