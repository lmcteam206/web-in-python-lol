
---

# 🌑 web-in-python-lol

**web-in-python-lol** is a lightweight, zero-dependency Python web framework designed for absolute simplicity. It replaces complex HTML templates and messy SQL with pure Python **Components** and an integrated **Smart-Store** database.


---

## 🚀 Key Features

* **Smart Persistence**: Forget `json.loads` and `json.dumps`. Use `app.fetch()` and `app.store()` to save lists and dictionaries directly to SQLite.
* **Zero-Config Routing**: Define routes using Python decorators. Supports Regex for dynamic URLs (e.g., `/user/(\d+)`).
* **Component-Driven UI**: Build your interface using Python classes like `Card()`, `Row()`, and `Navbar()`.
* **Error Boundaries**: If your logic crashes, the engine catches it and displays a developer-friendly traceback in the browser instead of killing the server.
* **Live-Polling**: The browser automatically refreshes when the database is updated.

---

## 📦 Project Structure

```text
my_app/
├── Engine/
│   └── core.py       # The Engine (Routing, Server, Components)
├── work_tracker.db   # Auto-created SQLite database
└── app.py            # Your Application Logic

```

---

## 🛠️ Getting Started

### 1. The "Smart" Database

No more manual JSON conversion. The framework treats your database like a persistent Python dictionary.

```python
# Saving data
tasks = [{"id": 1, "text": "Finish Engine"}]
app.store("tasks", tasks)

# Loading data (returns a real Python list)
tasks = app.fetch("tasks", default=[])

```

### 2. Basic Routing & UI

Build a dashboard in seconds without writing a single line of HTML.

```python
from Engine.core import WebApp, Text, Container, Card

app = WebApp()

@app.page("/")
def home(app_inst, params):
    return app_inst.build_page([
        Container([
            Text("Dashboard", size="32px", bold=True),
            Card([
                Text("Welcome to the Shadow Realm.")
            ])
        ])
    ])

app.start(port=8080)

```

### 3. Dynamic Slugs (Regex)

Capture variables from the URL and use them in your functions.

```python
@app.page("/member/(.+)")
def profile(app_inst, params, username):
    return app_inst.build_page([
        Text(f"Viewing profile: {username}")
    ])

```

---

## 🎨 Component Toolkit

| Component | Description |
| --- | --- |
| **Container** | Centered wrapper (max-width: 1000px). |
| **Row** | Flexbox row for side-by-side elements. |
| **Card** | Glass-morphism container with borders. |
| **Form** | Handles POST requests automatically. |
| **TextInput** | Styled input fields (supports hidden types). |

---

## ⚙️ How it Works

1. **Request**: `ShadowEngine` captures the incoming HTTP request.
2. **Route Match**: It uses Regex to find the matching function in `routes`.
3. **The Boundary**: The function is executed inside a `try-except` block.
4. **Auto-JSON**: If you call `app.fetch()`, the engine pulls from SQLite and deserializes the JSON string back into a Python object for you.
5. **Render**: Components are flattened into a single HTML string and injected into a base template.
6. **Polling**: A background script in the browser checks the `updated_at` timestamp in the DB every 1.5 seconds to trigger auto-refresh.

---

## 🛡️ License

Built for the fast-movers. Open-source and zero-dependency.

