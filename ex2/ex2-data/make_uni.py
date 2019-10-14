from sys import stdin

def counter():
    dic = {}
    for line in stdin:
        for i in line.replace(" ", "_"):
            dic[i] = dic.get(i, 0) + 1
    return dic

def output(dic, nums):
    print('F')
    print("(0 (1 <s>))")
    for key, value in dic.items():
        if key == "\n":
            print("(1 (F  " + "</s>" + " " + str(float(value)/float(nums)) + "))")
        else:
            print("(1 (1  " + str(key) + " " + str(float(value)/float(nums)) + "))")

character_dic = counter()
character_nums = sum(character_dic.values())

output(character_dic, character_nums)