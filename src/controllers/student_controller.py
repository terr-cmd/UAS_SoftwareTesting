from flask import Blueprint, request, jsonify
from src.models.student_model import ValidationError, StudentNotFoundError

student_bp = Blueprint("students", __name__)


def register_routes(app, service):
    """Daftarkan semua route mahasiswa ke Flask app."""

    @app.route("/students", methods=["POST"])
    def create_student():
        try:
            data = request.get_json()
            result = service.create_student(data)
            return jsonify(result), 201
        except ValidationError as e:
            return jsonify({"error": str(e)}), 400

    @app.route("/students", methods=["GET"])
    def get_all_students():
        result = service.get_all_students()
        return jsonify(result), 200

    @app.route("/students/<int:student_id>", methods=["GET"])
    def get_student(student_id):
        try:
            result = service.get_student_by_id(student_id)
            return jsonify(result), 200
        except StudentNotFoundError as e:
            return jsonify({"error": str(e)}), 404

    @app.route("/students/<int:student_id>", methods=["PUT"])
    def update_student(student_id):
        try:
            data = request.get_json()
            result = service.update_student(student_id, data)
            return jsonify(result), 200
        except StudentNotFoundError as e:
            return jsonify({"error": str(e)}), 404
        except ValidationError as e:
            return jsonify({"error": str(e)}), 400

    @app.route("/students/<int:student_id>", methods=["DELETE"])
    def delete_student(student_id):
        try:
            result = service.delete_student(student_id)
            return jsonify(result), 200
        except StudentNotFoundError as e:
            return jsonify({"error": str(e)}), 404
