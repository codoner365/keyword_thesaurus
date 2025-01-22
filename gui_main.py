import tkinter as tk
from tkinter import ttk
from en_generate_similar_sound import generate_en_similar_words
from kr_generate_similar_sound import generate_kr_similar_words
from similarity_calculation import calculate_similarity, filter_top_percentage
from text_type import categorize_text

is_filtered_text = False


def display_input():
    result_text.delete("1.0", tk.END)
    word = entry.get()
    text_type = categorize_text(word)
    input_label.config(text=f"입력된 내용: {word}")
    
    # filter_button의 동작 업데이트
    update_filter_button(word)

    similar_words = result_display(word, text_type)
    result_text.insert(tk.END," ".join(similar_words),"big")


def result_display(word, text_type):
    global is_filtered_text
    show_label(text_type)
    show_text()
    filter_button.place(x=480, y=50)
    plus_button.place(x=530, y=50)
    result_words = []
    result_words = on_search(word, text_type)
    if not isinstance(result_words, (list, tuple)):
        result_text.insert(tk.END, "\n오류")
        return 0
    if is_filtered_text:
        filter_activate(word,result_words)
    return result_words



def on_search(word, text_type):
    similar_words = []

    # 유사 소리 단어 출력 옵션  
    if text_type in ('기타'):
        result_text.insert(tk.END, "한글 또는 영어를 입력하세요")
        return []
    elif text_type in ('한글'):   
        similar_words = generate_kr_similar_words(word)    
    else:   
        similar_words = generate_en_similar_words(word)
        # check_label1.pack(pady=10)
        # check_label1.config(text=f"체크:{word}, {sorted_results}")
        
    sorted_results= calculate_similarity(word, similar_words)  

    # calculate_similarity는 (word, similarity) 튜플을 반환하므로 단어만 추출하여 리스트로 반환
    word_list = [word for word, _ in sorted_results]
    return word_list


def filter_activate(input_word, similar_words):
    global is_filtered_text
    
    filtered_text.delete("1.0", tk.END)
    try:
        results = calculate_similarity(input_word, similar_words)

        # 유사도 계산
        # 유사도가 0 초과인 단어 필터링
        # filtered_results = [(word, similarity) for word, similarity in results if similarity > 0]
        filtered_results = [word for word, similarity in results if similarity > 0]
        filtered_results = filter_top_percentage(results,90)
        filtered_word_list = [word for word, _ in filtered_results]

        if filtered_results:
            show_filtered_text()
            # 공백으로 구분하여 출력
            # 필터링된 결과 표시
            filtered_text.delete("1.0", tk.END)
            filtered_text.insert(tk.END, " ".join(filtered_word_list),"big")
            is_filtered_text = True
        else:
            filtered_text.delete("1.0", tk.END)
            filtered_text.insert(tk.END,"유사도가 0 초과인 단어가 없습니다.")
            # print("유사도가 0 초과인 단어가 없습니다.")

    except Exception as e:
        filtered_text.delete("1.0", tk.END)
        filtered_text.insert(tk.END,f"유사도 계산 중 오류 발생: {e}")
        print(f"유사도 계산 중 오류 발생: {e}")



# 필터 버튼의 command를 text_type에 따라 동적으로 설정
def update_filter_button(word):
    

    #text_type에 따라 filter_button의 command를 업데이트
    text_type = categorize_text(word)
    
    if text_type in ('한글'):
        filter_button.config(command=lambda: filter_activate(entry.get(), generate_kr_similar_words(entry.get())))
    elif text_type in ('영어'):
        filter_button.config(command=lambda: filter_activate(word, generate_en_similar_words(word)))

    

def show_label(text_type):   
    label.pack(pady=10)
    label.config(text=f"텍스트 타입: {text_type}")
    

def show_text():
    frame_result.pack(fill=tk.BOTH, expand=True, pady=10)
    result_text.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

def show_filtered_text():
    filtered_text.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
    

# convert_spaces_to_plus
def toggle_separator():
    # result_text 내용 가져오기
    result_text_content = result_text.get("1.0", tk.END).strip()

    if result_text_content:  # result_text가 비어 있지 않은 경우
        # '+' 포함 여부에 따라 공백/플러스 변환
        if "+" in result_text_content:
            updated_content = result_text_content.replace("+", " ")  # '+'를 공백으로 변환
        else:
            updated_content = result_text_content.replace(" ", "+")  # 공백을 '+'로 변환

        # 변경된 텍스트를 result_text 위젯에 업데이트
        result_text.delete("1.0", tk.END)
        result_text.insert(tk.END, updated_content, 'big')

    # filtered_text 내용 가져오기
    filtered_text_content = filtered_text.get("1.0", tk.END).strip()

    if filtered_text_content:  # filtered_text가 비어 있지 않은 경우
        # '+' 포함 여부에 따라 공백/플러스 변환
        if "+" in filtered_text_content:
            updated_filtered_content = filtered_text_content.replace("+", " ")  # '+'를 공백으로 변환
        else:
            updated_filtered_content = filtered_text_content.replace(" ", "+")  # 공백을 '+'로 변환

        # 변경된 텍스트를 filtered_text 위젯에 업데이트
        filtered_text.delete("1.0", tk.END)
        filtered_text.insert(tk.END, updated_filtered_content, 'big')
    


# 기본 창 생성
root = tk.Tk()
root.title("유사 단어 서치")  # 창 제목 설정
root.geometry("800x740")  # 창 크기 설정 (너비x높이)

# 입력 필드
entry = tk.Entry(root, width=30)
entry.pack(pady=10)

# 검색 버튼
button = tk.Button(root, text="입력 확인", command=display_input)
button.pack(pady=5)

# 플러스 버튼
plus_button = tk.Button(root, text=" + ", command=toggle_separator)

# 필터 버튼 (초기 command는 빈 값으로 설정)
filter_button = tk.Button(root, text="필터", command=lambda: None)
# filter_button.place(x=480, y=50)


# 입력 단어 결과 표시 레이블
input_label= tk.Label(root, text="입력단어")
input_label.pack(pady=10)

# 텍스트 타입 결과 표시 레이블
label = tk.Label(root, text="텍스트 타입")

# 텍스트와 스크롤바를 포함하는 프레임 생성
frame_result = ttk.Frame(root)


# 결과 표시 텍스트 위젯
result_text = tk.Text(frame_result, wrap=tk.WORD, height=10)


# 필터 결과 텍스트 위젯
filtered_text = tk.Text(frame_result, wrap=tk.WORD, height=10, fg="blue")


# 텍스트 위젯의 글꼴과 크기 세팅
result_text.tag_configure("big", font=(None, 14))  # 원하는 글꼴과 크기 설정
filtered_text.tag_configure("big", font=(None, 14)) 

# 디버깅용- 체크 레이블
check_label1  = tk.Label(root, text="시작전")
check_label2  = tk.Label(root, text="시작전")

# 실행
root.mainloop()
