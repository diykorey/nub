import nltk
import numpy as np
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from summarizer import Summarizer


# nltk.download('punkt')


# Create BERT Extractive Summarizer
def summarizer(text1):
    return Summarizer().run(text1)


def cosine_similarity_custom(text1, text2):
    """
    Повертає міру подібності Cosine між двома текстами.

    Аргументи:
      text1: Перший текст.
      text2: Другий текст.

    Повертає:
      Міра подібності Cosine між двома текстами.
    """

    # Препроцесуємо тексти, видаливши пунктуацію і стоп-слова.

    text1 = nltk.word_tokenize(text1.lower().replace(",", ""))
    text2 = nltk.word_tokenize(text2.lower().replace(",", ""))

    # Створимо вектори частот слів для кожного тексту.

    vector1 = nltk.FreqDist(text1)
    vector2 = nltk.FreqDist(text2)

    # Обчислимо міру подібності Cosine.

    numerator = sum(vector1[word] * vector2[word] for word in set(vector1) & set(vector2))
    denominator = np.sqrt(sum(vector1[word] ** 2 for word in vector1)) * np.sqrt(
        sum(vector2[word] ** 2 for word in vector2))

    return numerator / denominator


def cosine_similarity_sklearn(text1, text2):
    vectorizer = CountVectorizer().fit_transform([text1, text2])
    vectors = vectorizer.toarray()
    return cosine_similarity([vectors[0]], [vectors[1]])[0][0]


def jaccard_similarity(text1, text2):
    # Tokenize the texts
    tokens1 = set(word_tokenize(text1.lower()))
    tokens2 = set(word_tokenize(text2.lower()))
    # Calculate Jaccard similarity
    intersection_size = len(tokens1.intersection(tokens2))
    union_size = len(tokens1.union(tokens2))

    return intersection_size / union_size if union_size != 0 else 0
