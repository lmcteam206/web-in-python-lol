# 🌑 web-in-python-lol Framework

**web-in-python-lol** is a lightweight, general-purpose Python web framework designed for speed, simplicity, and composition. It moves away from complex HTML templates, allowing you to build full-stack web applications using pure Python "Components."


---

## 🚀 Key Features

* **Dynamic Regex Routing**: Create flexible URLs with variables (e.g., `/member/(.+)`) that pass variables directly to your functions.
* **Built-in Error Boundaries**: A specialized safety net that catches logic crashes and renders a beautiful developer-friendly debug page instead of killing the server.
* **Automatic Persistence**: Integrated `Application` class that handles loading and saving JSON data automatically.
* **Multipart File Handling**: Native support for binary image uploads without external libraries.
* **Zero Dependencies**: Built entirely on the Python Standard Library (HTTP, CGI, Re, Json).

---

## 📦 Project Structure

```text
api_maker/
├── Engine/
│   ├── core.py      # The Engine (Routing, Server, Error Boundaries)
│   └── comp.py      # UI Components (Text, Card, Row, Form)
├── save.json        # Automatic Data Storage
├── app.py           # Your Application Logic (The "Hunter" code)
└── [images].jpg     # Uploaded binary files

```

---

## 🛠️ Getting Started

### 1. Basic Routing

Define your pages using the `@web.page` decorator. The engine automatically handles static files and query parameters.

```python
from Engine import core, comp

web = core.WebApp()

@web.page("/")
def dashboard(params):
    return web.build_page([
        comp.Navbar(brand="SHADOW_OS", links={"Home": "/", "Add": "/add"}),
        comp.Container([
            comp.Text("System Active", size="30px", bold=True, color="#00ffcc")
        ])
    ])

```

### 2. Dynamic Slugs

Use regex in your routes to create profile pages for your data:

```python
@web.page("/member/(.+)")
def member_profile(params, name):
    return web.build_page([
        comp.Text(f"Viewing Hunter: {name}")
    ])

```

### 3. Error Handling

If your code crashes, ShadowEngine stops the crash and shows you exactly what happened:

---

## 🎨 Component Toolkit

| Component | Description |
| --- | --- |
| `Container` | Keeps content centered and readable. |
| `Row` | A flexbox wrapper for side-by-side elements. |
| `Card` | A grouping element with background and shadows. |
| `FileUpload` | A binary input field for images and files. |
| `Form` | Handles POST requests and file encoding. |

---

## ⚙️ How it Works

1. **Request**: The `ShadowEngine` receives a request and checks it against `routes`.
2. **Boundary**: The engine enters a `try-except` block (Error Boundary).
3. **Logic**: Your function runs, pulling data from `web.data` (loaded from `save.json`).
4. **Render**: Your Python components are converted into HTML strings.
5. **Response**: The raw HTML is sent back to the browser.

---

## 🛡️ License

Built by Hunters, for Hunters. This project is open-source.

