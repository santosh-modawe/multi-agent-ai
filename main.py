from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai.types import Content, Part

from workflow import root_agent

app = FastAPI()

session_service = InMemorySessionService()

runner = Runner(
    agent=root_agent,
    app_name="my_app",
    session_service=session_service
)

class ChatRequest(BaseModel):
    user_id: str
    session_id: str
    message: str

@app.post("/chat/stream")
async def chat(req: ChatRequest):

    try:
        await session_service.create_session(
            app_name="my_app",
            user_id=req.user_id,
            session_id=req.session_id
        )
    except:
        pass

    async def generate():

        user_message = Content(
            role="user",
            parts=[
                Part(text=req.message)
            ]
        )

        async for event in runner.run_async(
                user_id=req.user_id,
                session_id=req.session_id,
                new_message=user_message
        ):

            if not event.content:
                continue

            author = getattr(
                event,
                "author",
                "unknown"
            )

            for part in event.content.parts:

                if getattr(part, "text", None):
                    yield (
                        f'data: {{"agent":"{author}",'
                        f'"text":"{part.text}"}}\n\n'
                    )

    return StreamingResponse(
        generate(),
        media_type="text/event-stream"
    )