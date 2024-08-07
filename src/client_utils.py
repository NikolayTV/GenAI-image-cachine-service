import requests, os

def is_running_in_kubernetes():
    in_kubernetes_env = 'KUBERNETES_SERVICE_HOST' in os.environ
    in_kubernetes_fs = os.path.exists('/var/run/secrets/kubernetes.io/serviceaccount')
    return in_kubernetes_env or in_kubernetes_fs

def is_running_in_docker():
    return os.path.exists('/.dockerenv')

async def query_cached_image(avatar, user_id, diffusion_prompt, tags={}, n_results=1):
    """Запрашивает закэшированную картинку"""
    
    
    if is_running_in_docker() or is_running_in_kubernetes():
        host = 'localhost'
    else:
        host = 'imagecache'
        
    url = f"http://{host}:8017/get_image_candidate/"
    headers = {"accept": "application/json", "Content-Type": "application/json"}
    payload = {
        "diffusion_prompt": diffusion_prompt,
        "persona": avatar,
        "user_id": user_id,
        "tags": tags,
        "n_results": n_results
    }

    response = requests.post(url, headers=headers, json=payload)

    print(response.status_code)
