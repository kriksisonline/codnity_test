# Codnity Test Project

This project is a full-stack solution demonstrating a Hacker News scraper with a Flask backend and a React frontend. It includes scripts for easy setup and running both parts in separate terminals.

---

## Prerequisites

Before using the scripts, make sure you have:

- **Python 3** installed and added to your PATH
- **Node.js and npm** installed

---

## Project Structure

```
codnity_test/
├─ back/
│  ├─ venv/
│  ├─ api.py
│  └─ requirements.txt
├─ front/
│  ├─ package.json
│  └─ src/
├─ setup.bat
├─ start.bat
└─ README.md
```

---

## Setup

1. Open a terminal and navigate to the project root:

```bash
cd codnity_test
```

2. Run the setup script to install all dependencies:

```bash
setup.bat
```

This will:
- Create a Python virtual environment in `back/` and install required packages from `requirements.txt`
- Install npm packages for the React frontend in `front/`
- It does not start the servers, so you remain in control of when to run them

---

## Running the Project

To start both backend and frontend:

```bash
start.bat
```

This will:
- Open a new terminal for the Flask backend (`http://localhost:5000`)
- Open a new terminal for the React frontend (`http://localhost:5173`)
- Automatically open your default browser to the frontend URL
- Both terminals remain open, allowing you to monitor logs and stop servers individually

---

## Running the Scraper Separately

If you want to run the scraper without starting the frontend or backend server:

1. Activate the Python virtual environment:

```bash
call back\venv\Scripts\activate
```

2. Run the scraper manually:

```bash
python back\api.py
```

You can then call the API endpoints directly or test the scraper in isolation.

---

## API Endpoints

Once the backend is running, you can access:

- `GET /stories` – Retrieve all stored stories
- `GET /stories/newest` – Retrieve the newest story by creation date
- `POST /stories/refresh` – Scrape latest stories, update points, and insert new ones

---

## Notes

- Make sure ports **5000** (backend) and **5173** (frontend) are free before starting
- Closing the terminal windows will stop the respective server
- You can refresh stories from the frontend using the **Refresh** button, or call `/stories/refresh` manually