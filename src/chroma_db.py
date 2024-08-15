import chromadb
from mongo_db import is_running_in_docker

if is_running_in_docker():
    host = 'chroma-db'
else:
    host = 'localhost'
chroma_client = chromadb.HttpClient(host=host, port=8000, settings=chromadb.Settings(allow_reset=True, anonymized_telemetry=False))

async def chromadb_find_image_match(persona, metadata_filter, input_embedding, n_results):
    collection = chroma_client.get_collection(name=persona)
    res = collection.query(query_embeddings=input_embedding, n_results=n_results, where=metadata_filter)
    return res

async def chromadb_upsert_cached_image(persona, img_uuid, img_path, prompt, emb, tags):
    collection = chroma_client.get_or_create_collection(name=persona)
    metadatas = {}
    metadatas.update(tags)
    metadatas["img_uuid"] = str(img_uuid)
    metadatas["prompt"] = prompt
    
    documents = img_path
    collection.upsert(documents=documents, embeddings=emb, metadatas=metadatas, ids=img_uuid)


async def chromadb_remove_collection(collection):
    collections = chroma_client.list_collections()
    
    if collection in [x.name for x in collections]:
        chroma_client.delete_collection(collection)
        return f"{collection} removed"
    else:
        return f"{collection} not exists"
        

async def chromadb_list_collections():
    collections = chroma_client.list_collections()
    print('collections', collections)
    return [x.name for x in collections]