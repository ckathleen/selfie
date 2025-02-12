from typing import Optional, Any, List, Dict

from fastapi import APIRouter, HTTPException
from playhouse.shortcuts import model_to_dict
from pydantic import BaseModel

from selfie.database import DataManager

router = APIRouter()


class DataLoaderRequest(BaseModel):
    name: Optional[str]
    loader_module: str
    constructor_args: Optional[List[Any]] = []
    constructor_kwargs: Optional[Dict[str, Any]] = {}
    load_data_args: Optional[List[Any]] = []
    load_data_kwargs: Optional[Dict[str, Any]] = {}


@router.get("/data-sources")
async def get_data_sources():
    return DataManager().get_data_sources()


@router.post("/data-sources")
async def add_data_source(request: DataLoaderRequest):
    return model_to_dict(DataManager().add_data_source(
        request.name,
        request.loader_module,
        request.constructor_args,
        request.constructor_kwargs,
        request.load_data_args,
        request.load_data_kwargs,
    ))


@router.delete("/data-sources/{source_id}")
async def delete_data_source(source_id: int, delete_documents: bool = True, delete_indexed_data: bool = True):
    await DataManager().remove_data_source(source_id, delete_documents, delete_indexed_data)
    return {"message": "Data source removed successfully"}


@router.post("/data-sources/{source_id}/scan")
async def scan_data_sources(source_id: int):
    return DataManager().scan_data_sources([source_id])


@router.post("/data-sources/{source_id}/index")
async def index_data_source(source_id: int):
    manager = DataManager()
    data_source = manager.get_data_source(source_id)
    if isinstance(data_source, dict) and "error" in data_source:
        raise HTTPException(status_code=404, detail=data_source["error"])
    return await manager.index_documents(data_source)
