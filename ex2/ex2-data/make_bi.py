from sys import stdin
import numpy as np

def read_line():
    list = []
    for line in stdin:
        list.append(line.replace(" ", "_"))
    return np.asarray(list)

def counter(line_list):
    dic = {}
    for line in line_list:
        for i in line:
            dic[i] = dic.get(i, 0) + 1
    return dic

def bi_counter(line_list):
    dic = {}
    for line in line_list:
        for i in range(len(line)-1):
            s = line[i:i+2]
            dic[s] = dic.get(s, 0) + 1
    return dic

def bi_dic_classifier(uni_dic, bi_dic):
    '''
    Return a dictionary contains key collections in bi_dic \
    which sort out by the first letter.
    eg. {'y': ['ye', 'y_', 'yp', 'ys', 'yo']}
    '''
    dic = {}
    for key in uni_dic.keys():
        dic[key] = [bi_key for bi_key in bi_dic.keys() if key == bi_key[0]]
    # except the final state '\n'
    del dic['\n']
    return dic

def probability_calculator(uni_dic, bi_dic, bi_class_dic):
    dic = {}
    uni_sum = sum(uni_dic.values())
    # uni_key: a, b, c, ..., _, \n
    # bi_keys: ['aa', 'ab', ...], ['ba', 'bb',...]
    for uni_key, bi_keys in bi_class_dic.items():
        uni_num = uni_dic[uni_key]
        type_num = len(bi_keys)
        smooth_para = 1 - float(type_num)/float((uni_num + type_num))
        # character: a, b, c, ..., _, \n
        for character in uni_dic.keys():
            bi_key = uni_key + character
            bi_num = bi_dic.get(bi_key, 0)
            conditional_probability = bi_num / uni_num
            uni_probability = uni_num / uni_sum
            dic[bi_key] = smooth_para * conditional_probability + (1 - smooth_para) * uni_probability
    return dic

def output(uni_dic, bi_dic, nums):
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

    for key, value in bi_dic.items():
        if key[1] == "\n":
            pre = '(' + key[0] + ' '
            mid = '(' + 'F' + '  ' + '</s>' + ' '
            end = str(value) + '))'
        else:
            pre = '(' + key[0] + ' '
            mid = '(' + key[1] + '  ' + key[1] + ' '
            end = str(value) + '))'
        print(pre + mid + end)

line_list = read_line()
uni_dic = counter(line_list)
bi_dic = bi_counter(line_list)
bi_class_dic = bi_dic_classifier(uni_dic, bi_dic)
# print(probability_calculator(uni_dic, bi_dic, bi_class_dic))
output(uni_dic, probability_calculator(uni_dic, bi_dic, bi_class_dic), sum(uni_dic.values()))