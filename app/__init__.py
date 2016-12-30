# _*_ coding: utf-8 _*_
import os
from config import basedir
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import scoped_session, sessionmaker
# engine = create_engine('mysql://root:123456@localhost:3306/arg4rm?charset=utf8', convert_unicode=True)
# db_session = scoped_session(sessionmaker(autocommit=False,autoflush=False,bind=engine))
# Base = declarative_base()

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
bootstrap = Bootstrap(app)
login_manager = LoginManager()
login_manager.setup_app(app)

# {% extends "bootstrap/base.html" %}

# Base.query = db_session.query_property()
from app import control
# 必须按照该顺序进行，因为init顺序初始化在没有新教案app的时候是无法导入control的
# 造成依赖错误
from app import models
