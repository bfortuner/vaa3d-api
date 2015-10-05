#! /usr/bin/env python

import os

from flask.ext.script import Manager

from vaa3d_api import create_app


app = create_app(os.getenv('VAA_3_D_API_CONFIG', 'default'))
manager = Manager(app)


@manager.shell
def make_shell_context():
    return dict(app=app)


if __name__ == '__main__':
    manager.run()
