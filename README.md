# VSB Agents URL Generator

A Django-based web application for generating dynamic AI agent pages with chat functionality. Users can create unique URLs for AI-powered agents, interact with them in real-time, and manage their generated pages with ease.

---

## Features

- **Dynamic Page Generation:** Instantly create unique URLs for AI agents.
- **Interactive Chat:** Engage with AI agents on each generated page.
- **Modern UI:** Clean, responsive, and user-friendly interface using Tailwind CSS and Bootstrap.
- **Copy & Share:** Easily copy generated URLs to share with others.
- **Usage Guide:** Built-in guide and about sections for user support.

---

## Project Structure

```
.
├── url_generator/         # Django project settings and configuration
├── url_geapp/             # Main Django app with views, models, and components
│   └── Components/        # Modular logic for chat, dynamic pages, etc.
├── templates/             # HTML templates (base, home, dynamic_page, success)
├── static/                # Static files (CSS, JS, images) if used
├── manage.py
└── README.md
```

---

## Getting Started

### Prerequisites

- Python 3.11+
- pip (Python package manager)
- [Optional] Virtual environment tool (venv, virtualenv, etc.)

### Installation

1. **Clone the repository:**
    ```sh
    git clone https://github.com/yourusername/vsb-agents-url-generator.git
    cd vsb-agents-url-generator
    ```

2. **Create and activate a virtual environment:**
    ```sh
    python -m venv venv
    venv\Scripts\activate
    ```

3. **Install dependencies:**
    ```sh
    pip install django
    ```

4. **Apply migrations:**
    ```sh
    python manage.py migrate
    ```

5. **Run the development server:**
    ```sh
    python manage.py runserver
    ```

6. **Access the app:**
    Open your browser and go to [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

---

## Usage

- **Home:** Start by creating a new AI agent page.
- **Dynamic Page:** Chat with your AI agent and view details.
- **Success Page:** Copy and share your generated URL.
- **Navigation:** Use the header links for guide and about info.

---

## Customization

- **Templates:** Edit files in `templates/` for UI changes.
- **Components:** Extend logic in `url_geapp/Components/`.
- **Static Files:** Add custom CSS/JS in the `static/` directory.

---

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

---

## Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

---

## Contact

For questions or support, please open an issue on the repository.
