# 🌿 Agent Ai Builder (AAB)

_Modular, extensible, and privacy-first AI agent builder._  
Design and deploy context-driven “Agents” with persona-specific, scenario-aware responses in a no-code Streamlit UI.

**Live Demo:** https://mph-2025.streamlit.app

Tech pillars: **Context engineering** • **Layered prompt injection** • **Domain/shortcut modularity** • **Local data control**

---

## Table of Contents
- [About the App](#about-the-app)
- [Technical Features & Architecture](#technical-features--architecture)
  - [Context Engineering & Prompt Injection](#context-engineering--prompt-injection)
  - [Modularity & Extensibility](#modularity--extensibility)
  - [Local-first Data Persistence](#local-first-data-persistence)
  - [Modular UI & Navigation](#modular-ui--navigation)
- [File & Directory Structure](#file--directory-structure)
- [Installation & Setup](#installation--setup)
- [Configuration](#configuration)
- [Documentation](#documentation)
- [Privacy & Data Control](#privacy--data-control)
- [For Developers & Maintainers](#for-developers--maintainers)
- [Roadmap & Release Notes](#roadmap--release-notes)
- [Community & Support](#community--support)
- [License](#license)

---

## ⚡ About the App
Agent Ai Builder (AAB) enables parents, teachers, and domain experts to create highly customized AI helpers (“Agents”) with persona-specific, scenario-aware responses. Everything runs in a clean, mobile-friendly Streamlit UI. No code required.

- **Audience:** Parents, teachers, and domain experts  
- **Core capabilities:** Persona synthesis, layered prompt injection, structured response shortcuts, optional tools (RAG, web search), and local JSON persistence  
- **Design goals:** Modularity, transparency, portability, and privacy by default

---

## 🚀 Technical Features & Architecture

### 🔧 Context Engineering & Prompt Injection
**Dynamic Persona Profiles**
- Build agent profiles from sources (Book, Expert, Style, Domain)
- Include parent/child/teacher details, age/grade, and role
- Automated persona synthesis via multi-stage OpenAI prompt flow
- All parameters are available for prompt injection in every query for stateful, scenario-appropriate answers

**Layered Prompt Injection**
- System prompts are composed at runtime from:
  - Persona description (domain, principles, philosophy)
  - User/child names, age/grade (age/role targeting)
  - Current query
  - (Optional) Shortcut-specific instructions (e.g., “Explain with examples”)
- Fully modular and runtime-extensible—add new domains/instructions in the UI without code changes

**Structured Response Shortcuts**
- Define response shapes (e.g., summary, plan, counsel, checklist)
- User-editable, domain-aware, and persistent across sessions

### 💡 Modularity & Extensibility
- **Domain-specific & custom shortcuts:** Parent, Teacher, AV, or any custom domain; load, create, and persist templates
- **Plug-in ready:** Per-agent enablement for document upload (RAG), web search, and future tools (multi-modal, 3rd-party APIs)
- **Profile-specific tooling:** Flags for RAG/document search, web search, and extensible OpenAI tools/custom functions

### 📦 Local-first Data Persistence
- Everything stored locally in `/data/` (profiles, chats, memory, sources, shortcuts) as human-readable JSON
- Atomic save/load on every change → no silent data loss
- Portable files for easy backup or migration  
_Future cloud (planned):_ Optional encrypted sync, multi-device, and import/export via `/data/`

### 🧩 Modular UI & Navigation
- **Step-based UI:** Create agent → Edit → Chat → History → Sources/Settings (each as its own function/component)
- **Mobile-first:** Card-based navigation, responsive layout, touch-optimized controls
- **Separation of concerns:** Decoupled UI, data persistence, and agent/context logic

---

## ⚙️ File & Directory Structure

```text
AAB/
├─ main.py                      # Streamlit app & core logic
├─ requirements.txt             # Python dependencies
├─ assets/                      # Images, icons, UI assets
├─ data/
│  ├─ parent_helpers_profiles.json
│  ├─ parent_helpers_responses.json
│  ├─ parent_helpers_sources.json
│  ├─ parent_helpers_shortcuts.json
│  └─ parent_helpers_memory.json
├─ docs/
│  ├─ mphUserManual draft.docx
│  ├─ My Parent Helpers - Prompt Injection and Message Structures.docx
│  └─ README.md
└─ .gitignore
```

**Files & Purpose**

| File | Purpose |
|---|---|
| `main.py` / `app.py` | Streamlit app, modular UI/logic |
| `requirements.txt` | Python deps (Streamlit, OpenAI, pydantic, …) |
| `data/parent_helpers_profiles.json` | Saved agent profiles |
| `data/parent_helpers_responses.json` | Chat history |
| `data/parent_helpers_sources.json` | Book/expert/style/domain sources |
| `data/parent_helpers_shortcuts.json` | Response shortcut templates |
| `data/parent_helpers_memory.json` | Persistent chat memory per profile |

---

## 🛠️ Installation & Setup

**Requirements**
- Python 3.9+
- OpenAI API key

**Quick Start**
```bash
git clone https://github.com/yourusername/mph2025-app.git
cd mph2025-app
pip install -r requirements.txt
streamlit run main.py
```

**Run (alt)**
```bash
python -m streamlit run main.py
```

---

## 🔧 Configuration

**Streamlit secrets**
```toml
# .streamlit/secrets.toml
[general]
openai_key = "sk-xxxxxxxxxxxxxxxxx"
```
Or set via **Streamlit Cloud → Secrets** UI.

---

## 📖 Documentation

- **User Manual:** [docs/mphUserManual%20draft.docx](docs/mphUserManual%20draft.docx)
- **Prompt Engineering Guide:** [docs/My%20Parent%20Helpers%20-%20Prompt%20Injection%20and%20Message%20Structures.docx](docs/My%20Parent%20Helpers%20-%20Prompt%20Injection%20and%20Message%20Structures.docx)
- **Quick Start:** In-app onboarding (first run)

> Tip: For a direct download from GitHub, append `?raw=1` to the links above, e.g., `docs/mphUserManual%20draft.docx?raw=1`

---

## 🔒 Privacy & Data Control
- **Local by default:** Profiles, chats, and customizations are stored on your machine
- **No accounts, no forced sync**
- **Cloud support** is opt-in (planned) for encrypted sync and multi-device

---

## 🧪 For Developers & Maintainers
- **Extensible codebase:** Add new agent types, shortcuts, and UI pages with minimal changes
- **Data-driven:** Swap JSON files to test new shortcut/domain sets
- **Prompt/response modularity:** Modify context injection or structured prompts at function or data level
- **Integrations:** Built to support GPT-4o, OpenAI tools, file search, web search; easy to extend to more endpoints

**Typical extension points**
- New domain bundles (sources + shortcuts JSON)
- Additional tools (RAG, web search, custom APIs)
- UI pages (e.g., admin console, educator hub)

---

## 🛣️ Roadmap & Release Notes
- Release notes & roadmap: `docs/RELEASE_NOTES.md`
- Upcoming: Multi-user support, encrypted sync, plugin/extension API, agent export/import, enterprise support

---

## 🤝 Community & Support
- **Website:** https://myparenthelpers.com
- **Contributions:** Open source, MIT License — PRs and feature ideas welcome!

---

## 🪪 License
MIT License — see `LICENSE` (or repository header).
