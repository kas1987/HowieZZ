# ZELEX Development — Quick Start

Get a local ZELEX dev environment running in **~5 minutes**.

## Prerequisites

- **Docker Desktop** (Windows/Mac/Linux) — [install here](https://www.docker.com/products/docker-desktop)
- **Git** — clone or sync the repo
- **~2 GB disk** for Docker image + dependencies

No need to install Python, Node.js, or Caddy separately — Docker handles it all.

---

## Start Dev Server

### Windows
```powershell
.\start-dev.bat
```

### macOS / Linux
```bash
chmod +x start-dev.sh
./start-dev.sh
```

**What this does:**
- Builds Docker image (first run: ~90 sec)
- Installs Node.js + Python dependencies
- Runs test suite (`npm test` + `pytest`)
- Starts Python dev server on `http://localhost:9000`

The site opens automatically. Press `Ctrl+C` to stop.

---

## Commands

All commands work on Windows (`.bat`) and Unix (`.sh`):

| Command | What it does |
|---------|-----------|
| `./start-dev` | Start Python dev server (default) |
| `./start-dev caddy` | Start Caddy server (advanced) |
| `./start-dev test` | Run tests only (no server) |
| `./start-dev build` | Run data pipeline |
| `./start-dev shell` | Drop into container shell |
| `./start-dev rebuild` | Force rebuild Docker image |
| `./start-dev stop` | Stop all containers |

---

## Common Workflows

### I just cloned the repo. What now?

```bash
./start-dev              # Installs, tests, and runs the site
```

Open `http://localhost:9000` in your browser. Done.

### I edited a Python file. Do I need to rebuild?

No. Your local edits are **live-mounted** into the container. Just refresh your browser.

If you edited `scripts/*.py`, run the build pipeline:
```bash
./start-dev build        # Regenerates db/*.json
```

### I edited HTML/CSS/JS. How do I test?

Refresh your browser — changes are live. If tests fail before refresh:
```bash
./start-dev test         # Run all tests
```

### I want to run individual pytest tests.

Drop into the container and run pytest directly:
```bash
./start-dev shell
python -m pytest tests/test_build_profiles.py -v
```

### I want to use Caddy instead of Python server.

```bash
./start-dev caddy        # Starts both zelex and caddy services
```

Access at `http://localhost:2015` (or configure hosts file for `howiez.local`).

---

## Troubleshooting

### Docker fails to start

Check if Docker Desktop is running. On Windows, it should be in the System Tray.

```bash
docker ps                # Should list containers
```

### Port 9000 is already in use

Stop the container and try a different port:
```bash
./start-dev stop
docker-compose run -p 9001:9000 zelex python serve.py 9000
```

Or kill the process using 9000:
```bash
# Windows
netstat -ano | findstr :9000
taskkill /PID <PID> /F

# macOS / Linux
lsof -i :9000
kill -9 <PID>
```

### Tests fail on first run

This is usually network-related (npm/pip installation). Rebuild and retry:
```bash
./start-dev rebuild
./start-dev
```

### I need to install a new Python package

Edit `requirements.txt`, then:
```bash
./start-dev rebuild
```

Or add it in the shell:
```bash
./start-dev shell
pip install <package>
```

### How do I stop the server?

Press `Ctrl+C` in the terminal, or in another terminal:
```bash
./start-dev stop
```

---

## Next Steps

- Read **[common-tasks.md](common-tasks.md)** for common development tasks.
- Read **[CONTRIBUTING.md](CONTRIBUTING.md)** for branch/commit style.
- Explore **[docs/](docs/)** for detailed guides (pipeline, analytics, design tokens).
- View the **[Component Storybook](docs/component-storybook.html)** for UI patterns.

---

## Estimated Time to Productivity

| Task | Time |
|------|------|
| Prerequisites (Docker installed) | 0 min |
| Clone repo | 1 min |
| `./start-dev` (first run) | 3 min |
| Site loads in browser | 1 min |
| **Total first-time setup** | **~5 min** |
| Reading CONTRIBUTING.md | 5 min |
| Reading common-tasks.md | 10 min |
| Understanding data pipeline | 20 min |
| **Total onboarding (ready to contribute)** | **~1 hour** |

---

## Support

- **Tests failing?** Check [CONTRIBUTING.md](CONTRIBUTING.md#tests)
- **Pipeline issues?** See [`docs/pipeline-runbook.md`](docs/pipeline-runbook.md)
- **Design tokens?** See [`docs/design-tokens-runbook.md`](docs/design-tokens-runbook.md)
- **Questions?** Ask in your team Slack channel or check [`docs/phase1-faq.md`](docs/phase1-faq.md)
