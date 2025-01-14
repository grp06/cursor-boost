import subprocess
import os
from datetime import datetime

def run_commands(commands_list, project_dir=None):
    print(f"📊 Collecting {'project' if project_dir else 'system'} information...")
    output = []
    output.append(f"Timestamp: {datetime.utcnow().isoformat()}Z\n")
    
    if project_dir:
        original_dir = os.getcwd()
        base_project_path = config.get('base_project_path')
        if not base_project_path or base_project_path == "<your_project_path>":
            raise ValueError(
                "❌ Error: 'base_project_path' is not defined or is still set to '<your_project_path>' in the configuration file (config.json). "
                "Please update it to your project's root directory."
            )
        
        project_path = os.path.join(os.path.expanduser(base_project_path), project_dir)
        try:
            os.chdir(project_path)
            output.append(f"\n### Project: {project_dir} ###\n")
        except FileNotFoundError:
            print(f"  ❌ Project directory not found: {project_path}")
            return ""

    for command in commands_list:
        print(f"  ⚡ Running: {command}")
        try:
            result = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
            output.append(f"{command}:\n{result.decode('utf-8')}\n")
        except subprocess.CalledProcessError as e:
            print(f"  ❌ Failed: {command}")
            output.append(f"{command} (FAILED):\n{e.output.decode('utf-8')}\n")
    
    if project_dir:
        os.chdir(original_dir)
    
    return "\n".join(output)
