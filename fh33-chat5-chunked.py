from fasthtml.common import *
from claudette import *
from dotenv import load_dotenv
from starlette.responses import RedirectResponse, StreamingResponse
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
    Script(
        src="https://unpkg.com/htmx-ext-transfer-encoding-chunked@0.4.0/transfer-encoding-chunked.js"
    ),
)
app = FastHTML(
    hdrs=hdrs, ct_hdr=True, cls="p-4 max-w-lg mx-auto", live=True, debug=True
)


@app.route("/{fname:path}.{ext:static}")
async def get(fname: str, ext: str):
    return FileResponse(f"{fname}.{ext}")


# Set up a chat model (https://claudette.answer.ai/)
cli = Client(models[-1])
sp = "You are a helpful and concise assistant."


# Chat message component (renders a chat bubble)
def ChatMessage(msg, user: bool, id=None):
    bubble_class = "chat-bubble-primary" if user else "chat-bubble-secondary"
    chat_class = "chat-end" if user else "chat-start"
    return Div(cls=f"chat {chat_class}", id=f"msg-{id}")(
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
            "user" if user else "assistant",
            Time("2 hours ago", cls="text-xs opacity-50"),
            cls="chat-header",
        ),
        Div(msg, id=f"msg-{id}-content", cls=f"chat-bubble {bubble_class}"),
        Div("Seen" if user else "Delivered", cls="chat-footer opacity-50"),
        Hidden(msg, id=f"msg-{id}-hidden", name="messages"),
    )


# The input field for the user message. Also used to clear the
# input field after sending a message via an OOB swap
def ChatInput():
    return Input(
        name="msg",
        id="msg-input",
        placeholder="Type a message",
        cls="input input-bordered w-full",
        hx_swap_oob="true",
    )


# The main screen
@app.get("/")
def index():
    page = Form(
        hx_post="/",
        hx_ext="chunked-transfer",
        hx_target="#chatlist",
        hx_swap="beforeend",
        hx_disable_elt="#msg-group",
    )(
        Div(id="chatlist", cls="chat-box h-[73vh] overflow-y-auto"),
        Div(cls="flex space-x-2 mt-2")(
            Group(ChatInput(), Button("Send", cls="btn btn-primary"), id="msg-group")
        ),
    )
    return Titled("Chatbot Demo", page)


async def stream_response(msg, messages):
    yield to_xml(ChatMessage(msg, True, id=len(messages) - 1))
    yield to_xml(ChatMessage("", False, id=len(messages)))
    r = cli(messages, sp=sp, stream=True)
    response_txt = ""
    for chunk in r:
        response_txt += chunk
        yield to_xml(
            Div(
                response_txt,
                cls=f"chat-bubble chat-bubble-secondary",
                id=f"msg-{len(messages)}-content",
                hx_swap_oob="outerHTML",
            )
        )
        await asyncio.sleep(0.2)

    yield to_xml(
        Hidden(
            response_txt,
            name="messages",
            id=f"msg-{len(messages)}-hidden",
            hx_swap_oob="outerHTML",
        )
    )

    yield to_xml(ChatInput())


@app.post("/")
async def send(msg: str, messages: list[str] = None):
    if not messages:
        messages = []
    messages.append(msg.rstrip())
    return StreamingResponse(
        stream_response(msg, messages),
        media_type="text/plain",
        headers={"X-Transfer-Encoding": "chunked"},
    )


serve()
