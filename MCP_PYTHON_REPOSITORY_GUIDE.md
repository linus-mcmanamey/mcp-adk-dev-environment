# How to Use MCP to Attach to a Python Repository

## Overview

Model Context Protocol (MCP) allows AI assistants to access and understand your Python repositories by providing structured access to files, git history, and development tools.

## Quick Setup Guide

### 1. Configure Repository Access

The most important server is the **filesystem server**. Add your Python repository path to the `ALLOWED_DIRECTORIES`:

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem"],
      "env": {
        "ALLOWED_DIRECTORIES": "/workspaces,/path/to/your/python/repo,/another/repo"
      }
    }
  }
}
```

### 2. Essential MCP Servers for Python Development

**Core Servers (Working):**

- `@modelcontextprotocol/server-filesystem` - File and directory access
- `@modelcontextprotocol/server-memory` - Session context persistence  
- `@modelcontextprotocol/server-brave-search` - Documentation search
- `@modelcontextprotocol/server-github` - GitHub repository access

### 3. Step-by-Step Setup

#### Step 1: Update Configuration

Edit your `mcp-config.json` to include your Python repository:

```bash
# Example: Add your repo to the filesystem server
nano mcp-config.json
```

#### Step 2: Set Environment Variables

Create a `.env` file with:

```bash
# Optional but recommended
GITHUB_TOKEN=your_github_personal_access_token
BRAVE_API_KEY=your_brave_api_key  # Optional for enhanced search
```

#### Step 3: Test the Setup

```bash
# Test filesystem access
npx -y @modelcontextprotocol/server-filesystem

# Verify your repo path is accessible
ls -la /path/to/your/python/repo
```

## What the AI Assistant Can Do With Your Repository

Once MCP is configured, the AI assistant can:

### 📁 **File System Operations**

- Read and analyze Python source code
- Understand project structure and architecture
- Browse through directories and files
- Examine configuration files (requirements.txt, pyproject.toml, etc.)

### 🧠 **Code Understanding**

- Analyze function and class definitions
- Understand imports and dependencies
- Review code patterns and architectural decisions
- Identify potential issues or improvements

### 📚 **Documentation & Context**

- Read README files and documentation
- Understand project goals and setup instructions
- Access inline code comments and docstrings

### 🔍 **Development Assistance**

- Help debug issues by examining relevant code
- Suggest improvements based on codebase patterns
- Assist with refactoring and code organization
- Provide context-aware solutions

## Example Interaction

Once configured, you can ask the AI assistant:

- "Analyze the main.py file in my repository and explain what it does"
- "Help me debug this error by looking at the relevant functions"
- "Review my project structure and suggest improvements"
- "Find all the places where this function is used"
- "Help me write tests for the UserService class"

## Best Practices

### 1. **Security**

- Only include repositories you trust in `ALLOWED_DIRECTORIES`
- Use environment variables for sensitive tokens
- Review what directories you're exposing

### 2. **Performance**

- Start with essential servers (filesystem, memory)
- Add additional servers as needed
- Large repositories may take time to analyze initially

### 3. **Organization**

- Keep your MCP configuration in version control
- Document which repositories are accessible
- Use meaningful environment variable names

## Troubleshooting

### Common Issues

1. **"Directory not accessible"**
   - Check `ALLOWED_DIRECTORIES` paths are correct
   - Ensure proper file permissions

2. **"Server not found"**
   - Some MCP servers may not be available yet
   - Use the simplified configuration with working servers

3. **"Environment variables not set"**
   - Create `.env` file with required tokens
   - Export variables in your shell

## Testing Your Setup

Use this simple test to verify MCP is working:

```bash
# Test if filesystem server can access your repo
npx -y @modelcontextprotocol/server-filesystem
# Then point your AI client to the MCP configuration
```

The AI assistant should now be able to read and understand your Python repository! 🎉

## Next Steps

1. Connect your AI client (Claude, etc.) to the MCP servers
2. Start asking questions about your Python code
3. Use the AI to help with development tasks
4. Gradually add more MCP servers for enhanced functionality

---

**Remember**: MCP gives AI assistants deep insight into your codebase, making them much more effective at helping with Python development tasks!
