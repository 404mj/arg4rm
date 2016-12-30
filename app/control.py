# _*_ coding: utf-8 _*_
from app import app, db, login_manager
from flask import request, render_template, redirect, url_for, flash, g, jsonify
from flask_login import login_required, login_user, logout_user, current_user
from flask.ext.sqlalchemy import SQLAlchemy
from models import Arrange, Room, RoomUser, Role
from forms import LoginForm, RegistrationForm, QueryRoomsForm
from hashlib import md5
from datetime import datetime


# 在每次请求前执行
# @app.before_request
# def before_request():
# g.user = current_user

# 首页
@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")

# 登陆
@login_manager.user_loader
def load_user(userid):
    return RoomUser.query.get(int(userid))

@app.route('/login', methods=('GET', 'POST'))
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = RoomUser.query.filter_by(name=form.username.data.strip()).first()# 有必要
        login_user(user)
        flash("Logged in successfully.")
        g.user = current_user
        return redirect(url_for("index"))
    return render_template("login.html", form=form)

# 登出
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))

# 注册
@app.route('/register', methods=('GET', 'POST'))
def register():
    regForm = RegistrationForm(request.form)
    if regForm.validate_on_submit():
        # salt
        pass_md5 = md5(regForm.data['password']+'xuetuis.me')
        passw = pass_md5.hexdigest()
        # 默认注册用户角色都是use
        new_user = RoomUser(name = regForm.username.data, email = regForm.data['email'], password = passw, roleId=1)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html',form = regForm)


# 主页面,get查询展示，post新建，编辑
@app.route('/arranges', methods=['GET','POST'])
@login_required
def arranges():
    datetime_format = '%Y-%m-%d %H:%M:%S'
    # 这份地方在model总分明定义的是def为什么不能加()?!
    # querya = QueryArrangesForm()

    start_time = request.form.get('start_time',None) #try to solve the bad request error
    # datetime.strptime(, datetime_format)
    end_time = request.form.get('end_time', None)
    room_num = request.form.get('room_num', None)
    if room_num is None and start_time is None:
        # 初始请求
        print "----------parameter none"
        # 这里bug是is_admin要加()才能执行这份自定义的函数
        if current_user.is_admin():
            print "-----------------is admin"
            arrs = Arrange.query.all()
        else:
            print "-----------------not admin"
            arrs = Arrange.query.filter_by(userId = current_user.userId).all()
        print '---------------arr length%s' % str(len(arrs))
        return render_template('arranges.html', arranges = arrs)
    # elif querya.validate_on_submit():
    else:
        # Ajax请求
        print "----------------start_time: %s,,,room_num: %s" % (start_time, room_num)
        # rmNUm 应该使用模糊查询like%%
        # 使用sqlalchemy的查询问题不少
        # attrs = ('rm.rmNum == room_num', 'startTime >= start_time', 'endTime <= end_time')
        arrs = Arrange.query.filter(Arrange.startTime >= datetime.strptime(start_time, datetime_format)).filter(Arrange.endTime <= datetime.strptime(end_time,datetime_format)).all()

        print '----------length arrs %d' % len(arrs)
    # returndatas = arrs
    return jsonify([a.serialize() for a in arrs])
    # return arrs
    # return render_template('arranges.html', arranges = arrs) #这样是返回html给ajax的函数处理但是页面不刷新是无法显示正确页面的
    # 还有一种返回json，想利用list对应页面中的参数对应也就上面哪一种方式行不通除非刷新整个页面


# 房间查询管理，新建，编辑
@app.route('/rooms')
@login_required
def room():
    pass
