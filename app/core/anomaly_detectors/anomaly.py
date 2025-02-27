class Anomaly:
    """Represents an anomaly detected in ground station data."""
    
    def __init__(self, station_id, anomaly_type, description):
        self.station_id = station_id
        self.anomaly_type = anomaly_type
        self.description = description

    def to_dict(self):
        """Converts the anomaly instance into a dictionary for easy JSON serialization."""
        return {
            "station_id": self.station_id,
            "anomaly_type": self.anomaly_type,
            "description": self.description
        }
