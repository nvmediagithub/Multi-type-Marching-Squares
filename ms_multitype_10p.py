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


def fan_tris(poly):
    """Веерная триангуляция списка вершин poly."""
    return [[poly[0], poly[i], poly[i+1]] for i in range(1, len(poly)-1)]


def build_multitype_table_10p():
    """Генерирует таблицу из T^4 кейсов, где каждый кейс — dict:
       {0: [...tris], 1: [...], ..., 'aband': {...}}"""
    table = {}
    for vals in product(range(T), repeat=4):
        case_idx = sum(vals[i] * (T**i) for i in range(4))
        tables = {t: [] for t in range(T)}
        tables['aband'] = [[]]*2


        # Для каждого типа состояния внутри клетки
        for t in range(T):
            # границы сегментов для типа t
            segs = [e for e,(a,b) in EDGES.items() if (vals[a] == t) ^ (vals[b] == t)]

            # полностью однородная клетка: два больших треугольника
            if not segs:
                if all(v == t for v in vals):
                    tables[t] = [
                        [('p',0),('p',1),('p',2)],
                        [('p',0),('p',2),('p',3)],
                    ]


            # случай с 4 сегментами: используем внутренние точки для треугольников
            else:
                tris = []
                for c in range(4):
                    if vals[c] == t:
                        rel = [e for e in segs if c in EDGES[e]]
                        print(t, rel)
                        if len(rel) == 2:
                            tris.append([('p', c), ('e', rel[0]), ('e', rel[1])])
                            if c == 0 or c == 3:
                                tris.append([('e', rel[0]), ('e', rel[1]), ('ip', 0)])
                            if c == 1 or c == 2:
                                tris.append([('e', rel[0]), ('e', rel[1]), ('ip', 1)])




                        # if len(rel) == 1:
                        #     tris.append([('p', c), ('e', rel[0]), ('ip', rel[0])])
                        #     if c > rel[0] or (c == 0 and rel[0] == 3): # TODO костыль
                        #         tris.append([('p', c), ('e', (rel[0] + 1) % 4), ('ip', (rel[0] + 1) % 4)])
                        #         tris.append([('p', c), ('ip', rel[0]), ('ip', (rel[0] + 1) % 4)])
                        #     else:
                        #         tris.append([('p', c), ('e', (rel[0] - 1) % 4), ('ip', (rel[0] - 1) % 4)])
                        #         tris.append([('p', c), ('ip', rel[0]), ('ip', (rel[0] - 1) % 4)])
                        # if len(rel) == 0:
                        #     tris.append([('p', c), ('e', c), ('ip', c)])
                        #     tris.append([('p', c), ('ip', c), ('ip', (c - 1) % 4)])
                        #     tris.append([('p', c), ('e', (c - 1) % 4), ('ip', (c - 1) % 4)])

                tables['aband'][0] = [('ip', 0), ('ip', 1), ('e', 0)]
                tables['aband'][1] = [('ip', 1), ('ip', 0), ('e', 2)]
                tables[t] = tris

        table[case_idx] = tables
    return table


# === Интерполяция на ребре по весам ===
def interp(p1, p2, w1, w2):
    total = w1 + w2
    t = 0.5 if total == 0 else w1/total
    return (
        p1[0] + t * (p2[0] - p1[0]),
        p1[1] + t * (p2[1] - p1[1])
    )
