import math


def get_mean(data: list[float]) -> float:
    return sum(data) / len(data)


def get_std(data):
    size = len(data)
    mean = get_mean(data)
    std = math.sqrt((sum(x * x for x in data) / size) - (mean**2))
    return std


def get_percentile(percent: int, data: list[float]) -> float:
    data = sorted(data)
    n = len(data)
    i = (percent / 100) * (n - 1)
    lower = math.floor(i)
    upper = math.ceil(i)
    percentile = data[lower] * (upper - i) + data[upper] * (i - lower)
    return percentile


def get_min(data: list[float]) -> float:
    min_value = data[0]
    for element in data[1:]:
        if element < min_value:
            min_value = element
    return min_value


def get_max(data: list[float]) -> float:
    max_value = data[0]
    for element in data[1:]:
        if element > max_value:
            max_value = element
    return max_value


def dot_product(v1, v2):
    return sum(a * b for a, b in zip(v1, v2))


def outer_product(v1, v2):
    return [[a * b for b in v2] for a in v1]


def argmax(lst):
    return max(range(len(lst)), key=lambda i: lst[i])


def is_nan(x):
    return x != x


def contains_nan(matrix):
    for row in matrix:
        for val in row:
            if is_nan(val):
                return True
    return False


def transpose(matrix):
    return list(map(list, zip(*matrix)))


def add_column_ones(matrix):
    return [[1.0] + row for row in matrix]

#la symetrie/repartition des notes comparer a la moyenne
# 0 symetrique
# > 0 Beaucoup de petites valeurs, quelques très grandes
# < 0 Beaucoup de grandes valeurs, quelques très petites
def get_skewness(data): 
    mean = get_mean(data)
    std = get_std(data)
    n = len(data)
    return sum(((x - mean)/std)**3 for x in data) / n
