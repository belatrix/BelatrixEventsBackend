from random import randint


def random_element_list(list):
    if list.count() > 0:
        random_id = randint(0, list.count() - 1)
        return list[random_id]
    elif list.count() == 0:
        return list[0]
    else:
        return None
