# -*- coding=utf-8 -*-
from flask_wtf import Form
from flask_wtf.html5 import EmailField
from models import RoomUser, Role, Arrange, Room
from wtforms import StringField, SubmitField, PasswordField, TextAreaField, DateTimeField
from wtforms.validators import DataRequired, length, Regexp, ValidationError
# from wtforms.ext.sqlalchemy.fields import QuerySelectField
# 构建选择框
from werkzeug import secure_filename
from flask_wtf.file import FileField
from hashlib import md5
import re

class LoginForm(Form):
    username = StringField(u'用户名', validators=[DataRequired(), length(1, 25)])
    password = PasswordField(u'密码', validators=[DataRequired()])
    submit = SubmitField(u'登陆')
    def validate_username(self, field):
        username = self.data['username'].strip()
        u = RoomUser.query.filter_by(name=username).all()
        if len(u) < 1:
            raise ValidationError(u"用户不存在，请检查你的用户名")
        else:
            checkpass = md5(self.data['password']+'xuetuis.me').hexdigest()
            if checkpass!=u[0].password:
                raise ValidationError(u"密码错误！")



class RegistrationForm(Form):
    username = StringField(u'用户名', validators=[DataRequired(), length(1, 25)])
    password = PasswordField(u'密码', validators=[DataRequired()])
    confirm = PasswordField(u'重复密码', validators=[DataRequired()])
    email = EmailField(u'邮箱', validators=[DataRequired()])
    submit = SubmitField(u'注册')

    # 验证用户名是否合适规则，是否重复
    def validate_username(self,field):
        username = self.data['username'].strip()
        rematch = re.compile(r"^[A-Za-z][A-Za-z0-9_.]*$")
        if not rematch.match(username):
            raise ValidationError(u"用户名格式不正确！")
        else:
            c_u = RoomUser.query.filter_by(name=username).all()
            if len(c_u) != 0:
                raise ValidationError(u"不好意思，改用户名已经被注册！")
    # 验证密码是否一致
    def validate_password(self, field):
        password = field.data.strip()
        if self.data['confirm'] != password:
            raise ValidationError(u"两次输入的密码不一致！")
    def validate_email(self, field):
        email = field.data.strip()
        if not '@' in email:
            raise ValidationError(u"邮箱格式不正常！")

# 根据日期和房间号查询使用计划
# class QueryArrangesForm(Form):
    # 暂时要求两个条件都不能为空
    # start_time = DateTimeField(u'开始日期', format='%Y-%m-%d %H:%M:%S', validators=[DataRequired()])
# 房间号最好是一个下拉菜单选择，https://segmentfault.com/a/1190000000997917
    # end_time = DateTimeField(u'结束日期', format='%Y-%m-%d %H:%M:%S')
    # room_num = StringField(u'房间号', validators=[DataRequired()])


# 根据日期和人数查找可用的会议室
class QueryRoomsForm(Form):
    pass


# class PostArticleForm(Form):
#     title = StringField(u'标题', validators=[Required(), length(6, 64)])
#     body = TextAreaField(u'内容')
#     category_id = QuerySelectField(u'分类', query_factory=lambda: Category.query.all(
#     ), get_pk=lambda a: str(a.id), get_label=lambda a: a.name)
#     submit = SubmitField(u'发布')
