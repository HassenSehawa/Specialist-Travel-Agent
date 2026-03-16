# Specialist Travel Agent - Record Management System

## Project Overview
A desktop application for a specialist travel agent to manage **Client**, **Flight**, and **Airline** records. It features a Graphical User Interface (GUI) for CRUD operations (Create, Read, Update, Delete) and persists data using JSONL files.


## Project Structure
The application follows the **MVC (Model-View-Controller)** pattern:
```
src/
├── main.py                  # Entry point
├── models/
│   └── tables.py            # Model
├── views/
│   └── app_view.py          # View
├── controllers/
│   └── app_controller.py    # Controller
└── record/                  # JSONL data files

tests/                       # Unit tests
```

## Team Roles
* **Programmer**: Heba, Jack, Hassen
* **GUI / UX Designer**:  Yusuf, Hassen
* **Tester**: Golda, Sophie
* **Source Control Lead**: Hassen


## Prerequisites
* **Python Version:** 3.10 or higher
* **Git:** For version control


## Installation
1.  **Clone the repository:**
    ```bash
    git clone <https://github.com/HassenSehawa/Specialist-Travel-Agent.git>
    ```

2.  **Create a Virtual Environment (Recommended):**
    ```bash
    python -m venv venv
    ```

3.  **Activate the Environment:**
    ```bash
    # macOS / Linux
    source venv/bin/activate
    # Windows
    venv\Scripts\activate
    ```

## How to Run
```bash
cd src
python main.py
```

## Commit Guidelines
Every commit message must be descriptive and follow the format:
* `feat: ...` for new features.
* `fix: ...` for bug fixes.
* `refactor: ...` for code restructuring.
* `test: ...` for adding/updating tests.
* `docs: ...` for documentation changes.

## Workflow
We use a **Branch-per-Feature** workflow. **Never commit directly to `main`.**

1. **Create a branch** for your task: 
    `git checkout -b feat-data-model`
2. **Commit your changes** using the standard format: 
    `git commit -m "feat: add data model"`
3. **Push your branch**: 
    `git push origin feat-data-model`
4. **Open a Pull Request** on GitHub.

## PR Rules
* **Review:** At least one other team member (or the Source Control lead) must review the code.
* **No Conflicts:** Merge `main` into your branch (`git merge main`) to resolve conflicts locally before pushing.


## Data Management
Records are stored internally as a list of dictionaries and persisted as JSONL files in `src/record/`. Data is saved on application close and loaded automatically on startup.

