#similar_sound.py
from itertools import product
from hangul_utils import decompose_hangul, compose_hangul


# 유사 소리 매핑 (초성, 중성, 종성 각 자음 및 모음에 대해)
CHOSUNG_MAP = {
    'ㄱ': ['ㄱ', 'ㅋ', 'ㄲ'], 'ㄲ': ['ㄱ', 'ㅋ', 'ㄲ'], 'ㄴ': ['ㄴ', 'ㄹ'], 'ㄷ': ['ㄷ', 'ㅌ', 'ㄸ'],
    'ㄸ': ['ㄷ', 'ㅌ', 'ㄸ'], 'ㄹ': ['ㄹ'], 'ㅁ': ['ㅁ', 'ㅂ'], 'ㅂ': ['ㅂ', 'ㅃ'],
    'ㅃ': ['ㅂ', 'ㅍ', 'ㅃ'], 'ㅅ': ['ㅅ', 'ㅆ','ㅌ'], 'ㅆ': ['ㅅ', 'ㅆ'], 'ㅇ': ['ㅇ'], 'ㅈ': ['ㅈ', 'ㅊ'],
    'ㅉ': ['ㅉ', 'ㅈ', 'ㅊ'], 'ㅊ': ['ㅊ', 'ㅈ'], 'ㅋ': ['ㅋ', 'ㄱ'], 'ㅌ': ['ㅌ', 'ㄷ', 'ㅅ'], 'ㅍ': ['ㅍ', 'ㅂ'],
    'ㅎ': ['ㅎ']
}

JUNGSUNG_MAP = {
    'ㅏ': ['ㅏ', 'ㅓ', 'ㅗ'], 'ㅐ': ['ㅔ', 'ㅐ'], 'ㅑ': ['ㅏ', 'ㅑ'], 'ㅒ': ['ㅔ', 'ㅐ', 'ㅒ'], 'ㅓ': ['ㅓ', 'ㅗ'],
    'ㅔ': ['ㅔ', 'ㅐ'], 'ㅕ': ['ㅓ', 'ㅕ'], 'ㅖ': ['ㅔ', 'ㅖ'], 'ㅗ': ['ㅗ', 'ㅛ'], 'ㅘ': ['ㅘ', 'ㅏ'],
    'ㅙ': ['ㅙ', 'ㅐ'], 'ㅚ': ['ㅚ', 'ㅙ'], 'ㅛ': ['ㅛ', 'ㅗ'], 'ㅜ': ['ㅜ', 'ㅠ'], 'ㅝ': ['ㅝ', 'ㅓ'],
    'ㅞ': ['ㅞ', 'ㅔ'], 'ㅟ': ['ㅟ', 'ㅣ'], 'ㅠ': ['ㅠ', 'ㅜ'], 'ㅡ': ['ㅡ'], 'ㅢ': ['ㅡ', 'ㅢ'],
    'ㅣ': ['ㅣ']
}

JONGSUNG_MAP = {
    ' ': [' '], 'ㄱ': ['ㄱ'], 'ㄲ': ['ㄱ', 'ㄲ'], 'ㄳ': ['ㄱ', 'ㅅ'], 'ㄴ': ['ㄴ'], 'ㄵ': ['ㄴ', 'ㅈ'],
    'ㄶ': ['ㄴ'], 'ㄷ': ['ㄷ'], 'ㄹ': ['ㄹ'], 'ㄺ': ['ㄹ', 'ㄱ'], 'ㄻ': ['ㄹ', 'ㅁ'], 'ㄼ': ['ㄹ', 'ㅂ'],
    'ㄽ': ['ㄹ', 'ㅅ'], 'ㄾ': ['ㄹ', 'ㅌ'], 'ㄿ': ['ㄹ', 'ㅍ'], 'ㅀ': ['ㄹ'], 'ㅁ': ['ㅁ'], 'ㅂ': ['ㅂ'],
    'ㅄ': ['ㅂ', 'ㅅ'], 'ㅅ': ['ㅅ'], 'ㅆ': ['ㅅ', 'ㅆ'], 'ㅇ': ['ㅇ'], 'ㅈ': ['ㅈ'], 'ㅊ': ['ㅊ'],
    'ㅋ': ['ㅋ'], 'ㅌ': ['ㅌ'], 'ㅍ': ['ㅍ'], 'ㅎ': ['ㅎ']
}

def generate_kr_similar_words(word):
    """유사 소리 단어 생성"""
    try:
        hangul_check(word)  # 한글 체크 함수 호출
    except ValueError as e:
        err_text = f"오류: {e}"
        return [err_text]  # 오류가 나면 err_text 반환 (후속 코드 실행 안 함)

    decomposed = [decompose_hangul(char) for char in word]
    variants = []

    for chosung, jungsung, jongsung in decomposed:
        if jungsung is None:  # 한글이 아닌 경우
            variants.append([(chosung,)])
        else:
            chosung_variants = CHOSUNG_MAP.get(chosung, [chosung])
            jungsung_variants = JUNGSUNG_MAP.get(jungsung, [jungsung])

            # 종성이 없을 때는 종성 없이 처리
            if jongsung == ' ':
                jongsung_variants = [' ']  # 종성 없이 출력

            else:
                # 종성이 있을 때는 종성이 없는 변형도 포함
                jongsung_variants = JONGSUNG_MAP.get(jongsung, [jongsung])[:]
                jongsung_variants.append(' ')  # 새 리스트에 추가
                # print(f"variants 4: {variants}")
                # print(f"jongsung_variants: {jongsung_variants}")
            variants.append(list(product(chosung_variants, jungsung_variants, jongsung_variants)))
            # print(f"최종 variants: {variants}")
            # 디버깅용 - 각 단계의 변수를 확인
            # print(f"chosung_variants: {chosung_variants}")
            # print(f"jungsung_variants: {jungsung_variants}")
            # print(f"jongsung_variants: {jongsung_variants}")
    
    combinations = product(*variants)
    # 디버깅용
    # combinations, combinations_copy = tee(product(*variants))  # 복제
    # print(f"Generated combinations: {list(combinations_copy)}")  # 복제본을 리스트로 변환하여 출력

    similar_words = [''.join(compose_hangul(*syllable) for syllable in combination) for combination in combinations]
    return similar_words


def hangul_check(word):
    # 단어를 한글 자모로 분해
    decomposed = [decompose_hangul(char) for char in word]
    
    for chosung, jungsung, jongsung in decomposed:
        # 한글이 아닌 문자일 경우
        if chosung is None or jungsung is None:
            raise ValueError("초성과 종성 조합이 부적절하거나, 잘못된 것이 포함되어 있습니다.")
                
        # 초성, 중성, 종성 조합이 잘못된 경우
        if chosung not in CHOSUNG_MAP or jungsung not in JUNGSUNG_MAP or jongsung not in JONGSUNG_MAP:
            raise ValueError("초성, 중성, 종성 조합이 잘못되었습니다.")
