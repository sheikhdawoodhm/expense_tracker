import json
import os
import re

log_file = "/home/sheik-dawoodh/.gemini/antigravity/brain/27f11413-3cb7-4429-aa7f-052ac529aab0/.system_generated/logs/transcript_full.jsonl"
base_dir = "/home/sheik-dawoodh/Documents/projects/expense-tracking-app/backend/src"

file_contents = {}

with open(log_file, "r") as f:
    for line in f:
        try:
            data = json.loads(line)
            if "content" in data and "File Path:" in data["content"] and "The following code has been modified to include a line number before every line" in data["content"]:
                # Parse the view_file output
                content = data["content"]
                
                # Extract file path
                path_match = re.search(r"File Path: `file://([^`]+)`", content)
                if not path_match:
                    continue
                path = path_match.group(1)
                
                if not path.startswith(base_dir):
                    continue
                
                # Extract code lines
                lines = content.split("The following code has been modified to include a line number before every line, in the format: <line_number>: <original_line>. Please note that any changes targeting the original code should remove the line number, colon, and leading space.")[1]
                lines = lines.split("The above content shows the entire, complete file contents of the requested file.")[0]
                
                # Clean up line numbers
                clean_lines = []
                for l in lines.split("\n"):
                    if not l.strip():
                        continue
                    # Match <number>: <content>
                    m = re.match(r"^\d+:\s(.*)$", l)
                    if m:
                        clean_lines.append(m.group(1))
                    elif re.match(r"^\d+:$", l.strip()):
                        clean_lines.append("")
                        
                file_contents[path] = "\n".join(clean_lines) + "\n"
        except Exception as e:
            pass

print(f"Found {len(file_contents)} files from view_file logs.")
for target, content in file_contents.items():
    print(f"Recovering {target}...")
    os.makedirs(os.path.dirname(target), exist_ok=True)
    with open(target, "w") as out:
        out.write(content)
print("Recovery done.")
