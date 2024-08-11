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


@rt("/")
def get():
    items = todos()

    return Titled("Database CRUD demo app", Div(Ul(*items)))


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
