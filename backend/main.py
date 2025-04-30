from typing import Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(root_path='/api')

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

db_path = './app/data/database.db'

from backend.app.functions.routes.routes import (
    initialize,
    find_routes as base_find_routes,
    reload_graph
)

initialize(db_path)

def find_cheapest_routes(from_city: str, to_city: str,
                        max_cost: Optional[float] = None,
                        min_comfort: Optional[float] = None,
                        top_n: int = 3) -> list:
    """Адаптер для поиска самых дешевых маршрутов"""
    return base_find_routes(
        start_city=from_city,
        end_city=to_city,
        criterion='cost',
        max_cost=max_cost,
        min_comfort=min_comfort,
        top_n=top_n
    )

def find_most_comfortable_routes(from_city: str, to_city: str,
                                max_cost: Optional[float] = None,
                                min_comfort: Optional[float] = None,
                                top_n: int = 3) -> list:
    """Адаптер для поиска самых комфортных маршрутов"""
    return base_find_routes(
        start_city=from_city,
        end_city=to_city,
        criterion='comfort',
        max_cost=max_cost,
        min_comfort=min_comfort,
        top_n=top_n
    )

def find_fastest_routes(from_city: str, to_city: str,
                       max_cost: Optional[float] = None,
                       min_comfort: Optional[float] = None,
                       top_n: int = 3) -> list:
    """Адаптер для поиска самых быстрых маршрутов"""
    return base_find_routes(
        start_city=from_city,
        end_city=to_city,
        criterion='time_min',
        max_cost=max_cost,
        min_comfort=min_comfort,
        top_n=top_n
    )

# Ваши изначальные ручки (без изменений)
@app.get("/routes/cheapest/")
def routes_cheapest(
        from_city: str,
        to_city: str,
        max_cost: Optional[float] = None,
        min_comfort: Optional[float] = None,
        top_n: Optional[int] = 3
):
    print(from_city, to_city, top_n)
    routes = find_cheapest_routes(from_city, to_city,
                                 min_comfort=min_comfort,
                                 max_cost=max_cost,
                                 top_n=top_n)
    print(routes)
    return routes

@app.get("/routes/comfort/")
def routes_comfort(
        from_city: str,
        to_city: str,
        max_cost: Optional[float] = None,
        min_comfort: Optional[float] = None,
        top_n: Optional[int] = 3
):
    routes = find_most_comfortable_routes(from_city, to_city,
                                        min_comfort=min_comfort,
                                        max_cost=max_cost,
                                        top_n=top_n)
    print(routes)
    return routes

@app.get("/routes/fastest/")
def routes_fastest(
        from_city: str,
        to_city: str,
        max_cost: Optional[float] = None,
        min_comfort: Optional[float] = None,
        top_n: Optional[int] = 3
):
    routes = find_fastest_routes(from_city, to_city,
                               min_comfort=min_comfort,
                               max_cost=max_cost,
                               top_n=top_n)
    print(routes)
    return routes

# Функция для получения городов (нужно реализовать аналогично)
from backend.app.functions.cities.cities import get_cities

@app.get("/cities/")
def cities_get():
    cities = get_cities()
    return cities
