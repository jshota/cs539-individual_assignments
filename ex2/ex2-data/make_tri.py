from sys import stdin
from typing import List, Dict
import numpy as np

character_list = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 
'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 
'v', 'w', 'x', 'y', 'z', '_', '\n']

def read_line():
    list = []
    for line in stdin:
        list.append(line.replace(" ", "_"))
    return np.asarray(list)

def counter(n: int, line_list: List[str]) -> Dict:
    '''Count N-grams substrings in a given dataset.

    Args:
        n: the n of n-gram
        line_list: the input file stores in a list

    Returns:
        a dictionary contains all appeared n-gram and their appear times.
        eg:
            {'a':1, 'b':2 ...} or {'aa':1, 'ab':2 ...} or ...

    '''
    dic = {}
    # for i in range(n):
    #     for key in dic.keys():
    #         for c in character_list:
    #             dic[c] = 0
    for line in line_list:
        for i in range(len(line)-n+1):
            s = line[i:i+n]
            dic[s] = dic.get(s, 0) + 1
    return dic

def classifier(dic_1: Dict, dic_2: Dict) -> Dict:
    '''Classify keys in the later dictionary by keys in the former dictionary.

    Args:
        dic_1: the count dictionary with lower gram
        dic_2: the count dictionary with higher gram

    Returns:
        a dictionary contains classified keys of the later dictionary.
        eg: 
            {'y': ['ye', 'y_', 'yp', 'ys', 'yo'] ...}

    '''
    dic = {}
    for key_1 in dic_1.keys():
        dic[key_1] = [key_2 for key_2 in dic_2.keys() if key_1 == key_2[0:len(key_1)]]
    return dic

def probability_calculator(uni_dic: Dict, dic_1: Dict, dic_2: Dict, class_dic: Dict) -> Dict:
    '''Calculate the corpus probabilities by given dictionaries.

    Args:
        uni_dic: the count dictionary of uni_dic
        dic_1: the count dictionary with lower gram
        dic_2: the count dictionary with higher gram
        class_dic: contains classified keys of the later dictionary

    Returns:
        a dictionary contains the corpus probabilities.
        eg:
            {'ab':0.102, 'ac':0.082 ...}

    '''
    dic = {}
    sum_count_uni = sum(uni_dic.values())
    # key_1: a, b, c, ..., _, \n
    # keys_2: ['aa', 'ab', ...], ['ba', 'bb',...]
    for key_1, keys_2 in class_dic.items():
        count_1 = dic_1.get(key_1, 0)
        types = len(keys_2)
        # if we have wi-1... in the dataset, then use witten-bell smoothing
        if count_1 != 0:
            smooth_para = 1 - float(types)/float((count_1 + types))
        # if not the end of a sentence
        if key_1[-1] != '\n':
            # character: a, b, c, ..., _, \n
            for character in character_list:
                key_2 = key_1 + character
                count_2 = dic_2.get(key_2, 0)
                # if we have wi-1... in the dataset, then use witten-bell smoothing
                if count_1 != 0:
                    cond_prob = count_2 / count_1
                    uncond_prob = uni_dic[character] / sum_count_uni
                    dic[key_2] = smooth_para * cond_prob + (1 - smooth_para) * uncond_prob
                # or just use uniform distribution
                else:
                    dic[key_2] = 1.0 / len(character_list)
                # update dic_2 keys to all combinations derived from key_1
                dic_2[key_2] = dic_2.get(key_2, 0)
    return dic

def output(uni_dic, dic_list, nums, grams):
    print('F')
    print("(0 (1 <s>))")
    for key, value in uni_dic.items():
        if key == "\n":
            pre = "(1 (F  "
            mid = "</s>" + " "
            end = str(float(value)/float(nums)) + "))"
        else:
            pre = "(1 ({}  ".format(key)
            mid = str(key) + " "
            end = str(float(value)/float(nums)) + "))"
        print(pre + mid + end)

    for dic in dic_list:
        for key, value in dic.items():
            if key[-1] == "\n":
                pre = '(' + key[:-1] + ' '
                mid = '(' + 'F' + '  ' + '</s>' + ' '
                end = str(value) + '))'
            else:
                pre = '(' + key[:-1] + ' '
                mid = '(' + key[len(key)-(grams-1):] + '  ' + key[-1] + ' '
                end = str(value) + '))'
            print(pre + mid + end)

line_list = read_line()
uni_dic = counter(1, line_list)
bi_dic = counter(2, line_list)
tri_dic = counter(3, line_list)
output_dic = [probability_calculator(uni_dic, uni_dic, bi_dic, classifier(uni_dic, bi_dic)), probability_calculator(uni_dic, bi_dic, tri_dic, classifier(bi_dic, tri_dic))]
output(uni_dic, output_dic, sum(uni_dic.values()), 3)