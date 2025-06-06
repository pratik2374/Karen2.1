# Full-fledged RAG Chat App with CrewAI and Streamlit

import os
import tempfile
import time
import base64
import streamlit as st
from crewai import Agent, Crew, Task, Process
from crewai_tools import RagTool
from embedchain.models import data_type
from dotenv import load_dotenv
load_dotenv()

# Set OpenAI Key (You can replace this with your own method of loading secrets)
openai_api_key = os.getenv("OPENAI_API_KEY")
if openai_api_key is not None:
    os.environ["OPENAI_API_KEY"] = openai_api_key
else:
    raise ValueError("OPENAI_API_KEY environment variable is not set.")

# ============================
# Initialize RAG Tool
# ============================
rag_tool = RagTool(
    config=dict(
        embedder=dict(
            provider="openai",
            config=dict(
                model="text-embedding-ada-002"
            ),
        )
    )
)

# ============================
# Streamlit Setup
# ============================
st.set_page_config(page_title="RAG Chat App", layout="wide")
st.title("📚 RAG Chat Assistant with CrewAI")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "crew" not in st.session_state:
    st.session_state.crew = None

# ============================
# Upload and Add Files to RAG Tool
# ============================
st.sidebar.title("Upload Files")
uploaded_files = st.sidebar.file_uploader(
    "Upload PDF, CSV, DOCX, TXT, JSON",
    type=["pdf", "csv", "docx", "txt", "json"],
    accept_multiple_files=True
)

rag_tool = RagTool()

# EXT_TO_DATA_TYPE = {
#     ".pdf": "pdf",
#     ".csv": "csv",
#     ".docx": "docx",
#     ".txt": "txt",
#     ".json": "json",
# }

if uploaded_files:
    os.makedirs("temp_uploaded_files", exist_ok=True)

    for uploaded_file in uploaded_files:
        file_name = uploaded_file.name
        file_path = os.path.join("temp_uploaded_files", file_name)

        # Save file
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        try:
        # Determine data_type based on file extension
            ext = os.path.splitext(file_name)[-1].lower()
            ext = file_name.split(".")[-1].lower()
            if ext == "pdf":
                data_types =  "pdf_file"
            elif ext == "csv":
                data_types =  "csv"
            elif ext == "docx":
                data_types =  "docx"
            elif ext == "txt":
                data_types =  "text_file"
            elif ext in ["xls", "xlsx"]:
                data_types =  "excel_file"
            else:
                st.sidebar.error(f"Unsupported file type: {ext}")
                data_types = "directory"
                file_path = "temp_uploaded_files"
        except Exception as e:
            st.sidebar.error(f"Error determining file type for {file_name}: {str(e)}")
            continue

        if not data_type:
            st.sidebar.error(f"Unsupported file type: {ext}")
            continue

        try:
            rag_tool.add(
                source=file_path,
                data_type=data_types,
                # path=file_path
            )
            st.sidebar.success(f"Indexed: {file_name}")
        except Exception as e:
            st.sidebar.error(f"Failed to add {file_name}: {str(e)}")

# ============================
# Agent & Task Setup
# ============================
@st.cache_resource
def build_crew():
    retriever_agent = Agent(
        role="Retriever",
        goal="Retrieve relevant information for any user query using all available documents.",
        backstory="Expert in document analysis and information retrieval.",
        tools=[rag_tool],
        verbose=True
    )

    synthesizer_agent = Agent(
        role="Synthesizer",
        goal="Provide a clear, concise answer based on the retriever's results.",
        backstory="Expert at summarizing and responding to complex questions in human-like language.",
        verbose=True
    )

    retrieval_task = Task(
        description="Retrieve relevant information based on query: {query}",
        expected_output="Relevant snippets from documents.",
        agent=retriever_agent
    )

    response_task = Task(
        description="Synthesize an answer based on the retrieved information for query: {query}",
        expected_output="Clear and helpful response.",
        agent=synthesizer_agent
    )

    return Crew(
        agents=[retriever_agent, synthesizer_agent],
        tasks=[retrieval_task, response_task],
        process=Process.sequential,
        verbose=True
    )

if st.session_state.crew is None:
    st.session_state.crew = build_crew()

# ============================
# Chat Interface
# ============================
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

user_input = st.chat_input("Ask a question about your files...")
if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            result = st.session_state.crew.kickoff(inputs={"query": user_input}).raw

        response_area = st.empty()
        full_response = ""
        for chunk in result.split("\n"):
            full_response += chunk + "\n"
            response_area.markdown(full_response + "▌")
            time.sleep(0.1)
        response_area.markdown(full_response)

        st.session_state.messages.append({"role": "assistant", "content": full_response})

# ============================
# Footer & Clear Chat
# ============================
if st.sidebar.button("Clear Chat"):
    st.session_state.messages = []
    st.rerun()