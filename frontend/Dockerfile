# --- Stage 1: Development ---
# This stage is for local development with hot-reloading.
FROM node:20-alpine AS development

WORKDIR /app

# Install pnpm
RUN npm install -g pnpm

# Copy package management files
COPY package.json pnpm-lock.yaml ./

# Install dependencies
RUN pnpm install --frozen-lockfile

# Copy the rest of the application code
COPY . .

# Expose Vite's development server port
EXPOSE 5173

# Default command to start the development server
CMD ["pnpm", "run", "dev"]


# --- Stage 2: Build ---
# This stage is for building the production assets.
FROM node:20-alpine AS build

WORKDIR /app

COPY package.json pnpm-lock.yaml ./

RUN npm install -g pnpm && \
    pnpm install --frozen-lockfile

COPY . .
RUN pnpm run build


# --- Stage 3: Production ---
# This is the final production image with Nginx.
FROM nginx:alpine AS production

# Install curl for health checks
RUN apk add --no-cache curl

# Copy build artifacts from the build stage
COPY --from=build /app/dist /usr/share/nginx/html

# Copy Nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Set correct permissions
RUN chown -R nginx:nginx /usr/share/nginx/html && \
    chown -R nginx:nginx /var/cache/nginx && \
    chown -R nginx:nginx /var/log/nginx && \
    chown -R nginx:nginx /etc/nginx/conf.d && \
    touch /var/run/nginx.pid && \
    chown -R nginx:nginx /var/run/nginx.pid

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=20s --retries=3 \
    CMD curl -f http://localhost/health || exit 1

EXPOSE 80

USER nginx

CMD ["nginx", "-g", "daemon off;"]
