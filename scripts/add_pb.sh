#!/bin/bash

curl -X POST http://localhost:3000/inventory \
    -H 'Content-Type: application/json' \
    -d '{"upc": "051500245453"}