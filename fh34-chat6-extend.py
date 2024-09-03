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
        Div(
            Div(
                Img(
                    alt="Tailwind CSS chat bubble component",
                    src="https://impactmindai435-res.cloudinary.com/image/upload/v1723612512/bualabs/IMG_7477_%E0%B8%AA%E0%B8%B3%E0%B9%80%E0%B8%99%E0%B8%B2_%E0%B8%AA%E0%B8%B3%E0%B9%80%E0%B8%99%E0%B8%B2_Original_sk9in8.jpg",
                ),
                cls="w-10 rounded-full",
            ),
            cls="chat-image avatar",
        ),
        Div(
            Div(
                msg["role"],
                Time("2 hours ago", cls="text-xs opacity-50"),
                cls="chat-header",
            ),
            Div(
                msg["content"],
                cls=f"chat-bubble {bubble_class}",
                id=f"chat-content-{msg_idx}",
            ),
            Div(
                "Seen" if msg_idx % 2 == 1 else "Delivered",
                cls="chat-footer opacity-50",
            ),
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
        Form(
            Group(Button("New Chat", cls="btn btn-primary")),
            ws_send=True,
            hx_ext="ws",
            ws_connect="/wsnewchat",
            cls="flex space-x-2 mt-2",
        ),
        ChatList(messages),
        Form(
            Group(ChatInput(), Button("Send", cls="btn btn-primary")),
            ws_send=True,
            hx_ext="ws",
            ws_connect="/wscon",
            cls="flex space-x-2 mt-2",
        ),
        cls="p-4 max-w-lg mx-auto",
        # data_theme="dark",
        data_theme="cupcake",
    )
    return Title("Chatbot Demo"), page


def ChatList(msgs=[]):
    return Div(
        *[ChatMessage(msg_idx) for msg_idx, msg in enumerate(msgs)],
        id="chatlist",
        cls="chat-box h-[73vh] overflow-y-auto",
        hx_swap_oob="outerHTML",
    )


@app.ws("/wsnewchat")
async def newchat(send):
    # print("newchat")

    messages.clear()

    await send(ChatList())

    await send(ChatInput())


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
