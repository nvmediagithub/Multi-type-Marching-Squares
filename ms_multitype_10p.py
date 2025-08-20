from itertools import product

from data import T, EDGES


def to_base(n: int, base: int) -> str:
    if n == 0:
        return '0'
    digits = []
    while n > 0:
        digits.append(str(n % base))
        n //= base
    return ''.join(reversed(digits))


def build_multitype_table_10p():
    """Генерирует таблицу из T^4 кейсов, где каждый кейс — dict:
       {0: [...tris], 1: [...], ..., 'aband': {...}}"""
    table = {}
    for vals in product(range(T), repeat=4):
        case_idx = sum(vals[i] * (T ** i) for i in range(4))
        tables = {t: [] for t in range(T)}
        tables['aband'] = [[]] * 4

        # Для каждого типа состояния внутри клетки
        for t in range(T):
            # границы сегментов для типа t
            segs = [e for e, (a, b) in EDGES.items() if (vals[a] == t) ^ (vals[b] == t)]
            # print(t, case_idx, vals, segs)
            # полностью однородная клетка: два больших треугольника
            if len(set(vals)) == 1:
                print('not segs', t, case_idx, vals, segs)
                if all(v == t for v in vals):
                    tables[t] = [
                        [('p', 0), ('p', 1), ('p', 2)],
                        [('p', 0), ('p', 2), ('p', 3)],
                    ]
            elif len(set(vals)) == 2 and vals[0] != vals[2] and vals[1] != vals[3]:
                tris = []
                for c in range(4):
                    if vals[c] == t:
                        rel = [e for e in segs if c in EDGES[e]]
                        if len(rel) == 1:
                            if vals[c] == vals[(c + 1) % 4]:
                                tris.append([('p', c), ('e', (c - 1) % 4), ('e', (c - 3) % 4)])
                                tris.append([('p', c), ('p', (c + 1) % 4), ('e', (c + 1) % 4)])
                tables[t] = tris

            elif len(set(vals)) == 2 and \
                    (
                            (vals[0] != vals[2] and vals[1] == vals[3]) or \
                            (vals[0] == vals[2] and vals[1] != vals[3])
                    ):
                tris = []
                for c in range(4):
                    if vals[c] == t:
                        rel = [e for e in segs if c in EDGES[e]]
                        if len(rel) == 2:
                            tris.append([('p', c), ('e', rel[0]), ('e', rel[1])])
                            if c == 0 or c == 3:
                                tris.append([('e', rel[0]), ('e', rel[1]), ('ip', 0)])
                            if c == 1 or c == 2:
                                tris.append([('e', rel[0]), ('e', rel[1]), ('ip', 1)])
                        if len(rel) == 1:
                            if c == 1:
                                tris.append([('p', 1), ('e', 1), ('e', 0)])
                                tris.append([('e', 1), ('ip', 1), ('e', 0)])
                            if c == 2:
                                tris.append([('p', 2), ('e', 2), ('e', 1)])
                                tris.append([('e', 1), ('ip', 1), ('e', 2)])
                            if c == 0:
                                tris.append([('p', 0), ('e', 3), ('e', 0)])
                                tris.append([('e', 0), ('ip', 0), ('e', 3)])
                            if c == 3:
                                tris.append([('p', 3), ('e', 2), ('e', 3)])
                                tris.append([('e', 2), ('ip', 0), ('e', 3)])
                        if len(rel) == 0:
                            if c == 1:
                                tris.append([('p', 1), ('e', 1), ('e', 0)])
                                tris.append([('e', 1), ('ip', 1), ('e', 0)])
                            if c == 2:
                                tris.append([('p', 2), ('e', 2), ('e', 1)])
                                tris.append([('e', 1), ('ip', 1), ('e', 2)])
                            if c == 0:
                                tris.append([('p', 0), ('e', 3), ('e', 0)])
                                tris.append([('e', 0), ('ip', 0), ('e', 3)])
                            if c == 3:
                                tris.append([('p', 3), ('e', 2), ('e', 3)])
                                tris.append([('e', 2), ('ip', 0), ('e', 3)])
                tables['aband'][0] = [('ip', 0), ('ip', 1), ('e', 0)]
                tables['aband'][1] = [('ip', 1), ('ip', 0), ('e', 2)]
                tables[t] = tris

            elif len(set(vals)) == 4 or len(set(vals)) == 3 or (len(set(vals)) == 2 and vals[0] == vals[2]):
                tris = []
                for c in range(4):
                    if vals[c] == t:
                        rel = [e for e in segs if c in EDGES[e]]
                        # print(t, rel)
                        if len(rel) == 2:
                            tris.append([('p', c), ('e', rel[0]), ('e', rel[1])])
                            if c == 0 or c == 3:
                                tris.append([('e', rel[0]), ('e', rel[1]), ('ip', 0)])
                            if c == 1 or c == 2:
                                tris.append([('e', rel[0]), ('e', rel[1]), ('ip', 1)])
                        if len(rel) == 1:
                            if c == 1:
                                tris.append([('p', 1), ('e', 1), ('e', 0)])
                                tris.append([('e', 1), ('ip', 1), ('e', 0)])
                            if c == 2:
                                tris.append([('p', 2), ('e', 2), ('e', 1)])
                                tris.append([('e', 1), ('ip', 1), ('e', 2)])
                            if c == 0:
                                tris.append([('p', 0), ('e', 3), ('e', 0)])
                                tris.append([('e', 0), ('ip', 0), ('e', 3)])
                            if c == 3:
                                tris.append([('p', 3), ('e', 2), ('e', 3)])
                                tris.append([('e', 2), ('ip', 0), ('e', 3)])
                tables['aband'][0] = [('ip', 0), ('ip', 1), ('e', 0)]
                tables['aband'][1] = [('ip', 1), ('ip', 0), ('e', 2)]
                tables[t] = tris

        table[case_idx] = tables
    return table


# === Интерполяция на ребре по весам ===
def interp(p1, p2, w1, w2):
    total = w1 + w2
    t = 0.5 if total == 0 else w1 / total
    return (
        p1[0] + t * (p2[0] - p1[0]),
        p1[1] + t * (p2[1] - p1[1])
    )
