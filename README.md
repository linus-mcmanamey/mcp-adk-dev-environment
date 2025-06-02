# Google ADK Development Environment

This project is set up with a development container optimized for Google Agent Development Kit (ADK) development using Python 3.13.

## 🚀 Quick Start

1. **Prerequisites**: Make sure you have VS Code with the Dev Containers extension installed
2. **Open in Dev Container**: Open this folder in VS Code and click "Reopen in Container" when prompted
3. **Wait for Setup**: The container will build and install all dependencies automatically
4. **Start Developing**: You're ready to build Google ADK applications!

## 📦 What's Included

### Development Environment
- **Python 3.13** - Latest Python version
- **VS Code Extensions** - Python, Pylint, Black, Jupyter, Google Cloud Code, and more
- **Google Cloud SDK** - Pre-installed and ready to use
- **Git & GitHub CLI** - Version control tools

### Python Packages
- **Google Cloud Libraries** - Storage, BigQuery, AI Platform, Speech, Vision, etc.
- **Machine Learning** - TensorFlow, PyTorch, Transformers, LangChain
- **Web Frameworks** - FastAPI, Flask, with async support
- **Development Tools** - pytest, ruff, black, mypy, pre-commit
- **Data Processing** - pandas, numpy, matplotlib, plotly

### Features
- **Port Forwarding** - Common development ports (3000, 5000, 8000, 8080, 9000)
- **Custom Aliases** - Helpful shortcuts for ADK development
- **Auto-formatting** - Code formatting on save
- **Testing Setup** - pytest configuration
- **Jupyter Support** - For interactive development

## 🔧 Configuration

### Google Cloud Setup
1. Copy `.env.example` to `.env` and configure your settings
2. Run `adk-setup` to authenticate with Google Cloud
3. Set your project ID: `gcloud config set project YOUR_PROJECT_ID`

### Useful Commands
- `adk-setup` - Setup Google Cloud authentication
- `adk-test` - Run tests
- `adk-format` - Format code with black and fix with ruff
- `adk-lint` - Run ruff linter
- `adk-check` - Run full code quality check (ruff + mypy + pytest)

## 📁 Project Structure
```
.devcontainer/
├── devcontainer.json    # Dev container configuration
├── Dockerfile          # Container image definition
└── bashrc              # Custom bash configuration

requirements.txt         # Python dependencies
.env.example            # Environment variables template
```

## 🔍 Development Tips

1. **Package Management**: This setup uses `uv` for fast Python package installation
2. **Code Quality**: Pre-commit hooks are automatically installed with ruff, black, and mypy
3. **Authentication**: Use `gcloud auth application-default login` for local development
4. **Environment Variables**: Copy `.env.example` to `.env` and customize
5. **Testing**: Place tests in a `tests/` directory and run with `adk-test`
6. **Linting**: Use `adk-lint` for ruff linting or `adk-check` for comprehensive checks

## 📚 Additional Resources

- [Google Agent Development Kit Documentation](https://developers.google.com/assistant)
- [Google Cloud Python Client Libraries](https://cloud.google.com/python/docs/reference)
- [VS Code Dev Containers](https://code.visualstudio.com/docs/devcontainers/containers)

Happy coding! 🎉
