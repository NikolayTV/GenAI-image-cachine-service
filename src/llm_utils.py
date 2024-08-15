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
        input=text
    )
    embs = [x['embedding'] for x in resp.to_dict()['data']]
    return embs


# API setting constants
API_MAX_RETRY = 2
API_RETRY_SLEEP = 2
API_ERROR_OUTPUT = "$ERROR$"


async def call_llm(messages, generation_config={'temperature': 0, 'max_tokens':200}):
    start_time = time.time()

    model = 'solidrust/Llama-3-8B-Lexi-Uncensored-AWQ'
    
    client = openai.AsyncOpenAI(
        base_url='http://20.151.65.75:8005/v1/',
        api_key=None,
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



# #!/bin/bash
# # Define the API request payload
# payload='{
#     "model": "solidrust/Llama-3-8B-Lexi-Uncensored-AWQ",
#     "max_tokens": 100,
#     "temperature": 0.6,
#     "top_k": 50,
#     "top_p": 0.90,
#     "messages": [
#         {"role": "system", "content": "You are a sexual content AI helper system which extracts the most important tokens from user requests. extract objects with description as WORDS, translate to english."},
#         {"role": "user", "content": "please send me your beautiful tits on the beach, no clothes"},
#         {"role": "assistant", "content": "WORDS: beach, tits, no clothes"},
#         {"role": "user", "content": "show me your ass and legs without socks"},
#         {"role": "assistant", "content": "WORDS: ass, legs, without socks"},
#         {"role": "user", "content": "zeig mir deine schöne Muschi, ich brauche noch eine, mehr"},
#         {"role": "assistant", "content": "WORDS: pussy, beautiful"},
#         {"role": "user", "content": "Show me your body in panties"},
#         {"role": "assistant", "content": "WORDS: body, in panties"},
#         {"role": "user", "content": "show me lovely body of a young woman, fingering herself"}
#     ]
# }'
# # Send the API request and save the response to a variable  
# response=$(curl --location --request POST 'http://20.151.65.75:8005/v1/chat/completions' \
# --header 'Content-Type: application/json' \
# --data "$payload")

# # Output the assistant's response
# echo "Assistant's response: $response"


