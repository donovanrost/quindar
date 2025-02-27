from abc import ABC, abstractmethod
import pandas as pd

class BaseAnomalyDetector(ABC):
    """Base class for anomaly detection per ground station provider."""
    
    @abstractmethod
    def detect_anomalies(self, df: pd.DataFrame):
        """Detect anomalies based on provider-specific rules."""
        pass
