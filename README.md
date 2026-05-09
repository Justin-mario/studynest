# StudyNest

A specification-aligned learning tool for T-Level Digital Software Development students. Built around the DSD specification so every interaction maps to a performance outcome and assessment objective.

See `docs/studynest_requirements_v2_1.pdf` for the full requirements specification.

## Stack

| Layer | Choice |
| --- | --- |
| Backend | Flask 3.x (Python) |
| Templating | Jinja2 |
| Dynamic UI | HTMX + small vanilla JS |
| Styling | Tailwind CSS (CDN initially) |
| ORM | SQLAlchemy 2.x |
| Auth | Flask-Login + bcrypt |
| Database | Postgres (Supabase free tier) |
| Migrations | Alembic |
| LLM (primary) | Google Gemini Flash |
| LLM (fallback) | Groq |
| Voice input | Web Speech API (browser-side) |
| Hosting | alwaysdata.com |
| WSGI | Gunicorn (or alwaysdata's built-in Passenger) |

## Project layout

```
studynest/
├── app/                    Flask application package
│   ├── __init__.py         Application factory
│   ├── extensions.py       Shared extension singletons (db, login_manager, ...)
│   ├── routes/             Blueprints by surface (public, auth, student, admin)
│   ├── models/             SQLAlchemy models, one per entity
│   ├── services/           Domain services (content_loader, llm_client, ...)
│   ├── templates/          Jinja2 templates
│   └── static/             CSS/JS/images
├── content/                File-based content (Markdown topics, YAML quizzes)
├── prompts/                LLM system prompts (version-controlled)
├── tests/                  Pytest suite
├── scripts/                One-off scripts (content validation, seed data)
├── migrations/             Alembic migrations
├── docs/                   Requirements spec and supporting docs
├── config.py               Environment-driven config
├── run.py                  Local development entry point
├── wsgi.py                 Production WSGI entry point (alwaysdata)
├── requirements.txt        Runtime dependencies
└── requirements-dev.txt    Dev / test dependencies
```

## Local development

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements-dev.txt
copy .env.example .env
# edit .env — set SECRET_KEY, DATABASE_URL, LLM API keys
alembic upgrade head
python run.py
```

App runs at http://127.0.0.1:5000.

## Adding content

Topics, quizzes, command-verb guides, and misconceptions live as files in `content/` — no code changes needed to add a topic. See [content/README.md](content/README.md) for the schemas.

LLM system prompts live in `prompts/` and are version-controlled.

## Deployment (alwaysdata.com)

1. Create a Python site in alwaysdata, pointing to this repo's working directory.
2. Set the WSGI entry point to `wsgi.py` (callable `application`).
3. Set environment variables in the alwaysdata admin panel — same keys as `.env.example`.
4. Run `alembic upgrade head` once after first deploy.

## Testing

```powershell
pytest
pytest --cov=app --cov-report=term-missing
```

## License

TBD — MIT or Apache 2.0 likely. See requirements spec §18.4.
