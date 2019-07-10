"""
    :author: Zhang Yu (张宇)
    :copyright: © 2019 Zhang Yu <zhangyu18223@gmail.com>
    :create_date: 2019-07-09
"""
from sqlalchemy import func, desc

from app import db
from app.models import Message, Content
from app.utils import row2list

"""站内性的一些构思

当前只用到了第一种

第一种 点到个别
  采用和私信相同的方式，在发送一条消息时在Content表中插入消息内容并且设置Type=Private,同时在Message表中插入多条记录设置RecID=各接收者ID，Status=未读
  
  用户B查找RecID=B,并且Staus为未读，Type=Private,显示为私信未读，点击阅读后改变Status=已读

  用户B查找RecID=B,并且Staus为已读，Type=Private,显示为私信已读，删除设置Status=删除

第二种 点到局部
   点到局部是一对某角色或某用户组发送，例如管理员向普通用户组发送，在Content表插入消息内容，且设置Type=Public 和Group为用户组ID

   用户登录后分两种情况：

  1、未找到RecId=自己ID 且 Content中（Type=Public 和Group=自己所在组 ）  的消息ID不包含在Messgae的MessageID中

       提取出来显示为用户公共消息未读，在用户点击阅读的时候，将消息阅读状态写入Messgae表，Status=已读。

  2、找到RecId=自己ID 且 Content中（Type=Public 和Group=自己所在组 ） 的消息ID包含在Messgae的MessageID中

      将此部分消息提取出来，显示为用户公共消息已读，如果想“删除”（当然是逻辑上的删除，并非物理数据库删除），设置该Status=删除。

      注：此时可以不验证Group=自己所在组

第三种 点到全部
    点到全部和点到局部采用类似的处理方式。例如管理员向普通用户组发送，在Content表插入消息内容，且设置Type=Global

    用户登录后分两种情况：

    1、未找到RecId=自己ID 且 Content中（Type=Global ） 的消息ID不包含在Messgae的MessageID中

        提取出来显示为用户系统消息未读，在用户点击阅读的时候，将消息阅读状态写入Messgae表，Status=已读。

    2、找到RecId=自己ID 且 Content中（Type=Global ） 的消息ID包含在Messgae的MessageID中

        将此部分消息提取出来，显示为用户系统消息已读，如果想“删除”（逻辑上的删除，并非物理数据库删除），设置该Status=删除。

 
处理流程

1、Messgae表中RecId=自己ID 且Status=未读，显示为私信未读
2、Messgae表中RecId=自己ID 且Status=已读 且 Type=Private,显示为私信已读
3、Messgae表中未找到RecId=自己ID 且 Content中（Type=Public 和Group=自己所在组 ） 的消息ID不包含在Messgae的MessageID中，显示为公共消息未读            
4、Messgae表中找到RecId=自己ID 且 Content中（Type=Public ） 的消息ID包含在Messgae的MessageID中 ，显示为公共消息已读
5、Messgae表中未找到RecId=自己ID 且 Content中（Type=Global ） 的消息ID不包含在Messgae的MessageID中 ，显示为系统消息未读
6、Messgae表中找到RecId=自己ID 且 Content中（Type=Global ） 的消息ID包含在Messgae的MessageID中 ，显示为系统消息已读

"""


def create_by_one2one(data):
    """
    创建一条私密消息，用于少量用户的流程通知
    :param data: [send_id, rec_id, content, message_type, group]
    :return: 创建成功
    """
    send_id = data.get('send_id')
    rec_id = data.get('rec_id')
    content = data.get('content')
    message_type = data.get('type')
    group = data.get('group')
    if not message_type:
        message_type = Content.PRIVATE
    if not group:
        group = 'public'
    if send_id and rec_id and content:
        with db.auto_commit():
            content = Content(send_id=send_id, content=content, type=message_type, group=group)
            db.session.add(content)
            db.session.flush()
            content_id = content.id
            if content_id:
                with db.auto_commit():
                    for i in rec_id:
                        db.session.add(Message(rec_id=int(i), content_id=content_id, status=Message.UNREAD))
        return 0
    return 102


def _get_message_query_by_user_id(user_id):
    return Message.query.outerjoin(
        Content, Message.content_id == Content.id).add_columns(Content.content.label('content'),
                                                               Message.status.label('status'),
                                                               Message.id.label('id'),
                                                               func.date_format(Content.create_time,
                                                                                "%Y-%m-%d %H:%i:%s").label(
                                                                   'create_time')).filter(
        Message.rec_id == user_id, Content.type == Content.PRIVATE, Message.status != Message.DISABLE).order_by(
        desc(Message.id))


def get_all_message_by_user_id(user_id):
    """
    获取一个用户所有的信息，不论已读或者未读
    :param user_id: 用户
    :return: ['id', 'content', 'status', 'create_time']
    """
    messages = _get_message_query_by_user_id(user_id).all()
    keys = ['id', 'content', 'status', 'create_time']
    data = row2list(messages, keys)
    return 0, data


def get_10_message_by_user_id(user_id):
    """
    获取一个用户10最近10信息，不论已读或者未读
    :param user_id: 用户
    :return: ['id', 'content', 'status', 'create_time']
    """
    messages = _get_message_query_by_user_id(user_id).limit(10).all()
    keys = ['id', 'content', 'status', 'create_time']
    data = row2list(messages, keys)
    return 0, data


def get_all_read_message_by_user_id(user_id):
    """
    获取一个用户所有的已读信息
    :param user_id: 用户
    :return: ['id', 'content', 'status', 'create_time']
    """
    messages = _get_message_query_by_user_id(user_id).filter(Message.status == Message.READ).all()
    keys = ['id', 'content', 'status', 'create_time']
    data = row2list(messages, keys)
    return 0, data


def get_all_unread_message_by_user_id(user_id):
    """
    获取一个用户所有的已读信息
    :param user_id: 用户
    :return: ['id', 'content', 'status', 'create_time']
    """
    messages = _get_message_query_by_user_id(user_id).filter(Message.status == Message.UNREAD).all()
    keys = ['id', 'content', 'status', 'create_time']
    data = row2list(messages, keys)
    return 0, data


def change_status(user, message_id, message_type):
    """
    修改通知的状态，已读改为1，删除改为2
    :return: 修改成功
    """
    message = Message.query.filter(Message.id == message_id, Message.rec_id == user).first()
    try:
        with db.auto_commit():
            if message_type == 1:
                message.status = Message.READ
            else:
                message.status = Message.DISABLE
    except Exception as e:
        return 102, e
    else:
        return 0, None
