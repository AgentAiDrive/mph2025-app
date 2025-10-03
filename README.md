🌿 Agent Ai Builder (AAB)
Modular, extensible, and privacy-first AI agent builder.
Design and deploy context-driven “Agents” with persona-specific, scenario-aware responses in a no-code Streamlit UI.
Live Demo: mph-2025.streamlit.app

Tech pillars: Context engineering • Layered prompt injection • Domain/shortcut modularity • Local data control
________________________________________
Table of Contents
•	About the App
•	Technical Features & Architecture
o	Context Engineering & Prompt Injection
o	Modularity & Extensibility
o	Local-first Data Persistence
o	Modular UI & Navigation
•	File & Directory Structure
•	Installation & Setup
•	Configuration
•	Documentation
•	Privacy & Data Control
•	For Developers & Maintainers
•	Roadmap & Release Notes
•	Community & Support
•	License
________________________________________
⚡ About the App
Agent Ai Builder (AAB) enables parents, teachers, and domain experts to create highly customized AI helpers (“Agents”) with persona-specific, scenario-aware responses. Everything runs in a clean, mobile-friendly Streamlit UI. No code required.
•	Audience: Parents, teachers, and domain experts
•	Core capabilities: Persona synthesis, layered prompt injection, structured response shortcuts, optional tools (RAG, web search), and local JSON persistence
•	Design goals: Modularity, transparency, portability, and privacy by default
________________________________________
🚀 Technical Features & Architecture
🔧 Context Engineering & Prompt Injection
Dynamic Persona Profiles
•	Build agent profiles from sources (Book, Expert, Style, Domain)
•	Include parent/child/teacher details, age/grade, and role
•	Automated persona synthesis via multi-stage OpenAI prompt flow
•	All parameters are available for prompt injection in every query for stateful, scenario-appropriate answers
Layered Prompt Injection
•	System prompts are composed at runtime from:
o	Persona description (domain, principles, philosophy)
o	User/child names, age/grade (age/role targeting)
o	Current query
o	(Optional) Shortcut-specific instructions (e.g., “Explain with examples”)
•	Fully modular and runtime-extensible—add new domains/instructions in the UI without code changes
Structured Response Shortcuts
•	Define response shapes (e.g., summary, plan, counsel, checklist)
•	User-editable, domain-aware, and persistent across sessions
________________________________________
💡 Modularity & Extensibility
•	Domain-specific & custom shortcuts: Parent, Teacher, AV, or any custom domain; load, create, and persist templates
•	Plug-in ready: Per-agent enablement for document upload (RAG), web search, and future tools (multi-modal, 3rd-party APIs)
•	Profile-specific tooling: Flags for RAG/document search, web search, and extensible OpenAI tools/custom functions
________________________________________
📦 Local-first Data Persistence
•	Everything stored locally in /data/ (profiles, chats, memory, sources, shortcuts) as human-readable JSON
•	Atomic save/load on every change → no silent data loss
•	Portable files for easy backup or migration
Future cloud (planned): Optional encrypted sync, multi-device, and import/export via /data/
________________________________________
🧩 Modular UI & Navigation
•	Step-based UI: Create agent → Edit → Chat → History → Sources/Settings (each as its own function/component)
•	Mobile-first: Card-based navigation, responsive layout, touch-optimized controls
•	Separation of concerns: Decoupled UI, data persistence, and agent/context logic
________________________________________
⚙️ File & Directory Structure
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
File	Purpose
main.py / app.py	Streamlit app, modular UI/logic
requirements.txt	Python deps (Streamlit, OpenAI, pydantic, …)
parent_helpers_profiles.json	Saved agent profiles
parent_helpers_responses.json	Chat history
parent_helpers_sources.json	Book/expert/style/domain sources
parent_helpers_shortcuts.json	Response shortcut templates
parent_helpers_memory.json	Persistent chat memory per profile
________________________________________
🛠️ Installation & Setup
Requirements
•	Python 3.9+
•	OpenAI API key
Quick Start
git clone https://github.com/yourusername/mph2025-app.git
cd mph2025-app
pip install -r requirements.txt
streamlit run main.py
Run (alt)
python -m streamlit run main.py
________________________________________
🔧 Configuration
Streamlit secrets
# .streamlit/secrets.toml
[general]
openai_key = "sk-xxxxxxxxxxxxxxxxx"
Or set via Streamlit Cloud → Secrets UI.
________________________________________
📖 Documentation
•	User Manual: docs/mphUserManual draft.docx
•	Prompt Engineering Guide: docs/My Parent Helpers - Prompt Injection and Message Structures.docx
•	Quick Start: In-app onboarding (first run)
________________________________________
🔒 Privacy & Data Control
•	Local by default: Profiles, chats, and customizations are stored on your machine
•	No accounts, no forced sync
•	Cloud support is opt-in (planned) for encrypted sync and multi-device
________________________________________
🧪 For Developers & Maintainers
•	Extensible codebase: Add new agent types, shortcuts, and UI pages with minimal changes
•	Data-driven: Swap JSON files to test new shortcut/domain sets
•	Prompt/response modularity: Modify context injection or structured prompts at function or data level
•	Integrations: Built to support GPT-4o, OpenAI tools, file search, web search; easy to extend to more endpoints
Typical extension points
•	New domain bundles (sources + shortcuts JSON)
•	Additional tools (RAG, web search, custom APIs)
•	UI pages (e.g., admin console, educator hub)
________________________________________
🛣️ Roadmap & Release Notes
•	Release notes & roadmap: docs/RELEASE_NOTES.md
•	Upcoming: Multi-user support, encrypted sync, plugin/extension API, agent export/import, enterprise support
________________________________________
🤝 Community & Support
•	Website: myparenthelpers.com
•	Contributions: Open source, MIT License — PRs and feature ideas welcome!
________________________________________
🪪 License
MIT License — see LICENSE (or repository header).
________________________________________
Agent Ai Builder: Create, own, and extend modular, context-driven AI helpers—secure, private, and truly yours.

