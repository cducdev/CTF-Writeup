from flask import Flask, render_template, render_template_string, request


MAX_TEMPLATE_LENGTH = 200
DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 8000


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_mapping(MAX_CONTENT_LENGTH=4096)

    if test_config:
        app.config.update(test_config)

    @app.after_request
    def add_security_headers(response):
        response.headers["Content-Security-Policy"] = (
            "default-src 'self'; style-src 'self'; img-src 'none'; "
            "script-src 'none'; base-uri 'none'; form-action 'self'; "
            "frame-ancestors 'none'"
        )
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Referrer-Policy"] = "no-referrer"
        response.headers["Cache-Control"] = "no-store"
        return response

    @app.route("/", methods=["GET", "POST"])
    def index():
        payload = ""
        mode = "vulnerable"
        result = None
        error = None

        if request.method == "POST":
            payload = request.form.get("template", "")
            mode = request.form.get("mode", "vulnerable")

            if mode not in {"vulnerable", "safe"}:
                error = "Chế độ không hợp lệ."
            elif not payload.strip():
                error = "Hãy nhập một Jinja expression."
            elif len(payload) > MAX_TEMPLATE_LENGTH:
                error = f"Tối đa {MAX_TEMPLATE_LENGTH} ký tự."
            else:
                try:
                    if mode == "vulnerable":
                        # INTENTIONALLY VULNERABLE: user input becomes template source.
                        result = render_template_string(payload)
                    else:
                        # SAFE COMPARISON: the outer fixed template escapes this data.
                        result = payload
                except Exception as exc:
                    # A learning lab should show concise template runtime errors, not a 500.
                    error = f"Template error ({type(exc).__name__}): {exc}"

        return render_template(
            "index.html",
            error=error,
            max_length=MAX_TEMPLATE_LENGTH,
            mode=mode,
            payload=payload,
            result=result,
        )

    return app


app = create_app()


def run():
    app.run(host=DEFAULT_HOST, port=DEFAULT_PORT)


if __name__ == "__main__":
    run()
