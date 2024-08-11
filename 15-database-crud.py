from fasthtml.common import *


def render(todo):
    tid = f"todo-{todo.id}"
    toggle = A("Toggle", hx_get=f"/toggle/{todo.id}", target_id=tid)
    return Li(toggle, todo.title + (" 🗹" if todo.done else ""), id=tid)


app, rt, todos, Todo = fast_app(
    "todos.db", live=True, render=render, id=int, pk="id", title=str, done=bool
)


@rt("/")
def get():
    items = todos()

    return Titled("Database CRUD demo app", Div(Ul(*items)))


@rt("/toggle/{tid}")
def get(tid: int):
    todo = todos[tid]
    todo.done = not todo.done
    todos.update(todo)
    return todo


serve()
