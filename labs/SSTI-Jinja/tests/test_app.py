import pytest

import app as app_module
from app import create_app


@pytest.fixture()
def client():
    app = create_app({"TESTING": True})
    return app.test_client()


def test_index_displays_the_lab(client):
    response = client.get("/")

    assert response.status_code == 200
    assert "SSTI Lab" in response.get_data(as_text=True)


def test_vulnerable_mode_evaluates_jinja_expression(client):
    response = client.post(
        "/",
        data={"template": "{{ 7 * 7 }}", "mode": "vulnerable"},
    )

    body = response.get_data(as_text=True)
    assert response.status_code == 200
    assert '<output id="result">49</output>' in body


def test_safe_mode_treats_jinja_expression_as_text(client):
    response = client.post(
        "/",
        data={"template": "{{ 7 * 7 }}", "mode": "safe"},
    )

    body = response.get_data(as_text=True)
    assert response.status_code == 200
    assert '<output id="result">{{ 7 * 7 }}</output>' in body
    assert '<output id="result">49</output>' not in body


def test_safe_mode_escapes_html_once(client):
    response = client.post(
        "/",
        data={"template": "<b>hello</b>", "mode": "safe"},
    )

    body = response.get_data(as_text=True)
    assert '<output id="result">&lt;b&gt;hello&lt;/b&gt;</output>' in body


def test_invalid_template_shows_a_friendly_error(client):
    response = client.post(
        "/",
        data={"template": "{{", "mode": "vulnerable"},
    )

    body = response.get_data(as_text=True)
    assert response.status_code == 200
    assert "Template error" in body


def test_template_runtime_error_does_not_return_500(client):
    response = client.post(
        "/",
        data={"template": "{{ 1 / 0 }}", "mode": "vulnerable"},
    )

    body = response.get_data(as_text=True)
    assert response.status_code == 200
    assert "Template error (ZeroDivisionError)" in body


def test_input_is_limited(client):
    response = client.post(
        "/",
        data={"template": "a" * 201, "mode": "vulnerable"},
    )

    assert response.status_code == 200
    assert "Tối đa 200 ký tự" in response.get_data(as_text=True)


def test_security_headers_are_present(client):
    response = client.get("/")

    assert response.headers["X-Content-Type-Options"] == "nosniff"
    assert response.headers["X-Frame-Options"] == "DENY"
    assert response.headers["Content-Security-Policy"].startswith("default-src 'self'")


def test_stylesheet_is_available(client):
    response = client.get("/static/styles.css")

    assert response.status_code == 200
    assert response.content_type == "text/css; charset=utf-8"


def test_run_binds_to_conflict_free_local_port(monkeypatch):
    run_options = {}

    def fake_run(**options):
        run_options.update(options)

    monkeypatch.setattr(app_module.app, "run", fake_run)

    app_module.run()

    assert run_options == {"host": "127.0.0.1", "port": 8000}
