from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os, datetime, json
import uvicorn
from pydantic import BaseModel, Field
from typing import Dict, List, Optional

from mongo_db import mongodb_add_image_usage_record, mogodb_get_image_uuids_for_user
from llm_utils import get_embedding
from chroma_db import chromadb_find_image_match, chromadb_upsert_cached_image

from dotenv import load_dotenv
load_dotenv(dotenv_path='../.env')
load_dotenv(dotenv_path='.env')

app = FastAPI()


class ImageRequest(BaseModel):
    diffusion_prompt: str
    persona: str = 'angel'
    user_id: int = None
    tags: dict = {}
    n_results: int = 1

@app.post("/get_image_candidate/")
async def get_image_candidate(request: ImageRequest):
    """
    Get image data closes to provided prompt and meta-info
    """
    tags = request.tags
    user_id = request.user_id
    diffusion_prompt = request.diffusion_prompt
    n_results = request.n_results
    input_embedding = get_embedding(diffusion_prompt)[0]
    
    # Filter based on provided tags
    metadata_filter = {}
    if len(tags):
        metadata_filter.update(tags)
    
    # Filter images previously used for this user id
    if user_id:
        used_img_uuids = await mogodb_get_image_uuids_for_user(user_id)
        if len(used_img_uuids):
            metadata_filter['img_uuid'] = {"$nin": used_img_uuids}
    
    if len(metadata_filter) > 1:
        metadata_filter = {"$and": [{k: v} for k, v in metadata_filter.items()]}
        
    res = await chromadb_find_image_match(request.persona, metadata_filter, input_embedding, n_results)
    print("Get image candidate, metadata_filter:", metadata_filter)
    return json.dumps(res)


class RecordInput(BaseModel):
    user_id: int
    img_uuid: str
    img_path: str = None
    
@app.post("/add_image_usage_record/")
async def add_image_usage_record(request: RecordInput):
    """
    Add record into MongoDB to mark the image as used for user_id. Img_path is optional
    """
    await mongodb_add_image_usage_record(request.user_id, request.img_uuid, request.img_path)


class CachedImage(BaseModel):
    persona: str
    img_uuid: str
    img_path: str
    prompt: str
    emb: List[float]
    tags: Optional[Dict]
    
@app.post("/upsert_cached_image/")
async def upsert_cached_image(request: CachedImage):
    """
    Upsert (add new or update existing) record into MongoDB to mark the image as used for user_id
    """
    await chromadb_upsert_cached_image(request.persona, request.img_uuid, request.img_path, request.prompt, request.emb, request.tags)
    print("Upserted cached image: ")
    
            
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8017, 
        log_level="debug",
        reload=True,
    )