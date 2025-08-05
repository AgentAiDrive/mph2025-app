import streamlit as st
from openai import OpenAI
import json, os, time
from typing import List, Tuple, Callable
from typing import Dict, Optional
from pydantic import BaseModel, Field, ConfigDict

# ===================== MPH SPLASH SECTION (SHOWS ON APP LOAD) =====================

def mph_splash():
    st.markdown("")
    col = st.columns([1,2,1])[1]
    with col:
        start = st.button("🚀 Start", key="splash_start", use_container_width=True)
    st.markdown("<br>", unsafe_allow_html=True)
    return start
    st.markdown("""
    <style>
        .mph-splash { background: linear-gradient(135deg,#2fe273 0%,#09742a 100%)!important; border-radius:24px; padding:28px 20px 24px 20px; margin:22px auto 18px auto; box-shadow:0 4px 24px rgba(44,99,80,.10); max-width:450px; }
        .mph-splash h1 { text-align:center; font-size:2.2em; margin-bottom:0.35em; color:#18542e; font-weight:900;}
        .mph-splash h3 { text-align:center; font-size:1.2em; color:#23683c;}
        .mph-splash ul { padding-left:1.1em;}
        .mph-splash li { margin-bottom:4px; font-size:1.05em;}
        .mph-role {font-weight:700; font-size:1.09em;}
        .mph-getstarted {background:#fff; color:#15592c; padding:8px 14px; border-radius:16px; font-size:1.05em; margin:14px 0 8px 0;}
        .mph-btn {margin-top:1em; text-align:center;}
        .mph-shortcut { font-weight:600; color:#18542e; }
    </style>
    <div class="mph-splash">
        <h1>🌿 Welcome to My Parent Helpers (MPH)!</h1>
        <h3>Your digital team of AI-powered helpers—for parenting, teaching, and any expert support you need.</h3>
        <ul>
            <li><span class="mph-role">👨‍👩‍👧‍👦 Parent Agents:</span> Personalized, age-appropriate advice for your unique family.</li>
            <li><span class="mph-role">🧑‍🏫 Teacher Agents:</span> Lesson outlines, Q&A, and classroom support tailored for educators.</li>
            <li><span class="mph-role">🌟 Other (Expert) Agents:</span> Create custom assistants for any field—AV, science, health, and more.</li>
        </ul>
        <ul>
            <li><span class="mph-shortcut">💬 Shortcuts:</span> Instantly choose how you want answers: explain, teach, resolve, support, or just chat.</li>
            <li><span class="mph-shortcut">🧩 Fully Customizable:</span> Add your own sources, edit shortcuts, and create the helpers you need.</li>
            <li><span class="mph-shortcut">🔄 Save & Manage:</span> Save responses, edit profiles, and switch between Agents any time.</li>
            <li><span class="mph-shortcut">📱 Mobile-First:</span> Works on any device. No account needed. Your data stays private.</li>
        </ul>
        <div class="mph-getstarted">
            <b>Get Started:</b><br>
            1. Create an Agent (Parent, Teacher, or Expert)<br>
            2. Choose or add a source<br>
            3. Ask a question and pick a Shortcut<br>
            4. Save or revisit answers any time<br>
        </div>
        <div style="text-align:center; margin-top:10px; font-size:1.09em;">
            <b>MPH isn’t just AI advice—it’s a toolkit for shaping support, learning, and growth your way.</b>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("")
    col = st.columns([1,2,1])[1]
    with col:
        start = st.button("🚀 Start", key="splash_start", use_container_width=True)
    st.markdown("<br>", unsafe_allow_html=True)
    return start

# -------------------- SPLASH LOGIC - DO NOT SKIP THIS! --------------------
if "splash_done" not in st.session_state:
    st.session_state.splash_done = False

if not st.session_state.splash_done:
    st.set_page_config(page_title="My Parent Helpers", page_icon="🌿", layout="centered")
    if mph_splash():
        st.session_state.splash_done = True
        st.experimental_rerun()
    st.stop()
# ==========================================================================
# ---------------------------------------------------------------------------
# CONSTANTS & FILE PATHS (unchanged)
# ---------------------------------------------------------------------------
PROFILES_FILE   = "parent_helpers_profiles.json"
RESPONSES_FILE  = "parent_helpers_responses.json"
SOURCES_FILE    = "parent_helpers_sources.json"
MEMORY_FILE     = "parent_helpers_memory.json"
SHORTCUTS_FILE  = "parent_helpers_shortcuts.json"
DOMAIN_SHORTCUTS = {
    "Cardiologist": {
        " SUMMARY": "Concise findings summary.",
        " DIFFERENTIAL": "Differential diagnosis (list, brief).",
        " PLAN": "Recommended diagnostic/treatment plan.",
        " COUNSEL": "Key patient counseling points.",
        " RED FLAGS": "Red flag symptoms/warnings.",
    },
    "AI Prompt Engineer": {
        " OUTLINE": "Show step-by-step plan or pseudocode.",
        " EXPLAIN": "Explain with analogies/examples.",
        " DEBUG": "Suggest debugging/troubleshooting steps.",
        " FORMAT": "Format as markdown code block.",
        " PITFALLS": "List common mistakes to avoid.",
    },
    "AV Systems Design Engineer": {
        " SCOPE": "Summarize project/system scope.",
        " RISKS": "Identify design/deployment risks.",
        " DIAGRAM": "Describe/outline AV system diagram.",
        " SPECS": "Output key hardware/software specs.",
        " ROI": "Show business impact/ROI argument.",
    },
    "Geneticist": {
        " SUMMARY": "Summarize genetic findings.",
        " PATHWAYS": "Outline relevant pathways/genes.",
        " IMPLICATIONS": "Explain clinical/research impact.",
        " COUNSEL": "Suggest patient/family counseling.",
        " REFERENCES": "List key references/reviews.",
    },
    "Physicist": {
        " FORMULA": "State formula/principle used.",
        " STEPS": "Step-by-step calculation.",
        " EXPLAIN": "Explain in plain language.",
        " PITFALLS": "Common misconceptions.",
        " VISUAL": "Describe or suggest a diagram/graph.",
    }
}
DEFAULT_EXTRAS_MAP = {
    " DEFAULT":  "General purpose answer.",
    " CONNECT": " Help explain with examples.",
    " GROW":    " Offer advanced strategies.",
    " EXPLORE": " Age-appropriate Q&A.",
    " RESOLVE":" Step-by-step resolution.",
    "❤ SUPPORT":" Empathetic support."
}

# ---------------------------------------------------------------------------
# AGENT TYPES & SOURCES (corrected: domains preloaded dynamically)
# ---------------------------------------------------------------------------
AGENT_TYPES = ["Parent", "Teacher", "Other"]
PARENT_SOURCES = {
    "Book":   ["The Whole‑Brain Child", "Peaceful Parent, Happy Kids"],
    "Expert": ["Dr. Laura Markham", "Dr. Daniel Siegel"],
    "Style":  ["Authoritative", "Gentle Parenting"]
}
TEACHER_SOURCES = {
    "Book":   ["Teach Like a Champion", "Mindset"],
    "Expert": ["Carol Dweck", "Doug Lemov"],
    "Style":  ["Project-Based Learning", "SEL"]
}
# --- Automatically sync domain names with OTHER_SOURCES["Expert"]
other_expert_domains = list(DOMAIN_SHORTCUTS.keys())
custom_option = "Custom Expert (enter manually)"
OTHER_SOURCES = {
    "Book":   ["Custom Book (enter manually)"],
    "Expert": other_expert_domains + [custom_option],
    "Style":  ["Custom Style (enter manually)"]
}

# ---------------------------------------------------------------------------
# JSON LOAD / SAVE UTILITIES (unchanged)
# ---------------------------------------------------------------------------
def load_json(path: str):
    if not os.path.exists(path): return []
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        st.error(f"Error loading {path}: {e}")
        return []

def save_json(path: str, data):
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        st.error(f"Error writing {path}: {e}")

# ---------------------------------------------------------------------------
# OPENAI CLIENT
# ---------------------------------------------------------------------------
client = OpenAI(api_key=st.secrets.get("openai_key", "YOUR_OPENAI_API_KEY"))

# ---------------------------------------------------------------------------
# SESSION‑STATE INIT (unchanged)
# ---------------------------------------------------------------------------
st.session_state.setdefault("profiles",        load_json(PROFILES_FILE))
st.session_state.setdefault("saved_responses", load_json(RESPONSES_FILE))
st.session_state.setdefault("last_answer",     "")
st.session_state.setdefault("conversation",     load_json(MEMORY_FILE) or {})
st.session_state.setdefault("persistent_memory", False)
st.session_state.setdefault("temp_conversation", {})

if "sources" not in st.session_state:
    st.session_state["sources"] = {
        "Parent":  PARENT_SOURCES,
        "Teacher": TEACHER_SOURCES,
        "Other":   OTHER_SOURCES
    }
loaded = load_json(SHORTCUTS_FILE)
if isinstance(loaded, dict) and loaded:
    st.session_state.setdefault("extras_map", loaded)
else:
    st.session_state.setdefault("extras_map", DEFAULT_EXTRAS_MAP.copy())

# ---------------------------------------------------------------------------
#  GLOBAL CSS (unchanged)
# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------
#  GLOBAL CSS
# ---------------------------------------------------------------------------
st.markdown(
    """
<style>
/* ---- BODY & APP LAYOUT ---- */
body {
  background: linear-gradient(135deg,#2fe273 0%,#09742a 100%) !important;
  min-height: 100vh;
}
.stApp {
  background: linear-gradient(335deg,#2fe273 0%,#09742a 100%) !important;
  border-radius: 32px;
  max-width: 400px;
  min-height: 100vh;
  height: 100vh;
  margin: 32px auto;
  box-shadow: 0 8px 32px rgba(60,60,60,0.25), 0 1.5px 8px rgba(30,90,40,0.06);
  border: 3px solid #fff;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 10px;
  overflow-y: auto;
}

/* ---- LABELS ---- */
.biglabel, .biglabel-B, .biglabel-G, .biglabel-R {
  font-size: 1.1em;
  font-weight: 800;
  color: #fff;
  margin: 4px 0 10px;
  text-align: center;
  letter-spacing: 0.5px;
  padding: 6px 12px;
  border-radius: 12px;
}
.biglabel   { background: rgba(255,255,255,0.55); }
.biglabel-B { background: rgba(0,0,255,0.55); }
.biglabel-G { background: rgba(41,102,216,0.55); }
.biglabel-R { background: rgba(255,0,0,0.55); }

/* ---- AVATAR FRAME ---- */
.frame-avatar {
  font-size: 1.4em;
  margin: 6px 0;
  display: flex;
  justify-content: center;
  color: #fff;
}

/* ---- BUTTONS ---- */
.stButton>button, .st-btn-blue > button, .st-btn-green > button, .st-btn-red > button {
  font-weight: 700 !important;
  border-radius: 26px !important;
  padding: 0.4em !important;
  margin: 5% !important;
  box-shadow: 0 2px 12px rgba(44,99,180,0.12);
  transition: background 0.2s, filter 0.2s;
}
.stButton>button        { background: #1ec97b !important; color: #fff !important; font-size: 0.7em !important; width: 90% !important; border-radius: 20px !important;}
.st-btn-blue > button   { background: #2966d8 !important; color: #fff !important; font-size: 0.9em !important; width: 100% !important; border: none !important;}
.st-btn-green > button  { background: #1ec97b !important; color: #fff !important; font-size: 0.9em !important; width: 40% !important; border: none !important;}
.st-btn-red > button    { background: #d8293c !important; color: #fff !important; font-size: 0.9em !important; width: 100% !important; border: none !important; margin: 6px 0 !important; padding: 0.4em 0 !important;}

.stButton>button:hover,
.st-btn-blue>button:hover,
.st-btn-green>button:hover,
.st-btn-red>button:hover {
  filter: brightness(1.1);
}

/* ---- TOP NAVIGATION BAR ---- */
.top-nav-container {
  padding: 12px !important;
  border-radius: 32px !important;
  margin: -10px -10px 24px -10px !important;
  width: calc(100% + 20px) !important;
  position: sticky !important;
  top: 0 !important;
  z-index: 100 !important;
  background: rgba(0,0,0,0.1) !important;
}

/* ---- ANSWER BUBBLE ---- */
.answer-box {
  background: #23683c;
  border-radius: 12px;
  padding: 14px 18px;
  color: #fff;
  white-space: pre-wrap;
  margin-top: 8px;
}

/* ---- HOME CARDS & LISTS ---- */
.home-card {
  background: rgba(255,255,255,0.25) !important;
  border-radius: 20px !important;
  padding: 16px !important;
  margin: 6px;
  color: #fff;
  transition: transform 0.2s, box-shadow 0.2s !important;
}
.home-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 24px rgba(0,0,0,0.2) !important;
}
.home-card-title {
  font-size: 1.3em !important;
  color: #fff !important;
  letter-spacing: 1px !important;
  font-weight: 800;
  margin-bottom: 8px !important;
}
.home-small {
  font-size: 0.8em;
  font-weight: 800;
  color: #000;
  text-align: left;
  background: #fff;
  border: 3px solid #000;
  margin: 4px;
  padding: 4px;
}
.home-button {
  font-size: 0.8em;
  opacity: 0.85;
  background: #fff;
  border: 3px solid #000;
}

/* ---- DASHBOARD GRID ---- */
.stApp > div[data-testid="stVerticalBlock"] > div:nth-child(1) {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
  gap: 16px;
  width: 100%;
  padding: 0 8px;
}

/* ---- RESPONSIVE HEIGHT ---- */
@media (max-height:750px){
  .stApp { min-height: 640px; }
}

/* ---- BOTTOM NAV FIXED ---- */
@media (min-width: 400px) {
  .stApp > footer {
    position: fixed !important;
    bottom: 0 !important;
    width: 100% !important;
    background: rgba(0,0,0,0.1) !important;
  }
}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# PERSONA PROFILE MODEL (corrected for Pydantic v2)
# ---------------------------------------------------------------------------
class PersonaProfile(BaseModel):
    profile_name:        str
    parent_name:         str
    child_name:          str
    child_age:           int
    agent_type:          str
    source_type:         str
    source_name:         str
    persona_description: str

    rag_upload:        bool = False
    search_web:        bool = False
    search_documents:  bool = False
    vector_store_id:   Optional[str] = Field(default=None)
    documents:         List[str] = Field(default_factory=list)      # FIXED
    shortcuts:         Dict[str, str] = Field(default_factory=dict) # FIXED
    model_config = ConfigDict(arbitrary_types_allowed=True)

# ---------------------------------------------------------------------------
# Shortcuts domain fetch (ADDED HELPER)
# ---------------------------------------------------------------------------
def get_shortcuts_for_domain(domain):
    return DOMAIN_SHORTCUTS.get(domain, DEFAULT_EXTRAS_MAP.copy())

# ---------------------------------------------------------------------------
# FILE‑SEARCH TOOL for RAG (unchanged)
# ---------------------------------------------------------------------------
def get_openai_tools(profile: dict) -> list:
    tools = []
    if profile.get("search_documents") and profile.get("vector_store_id"):
        tools.append({
            "type": "file_search",
            "vector_store_ids": [profile["vector_store_id"]],
            "max_num_results": 5
        })
    if profile.get("search_web"):
        tools.append({"type": "web_search"})
    return tools

def add_tool_params(params: dict, profile: dict) -> dict:
    tools = get_openai_tools(profile)
    if tools:
        params["tools"] = tools
        if profile.get("vector_store_id"):
            params["include"] = ["output[*].file_search_call.search_results"]
        params["function_call"] = "auto"
    return params

# ---------------------------------------------------------------------------
# OPENAI API CALL WRAPPER (unchanged)
# ---------------------------------------------------------------------------
def openai_chat_or_responses(params: dict, fallback_prompt: str):
    """
    Use chat.completions.create when no tools are needed.
    Otherwise use responses.create (required for tools like file_search) with input=... and tools.
    """
    if hasattr(client, "chat") and hasattr(client.chat, "completions") and not params.get("tools"):
        return client.chat.completions.create(**params)
    else:
        return client.responses.create(
            model=params["model"],
            input=fallback_prompt,
            **({"tools": params["tools"]} if params.get("tools") else {})
        )

# ---------------------------------------------------------------------------
# MESSAGE BUILDERS (unchanged except tool_line changes)
# ---------------------------------------------------------------------------
def build_openai_agent_messages(profile, shortcut, shortcut_desc, query, history):
    tool_lines = []
    if profile.get("search_web"):
        tool_lines.append("You can search the web for up‑to‑date information.")
    if profile.get("vector_store_id"):
        tool_lines.append("You can use file_search to reference uploaded documents.")  # for auditing
    system = (
        f"You are a {profile['agent_type']} agent based on {profile['source_type']} “{profile['source_name']}”.\n"
        f"Persona: {profile['persona_description']}\n"
        f"Personalization: Parent {profile.get('parent_name','')}, Child {profile.get('child_name','')} (Age {profile.get('child_age','')}).\n"
        f"Shortcut “{shortcut}”: {shortcut_desc}\n"
        + ("\n".join(tool_lines) if tool_lines else "")
        + "\nAlways respond with a JSON object: {\"answer\": \"…\"}."
    )
    messages = [{"role": "system", "content": system}]
    if history:
        messages += [{"role": m["role"], "content": m["content"]} for m in history]
    messages.append({"role": "user", "content": query})
    return messages

def build_openai_params(profile, shortcut, shortcut_desc, query, history):
    params = {
        "model": "gpt-4o",
        "messages": build_openai_agent_messages(profile, shortcut, shortcut_desc, query, history)
    }
    return add_tool_params(params, profile)

# ---------------------------------------------------------------------------
#  HOME CARD RENDERER
# ---------------------------------------------------------------------------
def render_home_card(
    title: str,
    subtitle: str = None,
    buttons: List[Tuple[str, str, Callable, Callable]] = None,
    expander_label: str = None,
    expander_body: Callable = None,
) -> None:
    st.markdown(f'<div class="biglabel-B">{title}</div>', unsafe_allow_html=True)
    if subtitle:
        st.markdown(subtitle, unsafe_allow_html=True)
    if buttons:
        cols = st.columns(len(buttons), gap="small")
        for col, (label, key, cond, act) in zip(cols, buttons):
            with col:
                if st.button(label, key=key) and (cond is None or cond()):
                    act()
    if expander_label and expander_body:
        with st.expander(expander_label):
            expander_body()

def list_current_sources_and_shortcuts() -> None:
    """List all sources by Agent Type and then list all shortcut labels."""
    # 1) Sources by Agent Type
    for atype, cats in st.session_state["sources"].items():
        st.markdown(f"<p class='home-small'><strong>{atype}</strong></p>", unsafe_allow_html=True)
        for cat in ["Book", "Expert", "Style"]:
            items = cats.get(cat, [])
            joined = ", ".join(items) if items else "— none —"
            st.markdown(f"<p class='home-small'>&nbsp;&nbsp;{cat}: {joined}</p>", unsafe_allow_html=True)

    # 2) Shortcuts
    st.markdown("<hr style='border:1px solid rgba(255,255,255,0.3)'/>", unsafe_allow_html=True)
    st.markdown("<p class='home-small'><strong>Shortcuts</strong></p>", unsafe_allow_html=True)
    for key, desc in st.session_state["extras_map"].items():
        label = key.strip() or "(DEFAULT)"
        st.markdown(f"<p class='home-small'>&nbsp;&nbsp;{label}: {desc}</p>", unsafe_allow_html=True)
# ---------------------------------------------------------------------------
#  TOP NAVIGATION
# ---------------------------------------------------------------------------
def render_top_nav() -> None:
    """Render a sticky top navigation bar with just Home."""
    col1 = st.columns(1)[0]
    with col1:
        if st.button("🏠 Home", key="nav_home"):
            st.session_state.step = 0
            st.rerun()
# ---------------------------------------------------------------------------
#  BOTTOM NAVIGATION
# ---------------------------------------------------------------------------
def render_bottom_nav():
    st.markdown('<div class="biglabel-B"></div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        if st.button("💬 Chat", key="nav_chat_bottom"):
            st.session_state.step = 7 if st.session_state.profiles else 1
            st.rerun()
    with c2:
        if st.button("📂 Saved", key="nav_saved_bottom"):
            if st.session_state.saved_responses:
                st.session_state.step = 8
            else:
                st.warning("No saved responses yet.")
            st.rerun()
# ---------------------------------------------------------------------------
#  SHORTCUT EDITOR
# ---------------------------------------------------------------------------

def render_shortcut_editor():
    st.markdown("### Edit Shortcut Buttons (Label and Description)")

    extras_map = st.session_state.get("extras_map", {})
    shortcut_edits = []

    # Display current shortcuts with an immediate-delete button
    for i, (key, desc) in enumerate(list(extras_map.items())):
        cols = st.columns([2, 4, 1])
        with cols[0]:
            new_label = st.text_input(
                f"Label {i+1}", key=f"shortcut_label_{key}", value=key.strip()
            )
        with cols[1]:
            new_desc = st.text_input(
                f"Description {i+1}", key=f"shortcut_desc_{key}", value=desc
            )
        with cols[2]:
            # Immediate deletion on click
            if st.button("❌", key=f"delete_shortcut_{key}"):
                # Remove from session and persist
                st.session_state["extras_map"].pop(key, None)
                save_json(SHORTCUTS_FILE, st.session_state["extras_map"])
                st.success(f"Deleted shortcut '{key.strip()}'.")
                st.rerun()
        shortcut_edits.append((key, new_label.strip(), new_desc))

    st.markdown("---")
    st.markdown("**Add a new shortcut**")
    with st.form("add_shortcut_form", clear_on_submit=True):
        new_label = st.text_input("New shortcut label", key="add_shortcut_label")
        new_desc  = st.text_input("New shortcut description", key="add_shortcut_desc")
        add_it    = st.form_submit_button("Add Shortcut")
        if add_it:
            if not new_label:
                st.warning("Label is required.")
            elif new_label in extras_map:
                st.warning("That label already exists.")
            else:
                st.session_state["extras_map"][new_label] = new_desc
                save_json(SHORTCUTS_FILE, st.session_state["extras_map"])
                st.success(f"Added shortcut '{new_label}'.")
                st.rerun()

    # Renaming logic (if a label or description was edited)
    if st.button("Save Shortcut Edits", key="save_shortcuts"):
        updated_map = {}
        for old_key, new_key, new_desc in shortcut_edits:
            # skip if the user cleared out the label text
            if not new_key:
                continue
            # avoid collisions
            if new_key in updated_map and new_key != old_key:
                st.warning(f"Duplicate shortcut label: '{new_key}'")
                continue
            updated_map[new_key] = new_desc
        st.session_state["extras_map"] = updated_map
        save_json(SHORTCUTS_FILE, updated_map)
        st.success("Shortcut labels and descriptions updated!")
        st.rerun()

# ---------------------------------------------------------------------------
#  STEP 0: DASHBOARD
# ---------------------------------------------------------------------------

def render_step0():
    r1c1, r1c2 = st.columns(2)
    r2c1, r2c2 = st.columns(2)

    with r1c1:
        render_home_card(
            title="AGENTS",
            buttons=[
                ("EDIT AGENTS","home_profiles", lambda: st.session_state.profiles,
                    lambda: (st.session_state.update(step=9), st.rerun())),
                ("CREATE AGENT","home_create", None,
                    lambda: (st.session_state.update(step=1), st.rerun())),
            ],
            expander_label="Saved Agents 🖫",
            expander_body=lambda: [
                st.markdown(f"<p class='home-small'>{p['profile_name']}</p>", unsafe_allow_html=True)
                for p in st.session_state.profiles
            ] or st.markdown("<p class='home-small'>No profiles yet.</p>", unsafe_allow_html=True)
        )

    with r1c2:
        render_home_card(
            title="CHATS",
            buttons=[
                ("SAVED CHATS","home_saved", lambda: st.session_state.saved_responses,
                    lambda: (st.session_state.update(step=8), st.rerun())),
                ("START CHAT","home_chat", None,
                    lambda: (
                        st.session_state.update(step=7 if st.session_state.profiles else 1),
                        st.warning("No profiles – create one first.") if not st.session_state.profiles else None,
                        st.rerun()
                    )),
            ],
            expander_label="Chat History 🖫",
            expander_body=lambda: [
                st.markdown(f"<p class='home-small'>{i+1}. {r['profile']} – {r['shortcut']}</p>",
                            unsafe_allow_html=True)
                for i,r in enumerate(st.session_state.saved_responses)
            ] or st.markdown("<p class='home-small'>No saved chats.</p>", unsafe_allow_html=True)
        )

    with r2c1:
        render_home_card(
            title="SOURCES",
            buttons=[("EDIT SOURCES","home_sources",None,
                      lambda:(st.session_state.update(step=10), st.rerun()))],
            expander_label="Sources & Shortcuts",
            expander_body=list_current_sources_and_shortcuts
        )

    with r2c2:
        render_home_card(
            title="DATA",
            buttons=[("CLEAR DATA","home_clear",None,
                      lambda: (
                          st.session_state.update(profiles=[], saved_responses=[]),
                          save_json(PROFILES_FILE, []),
                          save_json(RESPONSES_FILE, []),
                          st.success("All data cleared.")
                      ))],
            expander_label="Types & Counts",
            expander_body=lambda: [
                st.markdown(f"<p class='home-small'>Profiles: {len(st.session_state.profiles)}</p>",
                            unsafe_allow_html=True),
                st.markdown(f"<p class='home-small'>Chats: {len(st.session_state.saved_responses)}</p>",
                            unsafe_allow_html=True)
            ]
        )

# ---------------------------------------------------------------------------
#  STEP 1: SELECT AGENT TYPE
# ---------------------------------------------------------------------------
def render_step1():
    st.markdown('<div class="biglabel-G">Step 1: Select Agent Type - Choose what kind of agent you want to create (e.g., Parent, Teacher, or Other).</div>', unsafe_allow_html=True)
    cols = st.columns(3)
    for label, key, atype in [("👪 Parent","btn_parent","Parent"),
                              ("🧑‍🏫 Teacher","btn_teacher","Teacher"),
                              ("✨ Other","btn_other","Other")]:
        with cols.pop(0):
            if st.button(label, key=key):
                st.session_state.agent_type = atype
                st.session_state.step        = 2
                st.rerun()
    render_top_nav()

# ---------------------------------------------------------------------------
#  STEP 2: SELECT SOURCE TYPE
# ---------------------------------------------------------------------------
def render_step2():
    st.markdown('<div class="biglabel-G">Step 2: Select Source Type - Pick the type of source you’d like your {st.session_state.agent_type} to be based on (Book, Style, or Expert).</div>', unsafe_allow_html=True)
    cols = st.columns(3)
    for label, key, stype in [("📚 Book","btn_book","Book"),
                              ("🧠 Expert","btn_expert","Expert"),
                              ("🎨 Style","btn_style","Style")]:
        with cols.pop(0):
            if st.button(label, key=key):
                st.session_state.source_type = stype
                st.session_state.step        = 3
                st.rerun() 
    render_top_nav()

# ---------------------------------------------------------------------------
#  STEP 3: CHOOSE SPECIFIC SOURCE
# ---------------------------------------------------------------------------
def render_step3(): 
    st.markdown(f'<div class="biglabel-G">Step 3: Select Source Name - Select a specific {st.session_state.source_type} name for your agent’s persona.</div>', unsafe_allow_html=True)
    agent_type = st.session_state.agent_type
    opts = st.session_state["sources"][agent_type].get(st.session_state.source_type, [])
    if "Other..." not in opts: opts.append("Other...")
    choice = st.selectbox("Select or enter your own:", opts)
    custom = st.text_input("Enter custom name") if choice == "Other..." else ""
    c1, c2 = st.columns(2)
    with c1:
        if st.button("← Back", key="btn_back3"):
            st.session_state.step = 2; st.rerun()
    with c2:
        if st.button("CREATE PERSONA →", key="btn_next3"):
            src = custom if choice=="Other..." else choice
            if not src:
                st.warning("Please provide a name.")
            else:
                st.session_state.source_name = src
                st.session_state.pop("persona_description", None)
                st.session_state.step = 4; st.rerun()
 
    render_bottom_nav();
    render_top_nav()
# ---------------------------------------------------------------------------
# RENDER FUNCTION (Step 4)
# ---------------------------------------------------------------------------

def render_step4():
    st.markdown('<div class="biglabel-B">GENERATING YOUR AGENT PERSONA</div>', unsafe_allow_html=True)
    placeholder = st.empty()
    for msg in ["Assimilating Knowledge…","Synthesizing Information…","Assessing Results…","Generating Persona…"]:
        placeholder.info(msg); time.sleep(0.5)

    if "persona_description" not in st.session_state:
        with st.spinner("Thinking…"):
            try:
                # Build system and user messages with all context
                profile_stub = {
                    "agent_type": st.session_state.agent_type,
                    "parent_name": "",
                    "child_name": "",
                    "child_age": "",
                    "source_type": st.session_state.source_type,
                    "source_name": st.session_state.source_name,
                    "persona_description": "",
                    "rag_upload": False,
                    "search_web": False,
                    "search_documents": False,
                }
                shortcut_label = " DEFAULT"
                shortcut_desc = "General purpose persona synthesis."
                query = (
                    f"Generate a concise persona description (domain, philosophy, core principles, and practices) "
                    f"of a {st.session_state.agent_type} agent based on the {st.session_state.source_type} \"{st.session_state.source_name}\". "
                    "In under 200 words. Return a JSON object: {\"persona_description\": \"...\"}"
                )
                params = build_openai_params(
                    profile_stub, shortcut_label, shortcut_desc, query, history=None
                )
                # Conditional: use chat.completions.create if available, else responses.create
                openai_method = None
                if hasattr(client, "chat") and hasattr(client.chat, "completions"):
                    openai_method = client.chat.completions.create
                elif hasattr(client, "responses") and hasattr(client.responses, "create"):
                    openai_method = client.responses.create
                else:
                    raise Exception("OpenAI client does not support chat.completions or responses.create")

                out = openai_method(**params)
                raw = (
                    out.choices[0].message.content
                    if hasattr(out, "choices") and out.choices and hasattr(out.choices[0], "message")
                    else getattr(out, "output_text", None)
                )
                if not raw:
                    st.error("No persona description returned from OpenAI.")
                    return
                try:
                    parsed = json.loads(raw)
                    st.session_state.persona_description = parsed.get("persona_description", raw)
                except Exception:
                    st.session_state.persona_description = raw
            except Exception as e:
                st.error(f"OpenAI API error: {e}")

    placeholder.empty()
    if desc := st.session_state.get("persona_description"):
        st.markdown(f"<div class='answer-box'>{desc}</div>", unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        if st.button("Retry →", key="btn_retry4"):
            st.session_state.pop("persona_description", None); st.rerun()
    with c2:
        if st.button("Save Persona", key="btn_save4"):
            st.session_state.step = 5; st.rerun()

    render_top_nav()

# ---------------------------------------------------------------------------
# RENDER FUNCTION (Step 5)
# ---------------------------------------------------------------------------
def render_step5():
    st.markdown('<div class="biglabel-G">Great! Now personalize your agent and add tools if desired</div>', unsafe_allow_html=True)
    agent_type   = st.session_state.agent_type
    source_type  = st.session_state.source_type
    source_name  = st.session_state.source_name

    # --- Per-profile shortcut logic ---
    # On first load, pre-fill from domain or default if new profile
    if "profile_shortcuts" not in st.session_state:
        if agent_type == "Other" and source_type == "Expert" and source_name in DOMAIN_SHORTCUTS:
            st.session_state["profile_shortcuts"] = get_shortcuts_for_domain(source_name)
        else:
            st.session_state["profile_shortcuts"] = DEFAULT_EXTRAS_MAP.copy()
    shortcut_map = st.session_state["profile_shortcuts"]

    # Editable list
    st.markdown("**Customize This Agent’s Shortcuts**")
    shortcut_items = list(shortcut_map.items())
    to_delete = set()
    new_shortcuts = {}

    for i, (label, desc) in enumerate(shortcut_items):
        cols = st.columns([2, 4, 1])
        with cols[0]:
            new_label = st.text_input(f"Label {i+1}", value=label, key=f"shortcut_label_{i}")
        with cols[1]:
            new_desc = st.text_input(f"Description {i+1}", value=desc, key=f"shortcut_desc_{i}")
        with cols[2]:
            if st.button("❌", key=f"delete_shortcut_{i}"):
                to_delete.add(label)
        # Only add non-deleted
        if new_label.strip() and label not in to_delete:
            new_shortcuts[new_label.strip()] = new_desc.strip()

    # Add new shortcut
    st.markdown("---")
    st.markdown("**Add New Shortcut**")
    new_slabel = st.text_input("New Shortcut Label", key="add_shortcut_label_pf")
    new_sdesc = st.text_input("New Shortcut Description", key="add_shortcut_desc_pf")
    if st.button("Add Shortcut to Agent Profile"):
        if new_slabel and new_slabel not in new_shortcuts:
            new_shortcuts[new_slabel] = new_sdesc
            st.session_state["profile_shortcuts"] = new_shortcuts
            st.success("Shortcut added!")
            st.rerun()
        else:
            st.warning("Shortcut label required and must be unique.")

    # Save in session for profile creation
    st.session_state["profile_shortcuts"] = new_shortcuts

    # --- Profile form ---
    with st.form("profile"):
        if agent_type == "Parent":
            p_name = st.text_input("Parent first name")
            c_age  = st.number_input("Child age", 1, 21)
            c_name = st.text_input("Child first name")
        elif agent_type == "Teacher":
            p_name = st.text_input("Teacher name")
            c_age  = st.number_input("Class grade", 1, 12)
            c_name = ""
        else:
            p_name = st.text_input("Name")
            c_age, c_name = 0, ""
        prof_nm    = st.text_input("Profile name")
        rag_upload = st.checkbox("Enable document uploads (RAG)")
        search_documents = st.checkbox("Enable document search")
        search_web = st.checkbox("Enable web search")
        uploads    = st.file_uploader("Upload documents", accept_multiple_files=True) if rag_upload else []
        saved      = st.form_submit_button("SAVE")

    if saved:
        missing = []
        if not prof_nm: missing.append("profile name")
        if not p_name: missing.append("name")
        if agent_type == "Parent" and not c_name: missing.append("child name")
        if missing:
            st.warning(f"Please fill: {', '.join(missing)}")
        else:
            docs_list = []
            for f in uploads:
                try: docs_list.append(f.name)
                except: pass

            profile = PersonaProfile(
                profile_name        = prof_nm,
                parent_name         = p_name,
                child_name          = c_name,
                child_age           = int(c_age),
                agent_type          = agent_type,
                source_type         = st.session_state.source_type,
                source_name         = st.session_state.source_name,
                persona_description = st.session_state.persona_description,
                rag_upload          = rag_upload,
                search_web          = search_web,
                search_documents    = search_documents,
                documents           = docs_list,
                shortcuts           = st.session_state["profile_shortcuts"]
            )

            if rag_upload and uploads:
                vs_name = f"{prof_nm}-{int(time.time())}"
                try:
                    vs = client.vector_stores.create(name=vs_name)
                    streams = [open(f.name, "rb") for f in uploads]
                    batch = client.vector_stores.file_batches.upload_and_poll(
                        vector_store_id=vs.id,
                        files=streams
                    )
                    profile.vector_store_id = vs.id
                except Exception as e:
                    st.warning(f"Vector store upload failed: {e}")
            st.session_state.profiles.append(profile.dict())
            save_json(PROFILES_FILE, st.session_state.profiles)
            st.success("Profile saved!")
            st.session_state.pop("profile_shortcuts", None)  # Reset for next profile
            st.session_state.step = 6; st.rerun()

    if st.button("← Back", key="btn_back5"):
        st.session_state.pop("profile_shortcuts", None)  # Clean up
        st.session_state.step = 4; st.rerun()

    render_top_nav()

# ---------------------------------------------------------------------------
#  STEP 6: PROFILE CREATED CONFIRMATION
# ---------------------------------------------------------------------------
def render_step6():
    st.markdown('<div class="biglabel-G">AGENT PROFILE CREATED!</div>', unsafe_allow_html=True)
    p = st.session_state.profiles[-1]
    st.markdown(f"""
    <div class="home-card">
      <p><strong>Profile:</strong> {p['profile_name']}</p>
      <p><strong>Parent:</strong> {p['parent_name']}</p>
      <p><strong>Child:</strong> {p['child_name']} (Age {p['child_age']})</p>
      <p><strong>Type:</strong> {p['agent_type']}</p>
      <p><strong>Source:</strong> {p['source_type']} – {p['source_name']}</p>
      <p><strong>Description:</strong></p>
      <div class="answer-box">{p['persona_description']}</div>
    </div>
    """, unsafe_allow_html=True)
    render_top_nav()

# ---------------------------------------------------------------------------
#  STEP 7: CHAT
# ---------------------------------------------------------------------------

def render_step7():
    render_top_nav()

    # 1. Agent selection
    st.markdown('<div class="biglabel-G">1. SELECT AN AGENT</div>', unsafe_allow_html=True)
    names = [p["profile_name"] for p in st.session_state.profiles]
    idx = st.selectbox("Agent Profiles:", range(len(names)),
                       format_func=lambda i: names[i],
                       key="chat_profile")
    sel = st.session_state.profiles[idx]

    # 2. Shortcut selection header
    st.markdown('<div class="biglabel-G">2. SELECT A SHORTCUT</div>', unsafe_allow_html=True)
    shortcuts_map = sel.get("shortcuts", DEFAULT_EXTRAS_MAP)
    if (
        "shortcut" not in st.session_state
        or st.session_state["shortcut"] not in shortcuts_map
    ):
        st.session_state["shortcut"] = next(iter(shortcuts_map), " DEFAULT")

    shortcuts = list(shortcuts_map.keys())

    # Display currently selected shortcut
    st.markdown(
        f"<div class='home-small'><strong>SELECTED SHORTCUT:</strong> "
        f"<span style='color:#2966d8;font-weight:bold'>"
        f"{st.session_state['shortcut'].strip()}"
        f"</span></div>",
        unsafe_allow_html=True
    )

    # Lay out shortcut buttons in rows of three
    from math import ceil
    rows = ceil(len(shortcuts) / 3)
    for row in range(rows):
        row_items = shortcuts[row*3:(row+1)*3]
        cols = st.columns(3)
        for sc, col in zip(row_items, cols):
            with col:
                if st.button(sc.strip(), key=f"sc_{sc}",
                             help=shortcuts_map[sc]):
                    st.session_state["shortcut"] = sc

    # ── Per-chat tool toggles ───────────────────────────────────────────────
    use_web  = st.checkbox(
        "ENABLE WEB SEARCH for this chat",
        value=sel.get("search_web", False),
        key="chat_use_web"
    )
    use_docs = st.checkbox(
        "ENABLE DOCUMENT SEARCH for this chat",
        value=sel.get("search_documents", False),
        key="chat_use_docs"
    )
    # ────────────────────────────────────────────────────────────────────────

    # 3. Persistent memory toggle
    use_mem = st.checkbox("ENABLE PERSISTENT MEMORY - CHAT HISTORY", key="persistent_memory")
    if use_mem:
        history = st.session_state.conversation.get(sel["profile_name"], [])
        with st.expander("View chat history"):
            if not history:
                st.info("No previous messages.")
            for msg in history:
                who  = "You" if msg["role"] == "user" else "Agent"
                style = "background:#144d2f;" if msg["role"] == "user" else ""
                st.markdown(
                    f"<div class='answer-box' style='{style}'>"
                    f"<strong>{who}:</strong> {msg['content']}</div>",
                    unsafe_allow_html=True
                )

    # 4. User query input
    st.markdown('<div class="biglabel-G">3. ASK & SEND</div>', unsafe_allow_html=True)
    query = st.text_area("Type here", key="chat_query")

    # 5. Show last answer if present
    if st.session_state.last_answer:
        st.markdown(
            "<div class='answer-box'><strong>Answer:</strong><br>"
            f"{st.session_state.last_answer}</div>",
            unsafe_allow_html=True
        )

    # 6. Save + Send buttons
    c1, c2 = st.columns(2)
    with c1:
        if st.button("SAVE RESPONSE 🖫", key="save_response"):
            record = {
                "profile":          sel["profile_name"],
                "shortcut":         st.session_state["shortcut"],
                "question":         query,
                "answer":           st.session_state.last_answer,
                "persistent_memory": use_mem
            }
            if use_mem:
                record["conversation"] = st.session_state.conversation.get(sel["profile_name"], []).copy()
            if record not in st.session_state.saved_responses:
                st.session_state.saved_responses.append(record)
                save_json(RESPONSES_FILE, st.session_state.saved_responses)
            st.success("Response saved!")

    with c2:
        if st.button("SEND →", key="send_btn"):
            history = (st.session_state.conversation.get(sel["profile_name"], [])
                       if use_mem else None)

            # make a one-off copy of the profile to override its tool flags
            oneoff = sel.copy()
            oneoff["search_web"]       = use_web
            oneoff["search_documents"] = use_docs

            params = build_openai_params(
                oneoff,
                st.session_state["shortcut"],
                shortcuts_map[st.session_state["shortcut"]],
                query,
                history
            )

            try:
                out = openai_chat_or_responses(params, fallback_prompt=query)
                raw = ""
                if hasattr(out, "choices") and out.choices:
                    raw = out.choices[0].message.content
                else:
                    raw = getattr(out, "output_text", "") or ""
                parsed = json.loads(raw) if raw.strip().startswith("{") else {}
                answer = parsed.get("answer", raw)
                st.session_state.last_answer = answer

                # Update memory
                if use_mem:
                    new_hist = (history or []) + [
                        {"role": "user", "content": query},
                        {"role": "assistant", "content": answer}
                    ]
                    st.session_state.conversation[sel["profile_name"]] = new_hist
                    save_json(MEMORY_FILE, st.session_state.conversation)
                    st.session_state.temp_conversation[sel["profile_name"]] = new_hist.copy()
                else:
                    tmp = st.session_state.temp_conversation.get(sel["profile_name"], [])
                    tmp += [
                        {"role": "user", "content": query},
                        {"role": "assistant", "content": answer}
                    ]
                    st.session_state.temp_conversation[sel["profile_name"]] = tmp

                st.rerun()

            except Exception as e:
                st.error(f"OpenAI API error (chat): {e}")

    render_bottom_nav()
# ---------------------------------------------------------------------------
#  STEP 8: VIEW SAVED CHATS
# ---------------------------------------------------------------------------
def render_step8():
    render_top_nav()
    st.markdown('<div class="biglabel-B">SAVED CHATS</div>', unsafe_allow_html=True)
    if not st.session_state.saved_responses:
        st.info("No saved responses."); st.session_state.step=0; st.rerun()
    titles = [f"{i+1}. {r['profile']} – {r['shortcut']}" for i,r in enumerate(st.session_state.saved_responses)]
    sel_idx = st.selectbox("Saved Chats:", range(len(titles)), format_func=lambda i: titles[i], key="saved_select")
    item = st.session_state.saved_responses[sel_idx]

    st.markdown(f"<p style='color:#fff;'><strong>Profile:</strong> {item['profile']}</p>", unsafe_allow_html=True)
    st.markdown(f"<p style='color:#fff;'><strong>Shortcut:</strong> {item['shortcut']}</p>", unsafe_allow_html=True)

    # Lookup and show shortcut description for this profile
    sel_profile = next((p for p in st.session_state.profiles if p['profile_name'] == item['profile']), None)
    sc_desc = ""
    if sel_profile and "shortcuts" in sel_profile:
        sc_desc = sel_profile["shortcuts"].get(item["shortcut"], "")
    if sc_desc:
        st.markdown(f"<p style='color:#fff;'><strong>Shortcut Description:</strong> {sc_desc}</p>", unsafe_allow_html=True)

    st.markdown(f"<p style='color:#fff;'><strong>Persistent memory:</strong> {'Yes' if item.get('persistent_memory') else 'No'}</p>", unsafe_allow_html=True)
    st.markdown(f"<p style='color:#fff;'><strong>Question:</strong></p><blockquote style='color:#fff;border-left:4px solid #27e67a;padding-left:8px;'>{item['question']}</blockquote>", unsafe_allow_html=True)
    st.markdown(f"<p style='color:#fff;'><strong>Answer:</strong></p><div class='answer-box'>{item['answer']}</div>", unsafe_allow_html=True)

    if convo := item.get("conversation"):
        with st.expander("Show conversation history"):
            for msg in convo:
                who = "You" if msg["role"]=="user" else "Agent"
                st.markdown(f"<p style='color:#fff;'><strong>{who}:</strong> {msg['content']}</p>", unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        if st.button("DELETE", key="btn_delete_saved"):
            st.session_state.saved_responses.pop(sel_idx)
            save_json(RESPONSES_FILE, st.session_state.saved_responses)
            st.rerun()
    with c2:
        if st.button("CLOSE", key="btn_close_saved"):
            st.session_state.step = 0; st.rerun()
# ---------------------------------------------------------------------------
#  STEP 9: EDIT PROFILES + SHORTCUTS
# ---------------------------------------------------------------------------
def render_step9():
    render_top_nav()
    st.markdown('<div class="biglabel-B">AGENT PROFILES</div>', unsafe_allow_html=True)

    # No profiles? Go home
    if not st.session_state.profiles:
        st.info("No profiles stored."); st.session_state.step=0; st.rerun()
    titles = [f"{i+1}. {p['profile_name']}" for i,p in enumerate(st.session_state.profiles)]
    idx = st.selectbox("Select a profile:", range(len(titles)), format_func=lambda i: titles[i], key="profile_select")
    prof = st.session_state.profiles[idx]

    # --- Begin Profile Edit Form ---
    with st.form("edit_profile"):
        p_name = st.text_input("Parent/Agent Name", value=prof.get("parent_name", ""))
        c_age  = st.number_input("Child Age (or Class Grade)", 1, 99, value=max(1, prof.get("child_age", 1)))
        c_name = st.text_input("Child Name", value=prof.get("child_name", ""))
        prof_nm = st.text_input("Profile Name", value=prof.get("profile_name", ""))
        a_type = st.selectbox("Agent Type", AGENT_TYPES, index=AGENT_TYPES.index(prof.get("agent_type", "Parent")))
        desc = st.text_area("Persona Description", value=prof.get("persona_description", ""), height=150)
        rag = st.checkbox("Enable document uploads (RAG)", value=prof.get("rag_upload", False))
        docs = st.checkbox("Enable document search", value=prof.get("search_documents", False))
        web = st.checkbox("Enable web search", value=prof.get("search_web", False))
        uploads = st.file_uploader("Upload documents", accept_multiple_files=True) if rag else []

        # --- Shortcuts Editor for this profile ---
        st.markdown("#### Shortcuts for this Agent")
        shortcuts = dict(prof.get("shortcuts", {}))
        shortcut_edits = []
        delete_keys = set()

        for i, (label, description) in enumerate(list(shortcuts.items())):
            cols = st.columns([2, 4, 1])
            with cols[0]:
                new_label = st.text_input(f"Shortcut Label {i+1}", value=label, key=f"profile_sc_label_{i}")
            with cols[1]:
                new_desc = st.text_input(f"Description {i+1}", value=description, key=f"profile_sc_desc_{i}")
            with cols[2]:
                to_delete = st.checkbox("Delete?", key=f"profile_sc_delete_{i}")
                if to_delete:
                    delete_keys.add(label)
            shortcut_edits.append((label, new_label.strip(), new_desc))

        st.markdown("---")
        st.markdown("**Add a new shortcut for this agent**")
        new_sc_label = st.text_input("New Shortcut Label", key="profile_new_sc_label")
        new_sc_desc  = st.text_input("New Shortcut Description", key="profile_new_sc_desc")
        add_sc = st.form_submit_button("Add Shortcut")
        if add_sc and new_sc_label:
            if new_sc_label in shortcuts:
                st.warning("That shortcut already exists for this agent.")
            else:
                shortcuts[new_sc_label] = new_sc_desc
                st.success(f"Added shortcut '{new_sc_label}'.")

        # --- Save Profile Edits ---
        saved = st.form_submit_button("SAVE CHANGES")

    # --- Apply Edits After Form Submission ---
    if saved:
        # Remove checked shortcuts
        for k in delete_keys:
            shortcuts.pop(k, None)
        # Apply edits (label/desc), renaming as needed
        new_shortcuts = {}
        for old_label, new_label, new_desc in shortcut_edits:
            if not new_label: continue  # skip empty
            if new_label in new_shortcuts and new_label != old_label:
                st.warning(f"Duplicate shortcut label: '{new_label}'")
                continue
            new_shortcuts[new_label] = new_desc
        shortcuts = {**shortcuts, **new_shortcuts}

        prof.update(
            parent_name=p_name,
            child_age=int(c_age),
            child_name=c_name,
            profile_name=prof_nm,
            persona_description=desc,
            agent_type=a_type,
            rag_upload=rag,
            search_documents=docs,
            search_web=web,
            documents=prof.get("documents", []),
            shortcuts=shortcuts,   # updated per-profile shortcuts
        )
        # If doc search disabled, forget old vector store
        if not docs:
            prof["vector_store_id"] = None
        st.session_state.profiles[idx] = prof
        save_json(PROFILES_FILE, st.session_state.profiles)
        st.success("Profile updated!")

    # --- Danger Zone ---
    c1, c2 = st.columns(2)
    with c1:
        if st.button("DELETE PROFILE", key="btn_delete_profile"):
            st.session_state.profiles.pop(idx)
            save_json(PROFILES_FILE, st.session_state.profiles)
            st.rerun()
    with c2:
        if st.button("CLOSE", key="btn_close_profile"):
            st.session_state.step = 0; st.rerun()
    render_bottom_nav()

# ---------------------------------------------------------------------------
#  STEP 10: EDIT SOURCES AND SHORTCUTS
# ---------------------------------------------------------------------------
def render_step10():
    render_top_nav()
    st.markdown('<div class="biglabel-G">EDIT SOURCE LISTS</div>', unsafe_allow_html=True)

    def save_sources(sources):
        try:
            with open(SOURCES_FILE, "w", encoding="utf-8") as f:
                json.dump(sources, f, indent=2)
        except Exception as e:
            st.error(f"Error saving sources: {e}")
    def load_sources():
        return load_json(SOURCES_FILE)

    if not st.session_state['sources']:
        st.session_state['sources'] = load_sources() or {
            "Parent":PARENT_SOURCES, "Teacher":TEACHER_SOURCES, "Other":OTHER_SOURCES
        }
    srcs = st.session_state['sources']

    agent_type  = st.selectbox("Agent Type", AGENT_TYPES, key="edit_agent_type")
    source_type = st.selectbox("Source Type", ["Book","Expert","Style"], key="edit_source_type")

    items    = srcs[agent_type].get(source_type, [])
    to_remove= st.multiselect("Select to remove", items, key="remove_sources")
    new_item = st.text_input(f"Add new {source_type}:", key="add_source")
    st.markdown('<div class="biglabel-R"></div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("Remove Selected"):
            srcs[agent_type][source_type] = [i for i in items if i not in to_remove]
            st.session_state['sources'] = srcs
            save_sources(srcs); st.success("Removed!"); st.rerun()
    with c2:
        if st.button("Add"):
            if new_item and new_item not in items:
                srcs[agent_type][source_type].append(new_item)
                st.session_state['sources'] = srcs
                save_sources(srcs); st.success(f"Added '{new_item}'!"); st.rerun()
            elif new_item:
                st.warning("Already in list.")
    with c3:
        if st.button("Back to Home"):
            st.session_state.step = 0; st.rerun()

    st.write(srcs[agent_type][source_type])
    render_bottom_nav()

    # --- DYNAMIC SHORTCUT EDITOR ---
    render_shortcut_editor()

# ---------------------------------------------------------------------------
#  ENTRY POINT
# ---------------------------------------------------------------------------
def main():
    step = st.session_state.get("step", 0)
    {
        0: render_step0,  1: render_step1,  2: render_step2,
        3: render_step3,  4: render_step4,  5: render_step5,
        6: render_step6,  7: render_step7,  8: render_step8,
        9: render_step9, 10: render_step10
    }.get(step, render_step0)()

if __name__ == "__main__":
    main()
