from typing import Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from backend.app.functions.cities.cities import get_cities
from backend.app.functions.routes.routes import find_routes_async, initialize

app = FastAPI(root_path='/api')

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    await initialize('./app/data/database.db')


@app.get("/routes/cheapest/")
async def routes_cheapest(
        from_city: str,
        to_city: str,
        max_price: Optional[float] = None,
        min_comfort: Optional[float] = None,
        top_n: Optional[int] = 3
):
    try:
        routes = await find_routes_async(
            start_city=from_city,
            end_city=to_city,
            criterion='cost',
            max_cost=max_price,
            min_comfort=min_comfort,
            top_n=top_n
        )
        return routes
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/routes/comfort/")
async def routes_comfort(
        from_city: str,
        to_city: str,
        max_price: Optional[float] = None,
        min_comfort: Optional[float] = None,
        top_n: Optional[int] = 3
):
    try:
        routes = await find_routes_async(
            start_city=from_city,
            end_city=to_city,
            criterion='comfort',
            max_cost=max_price,
            min_comfort=min_comfort,
            top_n=top_n
        )
        return routes
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/routes/fastest/")
async def routes_fastest(
        from_city: str,
        to_city: str,
        max_price: Optional[float] = None,
        min_comfort: Optional[float] = None,
        top_n: Optional[int] = 3
):
    try:
        routes = await find_routes_async(
            start_city=from_city,
            end_city=to_city,
            criterion='time_min',
            max_cost=max_price,
            min_comfort=min_comfort,
            top_n=top_n
        )
        return routes
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get('/cities')
def cities_get():
    return get_cities()