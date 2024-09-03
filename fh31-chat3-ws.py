from fasthtml.common import *
from claudette import *
from dotenv import load_dotenv
from starlette.responses import RedirectResponse
import asyncio

# Load environment variables from the .env file (if present)
load_dotenv()

# Set up the app, including daisyui and tailwind for the chat component
hdrs = (
    picolink,
    Script(src="https://cdn.tailwindcss.com"),
    Link(
        rel="stylesheet",
        href="https://cdn.jsdelivr.net/npm/daisyui@4.11.1/dist/full.min.css",
    ),
)
app = FastHTML(hdrs=hdrs, ws_hdr=True)

# Set up a chat model (https://claudette.answer.ai/)
cli = Client(models[-1])
sp = "You are a helpful and concise assistant."
messages = []


def ChatMessage(msg):
    bubble_class = (
        "chat-bubble-primary" if msg["role"] == "user" else "chat-bubble-secondary"
    )
    chat_class = "chat-end" if msg["role"] == "user" else "chat-start"
    return Div(
        Div(msg["role"], cls="chat-header"),
        Div(msg["content"], cls=f"chat-bubble {bubble_class}"),
        cls=f"chat {chat_class}",
    )


def ChatInput():
    return Input(
        type="text",
        name="msg",
        id="msg-input",
        placeholder="Type a message",
        cls="input input-bordered w-full",
        hx_swap_oob="true",
    )


@app.get("/")
def main():
    page = Body(
        H1("Chatbot Demo - WebSockets"),
        Div(
            *[ChatMessage(m) for m in messages],
            id="chatlist",
            cls="chat-box h-[73vh] overflow-y-auto",
        ),
        Form(
            Group(ChatInput(), Button("Send", cls="btn btn-primary")),
            ws_send=True,
            hx_ext="ws",
            ws_connect="/wscon",
            cls="flex space-x-2 mt-2",
        ),
        cls="p-4 max-w-lg mx-auto",
    )
    return Title("Chatbot Demo - WebSockets"), page


@app.ws("/wscon")
async def ws(msg: str, send):
    messages.append({"role": "user", "content": msg})
    await send(Div(ChatMessage(messages[-1]), hx_swap_oob="beforeend", id="chatlist"))

    await send(ChatInput())

    await asyncio.sleep(1)

    r = cli(messages, sp=sp)  # get response from chat model
    messages.append({"role": "assistant", "content": contents(r)})
    await send(Div(ChatMessage(messages[-1]), hx_swap_oob="beforeend", id="chatlist"))


if __name__ == "__main__":
    uvicorn.run("fh31-chat3-ws:app", host="0.0.0.0", port=8000, reload=True)
