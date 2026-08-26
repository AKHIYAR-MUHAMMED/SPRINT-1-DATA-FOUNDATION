"""
Export OpenAPI Specification and Postman Collection v2.1 for FastAPI Server.
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from fastapi.testclient import TestClient
from src.api.main import app

docs_dir = Path("docs")
docs_dir.mkdir(parents=True, exist_ok=True)

# 1. Export OpenAPI JSON
openapi_schema = app.openapi()
openapi_path = docs_dir / "openapi.json"
with open(openapi_path, "w", encoding="utf-8") as f:
    json.dump(openapi_schema, f, indent=2)
print(f"Exported OpenAPI spec to {openapi_path}")

# 2. Build and export Postman Collection v2.1
postman_items = []
for path, methods in openapi_schema.get("paths", {}).items():
    for method, spec in methods.items():
        summary = spec.get("summary", path)
        postman_items.append(
            {
                "name": summary,
                "request": {
                    "method": method.upper(),
                    "header": [],
                    "url": {
                        "raw": f"http://127.0.0.1:8000{path}",
                        "protocol": "http",
                        "host": ["127", "0", "0", "1"],
                        "port": "8000",
                        "path": [p for p in path.split("/") if p],
                    },
                    "description": spec.get("description", ""),
                },
                "response": [],
            }
        )

postman_collection = {
    "info": {
        "name": "N100 Financial Intelligence REST API",
        "description": "Postman Collection for all 16 endpoints of N100 REST API",
        "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json",
    },
    "item": postman_items,
}

postman_path = docs_dir / "postman_collection.json"
with open(postman_path, "w", encoding="utf-8") as f:
    json.dump(postman_collection, f, indent=2)
print(f"Exported Postman collection to {postman_path}")

# 3. Quick test client validation
client = TestClient(app)
res = client.get("/api/v1/health")
print("Health Check HTTP status:", res.status_code)
print("Health payload:", res.json())
