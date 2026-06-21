FROM python:3.11-slim

# Install Node.js (needed for npm test suite and vitest)
RUN apt-get update && apt-get install -y \
    curl \
    git \
    build-essential \
    && curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /workspace

# Copy package files and install Node dependencies
COPY package.json package-lock.json* ./
RUN npm ci || npm install

# Copy Python requirements and install Python dependencies
COPY requirements.txt* ./
RUN if [ -f requirements.txt ]; then pip install --no-cache-dir -r requirements.txt; fi

# Install pytest globally (no requirements.txt means minimal deps)
RUN pip install --no-cache-dir pytest pillow requests

# Copy git hooks installer
COPY hooks/ /workspace/hooks/

# Setup git hooks on container start
ENV GIT_TERMINAL_PROMPT=0
RUN echo 'if [ -d /workspace/.git ]; then git config --local core.hooksPath hooks; fi' >> /etc/bash.bashrc

# Expose ports
EXPOSE 9000 2015

# Default: Python dev server
CMD ["python", "serve.py", "9000"]
