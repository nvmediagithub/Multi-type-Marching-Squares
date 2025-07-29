from itertools import product

from data import T, EDGES, IP_ADJ


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


def build_multitype_table():
    """Генерирует таблицу из T^4 кейсов, где каждый кейс — dict:
       {0: [...tris], 1: [...], 2: [...], 3: [...], 'aband': [...]}"""
    table = {}
    for vals in product(range(T), repeat=4):
        case = sum(vals[i] * (T**i) for i in range(4))
        tables = {t: [] for t in range(T)}
        tables['aband'] = []

        for t in range(T):
            segs = [e for e, (a, b) in EDGES.items() if (vals[a] == t) ^ (vals[b] == t)]
            if not segs:
                if all(v == t for v in vals):
                    tables[t] = [
                        [
                            ('p', 0),
                            ('p', 1),
                            ('p', 2)
                        ],
                        [
                            ('p', 0),
                            ('p', 2),
                            ('p', 3)
                        ]
                    ]
            elif len(segs) in (2, 3):
                poly = []
                for i in range(4):
                    if i in segs:
                        poly.append(('e', i))
                    nxt = (i+1) % 4
                    if vals[nxt] == t:
                        poly.append(('p', nxt))
                if len(poly) >= 3:
                    tables[t] = fan_tris(poly)
            else:
                tris = []
                for c in range(4):
                    if vals[c] == t:
                        rel = [e for e in segs if c in EDGES[e]]
                        if len(rel) == 2:
                            tris.append([('p', c), ('e', rel[0]), ('e', rel[1])])
                center = [('e', e) for e in segs]
                tris += fan_tris(center)
                tables[t] = tris

        all_segs = set()
        for t in range(T):
            local = [e for e,(a,b) in EDGES.items() if (vals[a] == t) ^ (vals[b] == t)]
            all_segs |= set(local)
        band = [('e', e) for e in sorted(all_segs)]
        if len(band) >= 3:
            tables['aband'] = fan_tris(band)

        table[case] = tables
    return table

def build_multitype_table_2():
    """Генерирует таблицу из T^4 кейсов, где каждый кейс — dict:
       {0: [...tris], 1: [...], ..., 'aband': [...]}"""
    table = {}
    for vals in product(range(T), repeat=4):
        case_idx = sum(vals[i] * (T**i) for i in range(4))
        tables = {t: [] for t in range(T)}
        tables['aband'] = []

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
                            tris.append([('p', c), ('e', rel[0]), ('ip', rel[0])])
                            tris.append([('p', c), ('ip', rel[0]), ('ip', rel[1])])
                            tris.append([('p', c), ('ip', rel[1]), ('e', rel[1])])
                        if len(rel) == 1:
                            tris.append([('p', c), ('e', rel[0]), ('ip', rel[0])])
                            if c > rel[0] or (c == 0 and rel[0] == 3): # TODO костыль
                                tris.append([('p', c), ('e', (rel[0] + 1) % 4), ('ip', (rel[0] + 1) % 4)])
                                tris.append([('p', c), ('ip', rel[0]), ('ip', (rel[0] + 1) % 4)])
                            else:
                                tris.append([('p', c), ('e', (rel[0] - 1) % 4), ('ip', (rel[0] - 1) % 4)])
                                tris.append([('p', c), ('ip', rel[0]), ('ip', (rel[0] - 1) % 4)])
                        if len(rel) == 0:
                            tris.append([('p', c), ('e', c), ('ip', c)])
                            tris.append([('p', c), ('ip', c), ('ip', (c - 1) % 4)])
                            tris.append([('p', c), ('e', (c - 1) % 4), ('ip', (c - 1) % 4)])


                tables[t] = tris


        # Построение "розовой зоны" (aband) для всех сегментов
        all_segs = set()
        for t in range(T):
            local = [e for e,(a,b) in EDGES.items() if (vals[a] == t) ^ (vals[b] == t)]
            all_segs |= set(local)
        band = sorted(all_segs)
        if len(band) >= 3:
            # если 4 сегмента, делаем фан-триангуляцию по внутреннему квадрату
            if len(band) == 4:
                tris = []
                tris.append([('ip', 0), ('ip', 1), ('ip', 2)])
                tris.append([('ip', 0), ('ip', 2), ('ip', 3)])
                tables['aband'] = tris
            else:
                tables['aband'] = fan_tris([('e', e) for e in band])

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
