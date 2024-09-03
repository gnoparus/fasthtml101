from fasthtml.common import *
from claudette import *
from dotenv import load_dotenv

# Load environment variables from the .env file (if present)
load_dotenv()


tlink = (Script(src="https://cdn.tailwindcss.com"),)
dlink = (
    Link(
        rel="stylesheet",
        href="https://cdn.jsdelivr.net/npm/daisyui@4.11.1/dist/full.min.css",
    ),
)
app = FastHTML(hdrs=(tlink, dlink, picolink))

cli = Client(models[-1])
sp = """You are helpful and concise assistant."""
messages = []


def ChatMessage(msg_idx: int):
    msg = messages[msg_idx]
    text = "..." if msg["content"] == "" else msg["content"]
    bubble_class = (
        "chat-bubble-primary" if msg["role"] == "user" else "chat-bubble-secondary"
    )
    chat_class = "chat-end" if msg["role"] == "user" else "chat-start"
    generating = "generating" in messages[msg_idx] and messages[msg_idx]["generating"]
    stream_args = {
        "hx_trigger": "every 0.5s",
        "hx_swap": "outerHTML",
        "hx_get": f"/messages/{msg_idx}",
    }
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
            Div(text, cls=f"chat-bubble {bubble_class}"),
            Div(
                "Seen" if msg_idx // 2 == 0 else "Delivered",
                cls="chat-footer opacity-50",
            ),
        ),
        cls=f"chat {chat_class}",
        id=f"chat-message-{msg_idx}",
        **stream_args if generating else {},
    )


@app.get("/messages/{msg_idx}")
def get_chat_message(msg_idx: int):
    if msg_idx >= len(messages):
        return ""
    return ChatMessage(msg_idx)


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
def get():
    page = Body(
        H1("Chatbot Demo"),
        Div(
            *[ChatMessage(i) for i in range(len(messages))],
            id="chatlist",
            cls="chat-box h-[73vh] overflow-y-auto",
        ),
        Form(
            Group(ChatInput(), Button("Send", cls="btn btn-primary")),
            hx_post="/",
            hx_target="#chatlist",
            hx_swap="beforeend",
            cls="flex space-x-2 mt-2",
        ),
        cls="p-4 max-w-lg mx-auto",
    )
    return Title("Chatbot Demo - Polling"), Main(page)


@threaded
def get_response(r, idx):
    for chunk in r:
        messages[idx]["content"] += chunk
    messages[idx]["generating"] = False


@app.post("/")
def post(msg: str):
    idx = len(messages)
    messages.append({"role": "user", "content": msg.rstrip()})
    r = cli(messages, sp=sp, stream=True)  # get response from chat model
    messages.append({"role": "assistant", "generating": True, "content": ""})
    get_response(r, idx + 1)
    return (ChatMessage(idx), ChatMessage(idx + 1), ChatInput())


if __name__ == "__main__":
    uvicorn.run("fh30-chat2-polling:app", host="0.0.0.0", port=8000, reload=True)
