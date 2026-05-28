"""StudyNest application factory.

The factory wires together Flask extensions, registers route blueprints,
and (in production) syncs file-based content into the DB on startup.
"""
from __future__ import annotations

import logging

from flask import Flask

from config import get_config

from .extensions import csrf, db, limiter, login_manager


def create_app(config_class: type | None = None) -> Flask:
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object(config_class or get_config())

    _configure_logging(app)
    _init_extensions(app)
    _register_blueprints(app)
    _register_error_handlers(app)
    _bootstrap_database(app)
    _maybe_sync_content(app)

    return app


def _init_extensions(app: Flask) -> None:
    db.init_app(app)
    csrf.init_app(app)
    limiter.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "auth.sign_in"
    login_manager.login_message_category = "info"

    from .models.user import User  # noqa: WPS433  late import avoids circular

    @login_manager.user_loader
    def load_user(user_id: str) -> User | None:
        return db.session.get(User, user_id)


def _register_blueprints(app: Flask) -> None:
    from .routes import admin, auth, core_paper, dashboard, exam_technique, explainit, public, revision

    app.register_blueprint(public.bp)
    app.register_blueprint(auth.bp)
    app.register_blueprint(dashboard.bp)
    app.register_blueprint(core_paper.bp)
    app.register_blueprint(revision.bp)
    app.register_blueprint(exam_technique.bp)
    app.register_blueprint(explainit.bp)
    app.register_blueprint(admin.bp)


def _register_error_handlers(app: Flask) -> None:
    from flask import render_template

    @app.errorhandler(403)
    def forbidden(_err):  # noqa: ANN001
        return render_template("errors/403.html"), 403

    @app.errorhandler(404)
    def not_found(_err):  # noqa: ANN001
        return render_template("errors/404.html"), 404

    @app.errorhandler(500)
    def server_error(_err):  # noqa: ANN001
        return render_template("errors/500.html"), 500


def _bootstrap_database(app: Flask) -> None:
    """Create tables (dev only) and seed the initial admin account."""
    from .services.auth_seed import ensure_admin_account, ensure_tables

    with app.app_context():
        try:
            ensure_tables()
            ensure_admin_account()
        except Exception:  # noqa: BLE001
            app.logger.exception("Database bootstrap failed")


def _maybe_sync_content(app: Flask) -> None:
    if not app.config.get("CONTENT_SYNC_ON_STARTUP"):
        return
    from .services.content_loader import sync_all

    with app.app_context():
        try:
            sync_all()
        except Exception:  # noqa: BLE001
            app.logger.exception("Content sync failed on startup")


def _configure_logging(app: Flask) -> None:
    level = logging.DEBUG if app.debug else logging.INFO
    logging.basicConfig(level=level, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
