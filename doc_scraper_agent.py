import os
import autogen
import streamlit as st

# Set up OpenAI API key
os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]

# Load LLM config
config = autogen.config_list_from_json(
    "OAI_CONFIG_LIST.json",
    filter_dict={"model": ["gpt-4", "gpt-4-0613"]}
)

# Create Assistant Agent
assistant = autogen.AssistantAgent(
    name="DocScraperAssistant",
    llm_config={"config_list": config, "temperature": 0}
)

# Create Autonomous User Agent
user_proxy = autogen.UserProxyAgent(
    name="Autopen",
    code_execution_config={
        "work_dir": "doc_workspace",
        "use_docker": False
    },
    human_input_mode="NEVER"
)

# Streamlit UI
st.title("📄 AI Document Scraper Agent")
uploaded_file = st.file_uploader("Upload a PDF or DOCX file", type=["pdf", "docx"])

if uploaded_file:
    file_path = os.path.join("doc_workspace", uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.success(f"Uploaded {uploaded_file.name}")

    # Trigger the agent
    with st.spinner("Processing document with AI agent..."):
        user_proxy.initiate_chat(
            assistant,
            message=f"""
You are a document scraping assistant.

1. Load `doc_utils.py` from the current workspace.
2. Use it to extract text from `{uploaded_file.name}`.
3. Summarize the document in bullet points.
4. Print a JSON containing: {{"title": ..., "summary": ..., "keywords": [...]}}.
"""
        )
