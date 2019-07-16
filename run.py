"""
    :author: Zhang Yu (张宇)
    :copyright: © 2019 Zhang Yu <zhangyu18223@gmail.com>
    :create_date: 2019-07-09
"""
from flask import jsonify
from flask_swagger import swagger

from app import create_app
from config import HOST, PORT, DEBUG

# gunicorn等启动
app = create_app()


@app.route("/spec")
def spec():
    swag = swagger(app)
    swag['info']['version'] = "0.1"
    swag['info']['title'] = "Tcloud API"
    return jsonify(swag)


# 开发启动
if __name__ == '__main__':
    app.run(host=HOST, port=PORT, debug=DEBUG)
