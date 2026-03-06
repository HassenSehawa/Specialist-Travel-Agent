# Specialist Travel Agent - Record Management System

## Project Overview
This system is designed for a specialist travel agent to manage **Client**, **Flight**, and **Airline** records. It features a Graphical User Interface (GUI) for CRUD operations (Create, Read, Update, Delete) and ensures data persistence using a structured file system (JSON/Binary).


## Project Structure
* **`src/`**: Contains the core application logic, GUI, and record management.
* **`tests/`**: Unit tests for every module.

## 👥 Team Roles
* **Programmer**: Heba, Jack, Hassen
* **GUI / UX Designer**:  Yusuf, Hassen
* **Tester**: Golda, Sophie
* **Source Control Lead**: Hassen


### Prerequisites
* **Python Version:** 3.10 or higher
* **Git:** For version control


### Installation
1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
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

## How to run 

    python src/main.py

## Commit Guidelines
Every commit message must be descriptive and follow the format:
* `feat: ...` for new features.
* `fix: ...` for bug fixes.
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

### PR Rules:
* **Review:** At least one other team member (or the Source Control lead) must review the code.
* **No Conflicts:** Merge `main` into your branch (`git merge main`) to resolve conflicts locally before pushing.


## Data Management
Records are stored internally as a list of dictionaries. On exit, the system saves data to the file system. The system automatically checks for existing records upon startup.

