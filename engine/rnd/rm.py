import math

def variance(array):
    new_array = []
    if " " and "," in array:
        array_adj = array.strip().split(",")
        for i in array_adj:
            new_array.append(float(i))
    elif " " in array:
        array_adj = array.strip().split()
        new_array = [float(i) for i in array_adj]
    elif "," in array:
        array_adj = array.strip().split(",")
        new_array = [float(i) for i in array_adj]
    elif "\t" in array:
        array_adj = array.strip().split("\t")
        new_array = [float(i) for i in array_adj]
    elif "\n" in array:
        array_adj = array.strip().split("\t")
        new_array = [float(i) for i in array_adj]
    n = len(new_array)
    mean_a = sum(new_array) / n
    var = sum((xi - mean_a)**2 for xi in new_array) / (n - 1)
    return round(var, 6) 


def std_or_downside_dev(x):
    return round(math.sqrt(x) * 100, 2)


def semi_var(array, tgt=None):
    new_array = []
    if " " and "," in array:
        array_adj = array.strip().split(",")
        for i in array_adj:
            new_array.append(float(i))
    elif " " in array:
        array_adj = array.strip().split()
        new_array = [float(i) for i in array_adj]
    elif "," in array:
        array_adj = array.strip().split(",")
        new_array = [float(i) for i in array_adj]
    elif "\t" in array:
        array_adj = array.strip().split("\t")
        new_array = [float(i) for i in array_adj]
    elif "\n" in array:
        array_adj = array.strip().split("\t")
        new_array = [float(i) for i in array_adj]
    n = len(new_array)
    mean_a = sum(new_array) / n
    if tgt is not None:
        var = sum(min(0, (xi - tgt))**2 for xi in new_array) / (n - 1)
    var = sum(min(0, (xi - mean_a))**2 for xi in new_array) / (n - 1)
    return round(var, 6)


# Add formula of coefficient of variation