"""
    :author: Zhang Yu (张宇)
    :copyright: © 2019 Zhang Yu <zhangyu18223@gmail.com>
    :create_date: 2019-07-09
"""

from flask import Blueprint, request

from app.dao import create_by_one2one, get_all_message_by_user_id, get_10_message_by_user_id, change_status, \
    get_all_read_message_by_user_id, get_all_unread_message_by_user_id
from app.render import json_detail_render

api = Blueprint('', __name__)

"""
这些从request中获取userid是不合适的
后续应该从token中获取（更好的是由kong这类gateway中获得）
"""


@api.route('/', methods=['POST'])
def create():
    data = request.get_json()
    if data:
        code = create_by_one2one(data)
    else:
        code = 101
    return json_detail_render(code=code)


@api.route('/', methods=['GET'])
def get():
    user = request.args.get('user')
    isall = request.args.get('isall')
    if isall:
        code, data = get_all_message_by_user_id(user)
    else:
        code, data = get_10_message_by_user_id(user)
    return json_detail_render(code=code, data=data)


@api.route('/status', methods=['GET'])
def get_by_status():
    user = request.args.get('user')
    isread = request.args.get('isread')
    if isread:
        code, data = get_all_read_message_by_user_id(user)
    else:
        code, data = get_all_unread_message_by_user_id(user)
    return json_detail_render(code=code, data=data)


@api.route('/', methods=['PUT', 'DELETE'])
def modify():
    user = request.args.get('user')
    message_id = request.args.get('id')
    if request.method == 'PUT':
        code, message = change_status(user, message_id, 1)
    else:
        code, message = change_status(user, message_id, 2)
    return json_detail_render(code=code, message=message)
