# --- Stage 1: Builder Base ---
# This stage installs system dependencies needed to build some Python packages.
FROM python:3.11-slim as builder-base

# Install essential build tools
RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential libpq-dev && \
    rm -rf /var/lib/apt/lists/*

# --- Stage 2: Builder ---
# This stage installs the Python dependencies into a virtual environment.
FROM builder-base as builder

# Set up a virtual environment in a standard location
ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Copy and install Python requirements
# This is done in a separate layer to leverage Docker's cache.
# The layer will only be rebuilt if requirements.txt changes.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# --- Stage 3: Final Image ---
# This is the final, lightweight production image.
FROM python:3.11-slim as final

# Create a non-root user to run the application for better security
RUN useradd --create-home --shell /bin/bash appuser
WORKDIR /home/appuser

# Copy the virtual environment with dependencies from the builder stage
COPY --from=builder /opt/venv /opt/venv

# Copy the application source code
COPY . .

# Activate the virtual environment and set owner for the application files
ENV PATH="/opt/venv/bin:$PATH"
RUN chown -R appuser:appuser ./

# Switch to the non-root user
USER appuser

# Expose the port the app runs on
EXPOSE 5001

# Define the command to run the application using Gunicorn
# Gunicorn is a production-ready WSGI server.
CMD ["gunicorn", "--bind", "0.0.0.0:5001", "main:app"]
