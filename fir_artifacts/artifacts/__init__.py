# Import public API
from fir_artifacts.artifacts.base import AbstractArtifact
from fir_artifacts.artifacts.artifact_registry import registry

# Import core artifact types to register them
from fir_artifacts.artifacts.hash import Hash
from fir_artifacts.artifacts.ip import IP
from fir_artifacts.artifacts.url import URL
from fir_artifacts.artifacts.hostname import Hostname
from fir_artifacts.artifacts.email import Email
from fir_artifacts.artifacts.cve import CommonVulnerabilityAndExposure, CommonWeaknessEnumeration
from fir_artifacts.artifacts.mac import MAC


# Export public API
__all__ = [
    AbstractArtifact,
    registry
]
