# AI SQL Task Management Agent

An AI-powered Task Management application built with **Python, LangChain, LangGraph, Groq, SQLite, and Streamlit**.

The application allows users to manage tasks using natural language. Instead of manually writing SQL queries, the user can simply ask the AI agent to create, read, update, or delete tasks.

For example:

* "Show me all my tasks"
* "Create a task called Learn LangChain"
* "Mark Learn LangChain as completed"
* "Delete the task with id 2"

The AI agent understands the user's request, generates the appropriate SQL operation, executes it against the SQLite database, and returns the result through a Streamlit interface.

---

## Project Overview

This project demonstrates how an **LLM-powered SQL agent** can interact with a relational database using natural-language instructions.

### Architecture

```text
                 User
                  |
                  v
          Streamlit Chat UI
                  |
                  v
          LangChain Agent
                  |
                  v
              Groq LLM
                  |
                  v
       SQL Database Toolkit
                  |
                  v
             SQLite DB
                  |
                  v
            tasks table
```

The agent uses the LLM to understand the user's request and select the appropriate SQL database tools.

---

## Key Features

* Natural-language task management
* Create tasks
* Read/list tasks
* Update task status
* Delete tasks
* SQLite database integration
* LLM-powered SQL generation
* LangChain SQL Database Toolkit
* LangGraph agent architecture
* Streamlit chat interface
* Conversation memory using `InMemorySaver`
* Automatic database/table creation
* Structured task output
* SQL operation confirmation after modifications

---

## Technologies Used

| Technology         | Purpose                              |
| ------------------ | ------------------------------------ |
| Python             | Application development              |
| Streamlit          | Web-based user interface             |
| LangChain          | LLM and SQL agent integration        |
| LangGraph          | Agent execution and state management |
| Groq               | Large Language Model inference       |
| SQLite             | Relational database                  |
| SQLDatabase        | Database connection and interaction  |
| SQLDatabaseToolkit | SQL tools for the AI agent           |
| python-dotenv      | Environment variable management      |

---

## Project Structure

```text
AI-SQL-Task-Management-Agent/
│
├── 4_sql_agent.py
│
├── data/
│   └── sql_prompt.txt
│
├── README.md
├── requirements.txt
└── .gitignore
```

The SQLite database `my_tasks.db` is generated automatically when the application runs and is intentionally excluded from GitHub.

---

## Database Schema

The application creates a `tasks` table automatically.

```sql
CREATE TABLE IF NOT EXISTS tasks(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT,
    status TEXT CHECK (
        status IN ('pending', 'in_progress', 'completed')
    ) DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Columns

| Column      | Type      | Description                        |
| ----------- | --------- | ---------------------------------- |
| id          | INTEGER   | Unique task identifier             |
| title       | TEXT      | Task title                         |
| description | TEXT      | Optional task description          |
| status      | TEXT      | pending, in_progress, or completed |
| created_at  | TIMESTAMP | Task creation timestamp            |

---

## How the Agent Works

The project uses four main components to create the agent:

```text
LLM
Tools
Memory
System Prompt
```

### 1. LLM

The application uses Groq's `openai/gpt-oss-20b` model.

```python
model = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0,
    max_tokens=1000
)
```

The LLM is responsible for understanding the user's natural-language request and deciding which database operation is required.

---

### 2. Database

SQLite is used as the database.

```python
db = SQLDatabase.from_uri("sqlite:///my_tasks.db")
```

The database stores the task information in the `tasks` table.

---

### 3. SQL Database Toolkit

LangChain's SQL Database Toolkit provides tools that allow the agent to inspect and interact with the database.

```python
toolkit = SQLDatabaseToolkit(
    db=db,
    llm=model
)

tools = toolkit.get_tools()
```

The available tools allow the agent to work with the database rather than requiring the user to manually write SQL.

---

### 4. Agent

The LangChain agent combines the model, tools, memory, and system instructions.

```python
agent = create_agent(
    model=model,
    tools=tools,
    checkpointer=InMemorySaver(),
    system_prompt=system_prompt
)
```

---

## Agent Rules

The system prompt provides rules for safe and consistent database operations.

### SELECT operations

The agent is instructed to:

* Return a maximum of 10 records
* Sort results by `created_at DESC`

### CREATE / UPDATE / DELETE

After modifying the database, the agent performs a confirmation `SELECT` query to verify the result.

### Task status

Only these statuses are allowed:

```text
pending
in_progress
completed
```

---

## CRUD Operations

The agent supports the following operations.

### CREATE

Example:

```text
Create a task called Learn LangChain
```

Conceptually:

```sql
INSERT INTO tasks(title, description, status)
VALUES (...);
```

---

### READ

Example:

```text
Show me all tasks
```

Conceptually:

```sql
SELECT *
FROM tasks
ORDER BY created_at DESC
LIMIT 10;
```

---

### UPDATE

Example:

```text
Mark Learn LangChain as completed
```

Conceptually:

```sql
UPDATE tasks
SET status = 'completed'
WHERE title = 'Learn LangChain';
```

The agent then confirms the update with a `SELECT` query.

---

### DELETE

Example:

```text
Delete the Learn LangChain task
```

Conceptually:

```sql
DELETE FROM tasks
WHERE title = 'Learn LangChain';
```

---

## Streamlit Interface

The application provides a conversational interface using Streamlit.

Users can type natural-language commands into the chat input.

Example:

```text
User:
Mark Learn LangChain as completed
```

The agent processes the request and returns a structured response containing the updated task.

---

## Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/AI-SQL-Task-Management-Agent.git
```

### 2. Navigate to the project

```bash
cd AI-SQL-Task-Management-Agent
```

### 3. Create a virtual environment

Windows:

```bash
python -m venv env
```

Activate it:

```bash
env\Scripts\activate
```

### 4. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 5. Configure the Groq API key

Create a `.env` file:

```text
GROQ_API_KEY=your_groq_api_key
```

Do not commit the `.env` file to GitHub.

### 6. Run the application

```bash
python -m streamlit run 4_sql_agent.py
```

Streamlit will open the application in your browser.

---

## Example Queries

Try asking:

```text
Show me all tasks
```

```text
Create a task called Learn LangChain
```

```text
Create a task called Prepare for interview with description "Practice SQL agent questions"
```

```text
Mark Learn LangChain as completed
```

```text
Show completed tasks
```

```text
Delete the task with id 2
```

---

## What This Project Demonstrates

This project demonstrates practical knowledge of:

* LLM application development
* AI agents
* Tool calling
* SQL agents
* Natural-language database interaction
* LangChain
* LangGraph
* Groq
* SQLite
* Streamlit
* Prompt engineering
* State/checkpoint management
* CRUD operations
* Database schema design

---

## Future Improvements

Possible improvements include:

* PostgreSQL integration
* User authentication
* Multiple users and task ownership
* Task priorities
* Due dates
* Task search
* Task filtering
* Agent response streaming
* SQL query logging
* Production database deployment
* Cloud deployment
* Authentication and authorization
* Improved error handling
* Observability and agent tracing

---

## Author

**Nidhi Mehta**

Data Engineering / AI-ML / Generative AI

This project was created as part of my hands-on learning and portfolio development in **Generative AI, LLM Agents, LangChain, LangGraph, and AI-powered data applications**.
