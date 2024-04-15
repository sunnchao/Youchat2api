from flask import Flask, request, Response, g
import requests
import random
import string
import json
import uuid
import urllib.parse
import time
import os


app = Flask(__name__)

app.config['DELETE_SESSIONS'] = True  # 设置为 False 则不会删除会话

# 在程序开头设置每个cookie使用的最大对话次数
MAX_USES_PER_COOKIE = 50
current_cookie_index = 0
current_use_count = 0
cookies = []

# 获取当前工作目录
current_dir = os.getcwd()

# 立即加载 cookies
try:
    with open(os.path.join(current_dir, 'cookie.json'), 'r') as file:
        cookies = json.load(file)
except IOError:
    print("Error: File does not appear to exist.")
except json.JSONDecodeError as e:
    print("Failed to decode JSON:", e)


@app.route('/v1/chat/completions', methods=['POST'])
def chat_completions():
    global current_cookie_index, current_use_count
    data = request.get_json()
    messages = data['messages']
    model = data['model']
    ai_model = model
    stream = data.get('stream', False)

    concatenated_messages = " \n ".join([msg['content'] for msg in messages])
    total_tokens = sum([len(msg['content'].split()) for msg in messages])

    # Rotate cookie usage
    if current_use_count >= MAX_USES_PER_COOKIE:
        current_cookie_index = (current_cookie_index + 1) % len(cookies)
        current_use_count = 0

    cookie_data = cookies[current_cookie_index]
    current_use_count += 1

    cookie_string = '; '.join([f'{key}={value}' for key, value in cookie_data.items()])

    if total_tokens > 500:
        nonce = get_nonce(cookie_string)
        if nonce is None:
            return Response("Error getting nonce", status=500)
        upload_response = upload_messages(json.dumps(messages), cookie_string, nonce)
        if upload_response is None:
            return Response("Error uploading messages", status=500)
        encoded_question = urllib.parse.quote("Please answer the last question of user in this json in the correct language. The default is Chinese.")
    else:
        encoded_question = urllib.parse.quote(concatenated_messages)
    build_id = cookie_data.get('buildId', '')  # 从 cookies 中获取 buildId

    chat_id_url = f"https://you.com/_next/data/{build_id}/en-US/search.json?q={encoded_question}&fromSearchBar=true&tbm=youchat&chatMode=custom"
    chat_id_headers = {
        'accept': '*/*',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cookie': cookie_string,
        'referer': 'https://you.com/?chatMode=custom',
        'sec-ch-ua': '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
    }

    chat_id_response = requests.get(chat_id_url, headers=chat_id_headers)
    print("HTTP Status Code:", chat_id_response.status_code)
    print("Response Content:", chat_id_response.text)

    if chat_id_response.status_code == 200:
        initialTraceId = chat_id_response.json()['pageProps']['initialTraceId']
    else:
        return Response(f"Error from server: {chat_id_response.status_code}", status=chat_id_response.status_code)

    g.chat_id = initialTraceId  # Store chat ID globally for later use in after_request
    g.cookie_string = cookie_string
    g.encoded_question = encoded_question

    response_url = f"https://you.com/api/streamingSearch?q={encoded_question}&page=1&count=10&safeSearch=Moderate&mkt=ja-JP&responseFilter=WebPages,TimeZone,Computation,RelatedSearches&domain=youchat&use_personalization_extraction=true&queryTraceId={initialTraceId}&chatId={initialTraceId}&conversationTurnId={str(uuid.uuid4())}&pastChatLength=0&isSmallMediumDevice=true&selectedChatMode=custom&selectedAIModel={model}&traceId={initialTraceId}|{str(uuid.uuid4())}|2024-04-12T17:48:25.220Z&chat=%5B%5D"
    response_headers = {
        'accept': 'text/event-stream',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cache-control': 'no-cache',
        'cookie': cookie_string,
        'referer': f'https://you.com/search?q={encoded_question}&fromSearchBar=true&tbm=youchat&chatMode=custom',
        'sec-ch-ua': '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
    }

    if stream:
        return Response(generate_stream(response_url, response_headers, ai_model, g.chat_id, g.cookie_string, g.encoded_question), mimetype='text/event-stream')    
    else:
        chat_response = requests.get(response_url, headers=response_headers)
        response_data = handle_non_stream_response(chat_response, ai_model)
        return response_data
    
@app.after_request
def perform_cleanup(response):
    if 'chat_id' in g and app.config['DELETE_SESSIONS']:
        delete_chat_session(g.chat_id, g.cookie_string, g.encoded_question)  # Perform deletion after streaming
    return response


