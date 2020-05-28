#!/usr/bin/env python3
import argparse
from collections import defaultdict
import math

RECOGNIZER = "RECOGNIZER"
BEST_PARSE = "BEST-PARSE"
TOTAL_WEIGHT = "TOTAL-WEIGHT"


def multiply(a, b, c):
    mul = []
    for i in a:
        for j in b:
            for k in c:
                mul.append(i * j * k)
    return mul


def grammarGen(gr):
    grammar = defaultdict(list)
    prob = defaultdict(list)
    with open(gr, 'r') as mf:
        data = mf.readlines()
    for line in data:
        p = float(line.strip().split('\t')[0])
        lhs = line.strip().split('\t')[1]
        rhs = line.strip().split('\t')[2]
        grammar[rhs].append(lhs)
        rule = lhs + '-' + rhs
        prob[rule].append(p)
    return grammar, prob


def CKY(gr, sen):
    grammar, prob = grammarGen(gr)
    sents = sen.split()
    table = [[{} for _ in range(len(sents))] for _ in range(len(sents))]
    back = [[{} for _ in range(len(sents))] for _ in range(len(sents))]
    for end in range(len(sents)):
        for pt in grammar[sents[end]]:
            ptRule = pt + '-' + sents[end]
            table[end][end][pt] = prob[ptRule]
            back[end][end][pt] = [[sents[end], None, 0, -math.log(prob[ptRule][0], 2)]]
        if end >= 1:
            for start in range(end - 1, -1, -1):
                for mid in range(start, end):
                    for B in table[start][mid].keys():
                        for C in table[mid + 1][end].keys():
                            combine = B + ' ' + C  # rhs
                            for A in grammar[combine]:
                                ARule = A + '-' + combine
                                if A in table[start][end].keys():
                                    concate = multiply(prob[ARule], table[start][mid][B], table[mid + 1][end][C])
                                    table[start][end][A] += concate
                                    backList = [B, C, mid, -math.log(prob[ARule][0], 2)]
                                    back[start][end][A].append(backList)
                                else:
                                    table[start][end][A] = multiply(prob[ARule], table[start][mid][B],
                                                                    table[mid + 1][end][C])
                                    back[start][end][A] = [[B, C, mid, -math.log(prob[ARule][0], 2)]]
    return table, back


def parse_sym(back, i, j, sym):
    res = []
    for s in back[i][j][sym]:
        if s[1] is None:
            res.append((s[3], f"({sym} {s[0]})"))
            continue
        left = parse_sym(back, i, s[2], s[0])
        right = parse_sym(back, s[2] + 1, j, s[1])
        for l in left:
            for r in right:
                res.append((l[0] + r[0] + s[3], f"({sym} {l[1]} {r[1]})"))
    return res


def main():
    parser = argparse.ArgumentParser(description='Process argument')
    parser.add_argument("mode", choices={RECOGNIZER, BEST_PARSE, TOTAL_WEIGHT}, help="execution mode")
    parser.add_argument('grammar', type=str, help='a string of filepath')
    parser.add_argument('sentence', type=str, help='a string of filepath')
    ARGS = parser.parse_args()
    with open(ARGS.sentence, 'r') as sf:
        s = sf.readlines()
    for sen in s:
        table, back = CKY(ARGS.grammar, sen)
        start = list(table[0][len(table) - 1].keys())
        startProb = list(table[0][len(table) - 1].values())
        justify = ''
        best = ''
        res = ''
        if len(start) == 0 or start[0] != 'ROOT':
            justify = 'False'
        else:
            justify = 'True'
            res = parse_sym(back, 0, len(back) - 1, 'ROOT')
            print(table)
            print(back)
        if ARGS.mode == 'RECOGNIZER':
            print(justify)
        if ARGS.mode == 'BEST-PARSE':
            if justify == 'False':
                print('-\tNOPARSE')
            else:
                print(f"{round(min(res)[0], 3)}\t{min(res)[1]}")
        if ARGS.mode == 'TOTAL-WEIGHT':
            if justify == 'False':
                print('-')
            else:
                print(round(-math.log(sum(startProb[0]), 2), 3))


if __name__ == "__main__":
    main()
