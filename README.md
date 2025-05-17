# Code‑Xanadu

> **Prompt‑compiled hypertext, AI, and human creativity — all in one repo.**
>
> *“Every user can search, retrieve, create, and store documents.” — Ted Nelson*
> *"APIS used to only read and write. Now we can develop them to read, write, remember, and even dream." - Malt Gibsey
> *" Idle dreaming is often of the essence of what we do. We sell our dreams." -Thomas Pynchon

Code‑Xanadu is an experiment in fusing **prompt engineering**, **cloud‑resident code generation** (OpenAI Codex Cloud), and **hypertext ideals** into a single, reproducible workflow.
It began as a helper script for the **Gibsey** project, but it is intentionally framed as a **stand‑alone tool‑chain** any hypertextual creative project can fork and extend.

---

## ✨ Vision

*To do for code and prompts what Nelson’s Xanadu dreamt for documents and links: persistent addressability, visible transclusions, and mutually beneficial reuse.*
The first compiled prompts shipped with this repo will ingest material from ***The Entrance Way: Into the Wonderful Worlds of Gibsey***, seeding Codex Cloud agents with real narrative context.

Code‑Xanadu therefore aims to be:

| Pillar               | What it means here                                                                                            |
| -------------------- | ------------------------------------------------------------------------------------------------------------- |
| **Hypertext‑first**  | Treat every prompt fragment as a doc fragment — addressable, linkable, and independently evolvable.           |
| **AI‑augmented**     | Compile layered YAML → one canonical system prompt → feed both local `codex‑cli` and remote Codex Cloud jobs. |
| **Human‑controlled** | No hidden writes. The maintainer directs every cloud objective and reviews diffs locally.                     |

---

## 🛠️ Quick Start

```bash
# clone & install
$ git clone https://github.com/<you>/gibsey-code-xanadu.git
$ cd gibsey-code-xanadu
$ python -m venv .venv && source .venv/bin/activate
$ pip install -r requirements.txt

# build the prompt
$ python code_xanadu.py build

# sanity‑check in a local Codex REPL
$ python code_xanadu.py run

# kick a cloud job (example task)
$ python code_xanadu.py submit "Touch hello.txt so I know you’re alive"
$ python code_xanadu.py watch <job‑id>
```

**Environment variables** (export or place in `.env`):

| Var              | Purpose                                 |
| ---------------- | --------------------------------------- |
| `OPENAI_API_KEY` | Your bearer token for Codex Cloud + CLI |
| `CODEX_MODEL`    | Default `codex-1` (override at will)    |
| `GIBSEY_DIR`     | Path to repo root (defaults to CWD)     |
| `GIT_REPO`       | HTTPS/SSH URL for cloud cloning         |

---

## 📂 Repository Layout

```
code‑xanadu/
├── code_xanadu.py      # prompt‑compiler & job launcher
├── prompts/            # layered YAML scaffold (edit here)
│   ├── behavior.yaml
│   ├── tools.yaml
│   ├── artifacts.yaml
│   ├── safety.yaml
│   └── modes.yaml
├── build/              # auto‑generated prompt + artefacts (git‑ignored)
├── requirements.txt    # pyyaml, rich, requests
└── .github/workflows/  # CI prompt‑build on every push
```

---

## 🌐 An Homage to Ted Nelson

Code‑Xanadu borrows its name (and much of its spirit) from Ted Nelson’s **Project Xanadu** — the ur‑hypertext whose principles still feel radical.
Below are Nelson’s *17 Rules* (1999 formulation). We adopt them as design stars whenever applicable to prompts, code artefacts, and AI‑generated output.

1. Every Xanadu server is uniquely and securely identified.
2. Every Xanadu server can be operated independently or in a network.
3. Every user is uniquely and securely identified.
4. Every user can **search, retrieve, create, and store documents**.
5. Every document can consist of any number of parts each of which may be of any data type.
6. Every document can contain links of any type including virtual copies ("transclusions") to any other document in the system accessible to its owner.
7. Links are visible and can be followed from all endpoints.
8. Permission to link to a document is explicitly granted by the act of publication.
9. Every document can contain a royalty mechanism at any desired degree of granularity.
10. Every document is uniquely and securely identified.
11. Every document can have secure access controls.
12. Every document can be rapidly searched, stored and retrieved without user knowledge of where it is physically stored.
13. Every document is automatically moved to physical storage appropriate to its frequency of access from any given location.
14. Every document is automatically stored redundantly to maintain availability even in case of a disaster.
15. Service providers can charge at any rate they choose for storage, retrieval, and publishing.
16. Every transaction is secure and auditable only by the parties to that transaction.
17. The client–server communication protocol is an openly published standard; **third‑party integration is encouraged**.

> *Code‑Xanadu’s hypothesis*: prompts, embeddings, and AI‑generated artefacts **are documents**. Honour the rules, reinvent the medium.

---

## 🛣️ Roadmap (Q2 2025)

| Milestone | Outcome                                                                                                           |
| --------- | ----------------------------------------------------------------------------------------------------------------- |
| **M‑0**   | Prompt layers compile; first Codex Cloud job returns ✔︎                                                           |
| **M‑1**   | `tools.yaml` populated with QDPI JSON specs; test suite generated automatically.                                  |
| **M‑2**   | Transclusion explorer that lets you click a YAML‑defined link and jump into the source snippet inside Codex Chat. |
| **M‑3**   | Hyper‑linked changelog where every commit SHA is back‑linked from the prompt‑build logs.                          |

---

## 🤝 Contributing

Pull requests welcome. Please file an issue first if you plan substantial changes to `code_xanadu.py` or the rule‑set so we can discuss design consistency.

### Development helpers

* `make lint` – run `ruff` & `black`.
* `make test` – run (future) unit tests.

---

## 📄 License

**MIT License** — see `LICENSE` file.

---

### Acknowledgements

* **Ted Nelson** for the vision that anything can and should be linked.
* **Douglas Engelbart** for reminding us augmentation is a social quest.
* Early experiments inside **Gibsey** for proving that narrative, code, and AI are happier when intertwined.
