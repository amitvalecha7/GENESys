import paramiko
import logging
from typing import Tuple

logger = logging.getLogger(__name__)

def run_command(host: str, username: str, key_path: str, command: str, timeout: int = 30) -> Tuple[int, str, str]:
    """
    SSH to host and run a command.
    Returns (exit_code, stdout, stderr).
    """
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(hostname=host, username=username, key_filename=key_path, timeout=timeout)
        stdin, stdout, stderr = client.exec_command(command)
        exit_code = stdout.channel.recv_exit_status()
        out = stdout.read().decode()
        err = stderr.read().decode()
        return exit_code, out, err
    except Exception as e:
        logger.error(f"SSH command failed on {host}: {e}")
        raise
    finally:
        client.close()

def copy_file(local_path: str, host: str, username: str, key_path: str, remote_path: str):
    """
    SCP a local file up to the remote host.
    """
    transport = paramiko.Transport((host, 22))
    transport.connect(username=username, pkey=paramiko.RSAKey.from_private_key_file(key_path))
    sftp = paramiko.SFTPClient.from_transport(transport)
    try:
        sftp.put(local_path, remote_path)
    finally:
        sftp.close()
        transport.close()
