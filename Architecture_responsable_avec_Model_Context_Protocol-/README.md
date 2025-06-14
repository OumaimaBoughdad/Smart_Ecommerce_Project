# Responsible Architecture with Model Context Protocol

This repository implements a responsible AI architecture using the Model Context Protocol (MCP) for e-commerce product analysis.

## What is Model Context Protocol?

Model Context Protocol (MCP) is an open protocol that standardizes how applications provide context to LLMs. It enables communication between systems and locally running MCP servers that provide additional tools and resources to extend AI capabilities.

## Features

- Audit logging of all AI interactions
- Permission management for AI capabilities
- Context-aware AI responses
- Responsible data handling

## Usage

### Prerequisites

- Python 3.9+
- Required packages in requirements.txt

### Installation

```bash
pip install -r requirements.txt
```

### Running the MCP Server

```bash
python run_mcp.py
```

### Configuration

Edit `mcp_permissions.json` to configure access permissions:

```json
{
  "data_access": {
    "product_data": true,
    "user_data": false
  },
  "capabilities": {
    "product_analysis": true,
    "recommendation": true,
    "user_profiling": false
  }
}
```

## Audit Logging

All interactions are logged in `mcp_audit.log` and stored in `mcp_audit.db` for compliance and transparency.

## Integration with E-commerce ML System

This MCP implementation connects with the Top-K product selection system to provide:
- Ethical product recommendations
- Transparent decision explanations
- Audit trails for all AI decisions

## Deployment

To deploy the MCP server with the ML model:

1. Build and push the Docker image:
```bash
docker build -t oumaimaboughdad/ecommerce_mcp:latest .
docker push oumaimaboughdad/ecommerce_mcp:latest
```

2. Deploy to Kubernetes:
```bash
kubectl apply -f ../k8s/mcp-deployment.yaml
```