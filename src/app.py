from flask import Flask, render_template
from src.repositories.student_repository import StudentRepository
from src.services.student_service import StudentService
from src.controllers.student_controller import register_routes
import os


def create_app():
    """Factory function untuk membuat Flask app instance."""
    app = Flask(
        __name__,
        template_folder="templates",
        static_folder="static"
    )

    repo = StudentRepository()
    service = StudentService(repo)
    register_routes(app, service)

    @app.route("/")
    def home():
        return render_template("index.html")

    @app.route("/dashboard")
    def dashboard():
        return render_template("dashboard.html")

    @app.route("/view")
    def view():
        return render_template("view.html")

    return app


if __name__ == "__main__":
    create_app().run(debug=True)
