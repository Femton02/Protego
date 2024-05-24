from abc import ABC, abstractmethod
from pydantic import BaseModel

class DetectorInterface(ABC):
    """Abstract class for detectors to ensure that they all implement the same methods.

    Args:
        ABC (class): Abstract Base Class
    """

    @abstractmethod
    def detect(self):
        """Abstract method to detect what the detector is supposed to detect."""
        pass

    @abstractmethod
    def get_results(self):
        """Abstract method to get the results of the detection."""
        pass

class DependencyDetectionResult(BaseModel):
    """Result of the detection."""
    
    file_path: str
    name: str
    version: str