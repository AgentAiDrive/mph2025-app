# 🌿 My Parent Helpers (MPH)

**Test drive the app:** [mph-2025.streamlit.app](https://mph-2025.streamlit.app/)

**My Parent Helpers (MPH)** is your all-in-one, AI-powered assistant for real-world support—at home, in the classroom, or anywhere you need an expert at your side. MPH lets you create **personalized digital assistants (“Agents”)** based on your favorite books, experts, or styles, for Parenting, Teaching, or any custom domain you choose.

---

## 🚀 Key Features

### 🧠 Personalized, Context-Aware Guidance for Any Role

MPH’s advanced AI doesn’t just give generic advice—it uses everything you provide to deliver relevant, age-appropriate, and role-specific support, every time.

**Your Agents’ responses are always shaped by:**

* **Your chosen parenting style, educational approach, or expert** (select from included lists or add your own)
* **Your name and your child’s name (or your role as teacher/expert)**
* **Your child’s age, class grade, or leave blank for custom expert Agents**
* **The “Shortcut” you pick for each answer (see below!)**

---

### 👨‍👩‍👧‍👦🧑‍🏫🌟 Build Agents for Any Situation

* **Create up to 99 unique Agents**, each with their own:

  * Parenting source (Book, Expert, or Style)
  * Educational method or teaching philosophy
  * Custom domain expertise (technology, health, science, etc.)
  * GPT-powered, automatically generated persona—summarizing key principles and style
  * Editable values: name, age/grade, profile name, persona summary

**Perfect for:**

* Parents with kids of different ages or approaches
* Teachers with multiple classes or teaching methods
* Professionals who want a digital expert (custom “Other” Agents)

---

### 💬 AI Chat With Purposeful Shortcuts

**Every question can be fine-tuned with a “Shortcut” button.**
Shortcuts define the format, purpose, and level of every answer.

| Shortcut   | Example Use                  | Format / Focus         | Language Level |
| ---------- | ---------------------------- | ---------------------- | -------------- |
| 💬 Default | General chat/advice          | Conversational         | Adaptive       |
| 🤝 Connect | Explain something complex    | 3 Examples             | Child’s age    |
| 🌱 Grow    | Get strategies/tips          | 3 Advanced Suggestions | Adult/Parent   |
| 🔍 Explore | Learn something new/Q\&A     | Guided Answer          | Child’s age    |
| 🛠 Resolve | Resolve a conflict/challenge | Step-by-Step           | Child’s age    |
| ❤ Support  | Emotional guidance           | Supportive Advice      | Child’s age    |

**Teacher and Expert Agents come with their own shortcuts, too—like:**

* Lesson Outline
* Explain Concept
* Give Example
* Step-by-Step
* Pitfalls/Avoid

**Custom shortcuts for Other Agents are fully editable—make your Agent fit any domain or workflow!**

---

### 🔄 Save, Edit, and Manage—With Full Control

* **Save answers and conversations** for each Agent—review them anytime.
* **Edit or delete profiles, sources, and chats** with a tap.
* **All changes are instant**—no reload or restart needed.

---

### 🧩 Full Customization & Extensibility

* **Edit the lists of Books, Experts, Styles, and Domain Areas** for any Agent type—add your favorites or custom entries.
* **Add or modify shortcuts for any Agent**, at any time—tailor every chat to your real needs.
* **Instantly apply changes across the app**—new shortcuts and sources are available immediately for Agent creation and chat.

---

### 👨‍👩‍👧‍👦🧑‍🏫🌟 Multi-Role & Multi-Domain Support

* **Parent Agents:** Age-appropriate, style-aligned advice for any family scenario
* **Teacher Agents:** Lesson planning, Q\&A, explanations, and classroom support
* **Other/Expert Agents:** Build assistants for technology, healthcare, science, business, or any custom field

MPH is truly universal—**one app, endless possibilities**.

---

### 📱 Mobile-First, Friendly Interface

* **Works beautifully on phones, tablets, and computers**
* **Simple card-based navigation** for Agents, chats, and saved answers
* **Tooltips and in-app help everywhere**

---

## 🛡️ Private & Local

* Everything you create is saved **locally** on your device—your profiles, chats, and changes are yours alone.
* **No account required, no cloud storage** (unless you choose to sync).

---

## 🛠️ Getting Started

**What you need:**

* Python 3.9+
* An OpenAI API key (see below)

**To install:**

```sh
git clone https://github.com/yourusername/mph2025-app.git
cd mph2025-app
pip install -r requirements.txt
streamlit run app.py
```

**Set your OpenAI key:**

* On Streamlit Cloud: Go to your app’s **Secrets** tab, and add
  `openai_key = "sk-xxxxxxxxxxxx"`
* Locally: Create a file `.streamlit/secrets.toml`

  ```toml
  [general]
  openai_key = "sk-xxxxxxxxxxxx"
  ```

---

## 📂 Key Files

| File                            | Purpose                    |
| ------------------------------- | -------------------------- |
| `app.py`                        | Main application logic     |
| `parent_helpers_profiles.json`  | Saved Agent profiles       |
| `parent_helpers_responses.json` | Saved chat history         |
| `parent_helpers_sources.json`   | List of sources for Agents |
| `parent_helpers_shortcuts.json` | Saved shortcuts/actions    |
| `requirements.txt`              | Python dependencies        |

---

## 📖 Documentation & Help

* **Quick Start Guide and User Manual**—built into the app for first-time users
* **Dynamic tooltips and in-app help**—tap any “?” icon
* **Editable persona and Agent details**
* **All your changes are always saved**

**More resources:** [www.myparenthelpers.com](https://www.myparenthelpers.com)

---

## ✨ Why Choose MPH?

* **Customizable, multi-role Agents:** Parenting, teaching, or any expert support you need
* **Personalized and always in your words and style**
* **Local, private, and under your control**
* **Extensible for any new domain, shortcut, or method**
* **Perfect for families, educators, students, and professionals**

**MPH isn’t just AI-assisted—it’s AI-shaped by you.**

---

## 🤝 Questions or Suggestions?

We love feedback!
Visit [www.myparenthelpers.com](https://www.myparenthelpers.com) for support, feature requests, and contact info.

---

## 🛡️ License

MIT License

---

**MPH: Your own team of digital helpers, always ready to support your parenting, teaching, and expert needs—your way.**
