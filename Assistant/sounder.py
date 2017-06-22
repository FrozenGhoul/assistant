from metaphone import doublemetaphone as dm
from difflib import SequenceMatcher as sm
from munkres import Munkres
import sys

__all__ = ["RESERVED_WORDS", "filter", "search", "probability"]

RESERVED_WORDS = {"what", "where", "which", "how", "when", "who", "is", "are",
                  "makes", "made", "make", "did", "do", "to", "the", "of",
                  "from", "against", "and", "or", "you", "me", "we", "us",
                  "your", "my", "mine", 'yours', "could", "would", "may",
                  "might", "let", "possibly", 'tell', "give", "told", "gave",
                  "know", "knew", 'a', 'am', 'an', 'i', 'like', 'has', 'have',
                  'need', 'will', 'be', "this", 'that', "for"}
RESERVED_WORDS = frozenset(RESERVED_WORDS)

def probability(query, dataset, detailed=True, prediction=True, metaphone=True):
    if any(isinstance(i, str) for i in dataset):
        dataset = [dataset]
    if metaphone:
        query, dataset = _metaphones(query, dataset)
    chances = _process_chances(dataset, query)
    if prediction:
        index = _pick(chances)
        if detailed:
            return {'chances': chances[index], 'index': index}
        return {'chances': chances[index][0], 'index': index}
    if detailed:
        return chances
    return [chance[0] for chance in chances]

def search(query, dataset, metaphone=False):
    if metaphone:
        query, dataset = _metaphones(query, dataset)
    index = _pick(_process_chances(dataset, query))
    return index

def _process_chances(dataset, query):#module kwds, cmd kwds
    scores = []
    for data in dataset:#for kwd list on module kwds
        #[[r(q1, d1)... r(qn, d1)], [r(q1, d2)... r(qn, d2)]...]
        avg_scores = [[sm(a=kw, b=sw).ratio() for kw in query] for sw in data]
        print(f"avg_scores=\n{avg_scores}")
        word_score = [score[0] for score in _hungarian_algorithm(avg_scores)]
        print(f"word_score=\n{word_score}\n")
        avg_score = sum(word_score) / len(word_score)
        scores.append([avg_score, word_score])
    return scores

def filter(query, reserved_sub_words=RESERVED_WORDS):
    sub_words = []
    raw_text_array = query.lower().split()
    key_words = raw_text_array.copy()
    for index, raw_text in enumerate(raw_text_array):
        if raw_text in reserved_sub_words:
            sub_words.append(raw_text)
            key_words.remove(raw_text)
    return {'sub_words': sub_words, 'key_words': key_words}

def _metaphones(query, dataset):
    new_query = [dm(given_keyword)[0] for given_keyword in query]
    new_dataset = []
    for data in dataset:
        user_keywords = [dm(user_keyword)[0] for user_keyword in data]
        new_dataset.append(user_keywords)
    return new_query, new_dataset

def _hungarian_algorithm(matrix):
    temp_scores = []
    cost_matrix = []
    for row in matrix:
        cost_row = []
        for col in row:
            cost_row += [sys.maxsize - col]
        cost_matrix += [cost_row]
    indexes = Munkres().compute(cost_matrix)
    for row, column in indexes:
        score = matrix[row][column]
        index = column
        temp_scores.append([score, index])
    return temp_scores

def _pick(scores):
    max_score = max_index = 0
    for index, item in enumerate(scores):
        if item[0] > max_score:
            max_score = item[0]
            max_index = index
    picked = scores[max_index][1]
    perm_sum = sum(picked)
    perm_avg = perm_sum / len(picked)
    for index, item in enumerate(scores):
        if item[0] == max_score and index != max_index:
            temp_sum = sum(item[1])
            temp_avg = temp_sum / len(item[1])
            if temp_avg > perm_avg:
                max_index = index
                perm_sum = temp_sum
                perm_avg = temp_avg
            elif temp_avg == perm_avg:
                if temp_sum > perm_sum:
                    max_index = index
                    perm_sum = temp_sum
                    perm_avg = temp_avg
    return max_index
