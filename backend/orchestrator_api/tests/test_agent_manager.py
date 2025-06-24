import pytest
from app.services.agent_manager import DiscoveryAgent

# Use localhost and the new RSA key
@pytest.mark.parametrize("node", [
    {"host": "127.0.0.1", "user": "root", "key_path": "/root/.ssh/orchestrator_test_key"}
])
def test_discovery(node):
    result = DiscoveryAgent.discover_nodes([node])
    assert isinstance(result, list)
    assert "os" in result[0]
    assert "containers" in result[0]
