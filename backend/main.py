from typing import Optional

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.functions.cities.cities import get_cities
from backend.app.functions.routes.routes import find_cheapest_routes

app = FastAPI(
    root_path='/api'
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

path_db = './data.db'

@app.get("/routes/cheapest/")
def routes_cheapest(
        from_city: str,
        to_city: str,
        top_n: Optional[int] = 5
):
    routes = find_cheapest_routes(from_city, to_city, top_n)
    return routes

@app.get("/routes/comfort/")
def routes_comfort(
        from_city: str,
        to_city: str,
        top_n: Optional[int] = 5
):
    routes = find_cheapest_routes(from_city, to_city, top_n)
    return routes

@app.get("/routes/fastest")
def routes_fastest(
        from_city: str,
        to_city: str,
        top_n: Optional[int] = 5
):
    routes = find_cheapest_routes(from_city, to_city, top_n)
    return routes

@app.get("/cities/")
def cities():
    cities = get_cities()
    return cities