# Car API (Python)

A simple RESTful API for managing a collection of cars.

## Features

- List all cars
- Search cars (by query or by brand)
- Retrieve a car by ID
- Create, update, and delete cars

## Getting Started

### Requirements

- Python 3.10+

### Install dependencies

```sh
python -m pip install -r requirements.txt
```

### Run the API

```sh
uvicorn main:app --reload
```

The API will be available at `http://127.0.0.1:8000`.

## Deployment to Azure Container Instances

This app can be deployed as a container to Azure Container Instances.

### Prerequisites

- Azure CLI installed and logged in (`az login`)
- Docker (optional, for local testing)

### Steps

1. **Build the Docker image locally (optional)**:
   ```sh
   docker build -t carapi .
   docker run -p 8000:8000 carapi
   ```

2. **Deploy to Azure**:
   - Run the deployment script: `.\deploy-to-azure.ps1`
   - Or follow the manual steps in the script.

3. **Access the API**:
   - The script will output the public URL (e.g., `https://carapi-demo.eastus.azurecontainer.io`)
   - Append `/docs` for the interactive API documentation.

### Endpoints

> ✅ The API starts with a pre-populated in-memory list of demo cars. No database is required.

- `GET /cars` — list all cars
- `GET /cars/search?query=<term>` — search cars by make/model/year
- `GET /cars/brand/{brand}` — list cars by brand
- `GET /cars/{car_id}` — get car by ID
- `POST /cars` — create a new car
- `POST /cars/reset` — reset the list back to the seeded demo dataset
- `PUT /cars/{car_id}` — update a car
- `DELETE /cars/{car_id}` — delete a car

### Example Requests

```sh
# List all cars
curl http://127.0.0.1:8000/cars

# Search cars
curl "http://127.0.0.1:8000/cars/search?query=mustang"

# Search by brand
curl http://127.0.0.1:8000/cars/brand/Toyota

# Create a new car
curl -X POST http://127.0.0.1:8000/cars -H "Content-Type: application/json" -d '{"make":"Ford","model":"Mustang","year":2023,"brand":"Ford"}'
```
