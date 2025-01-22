# text_type.py

import re

def categorize_text(text):
    """
    입력된 텍스트가 한글, 영어, 기타 문자로 구분하여 반환
    :param text: 사용자 입력 문자열
    :return: '한글', '영어', '기타' 중 하나
    """
    # 한글 여부 확인
    if re.match('[가-힣]', text):
        return '한글'
    
    # 영어 여부 확인
    elif re.match('[a-zA-Z]', text):
        return '영어'
    
    # 기타 문자 (숫자, 특수문자 등)
    else:
        return '기타'

