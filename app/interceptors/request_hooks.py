import time

from flask import g, request


def register_hooks(app):
    @app.before_request
    def start_timer():
        g.start_time = time.perf_counter()

    @app.after_request
    def log_request(response):
        if hasattr(g, "start_time"):
            elapsed_ms = (time.perf_counter() - g.start_time) * 1000
            app.logger.debug(
                "%s %s → %s (%.1fms)",
                request.method,
                request.path,
                response.status_code,
                elapsed_ms,
            )
        return response
