from fasthtml.common import *


def render(todo):
    tid = f"todo-{todo.id}"
    toggle = A(
        " Toggle", hx_put=f"/todos/{todo.id}", target_id=tid, hx_swap="outerHTML"
    )
    delete = A(
        " Delete", hx_delete=f"/todos/{todo.id}", target_id=tid, hx_swap="outerHTML"
    )
    return Li(toggle, delete, todo.title + (" 🗹" if todo.done else ""), id=tid)


app, rt, todos, Todo = fast_app(
    "todos.db", live=True, render=render, id=int, pk="id", title=str, done=bool
)


def create_todo_form():
    return Input(placeholder="What needs to be done?", id="title", hx_swap_oob="true")


def home():
    frm = Form(
        Group(
            create_todo_form(),
            Button("Add"),
        ),
        hx_post="/todos",
        target_id="todos-list",
        hx_swap="beforeend",
    )

    return Titled("Todos", Card(Ul(*todos(), id="todos-list"), header=frm))


@rt("/")
def get():
    return home()


@rt("/todos")
def post(todo: Todo):
    return todos.insert(todo), create_todo_from()


@rt("/todos/{tid}")
def put(tid: int):
    todo = todos[tid]
    todo.done = not todo.done
    todos.update(todo)
    return todo


@rt("/todos/{tid}")
def delete(tid: int):
    todos.delete(tid)


serve()
