🌿 My Parent Helpers (MPH)

Test drive the app → https://mph-2025.streamlit.app/

My Parent Helpers (MPH) is a mobile-friendly, AI-powered application that enables parents to create personalized digital parenting assistants — called Agents — based on parenting books, experts, or styles. These agents provide contextual, age-appropriate guidance tailored to your child’s developmental needs and your preferred parenting approach.


---

🚀 Features

🧠 Contextual Prompt Engineering

MPH uses a multi-layered context injection technique to shape how the AI responds. Every query sent to the model dynamically injects:

✅ Persona Description – Synthesized from your chosen parenting source

✅ Parent and Child Names – For personalization

✅ Child’s Age – For developmentally appropriate language

✅ Structured Prompt Type – Defines format, tone, and purpose


This ensures every response is context-aware, customized, and aligned with your parenting goals.


---

👨‍👩‍👧‍👦 Agent Creation & Persona Generation

Create up to 99 unique parenting agents, each with:

A selected parenting source:

📚 Books

🧑‍ Experts

✨ Styles


A dynamically generated persona using GPT-4o

Custom values: Parent name, child name, age, profile name

Editable persona summaries before saving



---

💬 AI Chat With Purposeful Shortcuts

Each query can be refined using a response Shortcut that adjusts:

Format

Instruction to the model

Comprehension level


Shortcut	Purpose	Format	Language Level

💬 Default	Generic AI chat	Natural	Adaptive
🤝 Connect	Explain complex ideas	3 Examples	Child age
🌱 Grow	Parenting strategies	3 Advanced Tips	Adult
🔍 Explore	Interactive Q&A	Guided Answer	Child age
🛠 Resolve	Conflict resolution	Step-by-step	Child age
❤ Support	Emotional guidance	Supportive Advice	Child age



---

🔄 History & Management

Save and manage AI responses per profile

View and edit saved chats

Edit or delete agent profiles

Full export and persistence using local .json files



---

🔐 Requirements

Python 3.9+

OpenAI API key



---

📦 Installation

git clone https://github.com/yourusername/mph2025-app.git
cd mph2025-app
pip install -r requirements.txt
streamlit run app.py


---

🧬 Streamlit Secrets Setup

🔹 On Streamlit Cloud

1. Open your Streamlit Dashboard.


2. Go to your app → Secrets tab.


3. Add:



openai_key = "sk-xxxxxxxxxxxxxxxxxxxxx"

4. Save & rerun.



🔹 Locally

Create .streamlit/secrets.toml:

[general]
openai_key = "sk-xxxxxxxxxxxxxxxxxxxxx"

Or update directly in code:

openai.api_key = st.secrets.get("openai_key", "YOUR_OPENAI_API_KEY")


---

📂 Key Files

File	Purpose

app.py	Main application logic
parent_helpers_profiles.json	Saved agent profiles
parent_helpers_responses.json	Saved chat history
requirements.txt	Python dependencies



---

📖 Documentation

In-app User Manual and Quick Start Guide

Full walk-through for first-time users

Dynamic tooltips and responsive design

Editable persona fields and saved state management



---

✍️ Custom Sources & Editable Agents

MPH gives parents full control over the knowledge base powering each agent.

🔧 Source Management

You can edit the parenting Books, Experts, and Styles used to generate personas:

Add custom entries to the agent source lists

Remove or update existing parenting sources

Saved sources persist across sessions in a local JSON file

Changes are reflected immediately in new agent creation


🧑‍🎨 Editable Agent Personas

Once a persona is generated:

Review and approve the AI-generated summary

Edit the persona’s tone, principles, or values to match your parenting philosophy

Combine your custom source entries with a tailored persona for fully personalized parenting agents


This flexibility allows you to:

Reproduce advice aligned with your favorite parenting authors or mentors

Build unique agent voices and tones for different children

Continuously evolve your parenting strategies as your child grows


MPH isn't just AI-assisted — it's AI-shaped by you.


---

🛡️ License

MIT License


---

🤝 Contributing

We welcome contributions! Fork this repo and submit a PR for improvements or bug fixes.


---

📫 Contact

Questions or feedback? Visit www.myparenthelpers.com for support, resources, and contact options.
