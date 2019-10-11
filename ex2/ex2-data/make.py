from sys import stdin
line_list = []
character_dic = {}
character_nums = 0
def counter(line):
    for i in line:
        character_dic[i] = character_dic.get(i, 0) + 1
print('F')
print("(0 (1 <s>))")
# read file and replace space by '_'
for line in stdin:
    line_list.append(line.replace(" ", "_"))
for i in line_list:
    counter(i)
# the number of characters
character_nums = sum(character_dic.values())
for key, value in character_dic.items():
    if key == "\n":
        print("(1 (F  " + "</s>" + " " + str(float(value)/float(character_nums)) + "))")
    else:
        print("(1 (1  " + str(key) + " " + str(float(value)/float(character_nums)) + "))")