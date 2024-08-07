import os
import json
import time
from glob import glob
from dotenv import load_dotenv
from textwrap import dedent

import openai
import runpod


dotenv_path = os.path.join(os.path.dirname(__file__), '../', '.env')
load_dotenv()

def get_embedding(text):
    openai_client = openai.OpenAI(
        api_key=os.getenv('RUNPOD_API_KEY'), 
        base_url="https://api.runpod.ai/v2/xoktw5d8vlp238/openai/v1",
        timeout=60
    )

    resp = openai_client.embeddings.create(
        model="mixedbread-ai/mxbai-embed-large-v1",
        input=[text]
    )
    embs = [x['embedding'] for x in resp.to_dict()['data']]
    return embs


# API setting constants
API_MAX_RETRY = 2
API_RETRY_SLEEP = 2
API_ERROR_OUTPUT = "$ERROR$"


async def chat_completion_openai(messages, generation_config):
    start_time = time.time()

    model = generation_config['model']
    
    model_config = configs.models_config[model]
    client = openai.AsyncOpenAI(
        base_url=model_config['base_url'],
        api_key=model_config['api_key'],
        timeout=60
    )

    answer_text = None
    input_tokens = None
    output_tokens = None
    status = 'error'
    for _ in range(API_MAX_RETRY):
        try:
            completion = await client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=generation_config['temperature'],
                max_tokens=generation_config['max_tokens']
            )
            if completion.choices:
                answer_text = completion.choices[0].message.content
                input_tokens = completion.usage.prompt_tokens
                output_tokens = completion.usage.completion_tokens
                status = 'success'
                break
        except openai.RateLimitError as e:
            print(type(e), e)
            time.sleep(API_RETRY_SLEEP)
        except openai.BadRequestError as e:
            print(messages)
            print(type(e), e)
        except KeyError:
            print(type(e), e)
            break

    execution_time = time.time() - start_time
    return {'answer_text': str(answer_text), "input_tokens": input_tokens, "output_tokens": output_tokens, "execution_time": execution_time, "status": status}

