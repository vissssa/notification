"""
    :author: Zhang Yu (张宇)
    :copyright: © 2019 Zhang Yu <zhangyu18223@gmail.com>
    :create_date: 2019-07-10
"""
import multiprocessing

from gunicorn.app.base import BaseApplication
from gunicorn.six import iteritems

from app import create_app
from config import HOST, PORT


def number_of_workers():
    return (multiprocessing.cpu_count() * 2) + 1


options = {
    'bind': '{}:{}'.format(HOST, PORT),
    'workers': number_of_workers(),
    'worker_class': 'gevent',
    'timeout': '1800',
}


class Application(BaseApplication):

    def __init__(self, app, options=None):
        self.options = options or {}
        self.application = app
        super(Application, self).__init__()

    def load_config(self):
        config = dict([(key, value) for key, value in iteritems(self.options)
                       if key in self.cfg.settings and value is not None])
        for key, value in iteritems(config):
            self.cfg.set(key.lower(), value)

    def load(self):
        return self.application


def main():
    Application(create_app(), options).run()


if __name__ == "__main__":
    main()
