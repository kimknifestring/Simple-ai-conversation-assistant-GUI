import re

def extract_content_and_emotion(text):
    pattern = r"(.*)\{([^}]*)\}"
    match = re.match(pattern, text)
    
    if match:
        content = match.group(1).strip()  # 답변내용 추출 및 좌우 공백 제거
        emotion = match.group(2).strip()  # 감정 추출 및 좌우 공백 제거
        return content, emotion
    else:
        return None, None

# 테스트
text = "답변내용 dda{감정}"
content, emotion = extract_content_and_emotion(text)
if content is not None and emotion is not None:
    print("답변내용:", content)
    print("감정:", emotion)
else:
    print("답변내용 또는 감정을 찾을 수 없습니다.")
