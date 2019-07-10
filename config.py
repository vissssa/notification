"""
    :author: Zhang Yu (张宇)
    :copyright: © 2019 Zhang Yu <zhangyu18223@gmail.com>
    :create_date: 2019-07-09
"""

SQLALCHEMY_TRACK_MODIFICATIONS = False
HOST = '0.0.0.0'
PORT = 8848
DEBUG = True
MSG_MAP = {
    0: 'ok',

    101: 'can not find object',
    102: 'save object error',
    103: 'duplicate data',
    104: 'can not create object',
    105: 'remove failed',
    106: 'operate failed',
    108: 'permission denied',
    109: 'project permission denied',

    201: 'field required',
    202: 'field length error',

    301: 'password wrong',
    303: 'username or password wrong',

    403: 'not allowed',
    410: 'auth expired',
    411: 'auth error',
    412: 'not login',
    413: 'username is not exist or password error',
    414: 'invalid data',
}
try:
    from local_config import *
except Exception as e:
    pass
