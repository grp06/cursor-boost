from dotenv import load_dotenv
import os
import json
import time
from datetime import datetime

from config_loader import load_config
from command_runner import run_commands
from snapshot_writer import write_snapshot
from docker_logs import get_docker_logs
from openai_integration import generate_cursorrules

load_dotenv()

config = load_config()

ignore_patterns = '|'.join(config['tree']['ignore_patterns'])
ignore_extensions = '|'.join(config['tree']['ignore_extensions'])
combined_ignore = f"{ignore_patterns}|{ignore_extensions}"

system_commands = [
    "uname -a",
    "python --version",
    "pip list",
    "python -c 'import sys; print(sys.path)'",
    "docker ps",
    f"df -h | awk '(NR==1) || ($5+0 >= {config['system_commands']['disk_usage_threshold']})'",
    "vm_stat | awk '/Pages free:|Pages active:|Pages inactive:|Pages wired down:/ {print}'",
    "netstat -an | grep LISTEN | awk '{print $4}' | sort -u",
    "printenv | grep -v 'KEY\\|SECRET\\|PASS\\|TOKEN'",
]

project_commands = [
    f"tree -d -L {config['tree']['max_depth']} -I '{combined_ignore}'",
]

def get_project_directories():
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        projects_file = os.path.join(script_dir, 'containers-list.md')
        
        with open(projects_file, 'r') as f:
            projects = [
                line.strip('- \n') 
                for line in f.readlines() 
                if line.strip().startswith('-')
            ]
        return projects
    except FileNotFoundError:
        print("❌ Error: containers-list.md not found in .cursorboost directory")
        return []

def write_cursorrules(cursorrules):
    project_description = ""
    try:
        with open("project-description.txt", "r") as f:
            project_description = f"# Project Description:\n{f.read()}\n\n"
    except FileNotFoundError:
        print("Warning: project-description.txt not found")
    
    docker_logs = get_docker_logs()
    
    parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    cursorrules_path = os.path.join(parent_dir, '.cursorrules')
    
    with open(cursorrules_path, "w") as f:
        f.write(f"{project_description}{cursorrules}\n\n# Docker Container Logs:\n\n{docker_logs}")

def find_requirements_files(root_dir):
    requirements_files = []
    for dirpath, dirnames, filenames in os.walk(root_dir):
        if '.cursorboost' in dirpath:
            continue
        
        if 'requirements.txt' in filenames:
            requirements_files.append(os.path.join(dirpath, 'requirements.txt'))
    
    return requirements_files

root_directory = os.getcwd()
requirements_files = find_requirements_files(root_directory)
print("Found requirements files:", requirements_files)

if __name__ == "__main__":
    print("🚀 Starting Cursor Boost in continuous mode...")
    
    while True:
        print(f"\n⏰ Running update at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        projects = get_project_directories()
        if not projects:
            print("⚠️ No projects found in containers-list.md")
        
        system_snapshot = run_commands(system_commands)
        
        all_snapshots = [system_snapshot]
        for project in projects:
            print(f"📂 Processing project: {project}")
            project_snapshot = run_commands(project_commands, project)
            if project_snapshot:
                all_snapshots.append(project_snapshot)
        
        complete_snapshot = "\n\n".join(all_snapshots)
        
        write_snapshot(complete_snapshot)
        
        cursorrules = generate_cursorrules(complete_snapshot)
        if cursorrules:
            write_cursorrules(cursorrules)
            print("✅ .cursorrules updated successfully")
            print("✅ Snapshot saved to snapshot.txt")
        else:
            print("❌ Failed to generate .cursorrules")
            
        time.sleep(60)
