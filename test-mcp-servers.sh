#!/bin/bash

echo "🔍 Testing Available MCP Servers..."

# List of MCP servers to test
servers=(
    "@modelcontextprotocol/server-filesystem"
    "@modelcontextprotocol/server-memory" 
    "@modelcontextprotocol/server-brave-search"
    "@modelcontextprotocol/server-github"
)

working_servers=()
failed_servers=()

for server in "${servers[@]}"; do
    echo -n "Testing $server... "
    if timeout 10s npx -y "$server" --help >/dev/null 2>&1; then
        echo "✅ Working"
        working_servers+=("$server")
    else
        echo "❌ Failed"
        failed_servers+=("$server")
    fi
done

echo
echo "📊 Results:"
echo "✅ Working servers:"
for server in "${working_servers[@]}"; do
    echo "  - $server"
done

echo
echo "❌ Failed servers:"
for server in "${failed_servers[@]}"; do
    echo "  - $server"
done

echo
echo "💡 Use the working servers in your MCP configuration!"
