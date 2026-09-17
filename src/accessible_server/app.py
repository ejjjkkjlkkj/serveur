from __future__ import annotations

import html
import platform
import socket
import sys
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from . import __version__
from .database import add_event, database_path, initialize, recent_events


@asynccontextmanager
async def lifespan(_: FastAPI):
    initialize()
    add_event(f"Accessible Server {__version__} started")
    yield


app = FastAPI(
    title="Accessible Server",
    version=__version__,
    description="Serveur Windows administrable au clavier et avec lecteur d'ecran.",
    lifespan=lifespan,
)


def health_payload() -> dict[str, str]:
    return {
        "status": "ok",
        "version": __version__,
        "host": socket.gethostname(),
        "python": platform.python_version(),
        "platform": platform.platform(),
    }


def render_home() -> str:
    health = health_payload()
    events = recent_events(10)
    rows = "".join(
        "<tr>"
        f"<td>{html.escape(str(event['created_at']))}</td>"
        f"<td>{html.escape(str(event['level']))}</td>"
        f"<td>{html.escape(str(event['message']))}</td>"
        "</tr>"
        for event in events
    )
    if not rows:
        rows = '<tr><td colspan="3">Aucun événement enregistré.</td></tr>'

    return f"""<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Accessible Server — Administration</title>
<style>
:root {{ color-scheme: light dark; font-family: system-ui, sans-serif; }}
body {{ max-width: 72rem; margin: 0 auto; padding: 1rem; line-height: 1.55; }}
a {{ text-underline-offset: .2em; }}
.skip-link {{ position: absolute; left: .5rem; top: -4rem; padding: .75rem; background: Canvas; }}
.skip-link:focus {{ top: .5rem; }}
:focus-visible {{ outline: .2rem solid Highlight; outline-offset: .2rem; }}
nav ul {{ display: flex; flex-wrap: wrap; gap: 1rem; padding-left: 1.25rem; }}
dl {{ display: grid; grid-template-columns: max-content 1fr; gap: .35rem 1rem; }}
dt {{ font-weight: 700; }}
table {{ border-collapse: collapse; width: 100%; }}
th, td {{ border: 1px solid GrayText; padding: .5rem; text-align: left; vertical-align: top; }}
.status-ok {{ font-weight: 700; }}
</style>
</head>
<body>
<a class="skip-link" href="#contenu">Aller au contenu principal</a>
<header>
<h1>Accessible Server</h1>
<p>Administration locale conçue pour le clavier, NVDA, JAWS et le Narrateur.</p>
<nav aria-label="Navigation principale">
<ul>
<li><a href="#etat">État</a></li>
<li><a href="#journal">Journal</a></li>
<li><a href="/docs">API</a></li>
</ul>
</nav>
</header>
<main id="contenu">
<section id="etat" aria-labelledby="titre-etat">
<h2 id="titre-etat">État du serveur</h2>
<p class="status-ok" aria-live="polite">Serveur opérationnel.</p>
<dl>
<dt>Version</dt><dd>{html.escape(health['version'])}</dd>
<dt>Machine</dt><dd>{html.escape(health['host'])}</dd>
<dt>Python</dt><dd>{html.escape(health['python'])}</dd>
<dt>Plateforme</dt><dd>{html.escape(health['platform'])}</dd>
<dt>Base de données</dt><dd>{html.escape(str(database_path()))}</dd>
</dl>
</section>
<section id="journal" aria-labelledby="titre-journal">
<h2 id="titre-journal">Journal récent</h2>
<div tabindex="0" aria-label="Tableau défilable du journal">
<table>
<caption>10 derniers événements du serveur</caption>
<thead><tr><th scope="col">Date UTC</th><th scope="col">Niveau</th><th scope="col">Message</th></tr></thead>
<tbody>{rows}</tbody>
</table>
</div>
</section>
<section aria-labelledby="titre-clavier">
<h2 id="titre-clavier">Utilisation au clavier</h2>
<p>Utilisez Tab et Maj+Tab pour parcourir les commandes. Le lien « Aller au contenu principal » devient visible au focus.</p>
</section>
</main>
<footer>
<p>Accessible Server {html.escape(__version__)} — API de santé : <a href="/api/health">/api/health</a>.</p>
</footer>
</body>
</html>"""


@app.get("/", response_class=HTMLResponse, include_in_schema=False)
def home() -> str:
    return render_home()


@app.get("/api/health")
def health() -> dict[str, str]:
    return health_payload()


@app.get("/api/events")
def events(limit: int = 20) -> dict[str, object]:
    return {"events": recent_events(limit)}


@app.get("/api/runtime")
def runtime() -> dict[str, object]:
    return {
        "executable": sys.executable,
        "database": str(database_path()),
        "argv": sys.argv,
    }
