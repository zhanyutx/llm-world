# Stage 1: Build the Node.js application (if necessary, e.g., TypeScript)
FROM node:18-bullseye AS builder

# Set working directory
WORKDIR /usr/src/app

# Install Python 3 and pip (bullseye should have python3, ensure pip is available)
# Also install sudo for potential build scripts that might need it (though ideally not)
RUN apt-get update && \
    apt-get install -y python3 python3-pip sudo && \
    pip3 install --no-cache-dir --upgrade pip

# Copy package manager files
# Prioritize pnpm if pnpm-lock.yaml exists
COPY package.json ./
COPY pnpm-lock.yaml ./pnpm-lock.yaml*
COPY package-lock.json ./package-lock.json*

# Install Node.js dependencies
# Check for pnpm-lock.yaml first, then package-lock.json
RUN if [ -f pnpm-lock.yaml ]; then \
      npm install -g pnpm && pnpm install --frozen-lockfile; \
    elif [ -f package-lock.json ]; then \
      npm ci; \
    else \
      echo "No lockfile found. Please commit pnpm-lock.yaml or package-lock.json" && exit 1; \
    fi

# Copy Python requirements
COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the rest of the backend application source
COPY . .

# Transpile TypeScript to JavaScript
# The tsconfig.json specifies "outDir": "./dist"
RUN npm run build


# Stage 2: Setup the production environment
FROM node:18-bullseye AS production

WORKDIR /usr/src/app

# Install Python 3 and pip (needed for runtime if Python scripts are called directly)
RUN apt-get update && \
    apt-get install -y python3 python3-pip sudo && \
    pip3 install --no-cache-dir --upgrade pip

# Copy package manager files again for production dependencies
COPY package.json ./
COPY pnpm-lock.yaml ./pnpm-lock.yaml*
COPY package-lock.json ./package-lock.json*

# Install ONLY production Node.js dependencies
RUN if [ -f pnpm-lock.yaml ]; then \
      npm install -g pnpm && pnpm install --prod --frozen-lockfile; \
    elif [ -f package-lock.json ]; then \
      npm ci --omit=dev; \
    else \
      echo "No lockfile found. Please commit pnpm-lock.yaml or package-lock.json" && exit 1; \
    fi

# Copy Python requirements and install them
COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the built application from the builder stage
COPY --from=builder /usr/src/app/dist ./dist
# If server.ts is directly in src and app.ts in src, then after build they'd be in dist
# The main in package.json is "dist/server.js"

# Expose port (ensure this matches your backend server's listening port)
EXPOSE 8000

# Command to run the application
# Node.js needs access to environment variables like OPENAI_API_KEY passed by Docker Compose
# The Python script llm_handler.py will be called by the Node.js app and will inherit these.
CMD ["node", "dist/server.js"]
