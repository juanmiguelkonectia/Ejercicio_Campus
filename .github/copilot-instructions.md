# Copilot instructions — campus

## Quick project summary 🔧
- Single-file Flask web app: `app.py` is the main entry point. Templates live in `templates/` (`base.html`, `login.html`, `user.html`).
- Intended to accept a login form and (commented-out) save users to a PostgreSQL DB via `psycopg2`.
- Repo is minimal and educational; expect missing infra (no `requirements.txt`, no tests, no CI).

## Key files to inspect 📁
- `app.py` — routes and app logic (login handling, DB-connection example commented out).
- `templates/login.html` — Jinja2 template with form field names (note: `name="email"`).
- `templates/user.html` — shows how handler renders variables (`usuario`, `password`, `email`).

## Concrete, discoverable patterns & gotchas ⚠️
- Language/context: templates and variables are in Spanish (`usuario`, `correo`, etc.). Keep messages and variable names consistent.
- Field name mismatch: `app.py` reads `request.form["correo"]` while `login.html` uses `name="email"`. This causes KeyError on POST. Use `.get()` or fix the key.
  - Example fix: `email = request.form.get('email')` (prefer `.get()` to avoid exceptions).
- Current behavior leaks passwords: the app prints and renders the raw password (`print(...)` and `user.html` shows `{{ password }}`). Avoid committing or preserving this behavior in production changes.
- DB code is illustrative and commented out. If enabling DB: follow the style in the commented `conectarCampus()` and move credentials to env vars rather than hardcoding.

## Typical developer workflows (how to run locally) ▶️
- Activate the repo virtual env if available: `.venv` is present; use your usual activation on Windows (PowerShell): `.\.venv\Scripts\Activate.ps1`.
- Install dependencies (not provided): `pip install flask psycopg2-binary` (or preferred DB driver). Add a `requirements.txt` after confirming versions.
- Run locally (used by author): `Flask --app app run` (or `python -m flask run`) — this starts the dev server.
- Use `FLASK_DEBUG=1` or `set FLASK_ENV=development` for live reload while developing.

## Specific code change suggestions an agent can implement ✅
- Fix form key bug and make form parsing robust:
  - Replace `email = request.form["correo"]` with `email = request.form.get("email")` and use `.get()` for other fields.
- Remove printing of passwords and stop rendering passwords in `user.html`.
  - Replace `print("Password ingresado:", password)` with `app.logger.info("login attempt for %s", usuario)`.
- When adding DB persistence, use environment variables and parameterized queries (the commented example already uses `%s` placeholders — keep that pattern).
- Add `requirements.txt` and a simple `Procfile` or instructions in README to document run commands.

## Tests & CI (current state) 🧪
- No tests or CI exist. Helpful first tasks: add minimal Flask route tests using `pytest` and Flask test client, and a GitHub Action that runs `pytest`.

## Style & conventions to follow
- Use Spanish identifiers/messages where the existing code does (e.g., `usuario`). Keep new templates/messages consistent.
- Prefer `app.logger` to `print()` for server logs.
- Keep templates simple and use `templates/base.html` as the layout to extend.

## When in doubt — quick pointers for PRs ✍️
- Small, focused PRs that fix one of the concrete issues above (form key bug, password exposure, add requirements, or enable DB with env vars) are preferred.
- Include a reproduction step and a short test (e.g., a Flask test that POSTs to `/login`) for any behavioral change.

---
If you'd like, I can open a PR that (a) fixes the `email` key bug, (b) stops rendering/printing the password, and (c) adds a `requirements.txt` and a minimal test. Would you like me to proceed?