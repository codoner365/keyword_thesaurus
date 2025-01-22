import socket
import deepl

myApi_key = "3ed18e9a-6853-4413-ae3d-f658117e38bd:fx"

def is_internet_connected():
    """인터넷 연결 상태를 확인하는 함수"""
    try:
        # Google의 DNS 서버로 연결 확인
        socket.create_connection(("8.8.8.8", 53), timeout=3)
        return True
    except OSError:
        return False

# DeepL 텍스트 번역 함수
def translate_text(text, target_lang="EN-GB", api_key=myApi_key):
    if not is_internet_connected():
        return "인터넷에 연결되어 있지 않습니다. 번역을 실행할 수 없습니다."

    if not text.strip():  # 빈 텍스트 또는 공백만 있는 경우
        return "번역할 텍스트를 입력하세요."

    try:
        # DeepL API 객체 생성
        translator = deepl.Translator(api_key)
        
        # 텍스트 번역
        result = translator.translate_text(text, target_lang=target_lang)
        
        return result.text  # 번역된 텍스트 반환
    
    except deepl.DeepLException as e:  # DeepL API의 예외 처리
        return f"DeepL 오류 발생: {e}"

    except Exception as e:  # 일반적인 예외 처리
        return f"기타 오류 발생: {e}"
