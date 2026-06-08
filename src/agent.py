from agents import Agent, WebSearchTool, FileSearchTool , function_tool,Runner
from agents.model_settings import ModelSettings
from pydantic import BaseModel, Field
import asyncio
import os
from typing import Dict
from dotenv import load_dotenv
from openai import AsyncOpenAI
import requests
from agents import RunConfig
from agents import set_default_openai_client
from agents.models.openai_chatcompletions import OpenAIChatCompletionsModel
from openai import base_url

from src.tools.pushover import push, send_push_notification
from src.prompt import orchestrator_instructions, evaluator_instructions, worker_instruction


load_dotenv(override=True)

client = AsyncOpenAI(
    api_key=os.getenv('DEEPSEEK_API_KEY'),
    base_url="https://api.deepseek.com"
)

set_default_openai_client(client)

evaluator_agent = Agent(
    name='evaluator',
    instructions='you are an evaluator',
    model=OpenAIChatCompletionsModel(
        model='deepseek-v4-flash',
        openai_client=client
    )
)

worker_agent = Agent(
    name='worker',
    instructions='you are a worker agent whose job is to peform the tasks provided to you,you may use the tools as you see fit to complete the tasks',
    model=OpenAIChatCompletionsModel(
        model='deepseek-v4-flash',
        openai_client=client
    ),
    tools=[push]
)

evaluator_tool = evaluator_agent.as_tool(tool_name='evaluator',tool_description = 'you are an evalutor')
worker_tool = worker_agent.as_tool(tool_name='worker',tool_description='you are the worker')


tools = [worker_tool, evaluator_tool]

orchestrator_agent=Agent(
    name='Orca',
    instructions='you are the planner and your job is to plan how the task should be done and distribute the tasks',
    model=OpenAIChatCompletionsModel(
        model='deepseek-v4-flash',
        openai_client=client
    ),
    tools=tools
)

async def run_agent(prompt: str, notify: bool = True):
    result = await Runner.run(
        orchestrator_agent,
        prompt
    )

    if notify:
        send_push_notification(str(result.final_output))

    return result
