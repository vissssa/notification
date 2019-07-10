"""
    :author: Zhang Yu (张宇)
    :copyright: © 2019 Zhang Yu <zhangyu18223@gmail.com>
    :create_date: 2019-07-09
"""

from app import create_app
from config import HOST, PORT, DEBUG

# gunicorn等启动
app = create_app()

# 开发启动
if __name__ == '__main__':
    app.run(host=HOST, port=PORT, debug=DEBUG)
