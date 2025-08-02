import streamlit as st
import openai
import json
import os
import time
from pydantic import BaseModel

# ---------------------------------------------------------------------------
#  GLOBAL STYLE SHEET
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
  border-radius: 26px!important;
  font-weight: 700!important;
  font-size: .7em!important;
  padding: .4em 0!important;
  background: #2966d8!important;
  color: #fff!important;
  margin: 6px 0!important;
  width: 100%!important;
}
.st-btn-blue > button {
  border-radius: 26px !important;
  font-weight: 700 !important;
  font-size: .9em !important;
  padding: .4em 0 !important;
  background: #2966d8 !important;
  color: #fff !important;
  margin: 6px 0 !important;
  width: 100% !important;
  border: none !important;
  box-shadow: 0 2px 12px rgba(44,99,180,0.12);
  transition: background 0.2s;
}
.st-btn-green > button {
  border-radius: 26px !important;
  font-weight: 700 !important;
  font-size: .9em !important;
  padding: .4em 0 !important;
  background: #1ec97b !important;
  color: #fff !important;
  margin: 6px 0 !important;
  width: 100% !important;
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
    """Render the sticky top navigation bar with Home, Chat and Saved buttons."""
    st.markdown('<div class="top-nav-container">', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('<div class="st-btn-green">', unsafe_allow_html=True)
        if st.button(" Home", key="nav_home"):
            st.session_state.step = 0
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="st-btn-blue">', unsafe_allow_html=True)
        if st.button(" Chat", key="nav_chat"):
            st.session_state.step = 7 if st.session_state.profiles else 1
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="st-btn-red">', unsafe_allow_html=True)
        if st.button(" Saved", key="nav_saved"):
            if st.session_state.saved_responses:
                st.session_state.step = 8
            else:
                st.warning("No saved responses yet.")
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------------------------------
#  HELPER FUNCTIONS & CONSTANTS
# ---------------------------------------------------------------------------

PROFILES_FILE = "parent_helpers_profiles.json"
RESPONSES_FILE = "parent_helpers_responses.json"
SOURCES_FILE = "parent_helpers_sources.json"
# Path used to persist conversation history for the optional memory feature.
MEMORY_FILE = "parent_helpers_memory.json"

def load_json(path: str):
    """Load JSON data from a file or return an empty list if file does not exist."""
    if not os.path.exists(path):
        return []
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        st.error(f"Error loading {path}: {e}")
        return []

def save_json(path: str, data):
    """Save data to a JSON file, catching and displaying any errors."""
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        st.error(f"Error writing {path}: {e}")

# Initialize persistent session state keys
for key, default in {
    "profiles":        load_json(PROFILES_FILE),
    "saved_responses": load_json(RESPONSES_FILE),
    "last_answer":     "",
}.items():
    st.session_state.setdefault(key, default)

# Initialize conversation history and memory toggle.  The conversation
# dict maps profile names to a list of message dicts ({"role", "content"}).
st.session_state.setdefault("conversation", (load_json(MEMORY_FILE) or {}))
st.session_state.setdefault("persistent_memory", False)
# Temporary conversation history used for stateless sessions.
st.session_state.setdefault("temp_conversation", {})

# Configure OpenAI key
openai.api_key = st.secrets.get("openai_key", "YOUR_OPENAI_API_KEY")

# Agent types and default sources
AGENT_TYPES = ["Parent", "Teacher", "Other"]

PARENT_SOURCES = {
    "Book": ["The Whole-Brain Child", "Peaceful Parent, Happy Kids"],
    "Expert": ["Dr. Laura Markham", "Dr. Daniel Siegel"],
    "Style": ["Authoritative", "Gentle Parenting"]
}

TEACHER_SOURCES = {
    "Book": ["Teach Like a Champion", "Mindset"],
    "Expert": ["Carol Dweck", "Doug Lemov"],
    "Style": ["Project-Based Learning", "SEL"]
}

OTHER_SOURCES = {
    "Book": ["Custom Book (enter manually)"],
    "Expert": ["Custom Expert (enter manually)"],
    "Style": ["Custom Style (enter manually)"]
}

def get_source_options(agent_type: str):
    """Return the source dictionary for a given agent type from session state."""
    return st.session_state.get("sources", {}).get(agent_type, {})

# Initialize sources in session state if not already present
if 'sources' not in st.session_state:
    st.session_state['sources'] = {
        "Parent": {
            "Book": ["The Whole-Brain Child", "Peaceful Parent, Happy Kids"],
            "Expert": ["Dr. Laura Markham", "Dr. Daniel Siegel"],
            "Style": ["Authoritative", "Gentle Parenting"]
        },
        "Teacher": {
            "Book": ["Teach Like a Champion", "Mindset"],
            "Expert": ["Carol Dweck", "Doug Lemov"],
            "Style": ["Project-Based Learning", "SEL"]
        },
        "Other": {
            "Book": ["Custom Book (enter manually)"],
            "Expert": ["Custom Expert (enter manually)"],
            "Style": ["Custom Style (enter manually)"]
        }
    }

class PersonaProfile(BaseModel):
    """Data model for saving persona profiles."""
    profile_name: str
    parent_name: str
    child_name: str
    child_age: int
    agent_type: str
    source_type: str
    source_name: str
    persona_description: str

SHORTCUTS = [" DEFAULT"," CONNECT"," GROW"," EXPLORE"," RESOLVE","❤ SUPPORT"]
# Map shortcut labels to display emojis.  Providing actual emoji makes the
# buttons easier to identify in the UI.
EMOJIS = {
    " DEFAULT": "",       # default produces plain text answers
    " CONNECT": "🤝",       # handshake for connect
    " GROW": "📈",          # chart for grow
    " EXPLORE": "🔍",        # magnifying glass for explore
    " RESOLVE": "🛠️",        # tools emoji for resolve
    "❤ SUPPORT": "❤"         # heart for support
}
TOOLTIPS = {
    " DEFAULT":"No formatting",
    " CONNECT":"Help explain complex ideas with examples",
    " GROW":"Strategies to improve parenting",
    " EXPLORE":"Age-appropriate Q&A",
    " RESOLVE":"Step-by-step advice",
    "❤ SUPPORT":"Empathetic guidance"
}

# ---------------------------------------------------------------------------
#  HOME PAGE CARD RENDERING
# ---------------------------------------------------------------------------
def render_home_card(title, subtitle=None, buttons=None, expander_label=None, expander_body=None) -> None:
    st.markdown(f'<div class="biglabel-G">{title}</div>', unsafe_allow_html=True)
    if subtitle:
        st.markdown(subtitle, unsafe_allow_html=True)

    # Expander always rendered (before buttons)
    if expander_label and expander_body:
        with st.expander(expander_label):
            if callable(expander_body):
                expander_body()
            else:
                st.write(expander_body)

    # Buttons after expander
    if buttons:
        for label, key, condition, action in buttons:
            if st.button(label, key=key):
                if condition is None or condition():
                    action()

# ---------------------------------------------------------------------------
#  STEP FUNCTIONS
# ---------------------------------------------------------------------------

def render_step0():
    """Render the home page with cards for agents, chats, sources, and data."""
    row1_col1, row1_col2 = st.columns(2)
    row2_col1, row2_col2 = st.columns(2)

    # AGENTS card (expander before buttons)
    with row1_col1:
        render_home_card(
            "AGENTS",
            buttons=[
                ("SAVED AGENTS", "home_profiles", lambda: st.session_state.profiles,
                 lambda: (st.session_state.__setitem__('step', 9), st.rerun())),
                ("NEW AGENT",    "home_create",   None,
                 lambda: (st.session_state.__setitem__('step', 1),  st.rerun())),
            ],   
        expander_body=lambda: (
            [st.markdown(f"<p class='home-small'>{p['profile_name']}</p>", unsafe_allow_html=True)
             for p in st.session_state.profiles]
            if st.session_state.profiles 
            else st.markdown('<p class="home-small">No profiles yet.</p>', unsafe_allow_html=True)
        )

    # CHATS card (expander lists saved chat titles)
    with row1_col2:
        saved_titles = [
            f"{i+1}. {r['profile']} – {r['shortcut']}"
            for i, r in enumerate(st.session_state.saved_responses)
        ]
        render_home_card(
            "CHATS",
            buttons=[
                ("SAVED CHATS", "home_saved", lambda: st.session_state.saved_responses,
                 lambda: (st.session_state.__setitem__('step', 8), st.rerun())),
                ("NEW CHAT",    "home_chat",   None,
                 lambda: (
                     st.session_state.__setitem__('step', 7 if st.session_state.profiles else 1),
                     st.warning('No profiles – create one first.') if not st.session_state.profiles else None,
                     st.rerun()
                 ))
            ],
            expander_label="SAVED CHATS",
            expander_body=lambda: (
                [st.markdown(f"<p class='home-small'>{t}</p>", unsafe_allow_html=True)
                 for t in saved_titles]
                if saved_titles
                else st.markdown('<p class="home-small">No saved chats.</p>', unsafe_allow_html=True)
            )
        )
    # Card: SOURCES
    with row2_col1:
        render_home_card(
            "SOURCES",
            buttons=[
                ("EDIT SOURCES", "edit_sources", None,
                 lambda: (st.session_state.__setitem__('step', 10), 
                          st.rerun()))
            ], 
            expander_label="Counts",
            expander_body=lambda: [
                st.markdown(
                    f"<p class='home-small'>{atype}: "
                    f"{sum(len(st.session_state['sources'].get(atype, {}).get(t, [])) for t in ['Book','Expert','Style'])}</p>",
                    unsafe_allow_html=True
                ) for atype in AGENT_TYPES
            ]
        )
    # Card: DATA
    with row2_col2:
        render_home_card(
            "DATA",
            buttons=[
                ("CLEAR DATA", "clear_data", None, lambda: (
                    st.session_state.__setitem__('profiles', []),
                    st.session_state.__setitem__('saved_responses', []),
                    save_json(PROFILES_FILE, []),
                    save_json(RESPONSES_FILE, []),
                    st.success("All data cleared.")
                ))
            ],
            expander_label="Counts",
            expander_body=lambda: (
                st.markdown(f"<p class='home-small'>Profiles: "
                            f"{len(st.session_state.profiles)}</p>", 
                            unsafe_allow_html=True),
                st.markdown(f"<p class='home-small'>Chats: "
                            f"{len(st.session_state.saved_responses)}</p>", 
                            unsafe_allow_html=True)
            )
        )
        
def render_step1():
    """Render the page to select the agent type (Parent, Teacher, Other)."""
   
    st.markdown(
        """
        <div style="text-align:center;">
          <img src="https://img1.wsimg.com/isteam/ip/e13cd0a5-b867-446e-
af2a-268488bd6f38/myparenthelpers%20logo%20round.png" width="80" />
        </div>
        """,
        unsafe_allow_html=True,)
    st.markdown('<div class="biglabel-G">Select An Agent Type</div>', 
                unsafe_allow_html=True)
    st.markdown('<div class="frame-avatar"></div>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("  Parent", key="btn_agent_parent"):
            st.session_state.agent_type = "Parent"
            st.session_state.step = 2
            st.rerun()
    with col2:
        if st.button("‍  Teacher", key="btn_agent_teacher"):
            st.session_state.agent_type = "Teacher"
            st.session_state.step = 2
            st.rerun()
    with col3:
        if st.button("✨  Other", key="btn_agent_other"):
            st.session_state.agent_type = "Other"
            st.session_state.step = 2
            st.rerun()
    render_top_nav()
def render_step2():
    """Render the page to select the source type (Book, Expert, Style)."""
    st.markdown(
        """
        <div style="text-align:center;">
          <img src="https://img1.wsimg.com/isteam/ip/e13cd0a5-b867-446e-
af2a-268488bd6f38/myparenthelpers%20logo%20round.png" width="80" />
        </div>
        """,
        unsafe_allow_html=True,)
    st.markdown('<div class="biglabel-G">Select Agent Source Type</div>', 
                unsafe_allow_html=True)
    st.markdown('<div class="frame-avatar"></div>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("  Book", key="btn_book"):
            st.session_state.source_type = "Book"
            st.session_state.step = 3
            st.rerun()
    with col2:
        if st.button("‍  Expert", key="btn_expert"):
            st.session_state.source_type = "Expert"
            st.session_state.step = 3
            st.rerun()
    with col3:
        if st.button("  Style", key="btn_style"):
            st.session_state.source_type = "Style"
            st.session_state.step = 3
            st.rerun()
    render_top_nav()
def render_step3():
    """Render the page to choose a specific book/expert/style or enter a custom one."""
    st.markdown(
        """
        <div style="text-align:center;">
          <img src="https://img1.wsimg.com/isteam/ip/e13cd0a5-b867-446e-
af2a-268488bd6f38/myparenthelpers%20logo%20round.png" width="80" />
        </div>
        """,
        unsafe_allow_html=True,
    )
    # Determine current agent type and source options
    agent_type = st.session_state.get("agent_type", "Parent")
    sources = get_source_options(agent_type)
    source_type = st.session_state.get("source_type", "Book")
    options = sources.get(source_type, ["Other..."])
    # Always append "Other..." for custom entry
    if "Other..." not in options:
        options = options + ["Other..."]
    # Select display emoji for Expert vs Style vs Book
    emoji = "" if source_type == "Book" else "‍" if source_type == "Expert" else ""
    st.markdown(f'<div class="biglabel-G">Choose a {source_type}</div>', 
                unsafe_allow_html=True)
    st.markdown(f'<div class="frame-avatar">{emoji}</div>', 
                unsafe_allow_html=True)
    choice = st.selectbox("Select or enter your own:", options)
    custom = st.text_input("Enter custom name") if choice == "Other..." else ""
    col1, col2 = st.columns(2)
    with col1:
        if st.button("BACK", key="btn_back_step2"):
            st.session_state.step = 2
            st.rerun()
    with col2:
        if st.button("CREATE", key="btn_create_step2"):
            src_name = custom if choice == "Other..." else choice
            if not src_name:
                st.warning("Please provide a name.")
            else:
                st.session_state.source_name = src_name
                # clear any old persona so step 4 always regenerates
                st.session_state.pop("persona_description", None)
                st.session_state.step = 4
                st.rerun()
    render_top_nav()
def render_step4():
    """Generate the agent persona description using the OpenAI API."""
    st.markdown(
        """
        <div style="text-align:center;">
            <img src="https://img1.wsimg.com/isteam/ip/e13cd0a5-b867-446e-
af2a-268488bd6f38/myparenthelpers%20logo%20round.png" width="80" />
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown('<div class="biglabel-B">GENERATING YOUR AGENT PERSONA</div>',
                unsafe_allow_html=True)
    st.markdown('<div class="frame-avatar">✨</div>', unsafe_allow_html=True)
    placeholder = st.empty()
    # Show animated progress messages
    for msg in ["Assimilating Knowledge…", "Synthesizing Information…", 
                "Assessing Results…", "Generating Persona…"]:
        placeholder.info(msg)
        time.sleep(0.5)
    # Only call the API if persona description is not cached
    if "persona_description" not in st.session_state:
        with st.spinner("Thinking…"):
            try:
                prompt = (
                    f"You are creating a persona description based on the summarization of the domain, philosophy, core principles, and "
                    f"practices of the {st.session_state.source_type} "
                    f"'{st.session_state.source_name}'. This persona will be used to instruct the model to adopt the persona in future conversations.  In under 200 words to describe the persona. "
                    "Respond in a JSON object with 'persona_description'."
                )
                out = openai.chat.completions.create(
                    model="gpt-4o",
                    messages=[{"role": "user", "content": prompt}],
                    response_format={"type":"json_object"}
                )
                raw = out.choices[0].message.content
                st.session_state.persona_description = \
                    json.loads(raw)["persona_description"]
            except Exception as e:
                st.error(f"OpenAI API error: {e}")
    placeholder.empty()
    desc = st.session_state.get("persona_description")
    if desc:
        st.info(desc)
    col1, col2 = st.columns(2)
    with col1:
        if st.button("RETRY", key="btn_retry"):
            st.session_state.pop("persona_description", None)
            st.rerun()
    with col2:
        if st.button("SAVE", key="btn_save_persona"):
            st.session_state.step = 5
            st.rerun()
    render_top_nav()
def render_step5():
    """Render the page to personalize the agent and save the profile, with fields varying by agent type."""
    st.markdown(
        """
        <div style="text-align:center;">
          <img src="https://img1.wsimg.com/isteam/ip/e13cd0a5-b867-446e-af2a-268488bd6f38/myparenthelpers%20logo%20round.png" width="80" />
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown('<div class="biglabel-G">PERSONALIZE AGENT</div>', unsafe_allow_html=True)
    st.markdown('<div class="frame-avatar"></div>', unsafe_allow_html=True)

    agent_type = st.session_state.get("agent_type", "Parent")

    # Build the form fields dynamically based on agent_type
    with st.form("profile"):
        if agent_type == "Parent":
            p_name = st.text_input("Parent first name")
            c_age  = st.number_input("Child age", 1, 21)
            c_name = st.text_input("Child first name")
        elif agent_type == "Teacher":
            p_name = st.text_input("Teacher name")
            c_age  = st.number_input("Class grade", 1, 12)
            c_name = ""  # not used for teachers
        else:  # Other
            p_name = st.text_input("First name")
            c_age  = 0
            c_name = ""

        prof_nm = st.text_input("Profile name")
        saved   = st.form_submit_button("SAVE")

    if saved:
        # Validate required fields
        missing = []
        if not p_name:
            missing.append("name")
        if agent_type == "Parent" and not c_name:
            missing.append("child name")
        if not prof_nm:
            missing.append("profile name")

        if missing:
            st.warning(f"Please fill the following: {', '.join(missing)}.")
        else:
            # Create and store the profile
            profile = PersonaProfile(
                profile_name        = prof_nm,
                parent_name         = p_name,
                child_name          = c_name,
                child_age           = int(c_age),
                source_type         = st.session_state.source_type,
                source_name         = st.session_state.source_name,
                persona_description = st.session_state.persona_description,
                agent_type          = agent_type
            )
            st.session_state.profiles.append(profile.dict())
            save_json(PROFILES_FILE, st.session_state.profiles)
            st.success("Profile saved!")
            st.session_state.step = 6
            st.rerun()

    if st.button("BACK", key="btn_back_details"):
        st.session_state.step = 4
        st.rerun()
    render_top_nav()
def render_step6():
    """Display the newly created agent profile confirmation card."""
    st.markdown(
        """
        <div style="text-align:center;">
          <img src="https://img1.wsimg.com/isteam/ip/e13cd0a5-b867-446e-
af2a-268488bd6f38/myparenthelpers%20logo%20round.png" width="80" />
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown('<div class="biglabel">AGENT PROFILE CREATED!</div>', 
                unsafe_allow_html=True)
    st.markdown('<div class="frame-avatar"></div>', unsafe_allow_html=True)
    # Pull the latest profile
    profile = st.session_state.profiles[-1]
    # Render it in a colored “card”
    st.markdown(
        f"""
        <div class="home-card">
          <p><strong>Profile Name:</strong> {profile['profile_name']}</p>
          <p><strong>Parent:</strong> {profile['parent_name']}</p>
          <p><strong>Child:</strong> {profile['child_name']} (Age 
{profile['child_age']})</p>
          <p><strong>Agent Type:</strong> {profile['agent_type']}</p>
          <p><strong>Source ({profile['source_type']}):</strong> 
{profile['source_name']}</p>
          <p><strong>Persona Description:</strong></p>
          <div class="answer-box" style="margin-top:4px;">{profile['persona_description']}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    render_top_nav()
def render_step7():
    """Chat interface: choose profile, select response type, ask question and view/save answer."""
    render_top_nav()
    # Row: Section Title and Agent Selector in one line
    col1, col2 = st.columns([3, 5])
    # Column 1: Header
    with col1:
        st.markdown('<div class="biglabel-G">1. SELECT AN AGENT</div>', 
                    unsafe_allow_html=True)
    # Column 2: Selectbox and Info Icon
    names = [p["profile_name"] for p in st.session_state.profiles]
    col_dd, col_icon = col2.columns([4, 1])
    idx = col_dd.selectbox(
        "Agent Profiles:",
        range(len(names)),
        format_func=lambda i: names[i],
        key="chat_profile"
    )
    sel = st.session_state.profiles[idx]
    tooltip = (
        f"Profile: {sel['profile_name']} | "
        f"Agent: {sel.get('agent_type','Parent')} | "
        f"Type: {sel['source_type']} | "
        f"Source: {sel['source_name']} | "
        f"Child: {sel['child_name']} | "
        f"Age: {sel['child_age']} | "
        f"Parent: {sel['parent_name']} | "
        f"Persona: {sel['persona_description']}"
    )
    col_icon.markdown(
        f'<span title="{tooltip}" style="font-size:1.5em; cursor:help;">ℹ️</span>',
        unsafe_allow_html=True,
    )
    # Ensure session state key exists first
    st.session_state.setdefault("shortcut", " DEFAULT")
    # Row 1: Section Label and selection box
    col1, col2 = st.columns([3, 5])
    with col1:
        st.markdown('<div class="biglabel-G">2. SELECT A RESPONSE TYPE</div>',
                    unsafe_allow_html=True)
    with col2:
        st.markdown(
            f"""
            <div style="background:#fff;color:#000;padding:12px;border-radius:8px;margin-top:4px;margin-bottom:12px;">
              <strong>Selected:</strong> {st.session_state.shortcut}
            </div>
            """,
            unsafe_allow_html=True,
        )
    # Row 2: Emoji Buttons (Full Width)
    button_cols = st.columns(len(SHORTCUTS))
    for i, sc in enumerate(SHORTCUTS):
        with button_cols[i]:
            if st.button(EMOJIS[sc], key=f"type_{sc}", help=TOOLTIPS[sc]):
                st.session_state.shortcut = sc
    # Allow users to toggle persistent memory for the conversation.  When enabled
    # the chat history with this profile will be appended to each new query,
    # enabling the agent to remember prior exchanges.
    st.checkbox(
        "Use persistent memory",
        key="persistent_memory",
        help="Keep conversation context for this profile between turns."
    )
    # Display conversation history feed for this profile. When persistent memory
    # is enabled the feed comes from the persistent conversation; otherwise
    # it comes from a temporary conversation list for the current session.
    current_conv = []
    if st.session_state.get("persistent_memory"):
        current_conv = st.session_state.conversation.get(sel['profile_name'], [])
    else:
        current_conv = st.session_state.temp_conversation.get(sel['profile_name'], [])
    if current_conv:
        for msg in current_conv:
            if msg.get("role") == "user":
                # Build tooltip with profile details for hover
                tooltip_html = (
                    f"Profile: {sel['profile_name']} | "
                    f"Agent: {sel.get('agent_type','Parent')} | "
                    f"Type: {sel['source_type']} | "
                    f"Source: {sel['source_name']} | "
                    f"Child: {sel['child_name']} | "
                    f"Age: {sel['child_age']} | "
                    f"Parent: {sel['parent_name']} | "
                    f"Persona: {sel['persona_description']}"
                )
                st.markdown(
                    f"<div class='answer-box' style='background:#144d2f;'>"
                    f"<strong>You:</strong> {msg.get('content','')} "
                    f"<span title='{tooltip_html}' style='cursor:help;font-size:1.1em;'>ℹ️</span>"
                    f"</div>",
                    unsafe_allow_html=True
                )
            else:
                st.markdown(
                    f"<div class='answer-box'>"
                    f"{msg.get('content','')}"
                    f"</div>",
                    unsafe_allow_html=True
                )
    st.markdown('<div class="home-small">3. WHAT DO YOU WANT TO ASK?</div>',
                unsafe_allow_html=True)
    query = st.text_area("Type here", key="chat_query")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("SAVE RESPONSE", key="save_response"):
            record = {
                "profile": sel["profile_name"],
                "shortcut": st.session_state.shortcut,
                "question": query,
                "answer":   st.session_state.last_answer,
                # Persist whether persistent memory was used for this answer
                "persistent_memory": st.session_state.get("persistent_memory", False)
            }
            # If persistent memory is enabled, snapshot the current conversation for this profile.
            if record["persistent_memory"]:
                record["conversation"] = st.session_state.conversation.get(sel['profile_name'], []).copy()
            if record not in st.session_state.saved_responses:
                st.session_state.saved_responses.append(record)
                save_json(RESPONSES_FILE, st.session_state.saved_responses)
            # Provide feedback without leaving the chat
            st.success("Response saved!")
    with col2:
        if st.button("SEND", key="send_btn"):
            base = (
              f"Adopt the persona described here: {sel['persona_description']}. "
              f"You are conversing with:"
              f" Parent: {sel['parent_name']}, Child: {sel['child_name']}, "
              f"Age: {sel['child_age']}."
            )
            extra_map = {
              " CONNECT":" Help explain with examples.",
              " GROW":" Offer advanced strategies.",
              " EXPLORE":" Facilitate age-appropriate Q&A.",
              " RESOLVE":" Provide step-by-step resolution.",
              "❤ SUPPORT":" Offer empathetic support."
            }
            if st.session_state.get("persistent_memory"):
                # Build a messages list incorporating prior conversation history.
                conversation = st.session_state.conversation.get(sel['profile_name'], [])
                # Instruct the assistant to respond in JSON so the response_format feature works.
                system_content = base + extra_map.get(st.session_state.shortcut, "") + \
                    "\nRespond as JSON with 'answer'."
                messages = [{"role": "system", "content": system_content}]
                messages.extend(conversation)
                messages.append({"role": "user", "content": query})
                try:
                    out = openai.chat.completions.create(
                      model="gpt-4o",
                      messages=messages,
                      response_format={"type":"json_object"}
                    )
                    answer = json.loads(out.choices[0].message.content)["answer"]
                    # Update conversation history (persistent)
                    new_conv = conversation + [
                        {"role": "user", "content": query},
                        {"role": "assistant", "content": answer}
                    ]
                    st.session_state.conversation[sel['profile_name']] = new_conv
                    save_json(MEMORY_FILE, st.session_state.conversation)
                    # Mirror persistent conversation into temp conversation for UI feed
                    st.session_state.temp_conversation[sel['profile_name']] = new_conv.copy()
                    st.session_state.last_answer = answer
                    # Only rerun on success to display the answer
                    st.rerun()
                except Exception as e:
                    st.error(f"OpenAI API error: {e}")
            else:
                # Stateless chat: single-turn prompt and response
                prompt = base + extra_map.get(st.session_state.shortcut, "") + \
                         "\n" + query + "\nRespond as JSON with 'answer'."
                try:
                    out = openai.chat.completions.create(
                      model="gpt-4o",
                      messages=[{"role":"system","content":prompt}],
                      response_format={"type":"json_object"}
                    )
                    answer_val = json.loads(out.choices[0].message.content)["answer"]
                    st.session_state.last_answer = answer_val
                    # Update temporary conversation history for this profile
                    tmp = st.session_state.temp_conversation.get(sel['profile_name'], [])
                    tmp = tmp + [
                        {"role": "user", "content": query},
                        {"role": "assistant", "content": answer_val}
                    ]
                    st.session_state.temp_conversation[sel['profile_name']] = tmp
                    # Only rerun on success
                    st.rerun()
                except Exception as e:
                    st.error(f"OpenAI API error: {e}")

def render_step8():
    """List saved chats and allow deletion or closing."""
    render_top_nav()
    st.markdown('<div class="biglabel-B">SELECT A SAVED CHAT</div>', 
                unsafe_allow_html=True)
    if not st.session_state.saved_responses:
        st.info("No saved responses."); st.session_state.step = 0; st.rerun()
    titles = [f"{i+1}. {r['profile']} – {r['shortcut']}" for i, r in 
              enumerate(st.session_state.saved_responses)]
    sel_idx = st.selectbox("Saved Chats:", range(len(titles)), 
                           format_func=lambda i: titles[i], key="saved_select")
    item = st.session_state.saved_responses[sel_idx]
    for field in ("profile","shortcut"):
        st.markdown(f'''
          <p style="color:#fff;margin:4px 0;">
            <strong>{field.title()}:</strong> {item[field]}
          </p>''', unsafe_allow_html=True)
    # Show whether persistent memory was used for this chat
    mem_flag = item.get("persistent_memory", False)
    st.markdown(f'''
      <p style="color:#fff;margin:4px 0;">
        <strong>Persistent memory:</strong> {'Yes' if mem_flag else 'No'}
      </p>''', unsafe_allow_html=True)
    st.markdown('''
      <p style="color:#fff;margin:4px 0;"><strong>Question:</strong></p>''',
      unsafe_allow_html=True)
    st.markdown(f'''
      <blockquote style="color:#fff;border-left:4px solid #27e67a;
                        padding-left:8px;margin:4px 0;">
        {item["question"]}
      </blockquote>''', unsafe_allow_html=True)
    st.markdown('''
      <p style="color:#fff;margin:4px 0;"><strong>Answer:</strong></p>''',
      unsafe_allow_html=True)
    st.markdown(f'''
      <div class="answer-box" style="color:#fff;">
        {item["answer"]}
      </div>''', unsafe_allow_html=True)

    # If the item contains a conversation history, display it in an expander so
    # users can revisit previous turns when persistent memory was enabled.
    if item.get("conversation"):
        st.markdown('<p style="color:#fff;margin:4px 0;"><strong>Chat History:</strong></p>', unsafe_allow_html=True)
        with st.expander("Show conversation history"):
            for msg in item["conversation"]:
                role_label = "You" if msg.get("role") == "user" else "Agent"
                st.markdown(
                    f"<p style='color:#fff;margin:4px 0;'><strong>{role_label}:</strong> {msg.get('content','')}</p>",
                    unsafe_allow_html=True
                )
    c1, c2 = st.columns(2)
    with c1:
        if st.button("DELETE", key="btn_delete_saved"):
            st.session_state.saved_responses.pop(sel_idx)
            save_json(RESPONSES_FILE, st.session_state.saved_responses)
            st.rerun()
    with c2:
        if st.button("CLOSE", key="btn_close_saved"):
            st.session_state.step = 0
            st.rerun()

def render_step9():
    """List agent profiles and allow editing or deletion."""
    render_top_nav()
    st.markdown('<div class="biglabel-B">AGENT PROFILES</div>', 
                unsafe_allow_html=True)
    if not st.session_state.profiles:
        st.info("No profiles stored."); st.session_state.step = 0; st.rerun()
    titles = [f"{i+1}. {p['profile_name']}" for i,p in 
              enumerate(st.session_state.profiles)]
    idx = st.selectbox("Select a profile to view / edit", 
                       range(len(titles)), format_func=lambda i: titles[i], 
                       key="profile_select")
    prof = st.session_state.profiles[idx]
    with st.form("edit_profile"):
    p_name = st.text_input("Parent first name", value=prof.get("parent_name", ""))
    # Always force default_age into allowed range!
    min_age, max_age = 1, 21
    default_age = prof.get("child_age", min_age)
    if default_age < min_age or default_age > max_age:
        default_age = min_age
    c_age  = st.number_input("Child age", min_age, max_age, value=default_age)
    c_name = st.text_input("Child first name", value=prof.get("child_name", ""))
    prof_nm= st.text_input("Profile name", value=prof.get("profile_name", ""))
    a_type = st.selectbox("Agent type", ["Parent","Teacher","Other"], 
        index=["Parent","Teacher","Other"].index(prof.get("agent_type","Parent")))
    desc   = st.text_area("Persona description", value=prof.get("persona_description",""), height=150)
    saved  = st.form_submit_button("SAVE CHANGES")
    if saved:
        prof.update(parent_name=p_name, child_age=int(c_age), 
        child_name=c_name, profile_name=prof_nm, persona_description=desc, 
        agent_type=a_type)
        st.session_state.profiles[idx] = prof
        save_json(PROFILES_FILE, st.session_state.profiles)
        st.success("Profile updated!")
    c1, c2 = st.columns(2)
    with c1:
        if st.button("DELETE PROFILE", key="btn_delete_profile"):
            st.session_state.profiles.pop(idx)
            save_json(PROFILES_FILE, st.session_state.profiles)
            st.rerun()
    with c2:
        if st.button("CLOSE", key="btn_close_profile"):
            st.session_state.step = 0
            st.rerun()

def render_step10():
    """Render the page for editing the available source lists."""
    render_top_nav()
    st.markdown('<div class="biglabel-R">EDIT SOURCE LISTS</div>', 
                unsafe_allow_html=True)
    # persistence file for sources
    def save_sources(sources):
        """Persist updated sources to JSON file."""
        try:
            with open(SOURCES_FILE, "w", encoding="utf-8") as f:
                json.dump(sources, f, indent=2)
        except Exception as e:
            st.error(f"Error saving sources: {e}")
    def load_sources():
        """Load sources from file via the existing helper."""
        return load_json(SOURCES_FILE)
    # Initialize sources if needed
    if 'sources' not in st.session_state:
        st.session_state['sources'] = load_sources() or {
            "Parent": PARENT_SOURCES,
            "Teacher": TEACHER_SOURCES,
            "Other": OTHER_SOURCES
        }
    sources = st.session_state["sources"]
    agent_type = st.selectbox("Agent Type", AGENT_TYPES, 
                              key="edit_agent_type")
    source_type = st.selectbox("Source Type", ["Book", "Expert", "Style"], 
                               key="edit_source_type")
    items = sources.get(agent_type, {}).get(source_type, [])
    st.write(f"**Current {source_type}s for {agent_type}:**")
    to_remove = st.multiselect("Select to remove", items, 
                               key="remove_sources")
    new_item = st.text_input(f"Add new {source_type}:", key="add_source")
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("Remove Selected"):
            sources[agent_type][source_type] = [x for x in items if x not in to_remove]
            st.session_state["sources"] = sources
            save_sources(sources)
            st.success("Removed selected!")
            st.rerun()
    with c2:
        if st.button("Add"):
            if new_item and new_item not in items:
                sources[agent_type][source_type].append(new_item)
                st.session_state["sources"] = sources
                save_sources(sources)
                st.success(f"Added '{new_item}'!")
                st.rerun()
            elif new_item:
                st.warning("Already in list.")
    with c3:
        if st.button("Back to Home"):
            st.session_state.step = 0
            st.rerun()
    st.markdown("<br>", unsafe_allow_html=True)
    st.write("**Current list:**")
    st.write(sources.get(agent_type, {}).get(source_type, []))

# ---------------------------------------------------------------------------
#  ENTRY POINT
# ---------------------------------------------------------------------------

def main():
    """Entry point that dispatches to the appropriate step renderer."""
    step = st.session_state.get("step", 0)
    if step == 0:
        render_step0()
    elif step == 1:
        render_step1()
    elif step == 2:
        render_step2()
    elif step == 3:
        render_step3()
    elif step == 4:
        render_step4()
    elif step == 5:
        render_step5()
    elif step == 6:
        render_step6()
    elif step == 7:
        render_step7()
    elif step == 8:
        render_step8()
    elif step == 9:
        render_step9()
    elif step == 10:
        render_step10()
    else:
        # Fallback to home on unexpected step value
        st.session_state.step = 0
        render_step0()

if __name__ == "__main__":
    main()
