import requests

def is_internet_connected():
    try:
        # Google에 요청하여 인터넷 연결 확인
        requests.get("https://www.google.com", timeout=5)
        return True
    except requests.ConnectionError:
        return False

def get_similar_sounding_words(word):
    if not is_internet_connected():
        return "인터넷에 연결되어 있지 않습니다. 인터넷 연결을 확인해주세요."
    
    url = f"https://api.datamuse.com/words?sl={word}&max=20"
    response = requests.get(url)
    
    # JSON 응답을 파싱
    data = response.json()
    
    # 유사한 발음의 단어들만 리스트로 반환
    similar_words = [item['word'] for item in data]
    
    # # 유사한 단어들을 '+'로 결합하여 반환
    # return ' + '.join(similar_words)

    return similar_words

def main():
    print("단어를 입력하세요. 종료하려면 'exit'을 입력하세요.")
    
    while True:
        word = input("단어: ").strip()  # 사용자 입력 받기
        
        if word.lower() == "exit":  # 'exit' 입력 시 종료
            print("프로그램을 종료합니다.")
            break

        similar_words = get_similar_sounding_words(word)
        
        if similar_words:
            print(f"'{word}'와 유사한 발음의 단어들: {similar_words}")
        else:
            print("유사한 발음의 단어를 찾을 수 없습니다.")

if __name__ == "__main__":
    main()