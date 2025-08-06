🌿 Agent Ai Builder (AAB) – Technical Overview
Live Demo: mph-2025.streamlit.app

⚡ About the App
Agent Ai Builder (AAB) is a modular, extensible, and privacy-first AI agent builder platform. AAB empowers users (parents, teachers, domain experts) to design and deploy highly customized, context-driven AI helpers (“Agents”) with persona-specific, scenario-aware responses, all in a no-code Streamlit UI.
Core pillars: context engineering, layered prompt injection, domain/shortcut modularity, and local data control.

🚀 Technical Features & Architecture
🔧 Context Engineering & Prompt Injection
Dynamic Persona Profiles:
Persona synthesis is user-driven. Agent profiles are created using:

Source type/name (Book, Expert, Style, Domain)

Parent/child/teacher details, age/grade, and role

Automated persona synthesis using multi-stage OpenAI prompt flow

Every parameter is available for prompt injection in all queries, enabling stateful and scenario-appropriate answers

Layered Prompt Injection:

System prompts are dynamically composed with:

Persona description (domain, principles, philosophy)

User/child names, age/grade (for age/role targeting)

Current query

Optional: Shortcut-specific instructions (e.g., “Explain with examples”)

All prompt injection is modular and runtime-extensible—new domains or instructions can be added via UI without code changes

Structured Response Shortcuts:

Shortcuts define response formats (e.g., summary, plan, counsel, checklist)

User-editable, domain-aware, and persistent across sessions

💡 Modularity & Extensibility
Domain-Specific & Custom Shortcuts:

Parent, Teacher, AV, and any custom domain can be loaded or created with their own shortcut templates

Shortcuts and sources are editable and persisted in local JSON—extend or re-theme the app by editing these lists, not the code

Plug-in Ready:

Per-agent tool enablement: document upload (RAG), web search, etc.

Future integration for multi-modal input, third-party APIs, or custom toolchains

Profile-specific Tooling:

Each agent profile has flags for RAG/document search, web search, and can be extended with more OpenAI tools or custom functions

📦 Local-first Data Persistence
User Data is Local & Portable:

All profiles, chats, memory, sources, and shortcuts are stored as JSON files in /data/

No cloud or external sync required; files are portable and human-readable

Atomic save/load: every change is instantly written to disk; no silent data loss

Future Cloud Support:

Planned: Optional encrypted sync, multi-device, and import/export via /data/

🧩 Modular UI & Navigation
Step-based UI:

Each major operation (create agent, edit, chat, history, sources/settings) is its own function/component, allowing easy extension or refactoring

Mobile-first design:

Card-based navigation, responsive layout, and touch-optimized controls

Decoupled UI/Data/Logic:

Clean separation of data persistence, UI flow, and context/agent logic

⚙️ File & Directory Structure
pgsql
Copy
Edit
AAB/
├── main.py                        # Streamlit app & all logic
├── requirements.txt               # Python dependencies
├── assets/                        # Images, icons, UI assets
├── data/
│   ├── parent_helpers_profiles.json
│   ├── parent_helpers_responses.json
│   ├── parent_helpers_sources.json
│   ├── parent_helpers_shortcuts.json
│   └── parent_helpers_memory.json
├── docs/
│   ├── mphUserManual draft.docx
│   ├── My Parent Helpers - Prompt Injection and Message Structures.docx
│   └── README.md
└── .gitignore
File	Purpose
main.py / app.py	Streamlit app, modular UI/logic
requirements.txt	Python deps (Streamlit, OpenAI, pydantic, etc.)
parent_helpers_profiles.json	Saved agent profiles
parent_helpers_responses.json	Chat history
parent_helpers_sources.json	Book/expert/style/domain sources
parent_helpers_shortcuts.json	Response shortcut templates
parent_helpers_memory.json	Persistent chat memory per profile

🔌 Extensibility & Integration
Domain & shortcut modularity: Add or edit domains/shortcuts live via UI or JSON file

RAG & Tools: Enable document upload, vector search, and other tools per agent

Seamless OpenAI Integration: Support for GPT-4o, OpenAI tools, file_search, and web_search—easily extend to more endpoints

Future-Proof: PWA/mobile ready, cloud sync planned, easy to extend to new agent types and tools

🛠️ Installation & Setup
Requirements:

Python 3.9+

OpenAI API key

Quick Start:

sh
Copy
Edit
git clone https://github.com/yourusername/mph2025-app.git
cd mph2025-app
pip install -r requirements.txt
streamlit run main.py
Configure OpenAI API:

toml
Copy
Edit
# .streamlit/secrets.toml
[general]
openai_key = "sk-xxxxxxxxxxxxxxxxx"
Or use Streamlit Cloud secrets UI.

📖 Documentation
User Manual: /docs/mphUserManual draft.docx

Prompt Engineering Guide: /docs/My Parent Helpers - Prompt Injection and Message Structures.docx

Quick Start Guide: In-app onboarding (first use)

🔒 Privacy & Data Control
All data local by default: Profiles, chats, customizations are yours

No accounts, no forced sync: Cloud support is opt-in and planned only for future versions

🧪 For Developers & Maintainers
Extensible codebase:

Add new agent types, shortcuts, and UI pages with minimal code changes

Data files are modular and replaceable—test new shortcut or domain sets by swapping JSON

Prompt/response modularity:

Modify context injection or structured prompts at the function or data level

Upgrade & Changelog:

See /docs/ for feature history, roadmap, and upgrade notes

🛣️ Roadmap & Release Notes
Release notes & roadmap: /docs/RELEASE_NOTES.md

Upcoming: Multi-user support, encrypted sync, plugin/extension API, agent export/import, enterprise support

🤝 Community & Support
Web: myparenthelpers.com

Issues/Contributions: Open source, MIT License—PRs and feature ideas welcome!

Agent Ai Builder: Create, own, and extend your own modular, context-driven AI helpers—secure, private, and truly yours.

Would you like to add API reference, a detailed "for maintainers" section, or architecture diagrams? If you want a super-short version for GitHub or an extended version for internal onboarding, let me know!
