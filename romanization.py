from korean_romanizer.romanizer import Romanizer

# 한글을 로마자로 변환하는 함수
def romanize_korean(korean_text):
    try:
        romanized_text = Romanizer(korean_text).romanize()
        return romanized_text
    except Exception as e:
        return f"변환 중 오류 발생: {e}"


