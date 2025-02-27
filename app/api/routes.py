from flask import Blueprint, request, jsonify
from app.core.services.monitoring_service import MonitoringService
from app.core.exceptions import InvalidFileFormatException

monitoring_service = MonitoringService()
bp = Blueprint('api', __name__)

@bp.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    try:
        response = monitoring_service.process_file(file.stream)
        return jsonify(response)
    except InvalidFileFormatException as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        print(e)
        return jsonify({"error": "Internal server error"}), 500
