# food-admin

food-admin is a backend service that provides precise food inventory tracking for use by AI agents and automation tools. Its goal is to offload cognitive strain around meal planning, macro tracking, and grocery shopping by maintaining an up-to-date, queryable state of all food items.

It is not a meal planner itself, but a foundational component designed to integrate into an ecosystem of agents (e.g. GPT-based planners, fitness trackers, grocery bots). It supports diverse input types, precise quantities, expiration dates, locations, and usage metadata. This project is intended for personal use but is released under MIT for public use.

## Tech Stack

- **Frontend**: CLI and API only
- **Backend**: Python 3, FastAPI
- **Database**: SQLite
- **Deployment**: VPS, Raspberry Pi
- **Other Tools**: Git, systemd

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

## Core Feature Implementation

### Inventory Tracking

- CLI commands to add, update, list and delete items from the inventory
- Products database for quickly adding products to the inventory
- Support for quantities, expiration, location, tags, and empty container weights

### API for AI Function Calling

- Exposes REST endpoints for querying and updating inventory
- Supports integration with ChatGPT-style agents
- Mirrors CLI functionality

## Testing Strategy

### Unit Testing

- **Framework**: pytest
- **Coverage goal**: 90% core logic

### Integration Testing

- Simulate API calls to verify state changes
- Use fixtures for sample inventory items
