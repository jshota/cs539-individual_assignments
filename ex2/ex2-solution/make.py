from collections import defaultdict

START, END = ('<s>', '</s>')
lambdas = [.01, .09, .9]

with open('train.txt') as f:
    lines = f.read().splitlines()
f.close()

dict_uni = defaultdict(float)
dict_bi = defaultdict(lambda: defaultdict(float))
dict_tri = defaultdict(lambda: defaultdict(lambda: defaultdict(float)))
N = 0
for line in lines:
    chars = [START] + list(line.replace(' ', '_')) + [END]
    N += (len(chars)-1)
    dict_uni[START] += 1
    dict_uni[chars[1]] += 1
    dict_bi[START][chars[1]] += 1
    dict_bi[START][START] += 1
    dict_tri[START][START][chars[1]] += 1
    for i in range(2, len(chars)):
        dict_uni[chars[i]] += 1
        dict_bi[chars[i-1]][chars[i]] += 1
        dict_tri[chars[i-2]][chars[i-1]][chars[i]] += 1

voc = dict_uni.keys()
V = len(voc)
uni_wfsa = ['F', '(0 (1 '+START+'))']
bi_wfsa = ['F', '(0 (1 '+START+'))']
tri_wfsa = ['F', '(0 (11 '+START+'))']
for c1 in voc:
    s1 = ('1' if c1 == START else 'F' if c1 == END else c1)
    if c1 != START:
        uni_wfsa.append('(1 (' + ('F' if c1 == END else '1') +
                        ' ' + c1 + ' ' + str((dict_uni[c1] + 1) / (N + V)) + '))')
    if c1 != END:
        for c2 in voc:
            s2 = ('1' if c2 == START else 'F' if c2 == END else c2)
            if c2 != START:
                bi_wfsa.append('(' + s1 + ' (' + s2 + ' ' + c2 + ' ' +
                               str((dict_bi[c1][c2]+1) / (dict_uni[c1]+V)) + '))')
            if c2 != END:
                for c3 in voc:
                    s3 = ('1' if c3 == START else 'F' if c3 == END else c3)
                    if c3 != START:
                        p3 = lambdas[2]*dict_tri[c1][c2][c3]/(dict_bi[c1][c2] if dict_bi[c1][c2] > 0 else 1.0) + \
                            lambdas[1]*dict_bi[c2][c3]/dict_uni[c1] + \
                            lambdas[0]*dict_uni[c3]/N
                        tri_wfsa.append(
                            '(' + s1 + s2 + ' (' + (s2 if c3 != END else '') + s3 + ' ' + c3 + ' ' + str(p3) + '))')


with open('unigram.wfsa', 'w') as f1, \
        open('bigram.wfsa', 'w') as f2, \
        open('trigram.wfsa', 'w') as f3:
    print >> f1, '\n'.join(uni_wfsa)
    print >> f2, '\n'.join(bi_wfsa)
    print >> f3, '\n'.join(tri_wfsa)
