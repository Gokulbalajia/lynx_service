from fastapi import APIRouter, Depends, HTTPException
from typing import List, Type, Any, Dict
from uuid import UUID
from app.db.connection import get_supabase
from app.query.base_query import BaseQuery
from supabase import Client

def create_crud_router(table_name: str, response_model: Type[Any], name: str, tags: List[str]):
    router = APIRouter(prefix=f"/{name}", tags=tags)

    @router.get("/", response_model=List[response_model])
    def read_all(db: Client = Depends(get_supabase)):
        service = BaseQuery(db, table_name)
        return service.get_all()

    @router.get("/{id}", response_model=response_model)
    def read_one(id: UUID, db: Client = Depends(get_supabase)):
        service = BaseQuery(db, table_name)
        item = service.get_by_id(id)
        if not item:
            raise HTTPException(status_code=404, detail=f"{name.capitalize()} not found")
        return item

    @router.post("/", response_model=response_model)
    def create_one(data: Dict[str, Any], db: Client = Depends(get_supabase)):
        service = BaseQuery(db, table_name)
        return service.create(data)

    return router
