# 交互式讲故事平台

该项目是一个使用大型语言模型（LLMs）生成动态叙事的交互式讲故事平台。

## ❗ 重要提示：API 密钥配置 ❗

本平台的核心功能依赖于与来自 OpenAI 等提供商（未来可能包括 XAI）的大型语言模型 (LLM) 的交互。要启用这些功能，你**必须**配置必要的 API 密钥。

设置这些 API 密钥的详细说明如下：
- **[后端设置](#后端设置)** 部分（用于手动环境设置）。
- **[使用 Docker Compose 运行](#使用-docker-compose-运行)** 部分（用于 Docker 化设置，使用根 `.env` 文件）。

如果未配置这些密钥，依赖 LLM 的功能将无法工作。

## 项目结构

- `frontend/`: 包含 React 和 TypeScript 前端应用。
- `backend/`: 包含 Node.js 和 TypeScript 后端应用以及用于 LLM 代理逻辑的 Python 脚本。
- `shared/`: 包含前后端共享的类型和接口。
- `docker-compose.yml`: 定义了项目的各项服务。

## 开始使用

### 先决条件
- Node.js（推荐 v18 或更高版本）
- npm（通常随 Node.js 提供）或 pnpm（可选，但速度更快）
- Python（v3.9 或更高版本，适用于后端）
- pip（Python 包安装器）

### 前端设置

1. **进入前端目录：**
    ```bash
    cd interactive-storytelling-platform/frontend
    ```

2. **安装依赖项：**
    使用 npm（或者如果你已安装并更喜欢 pnpm，则可以使用 pnpm）：
    ```bash
    npm install
    ```
    或
    ```bash
    pnpm install
    ```

3. **启动开发服务器：**
    ```bash
    npm run dev
    ```
    或
    ```bash
    pnpm dev
    ```

4. **访问应用程序：**
    打开你的浏览器并访问 `http://localhost:5173`。Vite 通常默认使用 5173 端口。如果该端口已被占用，`dev` 命令的控制台输出会指示实际使用的端口。

### 后端设置

后端包含一个 Node.js/Express.js 服务器和一个用于 LLM 交互的 Python 环境。

1. **进入后端目录：**
    ```bash
    cd interactive-storytelling-platform/backend
    ```

2. **设置 Node.js 服务器：**
    *   **安装 Node.js 依赖项：**
        ```bash
        npm install
        ```
        或
        ```bash
        pnpm install
        ```
    *   **启动开发服务器：**
        后端使用 `nodemon` 监控变化并用 `ts-node` 直接运行 TypeScript。
        ```bash
        npm run dev
        ```
        或
        ```bash
        pnpm dev
        ```
        服务器通常会在端口 `8000` 上启动（如 `backend/src/server.ts` 中最终配置的那样，如果没有指定则使用默认值）。检查控制台输出以获取确切的端口号。

3. **设置 Python 环境：**
    *   **确保安装了 Python 3：**
        通过运行 `python3 --version` 来验证。
    *   **创建并激活虚拟环境（推荐）：**
        从 `interactive-storytelling-platform/backend` 目录开始：
        ```bash
        python3 -m venv venv
        source venv/bin/activate
        ```
        在 Windows 上，激活命令为 `venv\Scripts\activate`。
    *   **安装 Python 依赖项：**
        ```bash
        pip3 install -r requirements.txt
        ```
    *   **设置环境变量（至关重要）：**
        LLM 交互脚本 (`backend/src/agents/llm_handler.py`) 需要 `OPENAI_API_KEY`。
        -   **对于本地/手动设置（不使用 Docker）：** 在启动后端服务器之前，在终端会话中设置此环境变量。
            ```bash
            export OPENAI_API_KEY="your_actual_openai_api_key_here"
            ```
            （有关 OS 特定命令和如何在 `backend` 目录内使用 `.env` 文件的建议，请参阅 `backend/README.md`）。
        -   **对于 Docker Compose 设置：** 参考 [使用 Docker Compose 运行](#使用-docker-compose-运行) 部分中的说明，了解如何使用根 `.env` 文件。

        **XAI 集成的占位符：**
        如果实现了 XAI 集成，可能会使用以下键：
        -   `XAI_API_KEY`
        -   `XAI_BASE_URL`

        **没有所需的 API 密钥（例如 `OPENAI_API_KEY`），LLM 调用将会失败，相关功能将无法工作。**

4. **联合操作：**
    Node.js 服务器（使用 `npm run dev` 启动）负责处理 API 请求。当调用需要 LLM 交互的端点时，Node.js 服务器将调用 Python 脚本 (`llm_handler.py`)。因此，对于手动设置，Node.js 服务器必须正在运行并且 Python 环境（包括 API 密钥）必须正确设置。对于 Docker 设置，Docker Compose 处理此编排。

## 使用 Docker Compose 运行

Docker Compose 允许你使用单个命令构建和运行整个应用程序（前端和后端），从而简化部署和环境管理。

### 先决条件

1. **安装 Docker：**
    按照官方说明安装适用于你操作系统的 Docker Desktop：
    -   [Windows 版 Docker](https://docs.docker.com/desktop/install/windows-install/)
    -   [Mac 版 Docker](https://docs.docker.com/desktop/install/mac-install/)
    -   [Linux 版 Docker](https://docs.docker.com/desktop/install/linux-install/)
    Docker Desktop 包括 Docker Compose。

2. **验证 Docker Compose 安装：**
    安装 Docker 后，打开终端或命令提示符并运行：
    ```bash
    docker-compose --version
    ```
    此命令应显示已安装的 Docker Compose 版本。如果不是这样，你可能需要单独安装它（尤其是在 Linux 上如果不使用 Docker Desktop）：[安装 Docker Compose](https://docs.docker.com/compose/install/)。

### LLM 代理的环境变量（至关重要）

要在 Docker 化的后端服务中启用 LLM 交互，你**必须**提供必要的 API 密钥。

1. **创建 `.env` 文件：**
    在项目的根目录 (`interactive-storytelling-platform`) 中创建名为 `.env` 的文件。该文件将存储你的敏感 API 密钥，并由 Docker Compose 自动使用。

2. **将 API 密钥添加到 `.env`：**
    使用文本编辑器打开 `.env` 文件并按以下格式添加你的 API 密钥：
    ```env
    # 对于 OpenAI
    OPENAI_API_KEY=your_actual_openai_api_key_here

    # 对于未来的 XAI 集成（如果适用）：
    # XAI_API_KEY=your_actual_xai_api_key_here
    # XAI_BASE_URL=your_xai_api_base_url_if_needed # 示例：https://api.x.ai/v1
    ```
    **将 `your_actual_openai_api_key_here` 替换为你的实际 OpenAI API 密钥。** 当支持它们的功能实现时，根据需要添加其他密钥。

    **重要安全提示：** `.env` 文件**绝不**应提交到版本控制系统。确保项目根目录下的 `.gitignore` 文件包含 `.env` 的条目。如果不存在或不确定，添加它：
    ```bash
    echo ".env" >> .gitignore
    ```

3. **Docker Compose 配置用于环境变量：**
    `docker-compose.yml` 文件已经配置为读取项目根目录中的 `.env` 文件，并使这些变量对 `backend` 服务可用。Node.js 应用程序及其随后调用的 Python 脚本 `llm_handler.py` 将能够访问这些环境变量（例如，Node.js 中的 `process.env.OPENAI_API_KEY`，如果 Python 不直接通过 `os.environ` 访问的话，则需要传递给 Python 脚本）。

### 构建和运行应用程序

1. **导航到项目根目录：**
    确保你的终端位于包含 `docker-compose.yml` 的 `interactive-storytelling-platform` 目录中。

2. **构建和运行服务：**
    此命令将为 `frontend` 和 `backend` 服务构建 Docker 镜像（如果尚未构建或其 Dockerfiles 发生更改），然后启动服务。
    ```bash
    docker-compose up --build
    ```
    你将在终端中看到来自两个服务的日志。

3. **后台运行模式（可选）：**
    要以后台模式（分离模式）运行服务，请使用 `-d` 标志：
    ```bash
    docker-compose up -d --build
    ```
    如果在分离模式下运行，你可以使用 `docker-compose logs -f` 查看日志。

### 访问服务

一旦 Docker Compose 服务运行起来：

- **前端：** 打开你的浏览器并访问 `http://localhost:3000`。此端口在 `docker-compose.yml` 中定义为 `frontend` 服务的 `ports` 部分。
- **后端：** 后端服务将在 `http://localhost:8000` 上可用。此端口为 `docker-compose.yml` 中针对 `backend` 服务定义的。前端应用程序被配置为向此地址发出 API 调用。

### 停止服务

1. **如果在前台运行（无 `-d`）：**
    在运行 `docker-compose up` 的终端中按下 `Ctrl+C`。

2. **停止并移除容器（推荐在 `Ctrl+C` 后或处于分离模式时使用）：**
    在项目根目录中运行：
    ```bash
    docker-compose down
    ```
    此命令停止并移除容器、默认网络以及（如果指定了）由 `docker-compose up` 创建的卷。

## 贡献

（贡献指南待后续添加）

## 许可证

（许可证信息待后续添加）
