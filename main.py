from fastapi import FastAPI, HTTPException, Query
from typing import List

from models import Car, CarCreate, CarUpdate

app = FastAPI(
    title="Car API",
    description="A simple API for listing, searching and managing cars.",
    version="1.0.0",
)

# In-memory store (replace with a database in production)

def _make_demo_cars() -> List[Car]:
    """Generate a pre-populated list of cars for demo purposes."""

    demo_data = [
        ("Ford", "Mustang", 2023, "Ford", "Blue"),
        ("Toyota", "Camry", 2022, "Toyota", "White"),
        ("Tesla", "Model 3", 2024, "Tesla", "Red"),
        ("Honda", "Civic", 2021, "Honda", "Black"),
        ("Chevrolet", "Camaro", 2022, "Chevrolet", "Yellow"),
        ("BMW", "3 Series", 2023, "BMW", "Gray"),
        ("Audi", "A4", 2023, "Audi", "White"),
        ("Mercedes-Benz", "C-Class", 2022, "Mercedes-Benz", "Silver"),
        ("Volkswagen", "Golf", 2021, "Volkswagen", "Blue"),
        ("Subaru", "Outback", 2024, "Subaru", "Green"),
        ("Nissan", "Altima", 2022, "Nissan", "Red"),
        ("Hyundai", "Elantra", 2023, "Hyundai", "White"),
        ("Kia", "Sorento", 2024, "Kia", "Black"),
        ("Mazda", "CX-5", 2023, "Mazda", "Blue"),
        ("Lexus", "ES", 2022, "Lexus", "Gray"),
        ("Porsche", "911", 2024, "Porsche", "Red"),
        ("Tesla", "Model Y", 2023, "Tesla", "White"),
        ("Ford", "F-150", 2024, "Ford", "Black"),
        ("Chevrolet", "Silverado", 2023, "Chevrolet", "Blue"),
        ("Toyota", "RAV4", 2024, "Toyota", "Silver"),
        ("Honda", "Accord", 2023, "Honda", "White"),
        ("BMW", "X5", 2022, "BMW", "Black"),
        ("Audi", "Q5", 2023, "Audi", "Blue"),
        ("Mercedes-Benz", "GLE", 2024, "Mercedes-Benz", "Silver"),
        ("Volkswagen", "Tiguan", 2022, "Volkswagen", "Gray"),
        ("Subaru", "Forester", 2023, "Subaru", "Green"),
        ("Nissan", "Rogue", 2024, "Nissan", "White"),
        ("Hyundai", "Santa Fe", 2023, "Hyundai", "Red"),
        ("Kia", "Telluride", 2022, "Kia", "Black"),
        ("Mazda", "Mazda3", 2023, "Mazda", "Blue"),
    ]

    return [
        Car(id=i + 1, make=make, model=model, year=year, brand=brand, color=color)
        for i, (make, model, year, brand, color) in enumerate(demo_data)
    ]


_cars: List[Car] = _make_demo_cars()
_next_id = len(_cars) + 1


def _get_next_id() -> int:
    global _next_id
    current = _next_id
    _next_id += 1
    return current


@app.get("/cars", response_model=List[Car])
def list_cars():
    """List all cars."""
    return _cars


@app.get("/cars/search", response_model=List[Car])
def search_cars(query: str = Query(..., description="Search term (make/model/year)")):
    """Search cars by make/model/year."""
    q = query.strip().lower()
    results = [
        car
        for car in _cars
        if q in car.make.lower() or q in car.model.lower() or q in str(car.year)
    ]
    return results


@app.get("/cars/brand/{brand}", response_model=List[Car])
def search_cars_by_brand(brand: str):
    """Search cars by brand."""
    b = brand.strip().lower()
    return [car for car in _cars if car.brand.lower() == b]


@app.get("/cars/{car_id}", response_model=Car)
def get_car(car_id: int):
    """Get a single car by ID."""
    for car in _cars:
        if car.id == car_id:
            return car
    raise HTTPException(status_code=404, detail="Car not found")


@app.post("/cars", response_model=Car, status_code=201)
def create_car(car_in: CarCreate):
    """Create a new car."""
    car = Car(id=_get_next_id(), **car_in.dict())
    _cars.append(car)
    return car


@app.post("/cars/reset", response_model=List[Car], summary="Reset demo dataset")
def reset_demo_data():
    """Reset the in-memory car list back to the seeded demo data."""
    global _cars, _next_id
    _cars = _make_demo_cars()
    _next_id = len(_cars) + 1
    return _cars


@app.put("/cars/{car_id}", response_model=Car)
def update_car(car_id: int, car_in: CarUpdate):
    """Update an existing car."""
    for idx, car in enumerate(_cars):
        if car.id == car_id:
            updated = car.copy(update=car_in.dict(exclude_unset=True))
            _cars[idx] = updated
            return updated
    raise HTTPException(status_code=404, detail="Car not found")


@app.delete("/cars/{car_id}", status_code=204)
def delete_car(car_id: int):
    """Delete a car."""
    for idx, car in enumerate(_cars):
        if car.id == car_id:
            del _cars[idx]
            return
    raise HTTPException(status_code=404, detail="Car not found")
