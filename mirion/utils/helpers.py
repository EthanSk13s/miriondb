def check_for_release(x, y, i):
    if x.release == y[i + 1].release:
        return True
    else:
        return False


def list_grouper(x, check):
    grouped_list = []
    temp = []

    for i, item in enumerate(x):
        try:
            # 'check' here is any function that takes in the item,
            # an index and the list itelf
            # see check_for_release for an example
            if check(item, x, i):
                temp.append(item)
            else:
                temp.append(item)
                grouped_list.append([x for x in temp])
                temp.clear()
        except IndexError:
            temp.append(item)
            grouped_list.append([x for x in temp])

    return grouped_list
