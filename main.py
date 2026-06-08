import asyncio
from src.agent import run_agent

async def main():
    result=await run_agent(
        "tell me about max verstappen and send the data to my phone"
    )
    print(result)

if __name__ == "__main__":
    asyncio.run(main())
