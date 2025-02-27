def no_data_received(station_id, num_contacts, total_bytes_received, **kwargs):
    """Anomaly: Contacts initiated but no data received."""
    if num_contacts > 0 and total_bytes_received == 0:
        return {
            "station_id": station_id,
            "anomaly_type": "NoDataReceived",
            "description": "Contacts initiated but no data was received."
        }
    return None

def no_data_transmitted(station_id, num_contacts, total_bytes_sent, total_bytes_received, **kwargs):
    """Anomaly: No data sent or received despite contacts."""
    if num_contacts > 0 and total_bytes_sent == 0 and total_bytes_received == 0:
        return {
            "station_id": station_id,
            "anomaly_type": "NoDataTransmitted",
            "description": "No data sent or received despite contacts being initiated."
        }
    return None

def data_transmission_without_contacts(station_id, num_contacts, total_bytes_sent, total_bytes_received, **kwargs):
    """Anomaly: Data transmission detected without contacts."""
    if num_contacts == 0 and (total_bytes_sent > 0 or total_bytes_received > 0):
        return {
            "station_id": station_id,
            "anomaly_type": "DataWithoutContacts",
            "description": "Data transmission detected without any contacts being recorded."
        }
    return None

# Dictionary mapping anomaly names to functions
ANOMALY_CHECKS = {
    "NoDataReceived": no_data_received,
    "NoDataTransmitted": no_data_transmitted,
    "DataWithoutContacts": data_transmission_without_contacts
}
