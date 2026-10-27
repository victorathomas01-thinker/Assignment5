"""FastAPI routes for the Sandwich Maker Machine assignment."""
from fastapi import Depends, FastAPI, HTTPException, Response, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from .controllers import orders, sandwiches, resources, recipes, order_details
from .dependencies.database import engine, get_db
from .models import models, schemas

# Create the five tables on first start (does not migrate existing tables).
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Sandwich Maker API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_or_404(record, label):
    if record is None:
        raise HTTPException(status_code=404, detail=f"{label} not found")
    return record


@app.post("/orders/", response_model=schemas.Order, status_code=201, tags=["Orders"])
def create_order(order: schemas.OrderCreate, db: Session = Depends(get_db)):
    return orders.create(db=db, order=order)


@app.get("/orders/", response_model=list[schemas.Order], tags=["Orders"])
def read_orders(db: Session = Depends(get_db)):
    return orders.read_all(db)


@app.get("/orders/{order_id}", response_model=schemas.Order, tags=["Orders"])
def read_one_order(order_id: int, db: Session = Depends(get_db)):
    return get_or_404(orders.read_one(db, order_id), "Order")


@app.put("/orders/{order_id}", response_model=schemas.Order, tags=["Orders"])
def update_one_order(order_id: int, order: schemas.OrderUpdate, db: Session = Depends(get_db)):
    get_or_404(orders.read_one(db, order_id), "Order")
    return orders.update(db=db, order_id=order_id, order=order)


@app.delete("/orders/{order_id}", status_code=204, tags=["Orders"])
def delete_one_order(order_id: int, db: Session = Depends(get_db)):
    get_or_404(orders.read_one(db, order_id), "Order")
    orders.delete(db=db, order_id=order_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.post("/sandwiches/", response_model=schemas.Sandwich, status_code=201, tags=["Sandwiches"])
def create_sandwich(sandwich: schemas.SandwichCreate, db: Session = Depends(get_db)):
    return sandwiches.create(db=db, sandwich=sandwich)


@app.get("/sandwiches/", response_model=list[schemas.Sandwich], tags=["Sandwiches"])
def read_sandwiches(db: Session = Depends(get_db)):
    return sandwiches.read_all(db)


@app.get("/sandwiches/{sandwich_id}", response_model=schemas.Sandwich, tags=["Sandwiches"])
def read_one_sandwich(sandwich_id: int, db: Session = Depends(get_db)):
    return get_or_404(sandwiches.read_one(db, sandwich_id), "Sandwiches record")


@app.put("/sandwiches/{sandwich_id}", response_model=schemas.Sandwich, tags=["Sandwiches"])
def update_one_sandwich(sandwich_id: int, sandwich: schemas.SandwichUpdate, db: Session = Depends(get_db)):
    get_or_404(sandwiches.read_one(db, sandwich_id), "Sandwiches record")
    return sandwiches.update(db=db, sandwich_id=sandwich_id, sandwich=sandwich)


@app.delete("/sandwiches/{sandwich_id}", status_code=204, tags=["Sandwiches"])
def delete_one_sandwich(sandwich_id: int, db: Session = Depends(get_db)):
    get_or_404(sandwiches.read_one(db, sandwich_id), "Sandwiches record")
    sandwiches.delete(db=db, sandwich_id=sandwich_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.post("/resources/", response_model=schemas.Resource, status_code=201, tags=["Resources"])
def create_resource(resource: schemas.ResourceCreate, db: Session = Depends(get_db)):
    return resources.create(db=db, resource=resource)


@app.get("/resources/", response_model=list[schemas.Resource], tags=["Resources"])
def read_resources(db: Session = Depends(get_db)):
    return resources.read_all(db)


@app.get("/resources/{resource_id}", response_model=schemas.Resource, tags=["Resources"])
def read_one_resource(resource_id: int, db: Session = Depends(get_db)):
    return get_or_404(resources.read_one(db, resource_id), "Resources record")


@app.put("/resources/{resource_id}", response_model=schemas.Resource, tags=["Resources"])
def update_one_resource(resource_id: int, resource: schemas.ResourceUpdate, db: Session = Depends(get_db)):
    get_or_404(resources.read_one(db, resource_id), "Resources record")
    return resources.update(db=db, resource_id=resource_id, resource=resource)


@app.delete("/resources/{resource_id}", status_code=204, tags=["Resources"])
def delete_one_resource(resource_id: int, db: Session = Depends(get_db)):
    get_or_404(resources.read_one(db, resource_id), "Resources record")
    resources.delete(db=db, resource_id=resource_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.post("/recipes/", response_model=schemas.Recipe, status_code=201, tags=["Recipes"])
def create_recipe(recipe: schemas.RecipeCreate, db: Session = Depends(get_db)):
    return recipes.create(db=db, recipe=recipe)


@app.get("/recipes/", response_model=list[schemas.Recipe], tags=["Recipes"])
def read_recipes(db: Session = Depends(get_db)):
    return recipes.read_all(db)


@app.get("/recipes/{recipe_id}", response_model=schemas.Recipe, tags=["Recipes"])
def read_one_recipe(recipe_id: int, db: Session = Depends(get_db)):
    return get_or_404(recipes.read_one(db, recipe_id), "Recipes record")


@app.put("/recipes/{recipe_id}", response_model=schemas.Recipe, tags=["Recipes"])
def update_one_recipe(recipe_id: int, recipe: schemas.RecipeUpdate, db: Session = Depends(get_db)):
    get_or_404(recipes.read_one(db, recipe_id), "Recipes record")
    return recipes.update(db=db, recipe_id=recipe_id, recipe=recipe)


@app.delete("/recipes/{recipe_id}", status_code=204, tags=["Recipes"])
def delete_one_recipe(recipe_id: int, db: Session = Depends(get_db)):
    get_or_404(recipes.read_one(db, recipe_id), "Recipes record")
    recipes.delete(db=db, recipe_id=recipe_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.post("/order_details/", response_model=schemas.OrderDetail, status_code=201, tags=["Order Details"])
def create_order_detail(order_detail: schemas.OrderDetailCreate, db: Session = Depends(get_db)):
    return order_details.create(db=db, order_detail=order_detail)


@app.get("/order_details/", response_model=list[schemas.OrderDetail], tags=["Order Details"])
def read_order_details(db: Session = Depends(get_db)):
    return order_details.read_all(db)


@app.get("/order_details/{order_detail_id}", response_model=schemas.OrderDetail, tags=["Order Details"])
def read_one_order_detail(order_detail_id: int, db: Session = Depends(get_db)):
    return get_or_404(order_details.read_one(db, order_detail_id), "Order Details record")


@app.put("/order_details/{order_detail_id}", response_model=schemas.OrderDetail, tags=["Order Details"])
def update_one_order_detail(order_detail_id: int, order_detail: schemas.OrderDetailUpdate, db: Session = Depends(get_db)):
    get_or_404(order_details.read_one(db, order_detail_id), "Order Details record")
    return order_details.update(db=db, order_detail_id=order_detail_id, order_detail=order_detail)


@app.delete("/order_details/{order_detail_id}", status_code=204, tags=["Order Details"])
def delete_one_order_detail(order_detail_id: int, db: Session = Depends(get_db)):
    get_or_404(order_details.read_one(db, order_detail_id), "Order Details record")
    order_details.delete(db=db, order_detail_id=order_detail_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
