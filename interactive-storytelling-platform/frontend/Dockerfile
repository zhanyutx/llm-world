# Stage 1: Build the React application
FROM node:18-alpine AS builder

WORKDIR /app

# Check for pnpm-lock.yaml first, then package-lock.json
COPY package.json ./
COPY pnpm-lock.yaml ./pnpm-lock.yaml*
COPY package-lock.json ./package-lock.json*

# Install pnpm if pnpm-lock.yaml exists, otherwise use npm
RUN if [ -f pnpm-lock.yaml ]; then \
      npm install -g pnpm && pnpm install --frozen-lockfile; \
    elif [ -f package-lock.json ]; then \
      npm ci; \
    else \
      echo "No lockfile found. Please commit pnpm-lock.yaml or package-lock.json" && exit 1; \
    fi

# Copy the rest of the application source code
COPY . .

# Build the application
RUN if [ -f pnpm-lock.yaml ]; then \
      pnpm run build; \
    else \
      npm run build; \
    fi

# Stage 2: Serve the application with Nginx
FROM nginx:stable-alpine

# Copy the build output from the builder stage to Nginx's web root directory
COPY --from=builder /app/dist /usr/share/nginx/html

# Copy the custom Nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expose port 80
EXPOSE 80

# Start Nginx
CMD ["nginx", "-g", "daemon off;"]
