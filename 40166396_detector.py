import math
import sys
import string

translationTable = str.maketrans(string.punctuation+string.ascii_uppercase," "*len(string.punctuation)+string.ascii_lowercase)

COMMONWORDS = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours', 
                'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', 'her', 'hers', 'herself', 
                'it', 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 
                'who', 'whom', 'this', 'that', 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 
                'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 
                'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 
                'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 
                'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further',
                'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few',
                'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than',
                'too', 'very', 's', 't', 'can', 'will', 'just', 'don', 'should', 'now', 'False', 'def', 'if', 'raise',
                'None', 'del', 'import', 'return', 'True', 'elif', 'in', 'try', 'and', 'else', 'is', 'while', 'as',
                'except', 'lambda', 'with', 'assert', 'finally', 'nonlocal', 'yield', 'break', 'for', 'not', 'class',
                'form', 'or', 'continue', 'global', 'pass', 'auto', 'else', 'long', 'switch', 'break', 'enum', 'register',
                'typedef', 'case', 'extern', 'return', 'union', 'char', 'float', 'short', 'unsigned', 'const', 'for',
                'signed', 'void', 'continue', 'goto', 'sizeof', 'volatile', 'default', 'if', 'static', 'while', 'do',
                'int', 'struct', 'Packed', 'double' ]

def reader(filepath):
    try:
        with open(filepath,'r',encoding='utf-8') as f : 
            content = f.read()
            return content
    except:
        sys.exit()

def extractWordsfromLine(content):
    content = content.translate(translationTable)
    words = content.split()
    return words

def extractWords(filepath):
    content = reader(filepath)
    words = extractWordsfromLine(content)
    return words

def occurance_of_words_with_commonwords(wordsf1, wordsf2):
    dict1_words = {}
    dict2_words = {}
    for i in wordsf1:
        if i in COMMONWORDS and i in wordsf2:
            continue
        if i in dict1_words:
            dict1_words[i] = dict1_words[i] + 1
        else:
            dict1_words[i] = 1

    for j in wordsf2:
        if j in COMMONWORDS and j in wordsf1:
            continue
        if j in dict2_words:
            dict2_words[j] = dict2_words[j] + 1
        else:
            dict2_words[j] = 1
    return dict1_words, dict2_words
    

def occurance_of_words_without_commonwords(wordsf1, wordsf2):
    dict1_words = {}
    dict2_words = {}
    for i in wordsf1:
        if i in dict1_words:
            dict1_words[i] = dict1_words[i] + 1
        else:
            dict1_words[i] = 1

    for j in wordsf2:
        if j in dict2_words:
            dict2_words[j] = dict2_words[j] + 1
        else:
            dict2_words[j] = 1
    return dict1_words, dict2_words


#Using Cosine similairity method
def dotProductforCosinesimilarity(a,b):
    c = 0.0
    for i in a:
        if i in b:
            c += (a[i]*b[i])
    return c

def angle_between_dictionaries(a,b):
    c = dotProductforCosinesimilarity(a,b)
    d = math.sqrt(dotProductforCosinesimilarity(a,a) * dotProductforCosinesimilarity(b,b))
    return math.acos(c/d)

def percentagePlagiarism(dist):
    angle = dist * (180 / math.pi)
    percentage_uncommonwords = ((angle - 0)/(90-0))*(100-0)+0
    percentage_commonwords = 100 - percentage_uncommonwords
    return percentage_commonwords


#Using wordcount method
def plagiarisedWordscount(preprocessed_words_f1, preprocessed_words_f2):
    keyf1 = preprocessed_words_f1.keys()
    keyf2 = preprocessed_words_f2.keys()
    overall_count = 0
    for val in preprocessed_words_f1.values():
        overall_count += val
    for val in preprocessed_words_f2.values():
        overall_count += val
    similar_key = 0
    for k in keyf1:
        if k in keyf2:
            similar_key += min(preprocessed_words_f1[k],preprocessed_words_f2[k])
    plagiarised_words = (similar_key*2/overall_count)*100
    return plagiarised_words


#Using Jaccard Index method
def jaccardIndex(a, b):
    set_of_a = set(a)
    set_of_b = set(b)
    jaccard_similarity_index_count = len(set_of_a.intersection(set_of_b))/len(set_of_a.union(set_of_b))
    return jaccard_similarity_index_count * 100


#Checks the Average of similarity
def commonness(f1, f2):
    wordsf1 = extractWords(f1)
    wordsf2 = extractWords(f2)
    
    preprocessed_words_f1, preprocessed_words_f2 = occurance_of_words_with_commonwords(wordsf1, wordsf2)
    without_preproccesed_words_f1 , without_preproccesed_words_f2 = occurance_of_words_without_commonwords(wordsf1, wordsf2)
    
    plagiarism_using_jaccard_index = jaccardIndex(preprocessed_words_f1.keys(), preprocessed_words_f2.keys())
    plagiarism_without_jaccard_index = jaccardIndex(without_preproccesed_words_f1.keys(), without_preproccesed_words_f2.keys())
    
    plagiarism_using_wordcount = plagiarisedWordscount(preprocessed_words_f1, preprocessed_words_f2)
    plagiarism_without_wordcount = plagiarisedWordscount(without_preproccesed_words_f1, without_preproccesed_words_f1)
    
    dist1 = angle_between_dictionaries(preprocessed_words_f1, preprocessed_words_f2)
    plagiarism_using_cosine_similarity = percentagePlagiarism(dist1)
    dist2 = angle_between_dictionaries(without_preproccesed_words_f1, without_preproccesed_words_f2)
    plagiarism_without_cosine_similarity = percentagePlagiarism(dist2)
    
    final_average = (plagiarism_using_cosine_similarity + plagiarism_without_cosine_similarity + plagiarism_using_wordcount + plagiarism_without_wordcount + plagiarism_using_jaccard_index + plagiarism_without_jaccard_index)/6.0
    # print(final_average)
    return final_average


#Returns '0' or '1' based on threshold value
def calculatePlagiarism(path_f1, path_f2):
    try:
        percentage_of_plagiarism = commonness(path_f1, path_f2)
        if(percentage_of_plagiarism > 50.50):
            print('1')
        else:
            print('0')
    except:
        print('0')

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("0")
    else:
        calculatePlagiarism(sys.argv[1],sys.argv[2])