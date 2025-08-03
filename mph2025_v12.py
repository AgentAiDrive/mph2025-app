import streamlit as st
from openai import OpenAI
import json
import os
import time
from typing import List, Tuple, Callable, Dict
from pydantic import BaseModel, Field

# ---------------------------------------------------------------------------
#  CONSTANTS & FILE PATHS
# ---------------------------------------------------------------------------
PROFILES_FILE   = "parent_helpers_profiles.json"
RESPONSES_FILE  = "parent_helpers_responses.json"
SOURCES_FILE    = "parent_helpers_sources.json"
MEMORY_FILE     = "parent_helpers_memory.json"

# ---------------------------------------------------------------------------
#  JSON LOAD / SAVE UTILITIES
# ---------------------------------------------------------------------------
def load_json(path: str):
    if not os.path.exists(path):
        return []
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
#  OPENAI CLIENT
# ---------------------------------------------------------------------------
client = OpenAI(api_key=st.secrets.get("openai_key", "YOUR_OPENAI_API_KEY"))

# ---------------------------------------------------------------------------
#  AGENT TYPE DEFAULT SOURCES
# ---------------------------------------------------------------------------
AGENT_TYPES = ["Parent", "Teacher", "Other"]

PARENT_SOURCES = {
    "Book":   ["The Whole-Brain Child", "Peaceful Parent, Happy Kids"],
    "Expert": ["Dr. Laura Markham", "Dr. Daniel Siegel"],
    "Style":  ["Authoritative", "Gentle Parenting"]
}
TEACHER_SOURCES = {
    "Book":   ["Teach Like a Champion", "Mindset"],
    "Expert": ["Carol Dweck", "Doug Lemov"],
    "Style":  ["Project-Based Learning", "SEL"]
}
OTHER_SOURCES = {
    "Book":   ["Custom Book (enter manually)"],
    "Expert": ["Custom Expert (enter manually)"],
    "Style":  ["Custom Style (enter manually)"]
}

# ---------------------------------------------------------------------------
#  SESSION STATE INIT
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

