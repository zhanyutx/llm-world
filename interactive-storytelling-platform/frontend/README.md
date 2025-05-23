# Frontend Application - Interactive Storytelling Platform

This directory contains the React and TypeScript frontend application for the Interactive Storytelling Platform. It is built using Vite.

## Prerequisites

- Node.js (v18 or later recommended)
- npm (usually comes with Node.js) or pnpm (optional, but can be faster and more efficient)

## Setup and Running the Application

1.  **Navigate to the frontend directory:**
    From the root of the `interactive-storytelling-platform` project, change to the frontend directory:
    ```bash
    cd frontend
    ```
    If you are already in the root directory, it would be:
    ```bash
    cd interactive-storytelling-platform/frontend
    ```

2.  **Install Dependencies:**
    You can use either `npm` or `pnpm` to install the project dependencies. `pnpm` is recommended if you have it installed, as it can be faster and more efficient with disk space.

    Using `npm`:
    ```bash
    npm install
    ```

    Using `pnpm`:
    ```bash
    pnpm install
    ```
    This command will download and install all the necessary packages defined in `package.json`.

3.  **Start the Development Server:**
    Once the dependencies are installed, you can start the Vite development server.

    Using `npm`:
    ```bash
    npm run dev
    ```

    Using `pnpm`:
    ```bash
    pnpm dev
    ```
    This command will compile the application and start a local development server.

4.  **Access the Application:**
    After the development server starts, it will output a message indicating the local URL where the application is being served. By default, Vite typically uses **port 5173**.

    Open your web browser and navigate to:
    ```
    http://localhost:5173
    ```
    If port 5173 is already in use, Vite will automatically pick the next available port. Check the terminal output from the `npm run dev` or `pnpm dev` command to see the correct URL.

## Available Scripts

In the `package.json`, you will find other scripts:

-   `build`: Builds the application for production.
    ```bash
    npm run build
    # or
    pnpm build
    ```
-   `serve`: Serves the production build locally for preview.
    ```bash
    npm run serve
    # or
    pnpm serve
    ```

## Project Structure

-   `public/`: Contains static assets that are copied directly to the build output.
-   `src/`: Contains the main application source code.
    -   `components/`: Reusable UI components.
    -   `services/`: Services for API calls or other business logic (currently a placeholder).
    -   `App.tsx`: The main application component.
    -   `index.tsx`: The entry point of the application.
    -   `App.css`: Global styles for the application.
-   `vite.config.ts`: Vite configuration file.
-   `tsconfig.json`: TypeScript configuration for the project.
-   `package.json`: Project metadata and dependencies.
-   `Dockerfile`: Defines the Docker image for building and serving this frontend application using Nginx.
-   `nginx.conf`: Nginx configuration for serving the SPA.

## Containerization

This frontend application can be containerized using Docker. The `Dockerfile` in this directory is set up to:
1.  Build the React application using Node.js.
2.  Serve the built static assets using Nginx.

For instructions on how to build and run the entire application (including this frontend and the backend) using Docker Compose, please refer to the **[Running with Docker Compose](../../README.md#running-with-docker-compose)** section in the main project README.
