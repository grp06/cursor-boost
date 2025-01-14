import os
import json

def load_config():
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        config_file = os.path.join(script_dir, 'config.json')
        with open(config_file, 'r') as f:
            config = json.load(f)
            
            if 'tree' not in config or 'system_commands' not in config:
                raise KeyError("Missing required keys in config.json")
            
            return config
    except (FileNotFoundError, KeyError):
        print("⚠️ config.json not found or invalid, using default settings")
        return {
            "tree": {
                "max_depth": 3,
                "ignore_patterns": ["venv", "__pycache__", "node_modules", "build", "public", "dist", ".git"],
                "ignore_extensions": ["*.pyc", "*.pyo", "*.pyd", "*.so", "*.dll", "*.class"]
            },
            "system_commands": {
                "disk_usage_threshold": 80
            }
        }
