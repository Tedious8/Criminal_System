from FlagEmbedding import BGEM3FlagModel
import json
import pickle

# 加載嵌入
try:
    with open('./with_hie_with_kg_embeddings.pkl', 'rb') as f:
        embedding_dict = pickle.load(f)
except FileNotFoundError:
    raise FileNotFoundError("File not found.")

# 初始化模型
try:
    model = BGEM3FlagModel('BAAI/bge-m3', use_fp16=True)
except Exception as e:
    raise RuntimeError(f"{str(e)}")

# 加載法條對應資料
try:
    with open('./output_bgecriminal_all_predictions_with_law.json', 'r', encoding='utf-8') as f:
        law_data = json.load(f)
except FileNotFoundError:
    raise FileNotFoundError("File not found.")

# 提取條文編號函數
def extract_article_number(article_text):
    return article_text.split('_')[0]  # 以 "_" 分割，返回第一部分

# 查找條文對應罪名函數
def find_crime_by_article(target_article, law_data):
    target_article_number = extract_article_number(target_article)  # 提取條文編號
    for entry in law_data:
        for crime, articles in entry['law'].items():
            for article in articles:
                if article[0] == target_article_number:  # 比對條文編號
                    return crime
    return None

# 問答系統整合罪名
def qa_system_with_crime(question, top_k=30):
    # 將問題轉換為嵌入
    question_embeddings = model.encode([question], return_dense=True, return_sparse=True, return_colbert_vecs=True)

    # 計算與法律條文的相似度
    law_scores = []
    for article_text, article_embeddings in embedding_dict['articles'].items():
        dense_score = float(question_embeddings['dense_vecs'] @ article_embeddings['dense_vecs'].T)
        sparse_score = float(model.compute_lexical_matching_score(question_embeddings['lexical_weights'][0], article_embeddings['lexical_weights']))
        colbert_score = float(model.colbert_score(question_embeddings['colbert_vecs'][0], article_embeddings['colbert_vecs']))
        weighted_score = 0.4 * dense_score + 0.4 * sparse_score + 0.2 * colbert_score  # 權重可調整
        law_scores.append((article_text, weighted_score))

    # 按加權相似度排序
    law_scores = sorted(law_scores, key=lambda x: x[1], reverse=True)

    # 返回結果並附加罪名，避免重複條文
    seen_articles = set()  # 記錄已處理過的條文
    results = []
    for article, score in law_scores[:top_k]:
        article_number = extract_article_number(article)  # 提取條文編號
        if article_number in seen_articles:
            continue  # 跳過已處理的條文
        seen_articles.add(article_number)  # 記錄新條文
        crime = find_crime_by_article(article, law_data)
        results.append({
            'article': article,
            'crime': crime,
            'score': score
        })
    return results