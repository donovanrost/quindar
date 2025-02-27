import pandas as pd
import logging
from app.core.exceptions import InvalidFileFormatException

logger = logging.getLogger(__name__)

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

            # Detect anomalies
            anomalies = self.detect_anomalies(df)

            return {
                "stations_processed": df['station_id'].nunique(),
                "total_data_transferred": f"{total_data_transferred / 1e9:.2f} GB",
                "anomalies_detected": len(anomalies),
                "anomaly_details": anomalies
            }
        
        except Exception as e:
            logger.error(f"Error processing file: {str(e)}")
            raise

    def detect_anomalies(self, df):
        """Detects anomalies in the dataset."""
        anomalies = []

        for _, row in df.iterrows():
            station = row['station_id']
            num_contacts = row['num_contacts']
            total_bytes_received = row['total_bytes_received']
            total_bytes_sent = row['total_bytes_sent']

            if num_contacts > 0 and total_bytes_received == 0:
                anomalies.append({
                    "station": station,
                    "issue": "Contacts initiated but no data received"
                })

            if num_contacts > 0 and total_bytes_sent == 0 and total_bytes_received == 0:
                anomalies.append({
                    "station": station,
                    "issue": "No data sent or received despite contacts"
                })

        return anomalies
