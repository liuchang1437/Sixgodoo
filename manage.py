# -*- coding: utf-8 -*-
#!/usr/bin/env python
import os
from app import create_app, db
from app.models import Item, Blog, Tag, Category
from flask.ext.script import Manager, Shell
from flask.ext.migrate import Migrate, MigrateCommand

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app,db)

def make_shell_context():											   # import app,db,models automatically 
	return dict(app=app,db=db,Item=Item,Blog=Blog,Tag=Tag,Category=Category)

manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)							   # add database migaration. method : db migrate : db upgrade

@manager.command
def test():
	"""Run the unit tests."""
	import unittest
	tests = unittest.TestLoader().discover('tests')
	unittest.TextTestRunner(verbosity=2).run(tests)

if __name__ == '__main__':
	manager.run()
