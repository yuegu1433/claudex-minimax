from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Coroutine


class SandboxProviderType(str, Enum):
    E2B = "e2b"
    DOCKER = "docker"


@dataclass
class CommandResult:
    stdout: str
    stderr: str
    exit_code: int


@dataclass
class FileMetadata:
    path: str
    type: str
    size: int
    modified: float
    is_binary: bool = False


@dataclass
class FileContent:
    path: str
    content: str
    type: str
    is_binary: bool


@dataclass
class PtySession:
    id: str
    pid: int | None
    rows: int
    cols: int


@dataclass
class PtySize:
    rows: int
    cols: int


@dataclass
class CheckpointInfo:
    message_id: str
    created_at: str


@dataclass
class PreviewLink:
    preview_url: str
    port: int


@dataclass
class SecretEntry:
    key: str
    value: str


@dataclass
class DockerConfig:
    # Required parameters - must be provided explicitly (typically via create_docker_config() factory)
    preview_base_url: str  # Should be obtained from Settings.DOCKER_PREVIEW_BASE_URL
    image: str  # Docker image to use
    network: str  # Docker network name
    # Optional parameters with defaults
    host: str | None = None  # Docker host (None for local daemon)
    user_home: str = "/home/user"  # User home directory in container
    openvscode_port: int = 8765  # Port for OpenVSCode server


@dataclass
class SandboxContext:
    sandbox_id: str
    provider_type: SandboxProviderType
    connected: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)


PtyDataCallbackType = Callable[[bytes], Coroutine[Any, Any, None]]
