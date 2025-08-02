My Parent Helpers (MPH) 2025 App – User Guide

**Overview**
My Parent Helpers (MPH) is a Streamlit‑based mobile‑friendly web app for creating and chatting with
custom AI “helpers.” Each helper acts as a conversational agent whose persona is derived from a parent
teaching resource (book, expert or parenting style). Users can make new agents, chat with them, save
conversations and manage their profiles and data. The app opens inside a smartphone‑shaped frame with
a green gradient background. Main functions are grouped under Agents, Chats, Sources and Data on the
home screen .

**Getting Started**
Open the app – Navigate to https://mph‑2025.streamlit.app in a web browser. After it finishes loading, 
a phone‑shaped UI appears with four columns of options .

**Home screen layout** – The home page shows:
Agents column – a drop‑down list of saved agent profiles and buttons for Saved Agents and New
Agent.

Chats column – a drop‑down for Saved Chats and a button to start a New Chat.
Sources column – shows a Counts drop‑down summarising how many book/expert/style sources are
available for each agent type; contains an Edit Sources button for managing source lists.

Data column – shows a Counts drop‑down listing numbers of stored profiles and chats and a Clear
Data button to reset everything.

Use the scroll bar on the right side of the phone frame to reach content at the bottom .

**Working with Agents**
**Viewing Saved Profiles**
Click the Profiles drop‑down in the Agents column. A list of saved agent profiles appears .

Selecting a profile does not immediately open it; instead use the Saved Agents button.
Click Saved Agents. A modal opens showing editable fields for the chosen profile (parent name,
child name/age, profile name, agent type and persona description). 

Edit values and click Save Changes to update or use Delete Profile to remove it. 

Choose Close to return to the home screen (closing will not save changes).

**Creating a New Agent**
On the home screen press New Agent . You will be asked to select an agent type: Parent, Teacher
or Other. Choose one (e.g., Parent).

Choose the agent source type – Book, Expert or Style .

The following subsections describe each source type.
**Book‑Based Agents**
Select Book. On the Choose a Book screen use the drop‑down to pick a parenting/education book; for
example, Mindset . Click Create.

The app generates an agent persona summarising the chosen book’s philosophy. When ready, read
the description and choose Retry to regenerate or Save to accept .

After saving you will personalise the agent. Fill in the parent’s name, child age (use +/– to adjust) and
child name. Provide a Profile name (e.g., Mindset Agent) and click Save .

An Agent Profile Created! page confirms the profile and displays the persona description . Use
the Home button at the top to return to the home screen; the new profile appears in the Profiles list.

**Expert‑Based Agents**
Choose Expert as the agent source. Use the drop‑down to select an expert (e.g., Dr. Daniel Siegel)
and click Create.

The generated persona summarises the expert’s teachings and philosophy (mindfulness,
interpersonal neurobiology, etc.) . Press Save to continue.
Complete the same personalisation form as with book agents and click Save. The profile summary
lists the expert as the source and displays the full persona .

**Style‑Based Agents**
Choose Style as the agent source. A drop‑down appears prompting you to select or enter a
parenting style . Options include Authoritative, Gentle Parenting, or Other . Select a style
and click Create.

The app generates a persona that embodies the principles of the selected style (e.g., empathy and
respectful communication for Gentle Parenting). Read the text and click Save .
Provide the parent’s name, child age and name, and a profile name such as Gentle Parenting Agent
. Saving this form leads to the profile summary.

**Notes on Navigation**
Use the Home, Chat and Saved buttons at the top of most screens to navigate between sections.
If you scroll down within a page and do not see these buttons, press the Home key on your keyboard
or drag the scroll bar back to the top to reveal them. .
The top‑left edge of the phone frame can sometimes act as a hidden “back” area when other buttons
are not visible.

**Chatting with Agents**
Click New Chat in the Chats column on the home screen. A three‑step chat interface appears:
Select an agent – choose a profile from the drop‑down.
Select a response type – choose from icons representing how you want the answer formatted (e.g.,
simple explanation, connect to a story, or step‑by‑step breakdown). Hovering the mouse over icons
shows tooltips.

**Ask a question **– type your question in the text box and click Send.
The agent responds with a detailed answer. Scroll through the reply to read it; bullet points and
numbered lists help structure the guidance . Use Save Response to store the chat, or Send again
to ask another question.

**Managing Chats**
Saving and Viewing Past Chats
After sending a response, click Save Response. A notification confirms the chat was saved.
On the home screen choose Saved Chats. A list of saved chats appears; select one and press Saved
Chats again to open it. The chat details (profile name, question and answer) are displayed with
options to Delete or Close .

**Managing Sources**
On the home screen expand the Counts drop‑down under the Sources column to see how many
books, experts and styles are available for each agent type .
Click Edit Sources to modify source lists. In the edit screen, choose an Agent Type (Parent, Teacher
or Other) and a Source Type (Book, Expert or Style) . A list of current sources appears. You can
remove existing entries via the X button or add new ones by entering text and pressing add .
Use Back to Home to return after editing.

**Data Management**
The Counts drop‑down under the Data column displays how many profiles and chats are stored .
Clear Data resets all profiles and chats. Use this only if you want to wipe everything (there is no
undo).

**Tips and Best Practices**
**Save your agents **– always press Save after creating a persona to avoid losing it.
**Personalise thoughtfully** – use descriptive profile names to easily identify agents in the list.
**Experiment with response types** – different chat response icons change how the answer is
structured. For example, choose the orange icon to get a simple explanation or the purple icon for a
step‑by‑step plan.
**Check sources regularly** – update the sources list to add new books or experts. This helps keep
agent personas relevant.

**Conclusion**
MPH is a versatile tool for parents and teachers seeking personalised guidance. The app’s mobile‑friendly
interface makes it easy to create new agents based on favourite books, parenting experts or styles. Use
chats to ask questions and save meaningful conversations. Keep sources updated and manage your data
wisely for the best experience.

mph-2025.streamlit.app

## UI Workflow & Steps

| Step | UI Screen            | Function             | Notes                                       |
|:----:|----------------------|----------------------|---------------------------------------------|
|  0   | **Home**             | `render_step0()`     | Cards: Agents, Chats, Sources, Data         |
|  1   | Select Agent Type    | `render_step1()`     | Parent / Teacher / Other                    |
|  2   | Select Source Type   | `render_step2()`     | Book / Expert / Style                       |
|  3   | Choose Source        | `render_step3()`     | Dropdown or custom entry                    |
|  4   | Generate Persona     | `render_step4()`     | OpenAI call + loading animation             |
|  5   | Personalize Agent    | `render_step5()`     | Form fields adapt by `agent_type`           |
|  6   | Confirmation         | `render_step6()`     | Show saved profile card                     |
|  7   | Chat Interface       | `render_step7()`     | Profile selector, shortcuts, live feed      |
|  8   | Saved Chats          | `render_step8()`     | View/delete; expander for full history      |
|  9   | Edit Profiles        | `render_step9()`     | Update or delete Agent profiles             |
| 10   | Edit Sources         | `render_step10()`    | Add/remove Books/Experts/Styles             |



Streamlit
https://mph-2025.streamlit.app/
