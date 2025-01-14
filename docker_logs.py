import subprocess
import os

def get_docker_logs():
    try:
        ignore_containers = config.get('docker', {}).get('ignore_containers', [])
        
        containers = subprocess.check_output(
            "docker ps --format '{{.ID}} {{.Names}}'", 
            shell=True
        ).decode('utf-8').strip().split('\n')
        
        logs = []
        for container in containers:
            if not container:
                continue
                
            container_id, container_name = container.split()
            
            if container_name in ignore_containers:
                continue
                
            try:
                container_logs = subprocess.check_output(
                    f"docker logs --tail 25 {container_id}",
                    shell=True
                ).decode('utf-8')
                
                logs.append(f"\nDocker Logs for {container_name} ({container_id}):\n")
                logs.append(container_logs)
            except subprocess.CalledProcessError as e:
                logs.append(f"\nError getting logs for {container_name}: {str(e)}\n")
        
        return "\n".join(logs)
    except subprocess.CalledProcessError as e:
        return "Error getting Docker container list"
