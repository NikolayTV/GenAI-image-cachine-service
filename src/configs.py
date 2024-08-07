
import sys
sys.path.append('../')
import os

llm_scenarios_config = {
    "tagging": 
        {"temperature": 0.0, "max_tokens": 60, "model": "meta-llama/llama-3.1-8b-instruct:free"}
}


models_config = {
    "meta-llama/llama-3.1-8b-instruct:free": {"base_url": "https://openrouter.ai/api/v1", "api_key": os.environ.get('OPENROUTER_API_KEY')}
}