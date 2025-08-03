import streamlit as st
from openai import OpenAI
import json
import os
import time
from typing import List, Tuple, Callable
from pydantic import BaseModel, Field

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
@@ -239,52 +239,52 @@ def load_json(path: str):
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

# Configure OpenAI client
client = OpenAI(api_key=st.secrets.get("openai_key", "YOUR_OPENAI_API_KEY"))

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
@@ -297,76 +297,98 @@ if 'sources' not in st.session_state:
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
    rag_upload: bool = False
    search_documents: bool = False
    search_web: bool = False
    documents: List[str] = Field(default_factory=list)

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
#  TOOL HELPER FUNCTIONS
# ---------------------------------------------------------------------------

def get_enabled_tools(profile: dict) -> List[dict]:
    """Return OpenAI tool specifications enabled for a profile."""
    tools = []
    if profile.get("search_documents"):
        tools.append({"type": "file_search"})
    if profile.get("search_web"):
        tools.append({"type": "web_search"})
    return tools

def add_tool_params(params: dict, profile: dict) -> dict:
    """Attach tool definitions to a params dict if enabled for the profile."""
    tools = get_enabled_tools(profile)
    if tools:
        params["tools"] = tools
    return params

# ---------------------------------------------------------------------------
#  HOME PAGE CARD RENDERING
# ---------------------------------------------------------------------------

def render_home_card(
    title: str,
    subtitle: str = None,
    buttons: List[Tuple[str, str, Callable, Callable]] = None,
    expander_label: str = None,
    expander_body: Callable = None,
) -> None:
    """Render a card on the home page with:
       1. Title
       2. Optional subtitle
       3. Optional buttons (side-by-side)
       4. Optional expander (full width, under buttons)
    """
    # 1) Title
    st.markdown(f'<div class="biglabel-B">{title}</div>', unsafe_allow_html=True)

    # 2) Subtitle
    if subtitle:
        st.markdown(subtitle, unsafe_allow_html=True)

    # 3) Buttons (side-by-side)
    if buttons:
        # create one column per button
        btn_cols = st.columns(len(buttons), gap="small")
@@ -602,131 +624,145 @@ def render_step4():
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
                out = client.responses.create(
                    model="gpt-4o",
                    input=prompt,
                    response_format={"type": "json_object"}
                )
                raw = out.output_text
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
    render_bottom_nav()
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
        rag_upload = st.checkbox("Enable document uploads (RAG)")
        search_docs = st.checkbox("Enable document search")
        search_web = st.checkbox("Enable web search")
        uploads = st.file_uploader("Upload documents", accept_multiple_files=True) if rag_upload else []
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
            docs_list = []
            for f in uploads or []:
                try:
                    docs_list.append(f.read().decode("utf-8"))
                except Exception:
                    pass
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
                documents           = docs_list
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
@@ -864,91 +900,94 @@ def render_step7():
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
            # Build tool list from profile settings and send query
            if st.session_state.get("persistent_memory"):
                # Build a messages list incorporating prior conversation history.
                conversation = st.session_state.conversation.get(sel['profile_name'], [])
                system_content = base + extra_map.get(st.session_state.shortcut, "") + \
                    "\nRespond as JSON with 'answer'."
                messages = [{"role": "system", "content": [{"type": "text", "text": system_content}]}]
                for m in conversation:
                    messages.append({"role": m["role"], "content": [{"type": "text", "text": m["content"]}]})
                messages.append({"role": "user", "content": [{"type": "text", "text": query}]})
                try:
                    params = {
                        "model": "gpt-4o",
                        "messages": messages,
                        "response_format": {"type": "json_object"},
                    }
                    out = client.responses.create(**add_tool_params(params, sel))
                    answer = json.loads(out.output_text)["answer"]
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
                    params = {
                        "model": "gpt-4o",
                        "input": prompt,
                        "response_format": {"type": "json_object"},
                    }
                    out = client.responses.create(**add_tool_params(params, sel))
                    answer_val = json.loads(out.output_text)["answer"]
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
    render_bottom_nav()
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
@@ -997,58 +1036,77 @@ def render_step8():
            save_json(RESPONSES_FILE, st.session_state.saved_responses)
            st.rerun()
    with c2:
        if st.button("CLOSE", key="btn_close_saved"):
            st.session_state.step = 0
            st.rerun()
    render_bottom_nav()

def render_step9():
    """List agent profiles and allow editing or deletion."""
    render_top_nav()
    st.markdown('<div class="biglabel-B">AGENT PROFILES</div>', 
                unsafe_allow_html=True)
    if not st.session_state.profiles:
        st.info("No profiles stored."); st.session_state.step = 0; st.rerun()
    titles = [f"{i+1}. {p['profile_name']}" for i, p in enumerate(st.session_state.profiles)]
    idx = st.selectbox("Select a profile to view / edit", 
                       range(len(titles)), format_func=lambda i: titles[i], 
                       key="profile_select")
    prof = st.session_state.profiles[idx]
    with st.form("edit_profile"):
        p_name = st.text_input("Parent first name", value=prof.get("parent_name", ""))
        c_age  = st.number_input("Child age", 1, 21, value=max(1, prof.get("child_age", 1)))
        c_name = st.text_input("Child first name", value=prof.get("child_name", ""))
        prof_nm= st.text_input("Profile name", value=prof.get("profile_name", ""))
        a_type = st.selectbox("Agent type", ["Parent", "Teacher", "Other"],
            index=["Parent","Teacher","Other"].index(prof.get("agent_type", "Parent")))
        desc   = st.text_area("Persona description", value=prof.get("persona_description", ""), height=150)
        rag_upload = st.checkbox("Enable document uploads (RAG)", value=prof.get("rag_upload", False))
        search_docs = st.checkbox("Enable document search", value=prof.get("search_documents", False))
        search_web = st.checkbox("Enable web search", value=prof.get("search_web", False))
        uploads = st.file_uploader("Upload documents", accept_multiple_files=True) if rag_upload else []
        saved  = st.form_submit_button("SAVE CHANGES")
    if saved:
        docs_list = prof.get("documents", [])
        for f in uploads or []:
            try:
                docs_list.append(f.read().decode("utf-8"))
            except Exception:
                pass
        prof.update(
            parent_name=p_name,
            child_age=int(c_age),
            child_name=c_name,
            profile_name=prof_nm,
            persona_description=desc,
            agent_type=a_type,
            rag_upload=rag_upload,
            search_documents=search_docs,
            search_web=search_web,
            documents=docs_list,
        )
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
