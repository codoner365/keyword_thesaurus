import re

# 유니코드 한글 범위 및 초성, 중성, 종성 계산 상수
BASE_CODE, CHOSUNG, JUNGSUNG = 44032, 588, 28

# 초성, 중성, 종성 리스트
CHOSUNG_LIST = ['ㄱ', 'ㄲ', 'ㄴ', 'ㄷ', 'ㄸ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅃ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅉ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']
JUNGSUNG_LIST = ['ㅏ', 'ㅐ', 'ㅑ', 'ㅒ', 'ㅓ', 'ㅔ', 'ㅕ', 'ㅖ', 'ㅗ', 'ㅘ', 'ㅙ', 'ㅚ', 'ㅛ', 'ㅜ', 'ㅝ', 'ㅞ', 'ㅟ', 'ㅠ', 'ㅡ', 'ㅢ', 'ㅣ']
JONGSUNG_LIST = [' ', 'ㄱ', 'ㄲ', 'ㄳ', 'ㄴ', 'ㄵ', 'ㄶ', 'ㄷ', 'ㄹ', 'ㄺ', 'ㄻ', 'ㄼ', 'ㄽ', 'ㄾ', 'ㄿ', 'ㅀ', 'ㅁ', 'ㅂ', 'ㅄ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']

def decompose_hangul(char):
    """한글 음절을 초성, 중성, 종성으로 분리"""
    if re.match('[가-힣]', char):
        char_code = ord(char) - BASE_CODE
        chosung = char_code // CHOSUNG
        jungsung = (char_code % CHOSUNG) // JUNGSUNG
        jongsung = (char_code % CHOSUNG) % JUNGSUNG
        return CHOSUNG_LIST[chosung], JUNGSUNG_LIST[jungsung], JONGSUNG_LIST[jongsung]
    else:
        return char, None, None

def compose_hangul(chosung, jungsung, jongsung):
    """초성, 중성, 종성을 결합하여 한글 음절 생성"""
    if jungsung is None:  # 한글이 아닌 경우
        return chosung
    chosung_index = CHOSUNG_LIST.index(chosung)
    jungsung_index = JUNGSUNG_LIST.index(jungsung)
    jongsung_index = JONGSUNG_LIST.index(jongsung) if jongsung != ' ' else 0
    char_code = BASE_CODE + chosung_index * CHOSUNG + jungsung_index * JUNGSUNG + jongsung_index
    return chr(char_code)
