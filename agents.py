import os
import requests
from crewai import Agent, Task, Crew, Process
from crewai.llm import LLM
from dotenv import load_dotenv

load_dotenv()

# Hugging Face router is OpenAI-compatible; use native OpenAI provider with base_url
HF_API_KEY = os.environ["HUGGINGFACE_API_KEY"]

# provider="openai" forces CrewAI's native OpenAI client (no LiteLLM).
# HF router is OpenAI-compatible; base_url + model name is enough.
HF_LLM = LLM(
    model="mistralai/Mistral-7B-Instruct-v0.2",
    base_url="https://router.huggingface.co/v1",
    api_key=HF_API_KEY,
    provider="openai",
)

# Define an Agent for generating SQL in an analytics context.
sql_agent = Agent(
    role="Senior Analytics Engineer",
    goal="Write efficient, correct analytical SQL. If the user asks for a SQL query, you should write a SQL query to answer the question. If the user asks for a SQL query to answer a question, you should write a SQL query to answer the question. In case of any error, you should return the error message.",
    backstory="""
    You are a senior data engineer specializing in BigQuery and analytics SQL.
    You care about correctness, performance, and cost.
    """,
    allow_delegation=False,
    verbose=True,
    llm=HF_LLM,
)

schema_agent = Agent(
    role="Data Modeler",
    goal="Design clean, scalable analytical schemas",
    backstory="""
    You design star schemas, fact tables, and dimensions.
    You think about grain, keys, and query patterns.
    """,
    allow_delegation=False,
    verbose=True,
    llm=HF_LLM,
)

pipeline_agent = Agent(
    role="Data Platform Engineer",
    goal="Design reliable and cost-effective data pipelines",
    backstory="""
    You design batch and streaming pipelines.
    You consider orchestration, retries, incremental loads, and cost.
    """,
    allow_delegation=False,
    verbose=True,
    llm=HF_LLM,
)


sql_task = Task(
    name="sql",
    description="Write a BigQuery SQL query to calculate daily active users from an events table",
    expected_output="A correct and optimized BigQuery SQL query with explanation",
    agent=sql_agent
)

schema_task = Task(
    name="schema",
    description="Design a star schema for an e-commerce analytics warehouse",
    expected_output="Fact and dimension tables with keys and grain explained",
    agent=schema_agent
)

pipeline_task = Task(
    name="pipeline",
    description="Design a daily batch pipeline to ingest PostgreSQL data into BigQuery",
    expected_output="Step-by-step pipeline design including incremental logic",
    agent=pipeline_agent
)

# Define a Crew to orchestrate the agents and tasks.
# The crew will execute the tasks in sequential order.
# The verbose flag is set to True to print the output of the agents and tasks.
crew = Crew(
    agents=[sql_agent, schema_agent, pipeline_agent],
    tasks=[sql_task, schema_task, pipeline_task],
    process=Process.sequential,
    verbose=True
)

# result = crew.kickoff()
# print(result)
# print(type(result))

# Run the crew workflow
crew_output = crew.kickoff()

# Write aggregated crew output to a file
with open("crew_output.txt", "w", encoding="utf-8") as f:
    f.write(str(crew_output.raw))  # full raw output

# Also write individual task outputs
for i, task in enumerate(crew.tasks, start=1):
    print(task.name)
    print(type(task.output))
    print(task.output)
    print(task.output.raw)
    print("--------------------------------")

    with open(f"{task.name}_output.txt", "w", encoding="utf-8") as tf:
        tf.write(f"Task {i} — {task.description}\n")
        tf.write(task.output.raw)  # individual task output

