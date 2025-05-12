# Glance Server Status Agent
 
A Flask-based agent for monitoring server metrics, designed to work with the [Glance](https://github.com/glanceapp/glance) application's server status widget.
 
This is a fork of [kubakubakuba's glance-serverstatus-agent](https://github.com/kubakubakuba/glance-serverstatus-agent) with minor improvements.
 
> **Note:** This repository will become deprecated once the official Glance agent has been published.  
> See discussion: [Glance Status Agent #581](https://github.com/glanceapp/glance/discussions/581)
 
## Features
 
- Provides system information via a secured API endpoint
- Collects CPU, memory, and disk usage statistics
- Lightweight Docker container for easy deployment
- Minimal configuration with just two environment variables
 
## Quick Start
 
### 1. Clone the repository
 
```bash
git clone https://github.com/gsanders5/glance-serverstatus-agent
cd glance-serverstatus-agent
```
 
### 2. Build and run the Docker container
 
```bash
docker compose build
docker compose up -d
```
 
You can customize environment variables directly in the docker command:
 
```bash
SECRET_TOKEN=my_custom_token HOST_PORT=9090 docker compose up -d
```
 
### 3. Test the endpoint
 
```bash
curl -H "Authorization: Bearer glance_agent_token" http://localhost:8080/api/sysinfo/all
```
 
## Integrating with Glance
 
Add this agent to your Glance configuration by editing your Glance config file to include remote servers:
 
```yaml
servers:
  - type: local
    name: Local
  - type: remote
    name: Alpha
    url: http://alpha.server.com:8080
    token: glance_agent_token
  - type: remote
    name: Beta
    url: http://beta.server.com:8080
    token: glance_agent_token
  - type: remote
    name: Gamma
    url: http://gamma.server.com:8080
    token: glance_agent_token
```
 
## Configuration Options
 
| Environment Variable | Description | Default |
|---------------------|-------------|---------|
| `SECRET_TOKEN` | Authentication token for API access | `glance_agent_token` |
| `HOST_PORT` | External host port mapping | `8080` |
 
## Docker Compose Example
 
```yaml
version: '3.8'
 
services:
  glance-agent:
    build: .
    container_name: glance-serverstatus-agent
    ports:
      - "${HOST_PORT:-8080}:8080"
    environment:
      - SECRET_TOKEN=${SECRET_TOKEN:-glance_agent_token}
    volumes:
      - /sys:/sys:ro
      - /proc:/proc:ro
      - ./app.py:/app/app.py:ro
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "-H", "Authorization: Bearer ${SECRET_TOKEN:-glance_agent_token}", "http://localhost:8080/api/sysinfo/all"]
      interval: 1m
      timeout: 10s
      retries: 3
      start_period: 20s
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
```
 
## Updating the Agent
 
To update the agent to the latest version:
 
```bash
./update.sh
```
 
This script will:
1. Stop the current container
2. Pull the latest code from the repository
3. Rebuild the container
4. Start the updated container
 
## Acknowledgements
 
- Original project by [kubakubakuba](https://github.com/kubakubakuba/glance-serverstatus-agent)
- Licensed under GNU GPL v2