from app.core.anomaly_detectors.qdr_detector import QDRAnomalyDetector

class AnomalyDetectorFactory:
    """Factory to select the correct anomaly detection strategy based on provider."""
    
    PROVIDER_MAPPING = {
        "QDR": QDRAnomalyDetector,
    }

    @staticmethod
    def get_detector(provider: str):
        """Returns the appropriate anomaly detector based on the provider."""
        detector_class = AnomalyDetectorFactory.PROVIDER_MAPPING.get(provider.upper())
        if not detector_class:
            raise ValueError(f"No anomaly detector available for provider: {provider}")
        return detector_class()
