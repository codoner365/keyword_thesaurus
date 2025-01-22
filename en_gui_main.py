
import tkinter as tk
from tkinter import ttk
# from api_similarword import get_similar_sounding_words
from en_generate_similar_sound import generate_en_similar_words
from similarity_calculation import calculate_similarity, filter_top_percentage
from text_type import categorize_text



def display_input():
    # 이전 텍스트 삭제
    result_text.delete("1.0", tk.END)
    word = entry.get()
    text_type = categorize_text(word)
    input_label.config(text=f"입력된 내용: {word}")

    similar_words = result_display(word, text_type)
    
    result_text.insert(tk.END," ".join(similar_words),"big")
    
            
    
def result_display(word, text_type):
    show_label(text_type)
    show_text()
    filter_button.place(x=480, y=50)
    result_words = []
    result_words = on_search(word, text_type)
    if not isinstance(result_words, (list, tuple)):
        result_text.insert(tk.END, "오류")
        return 0

    return result_words
    
def on_search(word, text_type):
    similar_words = []

    if text_type in ('한글', '기타'):
        return []
    
    # 유사 소리 단어 출력 옵션      
    # similar_words = get_similar_sounding_words(word)
    similar_words = generate_en_similar_words(word)
    sorted_results= calculate_similarity(word, similar_words) 
    # check_label1.pack(pady=10)
    # check_label1.config(text=f"체크:{word}, {sorted_results}")
    
    # 결과에서 단어만 추출하여 리스트로 반환
    # calculate_similarity는 (word, similarity) 튜플을 반환하므로
    # 단어만 추출하여 리스트로 반환
    word_list = [word for word, _ in sorted_results]
    return word_list
    




def show_label(text_type):   
    label.pack(pady=10)
    label.config(text=f"텍스트 타입: {text_type}")
    


def show_text():
    frame_result.pack(fill=tk.BOTH, expand=True, pady=10)
    result_text.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
 

def filter_activate(input_word, similar_words):   
    try:        
        results = calculate_similarity(input_word, similar_words)

        # 유사도 계산
        # 유사도가 0 초과인 단어 필터링
        # filtered_results = [(word, similarity) for word, similarity in sorted_results if similarity > 0]
        filtered_results = [word for word, similarity in results if similarity > 0]
        filtered_results = filter_top_percentage(results,90)
        filtered_word_list = [word for word, _ in filtered_results]

        if filtered_results:
            show_filtered_text()
            # 공백으로 구분하여 출력
            # 필터링된 결과 표시
            filtered_text.delete("1.0", tk.END)
            filtered_text.insert(tk.END, " ".join(filtered_word_list),"big")
            # filtered_text.insert(tk.END, f"{filtered_results}")


        else:
            filtered_text.delete("1.0", tk.END)
            filtered_text.insert(tk.END,"유사도가 0 초과인 단어가 없습니다.")
            # print("유사도가 0 초과인 단어가 없습니다.")

    except Exception as e:
        filtered_text.delete("1.0", tk.END)
        filtered_text.insert(tk.END,f"유사도 계산 중 오류 발생: {e}")
        print(f"유사도 계산 중 오류 발생: {e}")

    
def show_filtered_text():
    filtered_text.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)




# 기본 창 생성
root = tk.Tk()
root.title("영어 유사 단어 서치")  # 창 제목 설정
root.geometry("800x740")  # 창 크기 설정 (너비x높이)

# 입력 필드
entry = tk.Entry(root, width=30)
entry.pack(pady=10)

# 검색 버튼
button = tk.Button(root, text="입력 확인", command=display_input)
button.pack(pady=5)

# 필터 버튼
filter_button = tk.Button(root, text="필터", command=lambda: filter_activate(entry.get(), generate_en_similar_words(entry.get())))
# filter_button = tk.Button(root, text="필터", command=result_filter)

# 입력 단어 결과 표시 레이블
input_label= tk.Label(root, text="입력단어")
input_label.pack(pady=10)

# 텍스트 타입 결과 표시 레이블
label = tk.Label(root, text="텍스트 타입")

# 텍스트와 스크롤바를 포함하는 프레임 생성
frame_result = ttk.Frame(root)
# frame_result.pack(fill=tk.BOTH, expand=True, pady=10)


# 결과 표시 텍스트 위젯
result_text = tk.Text(frame_result, wrap=tk.WORD, height=10)
# result_text.pack(side=tk.TOP, fill=tk.BOTH, expand=True)


# 필터 결과 텍스트 위젯
filtered_text = tk.Text(frame_result, wrap=tk.WORD, height=10, fg="blue")
# filtered_text.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

# 텍스트 위젯의 글꼴과 크기 세팅
result_text.tag_configure("big", font=(None, 14))  # 원하는 글꼴과 크기 설정
filtered_text.tag_configure("big", font=(None, 14)) 

# 디버깅용- 체크 레이블
check_label1  = tk.Label(root, text="시작전")
check_label2  = tk.Label(root, text="시작전")

# 실행
root.mainloop()