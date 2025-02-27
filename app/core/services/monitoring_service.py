
import pandas as pd
import logging
from app.core.exceptions import InvalidFileFormatException
from app.core.anomaly_detectors.factory import AnomalyDetectorFactory

logger = logging.getLogger(__name__)

PROVIDER_MAP = {
    "QDR": "QDR",
    "KSAT": "KSAT",
}

def get_provider_from_station_id(station_id):
    """Determines the provider based on the station_id prefix."""
    for prefix, provider in PROVIDER_MAP.items():
        if station_id.startswith(prefix):
            return provider
    return "UNKNOWN"  # Default if no match is found

class MonitoringService:
    REQUIRED_COLUMNS = {"station_id", "num_contacts", "total_bytes_received", "total_bytes_sent"}

    def process_file(self, file_content):
        """Processes the uploaded CSV file and detects anomalies."""
        try:
            df = pd.read_csv(file_content)

            # Validate Columns
            if not self.REQUIRED_COLUMNS.issubset(df.columns):
                raise InvalidFileFormatException("CSV file is missing required columns.")

            # Compute total data transferred per station
            df['total_data_transferred'] = df['total_bytes_sent'] + df['total_bytes_received']
            total_data_transferred = df['total_data_transferred'].sum()

            # Assign provider dynamically
            df['provider'] = df['station_id'].apply(get_provider_from_station_id)

            # Determine providers and use correct anomaly detector
            providers = df['provider'].unique()
            anomalies = []

            for provider in providers:
                if provider == "UNKNOWN":
                    logger.warning("Detected unknown provider in dataset.")
                provider_df = df[df['provider'] == provider]
                detector = AnomalyDetectorFactory.get_detector(provider)
                anomalies.extend(detector.detect_anomalies(provider_df))

            return {
                "stations_processed": df['station_id'].nunique(),
                "total_data_transferred": f"{total_data_transferred / 1e9:.2f} GB",
                "anomalies_detected": len(anomalies),
                "anomaly_details": [a.to_dict() for a in anomalies]
            }
        
        except Exception as e:
            logger.error(f"Error processing file: {str(e)}")
            raise
