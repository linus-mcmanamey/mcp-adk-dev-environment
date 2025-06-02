#!/bin/bash

# MCP Server Initialization Script for Google ADK Development
echo "🚀 Initializing MCP servers from mcp-config.json..."

# Check if required tools are installed
check_tool() {
    if ! command -v $1 &> /dev/null; then
        echo "❌ $1 is not installed. Please install it first."
        return 1
    else
        echo "✅ $1 is available"
        return 0
    fi
}

# Check essential tools
echo "📋 Checking required tools..."
check_tool "node" || exit 1
check_tool "npm" || exit 1
check_tool "git" || exit 1
check_tool "jq" || { echo "Installing jq..."; apt-get update && apt-get install -y jq; }

# Check if mcp-config.json exists
if [ ! -f "mcp-config.json" ]; then
    echo "❌ mcp-config.json not found in current directory"
    exit 1
fi

echo "✅ Found mcp-config.json"

# Load environment variables
if [ -f .env ]; then
    echo "📁 Loading environment variables from .env file..."
    export $(cat .env | grep -v '^#' | xargs)
else
    echo "⚠️  No .env file found. Please create one based on .env.example"
fi

# Function to start a server from config
start_server() {
    local server_name=$1
    local command=$(jq -r ".mcpServers.${server_name}.command" mcp-config.json)
    local args=$(jq -r ".mcpServers.${server_name}.args[]" mcp-config.json | tr '\n' ' ')
    local env_vars=$(jq -r ".mcpServers.${server_name}.env // empty | to_entries[] | \"\(.key)=\(.value)\"" mcp-config.json)
    
    if [ "$command" = "null" ]; then
        echo "⚠️  Server $server_name not found in config"
        return 1
    fi
    
    echo "🚀 Starting $server_name server..."
    
    # Set environment variables for this server
    if [ ! -z "$env_vars" ]; then
        while IFS= read -r env_var; do
            # Expand environment variables in the format ${VAR_NAME}
            expanded_var=$(echo "$env_var" | envsubst)
            export "$expanded_var"
        done <<< "$env_vars"
    fi
    
    # Start the server in background
    if [ "$command" = "python" ]; then
        $command $args &
    else
        $command $args &
    fi
}

# Get list of all servers from config
echo "📋 Loading MCP servers from configuration..."
servers=$(jq -r '.mcpServers | keys[]' mcp-config.json)

# Start essential Python development servers first
essential_servers=("filesystem" "git" "shell" "python" "docker" "sqlite" "memory" "time")

echo "🔧 Starting essential Python development servers..."
for server in "${essential_servers[@]}"; do
    if echo "$servers" | grep -q "^${server}$"; then
        start_server "$server"
    fi
done

echo "🌐 Starting web and API servers..."
# Start web-related servers
web_servers=("fetch" "web-search" "brave-search" "youtube-transcript" "puppeteer")
for server in "${web_servers[@]}"; do
    if echo "$servers" | grep -q "^${server}$"; then
        start_server "$server"
    fi
done

echo "🔗 Starting integration servers..."
# Start servers that require API keys/configuration
integration_servers=("github" "slack" "sentry" "postgres" "everart" "sequential-thinking")
for server in "${integration_servers[@]}"; do
    if echo "$servers" | grep -q "^${server}$"; then
        # Check if required environment variables are set
        case $server in
            "github")
                [ ! -z "$GITHUB_TOKEN" ] && start_server "$server" || echo "⚠️  Skipping GitHub server - GITHUB_TOKEN not set"
                ;;
            "slack")
                [ ! -z "$SLACK_BOT_TOKEN" ] && start_server "$server" || echo "⚠️  Skipping Slack server - SLACK_BOT_TOKEN not set"
                ;;
            "sentry")
                [ ! -z "$SENTRY_AUTH_TOKEN" ] && start_server "$server" || echo "⚠️  Skipping Sentry server - SENTRY_AUTH_TOKEN not set"
                ;;
            "postgres")
                [ ! -z "$POSTGRES_CONNECTION_STRING" ] && start_server "$server" || echo "⚠️  Skipping PostgreSQL server - POSTGRES_CONNECTION_STRING not set"
                ;;
            "brave-search")
                [ ! -z "$BRAVE_API_KEY" ] && start_server "$server" || echo "⚠️  Skipping Brave Search server - BRAVE_API_KEY not set"
                ;;
            "everart")
                [ ! -z "$EVERART_API_KEY" ] && start_server "$server" || echo "⚠️  Skipping EverArt server - EVERART_API_KEY not set"
                ;;
            *)
                start_server "$server"
                ;;
        esac
    fi
done

# Wait for servers to initialize
sleep 3

echo ""
echo "✨ MCP servers initialized successfully!"
echo ""
echo "🐍 Python & Google ADK Development MCP Servers:"
echo "   • Filesystem - File operations and project management"
echo "   • Git - Version control operations"
echo "   • Python - Python package management and development tools"
echo "   • Shell - Execute CLI commands (pip, uv, pytest, gcloud)"
echo "   • GitHub - Repository access and documentation"
echo "   • Docker - Container management"
echo "   • Web Search - Find solutions and documentation"
echo "   • Fetch - API testing and debugging for Google Cloud APIs"
echo "   • SQLite - Local database operations"
echo "   • Memory - Session persistence"
echo "   • Time - Date/time utilities"
echo ""
echo "🔧 Additional servers (if configured):"
echo "   • Slack - Team communication"
echo "   • Sentry - Error tracking"
echo "   • PostgreSQL - Backend database"
echo "   • Brave Search - Enhanced search capabilities"
echo "   • Puppeteer - Web automation and testing"
echo "   • YouTube Transcript - Documentation and learning"
echo "   • EverArt - Image generation and processing"
echo ""
echo "🚀 Your Python & Google ADK development environment is ready!"
echo "💡 Tip: Use Claude with these MCP servers for enhanced Python development assistance"
