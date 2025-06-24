from app.utils.ssh_client import run_command, copy_file
from typing import List, Dict

class DiscoveryAgent:
    @staticmethod
    def discover_nodes(nodes: List[Dict]) -> List[Dict]:
        """
        Given a list of nodes (with host, user, key_path),
        gather OS info and running containers.
        """
        results = []
        for node in nodes:
            host = node["host"]
            user = node["user"]
            key = node["key_path"]
            # Get OS info
            code_os, os_info, _ = run_command(host, user, key, "uname -a")
            # List containers
            code_ps, docker_ps, _ = run_command(host, user, key, "docker ps --format '{{.Names}}'")
            results.append({
                "host": host,
                "os": os_info.strip(),
                "containers": docker_ps.splitlines() if code_ps == 0 else []
            })
        return results

class ProvisionAgent:
    @staticmethod
    def provision_service(node: Dict, compose_file: str) -> bool:
        """
        Copy a docker-compose file and bring up services.
        """
        host = node["host"]
        user = node["user"]
        key = node["key_path"]
        remote_compose = "/root/deploy/docker-compose.yml"
        copy_file(compose_file, host, user, key, remote_compose)
        code, _, _ = run_command(host, user, key, f"docker-compose -f {remote_compose} up -d")
        return code == 0

class ValidationAgent:
    @staticmethod
    def run_checks(node: Dict) -> Dict:
        """
        Verify n8n is running as an example.
        """
        host = node["host"]
        user = node["user"]
        key = node["key_path"]
        code, out, _ = run_command(host, user, key, "docker ps --filter name=n8n --format '{{.Names}}'")
        return {"n8n_running": "n8n" in out}
