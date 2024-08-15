import requests, os, json 


def is_running_in_kubernetes():
    in_kubernetes_env = 'KUBERNETES_SERVICE_HOST' in os.environ
    in_kubernetes_fs = os.path.exists('/var/run/secrets/kubernetes.io/serviceaccount')
    return in_kubernetes_env or in_kubernetes_fs

def is_running_in_docker():
    return os.path.exists('/.dockerenv')


def upsert_cached_image(persona, img_uuid, img_path, prompt, emb, tags):
    if is_running_in_docker() or is_running_in_kubernetes():
        host = 'imagecache'
    else:
        host = 'localhost'
    url = f"http://{host}:8017/upsert_cached_image/"
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json"
    }
    payload = {
        "persona": persona, 
        "img_uuid": img_uuid,
        "img_path": img_path,
        "prompt": prompt,
        "emb": emb.tolist(),
        "tags": tags if tags else {}
    }

    response = requests.post(url, headers=headers, json=payload)
    print('Added cached image', response.status_code)

async def get_cached_image(persona, prompt, tags, user_id=None, n_results=1):
    SIMILARITY_THRESHOLD = 0.4
    
    if is_running_in_docker() or is_running_in_kubernetes():
        host = 'imagecache'
    else:
        host = 'localhost'
        
    url = f"http://{host}:8017/get_image_candidate/"
    prefix = os.getcwd() + '/'
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json"
    }
    payload = {
        "prompt": str(prompt),
        "persona": str(persona),
        "user_id": str(user_id),
        "tags": tags,
        "n_results": n_results
    }

    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        
        print('Query res:', response.json())
        resp = response.json()
        if isinstance('ads', str):
            resp = json.loads(resp)
            
        if resp['distances'][0][0] < SIMILARITY_THRESHOLD:
            img_path = prefix + resp['documents'][0][0]
            img_path = img_path.replace('\\', '/')
            img_uuid = resp['metadatas'][0][0]['img_uuid']
            if user_id:
                await add_cached_record(user_id, img_uuid, img_path)
            return {'img_path': img_path}
        else:
            print("No images below threshold.")
    else:
        print('ERROR imgcache service')
        print(response.text)
    
    return {}


async def add_cached_record(user_id, img_uuid, img_path):
    if is_running_in_docker() or is_running_in_kubernetes():
        host = 'imagecache'
    else:
        host = 'localhost'
    url = f"http://{host}:8017/add_image_usage_record/"
    
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json"
    }
    payload = {
        "user_id": str(user_id),
        "img_uuid": str(img_uuid),
        "img_path": str(img_path)
    }

    response = requests.post(url, headers=headers, json=payload)
    if response.status_code:
        print("Succesflly added cached record")
    else:
        print("Failed to add cached record")
        