# ---------------------------------------------------------------------------
#  GLOBAL CSS
# ---------------------------------------------------------------------------
st.markdown(
    """
<style>
body {
  background: linear-gradient(135deg,#2fe273 0%,#09742a 100%)!important;
  min-height: 100vh;
}
.stApp {
  background: linear-gradient(335deg,#2fe273 0%,#09742a 100%)!important;
  border-radius: 32px;
  max-width: 400px;
  min-height: 100vh;
  height: 100vh;
  overflow-y: auto;
  margin: 32px auto;
  box-shadow: 0 8px 32px rgba(60,60,60,.25), 0 1.5px 8px rgba(30,90,40,.06);
  border: 3px solid #ffffff;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 10px 10px 10px;
}
/* --- COLOR LABELS --- */
.biglabel-B {
  font-size: 1.1em;
  font-weight: 800;
  color: #ffffff;
  margin: 4px 0 10px;
  text-align: center;
  letter-spacing: 0.5px;
  background: rgba(0, 0, 255, 0.55);
  padding: 6px 12px;
  border-radius: 12px;
}
.biglabel-R {
  font-size: 1.1em;
  font-weight: 800;
  color: #ffffff;
  margin: 4px 0 10px;
  text-align: center;
  letter-spacing: 0.5px;
  background: rgba(255, 0, 0, 0.55);
  padding: 6px 12px;
  border-radius: 12px;
}
.biglabel-G {
  font-size: 1.1em;
  font-weight: 800;
  color: #ffffff;
  margin: 4px 0 10px;
  text-align: center;
  letter-spacing: 0.5px;
  background: rgba(0, 255, 0, 0.55);
  padding: 6px 12px;
  border-radius: 12px;
}
.biglabel {
  font-size: 1.1em;
  font-weight: 800;
  color: #ffffff;
  margin: 4px 0 10px;
  text-align: center;
  letter-spacing: 0.5px;
  background: rgba(255, 255, 255, 0.55);
  padding: 6px 12px;
  border-radius: 12px;
}
.frame-avatar {
  font-size: 1.4em;
  margin: 6px 0 6px;
  display: flex;
  justify-content: center;
  color: #ffffff;
}
/* --- COLOR BUTTONS --- */
.stButton>button {
  border-radius: 20px !important;
  font-weight: 700 !important;
  font-size: .7em !important;
  padding: .4em !important;
  background: #1ec97b !important;
  color: #fff !important;
  margin: 5% 5% !important;
  width: 90% !important;
}
.st-btn-blue > button {
  border-radius: 26px !important;
  font-weight: 700 !important;
  font-size: .9em !important;
  padding: .4em !important;
  background: #2966d8 !important;
  color: #fff !important;
  margin: 5% !important;
  width: 100% !important;
  border: none !important;
  box-shadow: 0 2px 12px rgba(44,99,180,0.12);
  transition: background 0.2s;
}
.st-btn-green > button {
  border-radius: 26px !important;
  font-weight: 700 !important;
  font-size: .9em !important;
  padding: .4em !important;
  background: #1ec97b !important;
  color: #fff !important;
  margin: 5% !important;
  width: 40% !important;
  border: none !important;
  box-shadow: 0 2px 12px rgba(44,180,99,0.12);
  transition: background 0.2s;
}
.st-btn-red > button {
  border-radius: 26px !important;
  font-weight: 700 !important;
  font-size: .9em !important;
  padding: .4em 0 !important;
  background: #d8293c !important;
  color: #fff !important;
  margin: 6px 0 !important;
  width: 100% !important;
  border: none !important;
  box-shadow: 0 2px 12px rgba(180,44,99,0.12);
  transition: background 0.2s;
}
/* --- TOP NAV BAR--- */
.top-nav-container {
  padding: 12px 12px 12px 12px !important;
  border-radius: 32px !important;
  margin: -10px -10px 24px -10px !important;
  width: calc(100% + 20px) !important;
}
/* --- Answer bubble --- */
.answer-box {
  background: #23683c;
  border-radius: 12px;
  padding: 14px 18px;
  color: #fff;
  white-space: pre-wrap;
  margin-top: 8px;
}
/* --- Home cards --- */
.home-card {
  background: rgba(255,255,255,0.15);
  border-radius: 16px;
  padding: 12px;
  margin: 6px;
  color: #fff;
}
.home-card-title {
  font-weight: 800;
  margin-bottom: 6px;
}
.home-small {
  font-size: 0.8em;
  opacity: 0.85;
  background: white;
  border: 3px solid #000000;
  margin: 4px 4px;
  padding: 4px;
}
.home-button {
  font-size: 0.8em;
  opacity: 0.85;
  background: white;
  border: 3px solid #000000;
}
@media (max-height:750px){
  .stApp{min-height:640px;}
}
</style>
    """,
    unsafe_allow_html=True
)

# ---------------------------------------------------------------------------
#  TOP NAVIGATION
# ---------------------------------------------------------------------------

def render_top_nav() -> None:
    """Render a sticky top navigation bar with just Home."""
    st.markdown('<div class="top-nav-container">', unsafe_allow_html=True)
    col1 = st.columns(1)[0]
    with col1:
        if st.button(" Home", key="nav_home"):
            st.session_state.step = 0
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
# ---------------------------------------------------------------------------
#  BOTTOM NAVIGATION
# ---------------------------------------------------------------------------

def render_bottom_nav():
    c1, c2 = st.columns(2)
    st.markdown('<div class="biglabel-B">', unsafe_allow_html=True)
    with c1:
        if st.button(" Chat", key="nav_chat_bottom"):
            st.session_state.step = 7 if st.session_state.profiles else 1
            st.rerun()
    with c2:
        if st.button(" Saved", key="nav_saved_bottom"):
            if st.session_state.saved_responses:
                st.session_state.step = 8
            else:
                st.warning("No saved responses yet.")
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
# ---------------------------------------------------------------------------
#  DATA MODEL & TOOL HELPERS
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

    rag_upload:        bool      = False
    search_documents:  bool      = False
    search_web:        bool      = False
    documents:         List[str] = Field(default_factory=list)

