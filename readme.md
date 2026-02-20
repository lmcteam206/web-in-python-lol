
# 🌑 web-in-python-lol Engine

A lightweight, **Python-only** UI engine designed for building rapid dashboards and web interfaces without touching HTML, CSS, or JavaScript. Built on top of a standard HTTP server with zero external Python dependencies.

## ✨ Features

* **Python-Native**: Write your entire UI in pure Python classes.
* **Zero Dependencies**: Uses only the standard library (`http.server`, `sqlite3`, etc.).
* **Hot Reloading**: Automatic page refreshes when the database state changes.
* **Built-in Persistence**: SQLite3 backend integrated directly into the `WebApp` class.
* **Responsive by Default**: Modern flexbox/grid components that work on mobile and desktop.
* **Lucide Icons**: Integrated professional SVG icons out of the box.

---

## 🚀 Quick Start

### 1. Installation


```bash
pip install web-in-python-lol

```

### 2. Create your first App

```python
from Engine.core import WebApp, Container, Card, Text, Button, Navbar

# Initialize the App
app = WebApp(name="MyDashboard")

@app.page("/")
def home(instance, params):
    return [
        Navbar("App", [("Home", "/"), ("Settings", "/settings")]),
        Container([
            Card([
                Text("Welcome to ShadowUI").font_size("24px").weight("bold"),
                Text("Building UIs in Python has never been this easy."),
                Button("Get Started").m_top("20px")
            ])
        ])
    ]

if __name__ == "__main__":
    app.start(port=8080)

```

---

## 🛠 Component Toolkit

ShadowUI provides a declarative way to build layouts. Every component supports **method chaining** for styling.

| Component | Description |
| --- | --- |
| `Container` | Centers content with a max-width (ideal for main pages). |
| `Row` / `Column` | Flexbox-based layouts for horizontal or vertical stacking. |
| `Grid` | Responsive CSS Grid for cards and galleries. |
| `Card` | A styled container with borders and padding. |
| `Navbar` | Responsive navigation bar with mobile hamburger menu support. |
| `Icon` | Embed 1,000+ professional icons via [Lucide](https://lucide.dev). |

---

## 💾 Database & State

 includes a thread-safe SQLite wrapper. Use it to store settings or app state that triggers auto-reloads.

```python
# Save data
app.store("user_theme", "dark")

# Fetch data
theme = app.fetch("user_theme", default="light")

```

---

## 📱 Mobile Support

 includes a built-in "hamburger" menu system. When the screen width drops below `768px`, the `Navbar` automatically collapses into a mobile-friendly toggle.

---

## 🤝 Contributing

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

