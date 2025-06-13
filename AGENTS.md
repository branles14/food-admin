
---
name: "food-admin"
description: "A Unix-style food inventory management service for Debian-based Linux systems, built in Python. Exposes a CLI utility and AI-compatible API for use in intelligent meal planning, grocery guidance, and macro tracking."
category: "AI Data Services"
author: "Suki"
authorUrl: "https://github.com/branles14"
tags: ["food", "inventory", "cli", "ai", "nutrition"] lastUpdated: "2025-06-12"
---

# food-admin

## Project Overview

food-admin is a backend service that provides precise food inventory tracking for use by AI agents and automation tools. Its goal is to offload cognitive strain around meal planning, macro tracking, and grocery shopping by maintaining an up-to-date, queryable state of all food items—raw ingredients, cooked meals, partially used containers, and more.

It is not a meal planner itself, but a foundational component designed to integrate into an ecosystem of agents (e.g. GPT-based planners, fitness trackers, grocery bots). It supports diverse input types, precise quantities, expiration dates, locations, and usage metadata. This project is intended for personal use but is released under MIT for public use.

## Tech Stack

- **Frontend**: None (CLI and API only)
- **Backend**: Python 3, FastAPI
- **Database**: SQLite (local), with option to expand to PostgreSQL
- **Deployment**: VPS or Raspberry Pi
- **Other Tools**: Git, Cron (optional), systemd

## Project Structure

```
food-admin/
├── src/
│   ├── cli/
│   ├── api/
│   ├── db/
│   ├── models/
│   └── utils/
├── tests/
├── docs/
├── scripts/
├── backup/
├── requirements.txt
└── README.md
```

## Development Guidelines

### Code Style

- Use black for consistent formatting
- Follow Python best practices (PEP8)
- Favor explicit over implicit logic

### Naming Conventions

- **File naming**: kebab-case for scripts, snake_case for modules
- **Variable naming**: snake_case
- **Function naming**: snake_case
- **Class naming**: PascalCase

### Git Workflow

- **Branch naming**: feature/, fix/, refactor/
- **Commits**: semantic and descriptive (feat: add UPC scanner)
- **Pull Requests**: required for all non-local changes

## Environment Setup

### Development Requirements

- Python 3.10+
- pip (or pipx)
- SQLite (optional PostgreSQL)

### Installation Steps

```bash
# 1. Clone the project
git clone https://github.com/branles14/food-admin

# 2. Setup virtual environment
python3 -m venv .venv && source .venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt
```

## Core Feature Implementation

### Inventory Tracking

- CLI commands to add, update, and delete items
- Support for quantities, expiration, location, tags, and container weights

```
# Example
inventory.add(
    name="Peanut Butter",
    quantity=400,
    unit="g",
    container_weight=100,
    upc="123456789012",
    tags=["tube", "protein"]
)
```

### API for AI Function Calling

- Exposes REST endpoints for querying and updating inventory
- Supports integration with ChatGPT-style agents
- Example: GET /inventory?available=true&macro_focus=protein

## Testing Strategy

### Unit Testing

- **Framework**: pytest
- **Coverage goal**: 90% core logic
- Test files organized by feature in /tests

### Integration Testing

- Simulate API calls to verify state changes
- Use fixtures for sample inventory items

### End-to-End Testing

- Cron-triggered scenarios for reminder testing
- (Future) Simulated GPT interaction scenarios


## Deployment Guide

### Build Process

```bash
# Local run for development
python -m src.cli.main
```

### Deployment Steps

1. Clone repo to server (Pi or VPS)
2. Configure virtualenv and dependencies
3. Run as a systemd service or via tmux
4. Enable daily cron for backup/export

### Environment Variables

```env
DATA_DIR=/home/user/food-admin/data
DATABASE_URL=sqlite:///data/inventory.db
BACKUP_DIR=/home/user/food-admin/backups
```

## Performance Optimization

### Backend Optimization

- Use indexed columns for frequent queries (e.g. expiration_date, tags)
- Optimize container handling for bulk goods
- Async endpoints via FastAPI

## Security Considerations

- Minimal surface area (CLI and local API only)
- Input validation and schema enforcement
- OAuth token support for webhooks or GPT integration

## Monitoring and Logging

- logging module with rotating logs
- Optional integration with Prometheus or other local tooling
- Export usage stats for agent analysis

---

This project is a foundational building block for AI-powered meal planning and personal assistant systems.

---