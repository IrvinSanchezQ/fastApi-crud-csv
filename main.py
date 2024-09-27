from fastapi import FastAPI, HTTPException,UploadFile, File
from models import Item
import os
import pandas as pd
from typing import List
from io import StringIO 


# Nombre del archivo CSV con una carpeta específica
CSV_FILE_Dir = "data/items.csv"
# ubicacion de archivo 
CSV_FILE = pd.read_csv("C:/Users/INGIR/python_apis/items.csv")

# Crear la carpeta 'data' si no existe
os.makedirs(os.path.dirname(CSV_FILE_Dir), exist_ok=True)
app = FastAPI()

# Base de datos simulada
items_db = []
df_test = CSV_FILE.values.tolist()
df = CSV_FILE

print('test :', df_test)
print('test2 :', items_db)
items: List[Item] = [Item(**row) for row in df.to_dict(orient="records")]

#para obtener todos los items
@app.get("/items/", response_model=list[Item])
def obtener_todos_items():

    # items: List[Item] = [Item(**row) for row in df.to_dict(orient="records")]
    print (items,"items de csv")
    print (items_db,"items de objeto local")
    return items

# Crear un nuevo ítem 
@app.post("/items/", response_model=Item)
def crear_item(item: Item):
    # items: List[Item] = [Item(**row) for row in df.to_dict(orient="records")]
    # Comprobar si ya existe un ítem con el mismo ID
    for db_item in items:
        if db_item.id == item.id:
            raise HTTPException(status_code=400, detail="ID ya existe")
    
    items.append(item)
    print('Full object: ',items)
    items_dicts = [item.model_dump() for item in items]
    df_temp = pd.DataFrame(items_dicts)
    df_temp.to_csv("items.csv", index=False)
    print('Full object to export: ',df_temp)
    return item

# Obtener un ítem por su ID 
@app.get("/items/{item_id}", response_model=Item)
def obtener_item(item_id: int):
    for item in items:
        if item.id == item_id:
            return item
    raise HTTPException(status_code=404, detail="Item no encontrado")

# Eliminar un ítem
@app.delete("/items/{item_id}")
def eliminar_item(item_id: int):
    for index, item in enumerate(items):
        if item.id == item_id:
            del items[index]
            items_dicts = [item.model_dump() for item in items]
            df_temp = pd.DataFrame(items_dicts)
            df_temp.to_csv("items.csv", index=False)
            return {"message": "Item eliminado correctamente"}
    raise HTTPException(status_code=404, detail="Item no encontrado")

# Actualizar un ítem
@app.put("/items/{item_id}", response_model=Item)
def actualizar_item(item_id: int, item_actualizado: Item):
    for index, item in enumerate(items):
        if item.id == item_id:
            items[index] = item_actualizado
            items_dicts = [item.model_dump() for item in items]
            df_temp = pd.DataFrame(items_dicts)
            df_temp.to_csv("items.csv", index=False)

            return item_actualizado
    raise HTTPException(status_code=404, detail="Item no encontrado")