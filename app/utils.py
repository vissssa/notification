"""
    :author: Zhang Yu (张宇)
    :copyright: © 2019 Zhang Yu <zhangyu18223@gmail.com>
    :create_date: 2019-07-09
"""


def row2list(rows, keys):
    data = []
    for i in rows:
        data.append({key: getattr(i, key) for key in keys})
    return data