def get_enabled_tools(profile: Dict) -> List[Dict]:
    tools = []
    if profile.get("search_documents"):
        tools.append({"type": "file_search"})
    if profile.get("search_web"):
        tools.append({"type": "web_search"})
    return tools

def add_tool_params(params: Dict, profile: Dict) -> Dict:
    tools = get_enabled_tools(profile)
    if tools:
        params["tools"] = tools
    return params

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
            expander_label="Saved Agents",
            expander_body=lambda: [
                st.markdown(f"<p class='home-small'>{p['profile_name']}</p>", unsafe_allow_html=True)
                for p in st.session_state.profiles
            ] or st.markdown("<p class='home-small'>No profiles yet.</p>", unsafe_allow_html=True)
        )

    with r1c2:
        titles = [f"{i+1}. {r['profile']} – {r['shortcut']}" for i,r in enumerate(st.session_state.saved_responses)]
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
            expander_label="Chat History",
            expander_body=lambda: [
                st.markdown(f"<p class='home-small'>{t}</p>", unsafe_allow_html=True)
                for t in titles
            ] or st.markdown("<p class='home-small'>No saved chats.</p>", unsafe_allow_html=True)
        )

    with r2c1:
        render_home_card(
            title="SOURCES",
            buttons=[("EDIT SOURCES","home_sources",None,
                      lambda:(st.session_state.update(step=10), st.rerun()))],
            expander_label="Types & Counts",
            expander_body=lambda: [
                st.markdown(
                    f"<p class='home-small'>{atype}: "
                    f"{sum(len(st.session_state['sources'][atype][cat]) for cat in ['Book','Expert','Style'])}</p>",
                    unsafe_allow_html=True)
                for atype in AGENT_TYPES
            ]
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
    st.markdown('<div class="biglabel-G">Select An Agent Type</div>', unsafe_allow_html=True)
    cols = st.columns(3)
    for label, key, atype in [("Parent","btn_parent","Parent"),
                              ("Teacher","btn_teacher","Teacher"),
                              ("Other","btn_other","Other")]:
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
    render_top_nav()
    st.markdown('<div class="biglabel-G">Select Agent Source Type</div>', unsafe_allow_html=True)
    cols = st.columns(3)
    for label, key, stype in [("📚 Book","btn_book","Book"),
                              ("🧠 Expert","btn_expert","Expert"),
                              ("🎨 Style","btn_style","Style")]:
        with cols.pop(0):
            if st.button(label, key=key):
                st.session_state.source_type = stype
                st.session_state.step        = 3
                st.rerun() 
    render_bottom_nav()

# ---------------------------------------------------------------------------
#  STEP 3: CHOOSE SPECIFIC SOURCE
# ---------------------------------------------------------------------------
def render_step3():
    render_top_nav(); 
    st.markdown(f'<div class="biglabel-G">Choose a {st.session_state.source_type}</div>', unsafe_allow_html=True)
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
        if st.button("Next →", key="btn_next3"):
            src = custom if choice=="Other..." else choice
            if not src:
                st.warning("Please provide a name.")
            else:
                st.session_state.source_name = src
                st.session_state.pop("persona_description", None)
                st.session_state.step = 4; st.rerun()
 
    render_bottom_nav()

# ---------------------------------------------------------------------------
#  STEP 4: GENERATE PERSONA DESCRIPTION
# ---------------------------------------------------------------------------
def render_step4():
    st.markdown('<div class="biglabel-B">GENERATING YOUR AGENT PERSONA</div>', unsafe_allow_html=True)
    placeholder = st.empty()
    for msg in ["Assimilating Knowledge…","Synthesizing Information…","Assessing Results…","Generating Persona…"]:
        placeholder.info(msg); time.sleep(0.5)

    if "persona_description" not in st.session_state:
        with st.spinner("Thinking…"):
            try:
                prompt = (
                    f"You are creating a persona description of the domain, philosophy, core principles, and "
                    f"practices of the {st.session_state.source_type} '{st.session_state.source_name}'. "
                    "In under 200 words, return a JSON object with key 'persona_description'."
                )
                params = {
                    "model": "gpt-4o",
                    "input": prompt,
                }
                # call Responses API (no response_format)
                out = client.responses.create(**add_tool_params(params, {}))
                raw = out.output_text
                try:
                    parsed = json.loads(raw)
                    st.session_state.persona_description = parsed.get("persona_description", raw)
                except Exception:
                    st.session_state.persona_description = raw
            except Exception as e:
                st.error(f"OpenAI API error: {e}")

    placeholder.empty()
    if desc := st.session_state.get("persona_description"):
        st.info(desc)

    c1, c2 = st.columns(2)
    with c1:
        if st.button("Retry", key="btn_retry4"):
            st.session_state.pop("persona_description", None); st.rerun()
    with c2:
        if st.button("Save Persona", key="btn_save4"):
            st.session_state.step = 5; st.rerun()

    render_top_nav(); render_bottom_nav()

# ---------------------------------------------------------------------------
#  STEP 5: PERSONALIZE & SAVE PROFILE
# ---------------------------------------------------------------------------
def render_step5():
    st.markdown('<div class="biglabel-G">PERSONALIZE AGENT</div>', unsafe_allow_html=True)
    agent_type = st.session_state.agent_type

    with st.form("profile"):
        # Name & age fields
        if agent_type == "Parent":
            p_name = st.text_input("Parent first name")
            c_age   = st.number_input("Child age", 1, 21)
            c_name = st.text_input("Child first name")
        elif agent_type == "Teacher":
            p_name = st.text_input("Teacher name")
            c_age   = st.number_input("Class grade", 1, 12)
            c_name  = ""
        else:
            p_name = st.text_input("Name")
            c_age, c_name = 0, ""

        prof_nm     = st.text_input("Profile name")
        rag_upload  = st.checkbox("Enable document uploads (RAG)")
        search_docs = st.checkbox("Enable document search")
        search_web  = st.checkbox("Enable web search")
        uploads     = st.file_uploader("Upload documents", accept_multiple_files=True) if rag_upload else []
        saved       = st.form_submit_button("SAVE")

    if saved:
        missing = []
        if not p_name: missing.append("name")
        if agent_type=="Parent" and not c_name: missing.append("child name")
        if not prof_nm: missing.append("profile name")
        if missing:
            st.warning(f"Please fill: {', '.join(missing)}")
        else:
            docs_list = []
            for f in uploads:
                try: docs_list.append(f.read().decode("utf-8"))
                except: pass

            profile = PersonaProfile(
                profile_name        = prof_nm,
                parent_name         = p_name,
                child_name          = c_name,
                child_age           = int(c_age),
                source_type         = st.session_state.source_type,
                source_name         = st.session_state.source_name,
                persona_description = st.session_state.persona_description,
                agent_type          = agent_type,
                rag_upload          = rag_upload,
                search_documents    = search_docs,
                search_web          = search_web,
                documents           = docs_list,
            )
            st.session_state.profiles.append(profile.dict())
            save_json(PROFILES_FILE, st.session_state.profiles)
            st.success("Profile saved!")
            st.session_state.step = 6; st.rerun()

    if st.button("← Back", key="btn_back5"):
        st.session_state.step = 4; st.rerun()

    render_top_nav()

# ---------------------------------------------------------------------------
#  STEP 6: PROFILE CREATED CONFIRMATION
# ---------------------------------------------------------------------------
def render_step6():
    st.markdown('<div class="biglabel">AGENT PROFILE CREATED!</div>', unsafe_allow_html=True)
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
#  STEP 7: CHAT INTERFACE
# ---------------------------------------------------------------------------
def render_step7():
    render_top_nav()

    st.markdown('<div class="biglabel-G">1. SELECT AN AGENT</div>', unsafe_allow_html=True)
    names = [p["profile_name"] for p in st.session_state.profiles]
    idx   = st.selectbox("Agent Profiles:", range(len(names)), format_func=lambda i: names[i], key="chat_profile")
    sel   = st.session_state.profiles[idx]

    # RESPONSE TYPE SHORTCUTS
    st.session_state.setdefault("shortcut", " DEFAULT")
    shortcuts = [" DEFAULT"," CONNECT"," GROW"," EXPLORE"," RESOLVE","❤ SUPPORT"]
    cols = st.columns(len(shortcuts))
    for sc, col in zip(shortcuts, cols):
        with col:
            if st.button(sc.strip(), key=f"sc_{sc}"):
                st.session_state.shortcut = sc

    # PERSISTENT MEMORY TOGGLE
    st.checkbox("Use persistent memory", key="persistent_memory")

    # DISPLAY HISTORY
    conv = (st.session_state.conversation.get(sel["profile_name"], [])
            if st.session_state.persistent_memory
            else st.session_state.temp_conversation.get(sel["profile_name"], []))
    for msg in conv:
        role = "You" if msg["role"]=="user" else "Agent"
        style = "background:#144d2f;" if msg["role"]=="user" else ""
        st.markdown(f"<div class='answer-box' style='{style}'><strong>{role}:</strong> {msg['content']}</div>", unsafe_allow_html=True)

    # USER QUERY
    st.markdown('<div class="home-small">3. WHAT DO YOU WANT TO ASK?</div>', unsafe_allow_html=True)
    query = st.text_area("Type here", key="chat_query")

    c1, c2 = st.columns(2)
    with c1:
        if st.button("Save Response", key="save_response"):
            record = {
                "profile": sel["profile_name"],
                "shortcut": st.session_state.shortcut,
                "question": query,
                "answer":   st.session_state.last_answer,
                "persistent_memory": st.session_state.persistent_memory
            }
            if record["persistent_memory"]:
                record["conversation"] = st.session_state.conversation.get(sel["profile_name"], []).copy()
            if record not in st.session_state.saved_responses:
                st.session_state.saved_responses.append(record)
                save_json(RESPONSES_FILE, st.session_state.saved_responses)
            st.success("Response saved!")

    with c2:
        if st.button("SEND", key="send_btn"):
            base = (
                f"Adopt the persona: {sel['persona_description']}. "
                f"You are conversing with Parent {sel['parent_name']} (Child: {sel['child_name']}, Age {sel['child_age']})."
            )
            extras = {
                " CONNECT":" Help explain with examples.",
                " GROW":" Offer advanced strategies.",
                " EXPLORE":" Age-appropriate Q&A.",
                " RESOLVE":" Step-by-step resolution.",
                "❤ SUPPORT":" Empathetic support."
            }[st.session_state.shortcut]

            prompt = base + extras + "\n" + query + "\nReturn a JSON object with key 'answer'."

            try:
                if st.session_state.persistent_memory:
                    hist = st.session_state.conversation.get(sel["profile_name"], [])
                    system = base + extras + "\nReturn a JSON object with key 'answer'."
                    messages = [{"role":"system","content":system}] + hist + [{"role":"user","content":query}]
                    params = {"model":"gpt-4o","messages":messages}
                else:
                    params = {"model":"gpt-4o","input":prompt}

                out = client.responses.create(**add_tool_params(params, sel))
                raw = out.output_text
                try:
                    parsed = json.loads(raw)
                    answer = parsed.get("answer", raw)
                except Exception:
                    answer = raw

                st.session_state.last_answer = answer

                # update history
                if st.session_state.persistent_memory:
                    new_hist = hist + [{"role":"user","content":query},{"role":"assistant","content":answer}]
                    st.session_state.conversation[sel["profile_name"]] = new_hist
                    save_json(MEMORY_FILE, st.session_state.conversation)
                    st.session_state.temp_conversation[sel["profile_name"]] = new_hist.copy()
                else:
                    tmp = st.session_state.temp_conversation.get(sel["profile_name"], [])
                    tmp += [{"role":"user","content":query},{"role":"assistant","content":answer}]
                    st.session_state.temp_conversation[sel["profile_name"]] = tmp

                st.rerun()
            except Exception as e:
                st.error(f"OpenAI API error: {e}")

    render_bottom_nav()

# ---------------------------------------------------------------------------
#  STEP 8: VIEW SAVED CHATS
# ---------------------------------------------------------------------------
def render_step8():
    render_top_nav()
    st.markdown('<div class="biglabel-B">SELECT A SAVED CHAT</div>', unsafe_allow_html=True)
    if not st.session_state.saved_responses:
        st.info("No saved responses."); st.session_state.step=0; st.rerun()
    titles = [f"{i+1}. {r['profile']} – {r['shortcut']}" for i,r in enumerate(st.session_state.saved_responses)]
    sel_idx = st.selectbox("Saved Chats:", range(len(titles)), format_func=lambda i: titles[i], key="saved_select")
    item = st.session_state.saved_responses[sel_idx]

    st.markdown(f"<p style='color:#fff;'><strong>Profile:</strong> {item['profile']}</p>", unsafe_allow_html=True)
    st.markdown(f"<p style='color:#fff;'><strong>Shortcut:</strong> {item['shortcut']}</p>", unsafe_allow_html=True)
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
        if st.button("Delete", key="btn_delete_saved"):
            st.session_state.saved_responses.pop(sel_idx)
            save_json(RESPONSES_FILE, st.session_state.saved_responses)
            st.rerun()
    with c2:
        if st.button("Close", key="btn_close_saved"):
            st.session_state.step = 0; st.rerun()

# ---------------------------------------------------------------------------
#  STEP 9: EDIT PROFILES
# ---------------------------------------------------------------------------
def render_step9():
    render_top_nav()
    st.markdown('<div class="biglabel-B">AGENT PROFILES</div>', unsafe_allow_html=True)
    if not st.session_state.profiles:
        st.info("No profiles stored."); st.session_state.step=0; st.rerun()
    titles = [f"{i+1}. {p['profile_name']}" for i,p in enumerate(st.session_state.profiles)]
    idx = st.selectbox("Select a profile:", range(len(titles)), format_func=lambda i: titles[i], key="profile_select")
    prof = st.session_state.profiles[idx]

    with st.form("edit_profile"):
        p_name = st.text_input("Parent first name", value=prof.get("parent_name",""))
        c_age  = st.number_input("Child age", 1, 21, value=max(1,prof.get("child_age",1)))
        c_name = st.text_input("Child first name", value=prof.get("child_name",""))
        prof_nm= st.text_input("Profile name", value=prof.get("profile_name",""))
        a_type = st.selectbox("Agent type", AGENT_TYPES, index=AGENT_TYPES.index(prof.get("agent_type","Parent")))
        desc   = st.text_area("Persona description", value=prof.get("persona_description",""), height=150)
        rag    = st.checkbox("Enable document uploads (RAG)", value=prof.get("rag_upload",False))
        docs   = st.checkbox("Enable document search",    value=prof.get("search_documents",False))
        web    = st.checkbox("Enable web search",         value=prof.get("search_web",False))
        uploads= st.file_uploader("Upload documents", accept_multiple_files=True) if rag else []
        saved  = st.form_submit_button("SAVE CHANGES")

    if saved:
        docs_list = prof.get("documents",[])
        for f in uploads:
            try: docs_list.append(f.read().decode("utf-8"))
            except: pass
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
            documents=docs_list,
        )
        st.session_state.profiles[idx] = prof
        save_json(PROFILES_FILE, st.session_state.profiles)
        st.success("Profile updated!")

    c1, c2 = st.columns(2)
    with c1:
        if st.button("Delete Profile", key="btn_delete_profile"):
            st.session_state.profiles.pop(idx)
            save_json(PROFILES_FILE, st.session_state.profiles)
            st.rerun()
    with c2:
        if st.button("Close", key="btn_close_profile"):
            st.session_state.step = 0; st.rerun()

# ---------------------------------------------------------------------------
#  STEP 10: EDIT SOURCES
# ---------------------------------------------------------------------------
def render_step10():
    render_top_nav()
    st.markdown('<div class="biglabel-R">EDIT SOURCE LISTS</div>', unsafe_allow_html=True)

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
