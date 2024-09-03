from fasthtml.common import *
from claudette import *
from dotenv import load_dotenv
import asyncio

# Load environment variables from the .env file (if present)
load_dotenv()

tlink = (Script(src="https://cdn.tailwindcss.com"),)
dlink = Link(
    rel="stylesheet",
    href="https://cdn.jsdelivr.net/npm/daisyui@4.11.1/dist/full.min.css",
)
app = FastHTML(hdrs=(tlink, dlink, picolink), ws_hdr=True)

cli = AsyncClient(models[-1])
sp = "You are a helpful and concise assistant."
messages = []


def ChatMessage(msg_idx, **kwargs):
    msg = messages[msg_idx]
    bubble_class = (
        "chat-bubble-primary" if msg["role"] == "user" else "chat-bubble-secondary"
    )
    chat_class = "chat-end" if msg["role"] == "user" else "chat-start"
    return Div(
        Div(msg["role"], cls="chat-header"),
        Div(
            msg["content"],
            cls=f"chat-bubble {bubble_class}",
            id=f"chat-content-{msg_idx}",
        ),
        id=f"chat-message-{msg_idx}",
        cls=f"chat {chat_class}",
        **kwargs,
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
def home():
    page = Body(
        H1("Chatbot Demo"),
        Div(
            *[ChatMessage(msg_idx) for msg_idx, msg in enumerate(messages)],
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
    return Title("Chatbot Demo"), page


@app.ws("/wscon")
async def ws(msg: str, send):
    messages.append({"role": "user", "content": msg.rstrip()})
    swap = "beforeend"

    await send(Div(ChatMessage(len(messages) - 1), hx_swap_oob=swap, id="chatlist"))

    await send(ChatInput())

    r = await cli(messages, sp=sp, stream=True)  # get response from chat model

    messages.append({"role": "assistant", "content": ""})
    await send(Div(ChatMessage(len(messages) - 1), hx_swap_oob=swap, id="chatlist"))

    async for chunk in r:
        messages[-1]["content"] += chunk
        await send(
            Span(chunk, id=f"chat-content-{len(messages) - 1}", hx_swap_oob=swap)
        )


serve()
