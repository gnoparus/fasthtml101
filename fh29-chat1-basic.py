from fasthtml.common import *
from claudette import *
from dotenv import load_dotenv
from starlette.responses import RedirectResponse

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
app = FastHTML(hdrs=hdrs, cls="p-4 max-w-lg mx-auto")

# Set up a chat model (https://claudette.answer.ai/)
cli = Client(models[-1])
sp = "You are a helpful and concise assistant."


# Chat message component (renders a chat bubble)
def ChatMessage(msg, user):
    bubble_class = "chat-bubble-primary" if user else "chat-bubble-secondary"
    chat_class = "chat-end" if user else "chat-start"
    return Div(cls=f"chat {chat_class}")(
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
        Div(msg, cls=f"chat-bubble {bubble_class}"),
        Div("Seen" if user else "Delivered", cls="chat-footer opacity-50"),
        Hidden(msg, name="messages"),
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
    page = Form(hx_post="/", hx_target="#chatlist", hx_swap="beforeend")(
        Div(id="chatlist", cls="chat-box h-[73vh] overflow-y-auto"),
        Div(cls="flex space-x-2 mt-2")(
            Group(ChatInput(), Button("Send", cls="btn btn-primary"))
        ),
    )
    return Titled("Chatbot Demo", page)


# Handle the form submission
@app.post("/")
def send(msg: str, messages: list[str] = []):
    if msg == "":
        return ""

    messages = [str(obj) for obj in messages]
    messages.append(msg.rstrip())
    r = contents(cli(messages, sp=sp))  # get response from chat model
    return (
        ChatMessage(msg, True),  # The user's message
        ChatMessage(r.rstrip(), False),  # The chatbot's response
        ChatInput(),
    )  # And clear the input field via an OOB swap


serve()
