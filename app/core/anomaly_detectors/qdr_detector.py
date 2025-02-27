from app.core.anomaly_detectors.base_detector import BaseAnomalyDetector
from app.core.anomaly_detectors.anomaly_checks import ANOMALY_CHECKS
from app.core.anomaly_detectors.anomaly import Anomaly

class QDRAnomalyDetector(BaseAnomalyDetector):
    """Anomaly detection rules for QDR ground stations."""

    def detect_anomalies(self, df):
        anomalies = []
        for _, row in df.iterrows():
            for check_name, check_function in ANOMALY_CHECKS.items():
                anomaly_data = check_function(
                    station_id=row['station_id'],
                    num_contacts=row['num_contacts'],
                    total_bytes_received=row['total_bytes_received'],
                    total_bytes_sent=row['total_bytes_sent']
                )
                if anomaly_data:
                    anomalies.append(Anomaly(**anomaly_data))
        return anomalies
