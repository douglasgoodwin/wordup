# -*- coding: utf-8 -*-
import os
from wordup.app import create_app
from wordup.settings import DevConfig, ProdConfig
# from wordup.user.models import User, Role
# from wordup.word.models import Word,Prompt,Audio
# from wordup.settings import DevConfig, ProdConfig
# from wordup.database import db

HERE = os.path.abspath(os.path.dirname(__file__))
TEST_PATH = os.path.join(HERE, 'tests')

if os.environ.get("WORDUP_ENV") == 'prod':
	app = create_app(ProdConfig)
else:
	app = create_app(DevConfig)

if __name__ == "__main__":
	app.run(host='0.0.0.0')
