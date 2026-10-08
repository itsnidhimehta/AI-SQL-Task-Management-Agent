## DB
## LLM
## tools
## create_agent
## system_prompt

from dotenv import load_dotenv
load_dotenv()

from langchain_groq import ChatGroq
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langgraph.checkpoint.memory import InMemorySaver
from langchain.agents import create_agent
import streamlit as st
import uuid

db=SQLDatabase.from_uri("sqlite:///my_tasks.db")
db.run("""
            CREATE TABLE IF NOT EXISTS tasks(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            status TEXT CHECK (status IN ('pending','in_progress','completed')) DEFAULT 'pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
"""
)

# TO CREATE AGENTS WE NEED
## llm, tools, memory, system_prompt 

model=ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0,
    max_tokens=4000
)
toolkit=SQLDatabaseToolkit(db=db,llm=model)
tools=toolkit.get_tools()


system_prompt="""
You are a task management assistant that interacts with a SQL database containing a 'tasks' table.

TASK RULES:
1. Limit SELECT queries to 10 results max with ORDER BY created_at DESC
2. After CREATE/UPDATE/DELETE, confirm with SELECT query
3. If the user requests a list of tasks, present the output in a structured table format to ensure a clean and organised display in the browser.

CRUD OPERATIONS:
    CREATE: INSERT INTO tasks(title, description,status)
    READ: SELECT* FROM tasks WHERE ... LIMIT 10
    UPDATE: UPDATE tasks SET status=? WHERE id=? OR title=?
    DELETE: DELETE FROM tasks WHERE id=? or title=?

Table schema: id, title, description,status(pending/in_progress/completed), created_at
"""

@st.cache_resource
def get_agent():
    agent= create_agent(
        model=model,
        tools=tools,
        checkpointer=InMemorySaver(),
        system_prompt=system_prompt
    )
    return agent

agent=get_agent()

st.subheader("TaskBot - Manage Your Tasks")
st.caption("Try: 'Create a task called Prepare for interview' · 'Show all tasks' · 'Mark task 1 as completed'")

if "messages" not in st.session_state:
    st.session_state.messages=[]
if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())

for message in st.session_state.messages:
    st.chat_message(message["role"]).markdown(message["content"])

prompt=st.chat_input("Ask me to manage your tasks?")
if prompt:
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role":"user","content":prompt})

with st.chat_message("ai"):
      with st.spinner("Processing..."):
           try:
                response = agent.invoke(
                    {"messages":[{"role":"user","content":prompt}]},
                    {"configurable":{"thread_id":st.session_state.thread_id}}
                )
                result = response["messages"][-1].content
            except Exception as e:
                print(f"[ERROR] agent.invoke failed: {e!r}")
                result = "Sorry, I couldn't process that. Please try rephrasing your request."
            st.markdown(result)
            st.session_state.messages.append({"role":"ai","content":result})
