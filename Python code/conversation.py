import json
import openai
import os
import pyttsx3


# OpenAI API 액세스 키 설정

script_dir = os.path.dirname(os.path.abspath(__file__))
api = os.path.join(script_dir, '../apiKey.json')

with open(api) as f:
    data = json.load(f)

gptapi = data['gptapi']

api_key = gptapi
openai.api_key = api_key

script_dir = os.path.dirname(os.path.abspath(__file__))
conversation_file = os.path.join(script_dir, '../conversation.txt')

script_dir = os.path.dirname(os.path.abspath(__file__))
persona_file = os.path.join(script_dir, '../persona.txt')

def load_persona():
    try:
        with open(persona_file, 'r', encoding='utf-8') as f:
            persona_data = f.read().splitlines()
    except FileNotFoundError:
        # 파일이 없는 경우 빈 리스트 반환
        persona_data = []
    return persona_data

persona = load_persona()

def start_conversation(prompt):
    """
    대화를 시작하는 함수. 주어진 프롬프트를 사용하여 대화의 첫 번째 메시지를 생성합니다.
    
    :param prompt: 대화 시작 프롬프트
    :return: OpenAI 응답 내용
    """
    conversation_history = load_conversation_history()  # 기존 대화 기록 불러오기
    prompt_with_history = combine_prompt(prompt, conversation_history)  # 대화 기록과 함께 프롬프트 생성
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0125",
        messages=[
            {"role": "system", "content": prompt_with_history},  # 시스템 역할로 프롬프트 제공
            {"role": "user", "content": "안녕? 너는 누구니?"}  # 사용자 역할로 첫 질문 제공
        ]
    )
    return response.choices[0].message['content']  # 응답 내용 반환
    
def generate_response(user_message):
    # 파일에서 대화 기록 불러오기
    conversation_history = load_conversation_history()
    # 사용자의 메시지를 포함한 프롬프트를 생성하여 OpenAI API에 전달하고, 챗봇의 응답을 반환합니다.
    prompt_with_history = combine_prompt(user_message, conversation_history)
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0125",
        messages=[
            {"role": "system", "content": prompt_with_history},
            {"role": "user", "content": user_message}
        ]
    )
    print(prompt_with_history)
    print(f"user: {user_message}")
    # 대화 기록에 사용자의 메시지와 챗봇의 응답 추가
    add_to_conversation_history(conversation_history, user_message, response.choices[0].message['content'])
    return response.choices[0].message['content']

def load_conversation_history():
    try:
        with open(conversation_file, 'r', encoding='utf-8') as f:
            conversation_history = f.read().splitlines()
    except FileNotFoundError:
        # 파일이 없는 경우 빈 리스트 반환
        conversation_history = []
    return conversation_history


def add_to_conversation_history(conversation_history, user_message, bot_response):
    with open(conversation_file, 'a', encoding='utf-8') as f:
        f.write(f"user: {user_message}\nbot: {bot_response}\n")

def combine_prompt(prompt, conversation_history):
    # 이전 대화 내용을 프롬프트에 추가하여 새로운 프롬프트 생성
    prompt_with_history = prompt
    if conversation_history:
        for line in conversation_history:
            prompt_with_history += f"\n{line}"
    persona_string = '\n'.join(persona)
    prompt_with_history = persona_string + '\n'
    return prompt_with_history


def text_to_speech(text):
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)  # 음성 속도 조절 (기본값은 200)
    engine.say(text)
    engine.runAndWait()