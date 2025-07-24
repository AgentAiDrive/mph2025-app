Test drive the application at: [https://mph-10.streamlit.app/]
My Parent Helpers (MPH)

My Parent Helpers is a Streamlit-powered application designed to assist parents with personalized parenting advice, guidance, and educational support. The app allows users to generate multiple parenting helper profiles ("Agents") with personas based on a selected book, expert, or parenting style.  Edit and approve the persona generated to ensure it aligns with your understanding then the profiles details.

These personalized parenting profiles are used in the applications prompt scheme which leverages mutiple parts of the prompt's structure - the entire context and combines with  and injects these profiles into queries sent to OpenAI models.

🚀 Features

Create personalized parenting profiles using:

👪 Parent agents, 🧑‍🏫 Teacher agents, or ✨ Other agents
📚 Books
🧑‍ Experts
✨ Styles

AI-generated persona descriptions aligned to your selected source.

Save and manage up to 99 profiles, each with personalized data including parent and child names, child age, and persona style.

Dynamic prompt injection for contextual, age-appropriate responses.

Multiple response shortcuts:

💬 Default
🤝 Connect
🌱 Grow
🔍 Explore
🛠 Resolve
❤ Support

Save and review previous prompts and AI responses.

Simple, mobile-friendly UI with profile tooltips and navigation.

🔑 Requirements

Python 3.9+

OpenAI API Key (required to use the AI features)

## 🔐 Streamlit Secrets Setup

**On Streamlit Community Cloud:**
- Go to your app’s dashboard.
- Click the “Secrets” tab.
- Add:
    openai_key = "sk-xxxxxxYOURKEYHERExxxxxxx"
- Click Save and rerun the app.

**Locally:**  
- Create a `.streamlit/secrets.toml` file with the same content above.
Set your OpenAI API key via Streamlit Secrets Manager or by directly editing the code:

openai.api_key = st.secrets.get("openai_key", "YOUR_OPENAI_API_KEY")

🛠 Installation

1. Clone the repository:

git clone 
https://github.com/yourusername/mph2025-app.git

2. Install dependencies:

pip install -r requirements.txt

3. Run the app:

streamlit run app.py

📂 Files

app.py : Main application logic

parent_helpers_profiles.json : 
Stores user profiles

parent_helpers_responses.json : Stores saved responses

requirements.txt : Required Python packages

📖 Documentation

For detailed usage instructions, please refer to the User Manual or the Quick Start Guide within the application.

🛡️ License

This project is licensed under the MIT License.

🤝 Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your improvements or bug fixes.

📫 Contact

For support or inquiries, please contact us via www.myparenthelpers.com.

