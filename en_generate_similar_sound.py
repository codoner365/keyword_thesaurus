import re
import nltk 
from nltk.corpus import words

# 자음, 모음, 이중 모음 및 자음 조합 매핑 규칙 정의
mapping_rules = {
    'consonants': {
        'b': ['p', 'v'],
        'c': ['k', 's', 'ch'],
        'd': ['t','dd','th'],
        'f': ['ph', 'v', 'p'],
        'g': ['j', 'k', 'z'],
        'h': [''],
        'j': ['g', 'z'],
        'k': ['c', 'q'],
        'l': ['r', 'll'],
        'm': ['n', 'mm'],
        'n': ['m', 'nn'],
        'p': ['b', 'f', 'ph'],
        'q': ['k', 'c'],
        'r': ['l', 're', 'rr'],
        's': ['ss', 'z', 'c'],
        't': ['d','tt'],
        'v': ['f', 'b'],
        'w': ['v'],
        'x': ['ks', 'z'],
        'y': ['i', 'j'],
        'z': ['s', 'ts','g', 'ze', 'zz'],
    },
    'vowels': {
        'a': ['e', 'o', 'i', 'ar', 'ah'],
        'e': ['a', 'i', 'ee', 'ea', 'er'],
        'i': ['e', 'y', 'ee','ai',  'ie', 'ey'],
        'o': ['a', 'u', 'au', 'oa', 'or', 'au'],
        'u': ['o', 'oo', 'ue', 'ou','au'],
    },
    'diphthongs': {
        'ee': ['i', 'ei', 'ie', 'y'],
        'ou': ['ow', 'oo', 'aw', 'u'],
        'ai': ['ay', 'ei', 'e'],
        'oa': ['o', 'a', 'ou'],
        'ph': ['f', 'p'],
        'ch': ['k','c', 'tch'],
        'sh': ['s', 'ch'],
        'th': ['t', 'd','s'],
        'gh': ['', 't', 'g'],
        'ny': ['nny', 'ney' ],
        'my': ['mmy', 'mey' ],
        'ry': ['rry', 'rey' ]
    },
}

# 단어 변환 함수
def generate_en_similar_words(word):
    similar_words = {word}  # 원본 단어 포함
    word = word.lower()

    # 이중 모음 및 자음 조합 처리
    for diphthong, replacements in mapping_rules['diphthongs'].items():
        if diphthong in word:
            for replacement in replacements:
                new_word = word.replace(diphthong, replacement)
                similar_words.add(new_word)

    # 단일 자음 및 모음 처리
    for i, char in enumerate(word):
        if char in mapping_rules['consonants']:
            for replacement in mapping_rules['consonants'][char]:
                new_word = word[:i] + replacement + word[i+1:]
                similar_words.add(new_word)
        elif char in mapping_rules['vowels']:
            for replacement in mapping_rules['vowels'][char]:
                new_word = word[:i] + replacement + word[i+1:]
                similar_words.add(new_word)

    # 이중 변환 처리
    additional_words = set()
    for base_word in similar_words:
        for i, char in enumerate(base_word):
            if char in mapping_rules['consonants']:
                for replacement in mapping_rules['consonants'][char]:
                    new_word = base_word[:i] + replacement + base_word[i+1:]
                    additional_words.add(new_word)
            elif char in mapping_rules['vowels']:
                for replacement in mapping_rules['vowels'][char]:
                    new_word = base_word[:i] + replacement + base_word[i+1:]
                    additional_words.add(new_word)

    similar_words.update(additional_words)
    # 연속된 동일 알파벳을 하나로 줄여서 새로운 단어를 추가
    similar_words.update(create_words_with_reduced_repeated_letters(similar_words))

    remove_repeated_letters = remove_words_with_repeated_letters(similar_words)
    return list(remove_repeated_letters) # 리스트로 변환


# 연속된 동일 알파벳을 하나로 축소한 단어를 생성하는 함수
def create_words_with_reduced_repeated_letters(words):
    reduced_words = set()
    for word in words:
        # 연속된 동일한 문자(알파벳)을 하나로 변환
        reduced_word = re.sub(r'(.)\1+', r'\1', word)  # 예: 'mamm' -> 'mam'
        if reduced_word != word:  # 원래 단어와 다를 경우에만 추가
            reduced_words.add(reduced_word)
    return reduced_words

# 연속된 동일 알파벳을 가진 단어 제거 함수
def remove_words_with_repeated_letters(words):
    return {word for word in words if not re.search(r'(\w)\1{2,}', word)}

# 결과를 알파벳 올림차순으로 정렬하는 함수
def sort_words_alphabetically(words):
    return sorted(words)


# NLTK 사전을 사용한 유효 단어 필터링
def NLTK_filter(similar_sounding_words):
    try:
        nltk.download('words', quiet=True)
        word_list = set(words.words())
        
        valid_words = [word for word in similar_sounding_words if word in word_list]
        if valid_words:
            print("\nValid English words (found in dictionary):")
            print(", ".join(valid_words))
            return valid_words, None  # 결과와 함께 경고문 없음
        else:
            # print("\nNo valid English words found in dictionary.")
            return [], "No valid English words found in dictionary."
    except ImportError:
        warning_message = "NLTK is not installed. Skipping dictionary check."
        return [], warning_message  # 빈 리스트와 경고문 반환
    


