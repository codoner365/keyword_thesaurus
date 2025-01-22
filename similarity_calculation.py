from fuzzywuzzy import fuzz

def calculate_similarity(input_word, similar_words):
    """
    입력된 단어와 유사 단어들 간의 유사도를 계산
    """
    similarities = []
    for word in similar_words:
        similarity = fuzz.ratio(input_word, word)
        similarities.append((word, similarity))
    sorted_similarities = sort_by_similarity(similarities)
    return sorted_similarities


def sort_by_similarity(similarity_results):
    """
    유사도 결과를 유사도가 높은 순으로 정렬
    :param similarity_results: [(word, similarity), ...] 형식의 리스트
    :return: 유사도가 높은 순으로 정렬된 리스트
    """
    if not isinstance(similarity_results, list) or not all(isinstance(item, tuple) and len(item) == 2 for item in similarity_results):
        raise ValueError("Input must be a list of tuples (word, similarity).")

    # 유사도를 기준으로 내림차순 정렬
    sorted_results = sorted(similarity_results, key=lambda x: x[1], reverse=True)
    return sorted_results

def filter_top_percentage(similarity_results, percentage=70):
    """
    유사도 결과 중 상위 일정 비율만 반환
    :param similarity_results: [(word, similarity), ...] 형식의 리스트
    :param percentage: 반환할 유사도 상위 비율 (기본값 70%)
    :return: 유사도가 높은 상위 n% 단어 리스트
    """
    if percentage < 0 or percentage > 100:
        raise ValueError("Percentage must be between 0 and 100.")
    
    # 유사도 순으로 정렬
    sorted_results = sort_by_similarity(similarity_results)
    
    # 상위 비율에 해당하는 개수 계산
    top_count = int(len(sorted_results) * (percentage / 100))
    
    # 상위 n%에 해당하는 단어만 반환
    return sorted_results[:top_count]

if __name__ == '__main__':
    import sys
    # 인자로 입력된 텍스트와 유사 단어 리스트 처리
    input_word = sys.argv[1]
    similar_words = sys.argv[2:]  # 나머지 인자들을 유사 단어로 간주
    percentage = int(sys.argv[3])
    results = calculate_similarity(input_word, similar_words)
    top_n_percent_results = filter_top_percentage(results, percentage)

    