def get_nonce(cookie_string):
    url = 'https://you.com/api/get_nonce'
    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cookie': cookie_string,
        'referer': 'https://you.com/?chatMode=custom',
        'sec-ch-ua': '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.text
    else:
        print(f"Error getting nonce: {response.status_code}")
        return None

def upload_messages(messages_string, cookie_string, nonce):
    boundary = '----WebKitFormBoundary' + ''.join(random.sample(string.ascii_letters + string.digits, 16))
    url = 'https://you.com/api/upload'
    headers = {
        'accept': 'multipart/form-data',
        'accept-language': 'zh-CN,zh;q=0.9',
        'content-type': f'multipart/form-data; boundary={boundary}',
        'cookie': cookie_string,
        'origin': 'https://you.com',
        'referer': 'https://you.com/?chatMode=custom',
        'sec-ch-ua': '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
        'x-upload-nonce': nonce
    }
    data = f'--{boundary}\r\nContent-Disposition: form-data; name="file"; filename="messages.json"\r\nContent-Type: text/plain\r\n\r\n{messages_string}\r\n--{boundary}--'  # Change Content-Type to text/plain

    # Debugging information
    print("Uploading messages with the following details:")
    print(f"URL: {url}")
    print(f"Headers: {headers}")
    print(f"Data: {data[:100]}...")  # Print the first 100 characters of the data

    response = requests.post(url, headers=headers, data=data)
    if response.status_code == 200:
        print("Upload successful.")
        return response.text
    else:
        print(f"Error uploading messages: {response.status_code}")
        print(f"Response text: {response.text}")
        return None




def generate_stream(response_url, headers, ai_model, chat_id, cookie_string, encoded_question):
    chat_response = requests.get(response_url, headers=headers, stream=True)
    first_data_line = True
    try:
        for line in chat_response.iter_lines():
            if line:
                result = parse_sse_line(line)
                if result:
                    data_string = json.dumps({
                        'id': 'chatcmpl-' + str(uuid.uuid4()),
                        'object': 'chat.completion.chunk',
                        'created': int(time.time()),
                        'model': ai_model,
                        'choices': [
                            {
                                'delta': {
                                    'content': result['youChatToken']
                                },
                                'finish_reason': None
                            }
                        ]
                    })
                    if not first_data_line:
                        yield "\n"
                    yield f"data: {data_string}\n"
                    first_data_line = False
    finally:
        pass  # Deletion will be handled by after_request




def handle_non_stream_response(chat_response, ai_model):
    result = []
    for line in chat_response.iter_lines():
        if line:
            print(f"Line from server: {line}")  # Print each line from the server
            temp_result = parse_sse_line(line)
            if temp_result:
                if 'youChatToken' in temp_result:
                    result.append(temp_result['youChatToken'])
    if not result:
        result = ['']  # Return an empty string if no results
    joined_result = ''.join(result)
    response_data = {
        "id": "chatcmpl-" + str(uuid.uuid4()),
        "object": "chat.completion",
        "created": int(time.time()),
        "model": ai_model,
        "choices": [
            {
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": joined_result
                },
                "finish_reason": "stop"
            }
        ],
        "usage": {
            "prompt_tokens": 0,
            "completion_tokens": 0,
            "total_tokens": 0
        }
    }
    print(f"Response data: {response_data}")  # Print the response data
    return response_data

def delete_chat_session(chat_id, cookie_string, encoded_question):
    delete_url = 'https://you.com/api/chat/deleteChat'
    delete_headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'zh-CN,zh;q=0.9',
        'content-type': 'application/json',
        'cookie': cookie_string,
        'origin': 'https://you.com',
        'referer': f'https://you.com/search?q={encoded_question}&fromSearchBar=true&tbm=youchat&chatMode=custom&cid={chat_id}',
        'sec-ch-ua': '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
    }
    delete_data = json.dumps({"chatId": chat_id})
    delete_response = requests.delete(delete_url, headers=delete_headers, data=delete_data)
    print(f"DELETE response status: {delete_response.status_code}")
    print(f"DELETE response body: {delete_response.text}")

def parse_sse_line(line):
    line = line.decode('utf-8')
    print(f"parse_sse_line input: {line}")  # Log input for debugging
    if line.startswith("event:"):
        parse_sse_line.event_name = line.split(":", 1)[1].strip()
    elif line.startswith("data:") and parse_sse_line.event_name:
        data_str = line.split(":", 1)[1].strip()
        try:
            data = json.loads(data_str)
            print(f"parse_sse_line output: {data}")  # Log output for debugging
            return data if "youChatToken" in data else {}
        except json.JSONDecodeError:
            print("JSON decoding error: ", data_str)
            # Ignore non-JSON formatted lines instead of returning an error
            return {}

parse_sse_line.event_name = None

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=2222)