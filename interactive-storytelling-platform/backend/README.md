# Backend Service for Interactive Storytelling Platform

This directory contains the Node.js/Express.js backend and Python LLM agent interaction scripts. The backend is responsible for handling API requests, managing game state (in later phases), and interacting with LLM agents via Python scripts.

## Prerequisites

- Node.js (v18 or later recommended)
- npm (usually comes with Node.js) or pnpm (optional)
- Python (v3.9 or later)
- pip (Python package installer, usually comes with Python)

## Setup and Running the Application

The backend has two main parts that need to be set up: the Node.js server and the Python environment for LLM interactions.

### 1. Navigate to the Backend Directory

From the root of the `interactive-storytelling-platform` project, change to the backend directory:
```bash
cd backend
```
(If you are already in the root directory, use `cd interactive-storytelling-platform/backend`)

### 2. Node.js Server (TypeScript/Express.js)

This server handles incoming API requests from the frontend.

   a. **Install Node.js Dependencies:**
      Use `npm` or `pnpm` to install the project dependencies defined in `package.json`.
      ```bash
      npm install
      ```
      or
      ```bash
      pnpm install
      ```

   b. **Start the Development Server:**
      The `dev` script uses `nodemon` to automatically restart the server on file changes and `ts-node` to execute TypeScript files directly.
      ```bash
      npm run dev
      ```
      or
      ```bash
      pnpm dev
      ```
      The server is configured to listen on **port 8000** (this will be explicitly set in `src/server.ts` as development progresses). Check the console output for confirmation or any changes to the port.

### 3. Python Environment (LLM Agent Interaction)

This environment is used to run Python scripts that interface with Large Language Models (LLMs).

   a. **Ensure Python 3 is Installed:**
      Verify your Python installation:
      ```bash
      python3 --version
      ```
      If not installed, download and install it from [python.org](https://www.python.org/).

   b. **Create and Activate a Virtual Environment (Recommended):**
      It's highly recommended to use a virtual environment to manage Python dependencies for this project. From within the `interactive-storytelling-platform/backend` directory:
      ```bash
      python3 -m venv venv
      ```
      Activate the virtual environment:
      -   On macOS and Linux:
          ```bash
          source venv/bin/activate
          ```
      -   On Windows (Git Bash or PowerShell):
          ```bash
          venv\Scripts\activate
          ```
      Your terminal prompt should change to indicate that the virtual environment is active (e.g., `(venv) ...`).

   c. **Install Python Dependencies:**
      With the virtual environment active, install the required packages from `requirements.txt`:
      ```bash
      pip3 install -r requirements.txt
      ```
      This will install `openai` and any other necessary Python libraries.

   d. **Set Environment Variables (CRUCIAL):**
      The Python script (`src/agents/llm_handler.py`) that interacts with LLM providers **requires** API keys to be set as environment variables. The primary key needed currently is `OPENAI_API_KEY`.

      **This is critical for LLM functionality.**

      **For Manual Setup (running `npm run dev` directly in this directory):**
      You can set these variables in your terminal session or by using a `.env` file within this `backend` directory.

      1.  **Using a `.env` file (Recommended for local development):**
          -   Create a file named `.env` in this `interactive-storytelling-platform/backend/` directory.
          -   Add your API keys to it, for example:
              ```env
              OPENAI_API_KEY="your_actual_openai_api_key_here"
              # For future XAI integration (if applicable):
              # XAI_API_KEY="your_actual_xai_api_key_here"
              # XAI_BASE_URL="your_xai_api_base_url_if_needed"
              ```
          -   **Important**: Ensure `backend/.env` is added to your `.gitignore` file to prevent committing your keys. If you don't have a `.gitignore` in this `backend` directory, create one and add `.env` to it.
              ```bash
              echo ".env" >> .gitignore 
              ```
          -   The Node.js application (and by extension, the Python script it calls) will need to be configured to load variables from this `.env` file (e.g., using a library like `dotenv` in `app.ts` or `server.ts`). *This step is not yet implemented in the current code but is a standard practice.*

      2.  **Setting directly in the terminal:**
          Set the variable(s) in your terminal session before running `npm run dev`:
          -   On macOS and Linux:
              ```bash
              export OPENAI_API_KEY="your_actual_openai_api_key_here"
              # export XAI_API_KEY="your_actual_xai_api_key_here" # If using XAI
              ```
          -   On Windows (Command Prompt):
              ```bash
              set OPENAI_API_KEY="your_actual_openai_api_key_here"
              ```
          -   On Windows (PowerShell):
              ```bash
              $env:OPENAI_API_KEY="your_actual_openai_api_key_here"
              ```

      **Placeholders for future XAI integration:**
      -   `XAI_API_KEY`
      -   `XAI_BASE_URL` (e.g., `https://api.x.ai/v1`)

      **Without the required API key(s) (e.g., `OPENAI_API_KEY`), the LLM calls made by the Python script will fail, and the `/api/llm/generate` endpoint will return errors.**

      **Note on Docker Setup:** If you are running the application using Docker Compose, refer to the main project `README.md` for instructions on using a root-level `.env` file, which is handled by `docker-compose.yml`.

### 4. Combined Operation

-   The **Node.js server** (started with `npm run dev`) listens for API requests from the frontend.
-   When an API endpoint that requires LLM interaction (like `/api/llm/generate`) is triggered, the Node.js server executes the **Python script** (`src/agents/llm_handler.py`) as a child process.
-   Therefore, for the backend to be fully functional, the Node.js server must be running, and the Python environment (including the `OPENAI_API_KEY`) must be correctly configured and its virtual environment activated if used.

## Available Scripts (Node.js)

-   `npm run build`: Compiles TypeScript to JavaScript in the `dist` directory.
-   `npm run start`: Starts the compiled JavaScript application (meant for production).
-   `npm run dev`: Starts the development server with `nodemon` and `ts-node`.

## API Endpoints

-   `GET /`: Basic test route.
-   `POST /api/llm/generate`: Endpoint to generate text using an LLM.
    -   Body: `{ "prompt": "Your prompt text", "provider": "openai" }` (provider is optional, defaults to openai)

(More endpoints will be added as the project develops.)

## Containerization

This backend application can be containerized using Docker. The `Dockerfile` in this directory is configured to:
1.  Set up a Node.js environment.
2.  Install Node.js dependencies.
3.  Set up a Python environment and install Python dependencies from `requirements.txt`.
4.  Build the TypeScript application to JavaScript.
5.  Run the compiled Node.js application.

The "Note on Docker Setup" within the "Set Environment Variables (CRUCIAL)" section above correctly directs to the main project `README.md` for Docker Compose instructions, especially regarding the root `.env` file for API keys. For full application deployment using Docker Compose, which orchestrates this backend service with the frontend and manages networking and environment variables, please refer to the **[Running with Docker Compose](../../README.md#running-with-docker-compose)** section in the main project README.
