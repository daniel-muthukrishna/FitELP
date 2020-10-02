

def sum_dict_values(dict1, dict2):
    result = {key: dict1.get(key, 0) + dict2.get(key, 0) for key in set(dict1) | set(dict2)}

    return result
