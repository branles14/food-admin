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

### Example Scenario

Let’s say I buy Jif Creamy Peanut Butter Pouch for the first time. I give the CLI the UPC 051500245453. Since it’s not in the products database yet, the CLI asks me to provide the product name, nutrition facts (one by one), and the amount it contains (e.g. 13oz). The program automatically converts all measurements to metric and stores them that way in the database.

Once the product info is saved, the CLI asks how many I’m adding to my inventory. I say “2,” so it adds two instances of Jif Creamy Peanut Butter Pouch to my inventory database, each with a unique UUID.

Then, next time I buy more of the same peanut butter, I just enter the same UPC. The CLI recognizes it from the products database and simply asks how many I want to add—no need to re-enter any product details

## Testing Strategy

### Unit Testing

- **Framework**: pytest
- **Coverage goal**: 90% core logic

### Integration Testing

- Simulate API calls to verify state changes
- Use fixtures for sample inventory items
