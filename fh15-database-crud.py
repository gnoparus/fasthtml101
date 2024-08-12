from fasthtml.common import *


def render(todo):
    tid = f"todo-{todo.id}"
    toggle = A(
        "Toggle", hx_put=f"/todos/{todo.id}/toggle", target_id=tid, hx_swap="outerHTML"
    )
    edit = A(
        "Edit",
        hx_get=f"/todos/{todo.id}/edit",
        target_id=tid,
    )
    delete = A(
        "Delete", hx_delete=f"/todos/{todo.id}", target_id=tid, hx_swap="outerHTML"
    )
    return Li(toggle, edit, delete, todo.title + (" 🗹" if todo.done else ""), id=tid)


app, rt, todos, Todo = fast_app(
    "todos.db", live=True, render=render, id=int, pk="id", title=str, done=bool
)


def create_todo_form():
    return Input(placeholder="What needs to be done?", id="title", hx_swap_oob="true")


def edit_todo_form(todo):
    tid = f"todo-{todo.id}"
    return Form(
        Group(
            Input(value=todo.title, id="title"),
            Checkbox(checked=todo.done, id="done"),
            Button(
                "Save", hx_put=f"/todos/{todo.id}", target_id=tid, hx_swap="outerHTML"
            ),
            Button(
                "Cancel", hx_get=f"/todos/{todo.id}", target_id=tid, hx_swap="outerHTML"
            ),
        ),
    )


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


@rt("/todos/{tid}")
def get(tid: int):
    return todos[tid]


@rt("/todos/{tid}/edit")
def get(tid: int):
    return edit_todo_form(todos[tid])


@rt("/todos")
def post(todo: Todo):
    return todos.insert(todo), create_todo_form()


@rt("/todos/{tid}/toggle")
def put(tid: int):
    todo = todos[tid]
    todo.done = not todo.done
    todos.update(todo)
    return todo


@rt("/todos/{tid}")
def put(tid: int, newtodo: Todo):
    todo = todos[tid]
    todo.title = newtodo.title
    todo.done = newtodo.done
    todos.update(todo)
    return todo


@rt("/todos/{tid}")
def delete(tid: int):
    todos.delete(tid)


serve()
