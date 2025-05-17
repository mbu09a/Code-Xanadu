# Code‑Xanadu

> **Prompt‑compiled hypertext, AI, and human creativity — all in one repo.**
>
> *"Every user can search, retrieve, create, and store documents." — Ted Nelson*

Code‑Xanadu is an experiment in fusing **prompt engineering**, **cloud‑resident code generation** (OpenAI Codex Cloud), and **hypertext ideals** into a single, reproducible workflow.

## 🛠️ Quick Start

```bash
# clone & install
$ git clone https://github.com/<your-username>/gibsey-code-xanadu.git
$ cd gibsey-code-xanadu
$ python -m venv .venv && source .venv/bin/activate
$ pip install -r requirements.txt

# build the prompt
$ python code_xanadu.py build

# sanity‑check in a local Codex REPL
$ python code_xanadu.py run

# kick a cloud job (example task)
$ python code_xanadu.py submit "Touch hello.txt so I know you're alive"
$ python code_xanadu.py watch <job‑id>
```

## Environment Variables

Export these variables or place them in a `.env` file:

| Var              | Purpose                                 |
| ---------------- | --------------------------------------- |
| `OPENAI_API_KEY` | Your bearer token for Codex Cloud + CLI |
| `CODEX_MODEL`    | Default `codex-1` (override at will)    |
| `GIBSEY_DIR`     | Path to repo root (defaults to CWD)     |
| `GIT_REPO`       | HTTPS/SSH URL for cloud cloning         |

## 📂 Repository Layout

```
code‑xanadu/
├── code_xanadu.py      # prompt‑compiler & job launcher
├── prompts/            # layered YAML scaffold (edit here)
│   ├── behavior.yaml
│   ├── tools.yaml
│   ├── artifacts.yaml
│   ├── safety.yaml
│   └── modes.yaml
├── build/              # auto‑generated prompt + artefacts (git‑ignored)
├── requirements.txt    # pyyaml, rich, requests
└── .github/workflows/  # CI prompt‑build on every push
```

## 📄 License

**MIT License** — see `LICENSE` file.