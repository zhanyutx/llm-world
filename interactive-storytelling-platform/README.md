# Interactive Storytelling Platform

This project is an interactive storytelling platform that uses LLMs to generate dynamic narratives.

## ❗ Important: API Key Configuration ❗

Core features of this platform rely on interactions with Large Language Models (LLMs) from providers such as OpenAI (and potentially XAI in the future). To enable these features, you **must** configure the necessary API keys.

Detailed instructions for setting up these API keys are provided in:
-   The **[Backend Setup](#backend-setup)** section (for manual environment setup).
-   The **[Running with Docker Compose](#running-with-docker-compose)** section (for Dockerized setup, which uses a root `.env` file).

Failure to configure these keys will result in the LLM-dependent functionalities not working.

## Project Structure

- `frontend/`: Contains the React and TypeScript frontend application.
- `backend/`: Contains the Node.js and TypeScript backend application, along with Python scripts for LLM agent logic.
- `shared/`: Contains shared types and interfaces between the frontend and backend.
- `docker-compose.yml`: Defines the services for the project.

## Getting Started

### Prerequisites
- Node.js (v18 or later recommended)
- npm (usually comes with Node.js) or pnpm (optional, but can be faster)
- Python (v3.9 or later for the backend)
- pip (Python package installer)

### Frontend Setup

1.  **Navigate to the frontend directory:**
    ```bash
    cd interactive-storytelling-platform/frontend
    ```

2.  **Install dependencies:**
    Use npm (or pnpm if you have it installed and prefer it):
    ```bash
    npm install
    ```
    or
    ```bash
    pnpm install
    ```

3.  **Start the development server:**
    ```bash
    npm run dev
    ```
    or
    ```bash
    pnpm dev
    ```

4.  **Access the application:**
    Open your web browser and go to `http://localhost:5173`. Vite typically defaults to port 5173. If this port is in use, the console output from the `dev` command will indicate the actual port.

### Backend Setup

The backend consists of a Node.js/Express.js server and a Python environment for LLM interactions.

1.  **Navigate to the backend directory:**
    ```bash
    cd interactive-storytelling-platform/backend
    ```

2.  **Set up the Node.js Server:**
    *   **Install Node.js dependencies:**
        ```bash
        npm install
        ```
        or
        ```bash
        pnpm install
        ```
    *   **Start the development server:**
        The backend uses `nodemon` to watch for changes and `ts-node` to run TypeScript directly.
        ```bash
        npm run dev
        ```
        or
        ```bash
        pnpm dev
        ```
        The server will typically start on port `8000` (as configured in `backend/src/server.ts` eventually, or a default if not specified). Check the console output for the exact port.

3.  **Set up the Python Environment:**
    *   **Ensure Python 3 is installed:**
        Verify by running `python3 --version`.
    *   **Create and activate a virtual environment (recommended):**
        From the `interactive-storytelling-platform/backend` directory:
        ```bash
        python3 -m venv venv
        source venv/bin/activate
        ```
        On Windows, activation is `venv\Scripts\activate`.
    *   **Install Python dependencies:**
        ```bash
        pip3 install -r requirements.txt
        ```
    *   **Set Environment Variables (Crucial):**
        The LLM interaction script (`backend/src/agents/llm_handler.py`) requires the `OPENAI_API_KEY`.
        -   **For local/manual setup (without Docker):** Set this environment variable in your terminal session before starting the backend server.
            ```bash
            export OPENAI_API_KEY="your_actual_openai_api_key_here"
            ```
            (See the `backend/README.md` for OS-specific commands and advice on using a `.env` file within the `backend` directory for this method).
        -   **For Docker Compose setup:** Refer to the [Running with Docker Compose](#running-with-docker-compose) section for instructions on using a root `.env` file.

        **Placeholders for future XAI integration:**
        If XAI integration is implemented, the following keys might be used:
        -   `XAI_API_KEY`
        -   `XAI_BASE_URL`

        **Without the required API key(s) (e.g., `OPENAI_API_KEY`), LLM calls will fail, and related features will not work.**

4.  **Combined Operation:**
    The Node.js server (started with `npm run dev`) is responsible for handling API requests. When an endpoint that requires LLM interaction is called, the Node.js server will invoke the Python script (`llm_handler.py`). Therefore, for manual setup, both the Node.js server must be running and the Python environment (including the API key) must be correctly set up. For Docker setup, Docker Compose handles this orchestration.

## Running with Docker Compose

Docker Compose allows you to build and run the entire application (frontend and backend) with a single command, simplifying deployment and environment management.

### Prerequisites

1.  **Install Docker:**
    Follow the official instructions to install Docker Desktop for your operating system:
    -   [Docker for Windows](https://docs.docker.com/desktop/install/windows-install/)
    -   [Docker for Mac](https://docs.docker.com/desktop/install/mac-install/)
    -   [Docker for Linux](https://docs.docker.com/desktop/install/linux-install/)
    Docker Desktop includes Docker Compose.

2.  **Verify Docker Compose Installation:**
    After installing Docker, open a terminal or command prompt and run:
    ```bash
    docker-compose --version
    ```
    This command should display the installed Docker Compose version. If not, you might need to install it separately (especially on Linux if not using Docker Desktop): [Install Docker Compose](https://docs.docker.com/compose/install/).

### Environment Variables for LLM Agents (Crucial)

To enable LLM interactions within the Dockerized backend service, you **must** provide the necessary API keys.

1.  **Create a `.env` file:**
    In the root directory of the project (`interactive-storytelling-platform`), create a file named `.env`. This file will store your sensitive API keys and will be automatically used by Docker Compose.

2.  **Add API Keys to `.env`:**
    Open the `.env` file with a text editor and add your API keys in the following format:
    ```env
    # For OpenAI
    OPENAI_API_KEY=your_actual_openai_api_key_here

    # For future XAI integration (if applicable):
    # XAI_API_KEY=your_actual_xai_api_key_here
    # XAI_BASE_URL=your_xai_api_base_url_if_needed # Example: https://api.x.ai/v1
    ```
    **Replace `your_actual_openai_api_key_here` with your real OpenAI API key.** Add other keys as needed when support for them is implemented.

    **Important Security Note:** The `.env` file should **never** be committed to version control. Ensure your project's root `.gitignore` file contains an entry for `.env`. If it doesn't, or if you're unsure, add it:
    ```bash
    echo ".env" >> .gitignore
    ```

3.  **Docker Compose Configuration for Environment Variables:**
    The `docker-compose.yml` file is already configured to read the `.env` file in the project's root directory and make these variables available to the `backend` service. The Node.js application, and subsequently the Python script `llm_handler.py` it calls, will have access to these environment variables.

### Build and Run the Application

The `frontend` and `backend` services are defined in `docker-compose.yml` and are built using their respective Dockerfiles (`frontend/Dockerfile` and `backend/Dockerfile`). These Dockerfiles encapsulate the build environment and process for each service, ensuring a reproducible and self-contained setup.

1.  **Navigate to the Project Root:**
    Ensure your terminal is in the `interactive-storytelling-platform` directory (the one containing `docker-compose.yml`).

2.  **Build and Run Services:**
    This command will build the Docker images for the `frontend` and `backend` services using their Dockerfiles (if the images don't exist or if the Dockerfiles/source code have changed) and then start the services.
    ```bash
    docker-compose up --build
    ```
    You will see logs from both services in your terminal. This is the primary command for running the application with Docker.

3.  **Run in Detached Mode (Optional):**
    To run the services in the background (detached mode), use the `-d` flag:
    ```bash
    docker-compose up -d --build
    ```
    You can view logs using `docker-compose logs -f` if running in detached mode.

### Accessing Services

Once the Docker Compose services are running:

-   **Frontend:** Open your web browser and navigate to `http://localhost:3000`. This port is defined in the `ports` section of the `frontend` service in `docker-compose.yml`.
-   **Backend:** The backend service will be accessible at `http://localhost:8000`. This port is defined for the `backend` service in `docker-compose.yml`. The frontend application is configured to make API calls to this address.

### Stopping Services

1.  **If Running in the Foreground (without `-d`):**
    Press `Ctrl+C` in the terminal where `docker-compose up` is running.

2.  **To Stop and Remove Containers (Recommended after `Ctrl+C` or if in detached mode):**
    From the project root directory, run:
    ```bash
    docker-compose down
    ```
    This command stops and removes the containers, default networks, and (if specified) volumes created by `docker-compose up`.

## Contributing

(Guidelines for contributing to be added later)

## License

(License information to be added later)
