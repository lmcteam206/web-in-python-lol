from Engine.core import *

app = WebApp("work_tracker.db")

CATEGORIES = [
    ("Dashboard", "/"), 
    ("Tasks", "/tasks"), 
    ("Completed", "/completed")
]

@app.page("/")
def home(app, query, is_post=False):
    tasks = app.fetch("tasks", default=[])
    done = [t for t in tasks if t.get("done")]
    pending = [t for t in tasks if not t.get("done")]

    return app.build_page([
        Navbar("/", CATEGORIES),
        Container([
            Text("Overview", size="32px", bold=True),
            Spacer("20px"),
            Row([
                Card([Text("Total", color="#888"), Text(str(len(tasks)), size="24px", bold=True)]),
                Card([Text("Remaining", color="#888"), Text(str(len(pending)), size="24px", bold=True, color="#facc15")]),
                Card([Text("Success", color="#888"), Text(str(len(done)), size="24px", bold=True, color="#4ade80")])
            ])
        ])
    ])

@app.page("/tasks")
def task_manager(app, query, is_post=False):
    tasks = app.fetch("tasks", default=[])

    if is_post and query.get("task_name"):
        # Add the new task to our list
        tasks.append({"id": len(tasks), "name": query.get("task_name"), "done": False})
        # Just store! No more json.dumps() needed.
        app.store("tasks", tasks)

    pending_list = [
        Card([
            Row([
                Text(t["name"], bold=True),
                Form("/complete-task", [
                    TextInput("", "task_id", type="hidden", value=str(t["id"])),
                    Button("Done", primary=False),
                ]),
            ], style={"align-items": "center", "justify-content": "space-between"})
        ], style={"margin-bottom": "10px"}) 
        for t in tasks if not t.get("done")
    ]

    return app.build_page([
        Navbar("/tasks", CATEGORIES),
        Container([
            Text("Pending Work", size="32px", bold=True),
            Spacer("20px"),
            Card([
                Text("New Task"),
                Form("/tasks", [
                    TextInput("", "task_name", placeholder="Enter task name..."),
                    Button("Add Task"),
                ]),
            ]),
            Spacer("20px"),
            *(pending_list if pending_list else [Text("No pending tasks!", color="#888")])
        ])
    ])

@app.page("/complete-task")
def complete_logic(app, params, is_post=False):
    if is_post:
        tid = params.get("task_id")
        tasks = app.fetch("tasks", default=[])
        for t in tasks:
            if str(t["id"]) == str(tid):
                t["done"] = True
        app.store("tasks", tasks)
    return "" 

@app.page("/completed")
def completed_page(app, query, is_post=False):
    tasks = app.fetch("tasks", default=[])
    done_items = [
        Card([Text(t["name"], color="#4ade80")]) for t in tasks if t.get("done")
    ]
    return app.build_page([
        Navbar("/completed", CATEGORIES),
        Container([
            Text("Completed Log", size="32px", bold=True),
            Spacer("20px"),
            *(done_items if done_items else [Text("No completed tasks.", color="#888")]),
        ])
    ])

if __name__ == "__main__":
    app.start(port=8080, open_browser=True)