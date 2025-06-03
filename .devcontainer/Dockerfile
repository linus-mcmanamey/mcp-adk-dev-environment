# Use Python 3.13 as base image with uv
FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies
RUN apt-get update && apt-get install -y \
    # Essential build tools
    build-essential \
    gcc \
    g++ \
    make \
    cmake \
    # Git and version control
    git \
    git-lfs \
    # Network tools
    curl \
    wget \
    # Development tools
    vim \
    nano \
    htop \
    tree \
    # Google Cloud SDK dependencies
    apt-transport-https \
    ca-certificates \
    gnupg \
    lsb-release \
    # Audio/video processing (for ADK multimedia capabilities)
    ffmpeg \
    libavcodec-dev \
    libavformat-dev \
    libswscale-dev \
    # Image processing
    libjpeg-dev \
    libpng-dev \
    # Database clients
    sqlite3 \
    # SSL/TLS support
    libssl-dev \
    libffi-dev \
    # XML processing
    libxml2-dev \
    libxslt1-dev \
    # Protocol Buffers
    protobuf-compiler \
    # Cleanup
    && rm -rf /var/lib/apt/lists/*

# Install Google Cloud SDK
# RUN echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main" | tee -a /etc/apt/sources.list.d/google-cloud-sdk.list \
#     && curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | gpg --dearmor -o /usr/share/keyrings/cloud.google.gpg \
#     && apt-get update && apt-get install -y google-cloud-cli \
#     && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN groupadd --gid 1000 vscode \
    && useradd --uid 1000 --gid vscode --shell /bin/bash --create-home vscode \
    && echo "vscode ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

# Install uv - fast Python package installer


# Install development tools globally with uv
RUN uv pip install --system --no-cache \
    # Core development tools
    google-adk \
    pre-commit \
    ruff \
    # Keep essential tools for global access
    pytest \
    pydantic \
    anthropic

# Set working directory
WORKDIR /workspace

# Copy all files from the workspace root directory
COPY . /workspace/

# Change ownership of workspace files to vscode user
RUN chown -R vscode:vscode /workspace

# Switch to non-root user
USER vscode

# Configure git for the user
RUN git config --global user.name "linus-mcmanamey" \
    && git config --global user.email "linus.mcmanamey@gmail.com" \
    && git config --global init.defaultBranch main

# Create useful aliases and environment setup
RUN echo 'alias ll="ls -la"' >> ~/.bashrc \
    && echo 'alias la="ls -A"' >> ~/.bashrc \
    && echo 'alias l="ls -CF"' >> ~/.bashrc \
    && echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc \
    && echo 'export PYTHONPATH="/workspace:$PYTHONPATH"' >> ~/.bashrc

# Expose common development ports
EXPOSE 8000 8080 3000 5000 9000

# Default command
CMD ["/bin/bash"]
