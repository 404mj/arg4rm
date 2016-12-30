# _*_ coding: utf-8 _*_
from app import db
from utils import formatTime
from flask_login import UserMixin
# from sqlalchemy.orm import relationship
# from sqlalchemy import Integer, String, DateTime, ForeignKey
'''
ORM实体类
2016-11-07
zsx
TODO: 没有使用flask-sqlalchemy的db方式，不知道可不可以？
'''

# 使用计划
class Arrange(db.Model):
    __tablename__ = 'arrange'

    arrId = db.Column('arr_id', db.Integer, primary_key=True)
    createTime = db.Column('create_time', db.DateTime)
    startTime = db.Column('start_time', db.DateTime)
    endTime = db.Column('end_time', db.DateTime)
    useNum = db.Column('use_num', db.Integer)
# 描述映射关系
    userId = db.Column('user_id', db.Integer, db.ForeignKey('room_user.user_id'))
# 下面这一行是必须添加的，为的是让多的以防能够引用其所属的一的对象,并且要在一的一方那里写上cascade，orm就是事儿多，
# 让我想起来了java中的jpa的关系映射
# TODO: 还是要多读文档呀！
    user = db.relationship('RoomUser')
    rmId = db.Column('rm_id', db.Integer, db.ForeignKey('room.rm_id'))
    rm = db.relationship('Room')

    def __repr__(self):
        return "arrange:start_time=%s, rm_id=%d" % (self.startTime,self.rmId)

    def serialize(self):
        return {
        'createTime': formatTime(self.createTime),
        'startTime': formatTime(self.startTime),
        'endTime': formatTime(self.endTime),
        'linked_username': self.user.name,
        'linked_rmNum': self.rm.rmNum
        }



# 房间实体
class Room(db.Model):
    __tablename__ = 'room'

    rmId = db.Column('rm_id', db.Integer,primary_key=True)
    rmNum = db.Column('rm_num', db.String(10))
    capacity = db.Column('capacity', db.Integer)
    # 一个房间有多个使用计划
    arranges = db.relationship("Arrange", backref = "room", lazy = "dynamic", cascade="all, delete-orphan")

    def __repr__(self):
        return "room:rmNum= %s,rmId=%d" % (self.rmNum, self.rmId)

# 使用者联系人实体，有多个使用计划
class RoomUser(db.Model, UserMixin):
    __tablename__ = 'room_user'

    userId = db.Column('user_id', db.Integer,primary_key=True)
    name = db.Column('user_name', db.String(15))
    email = db.Column('email',db.String(25))
    password = db.Column('password',db.String(50))
    # 一个用户有多个使用计划
    arranges = db.relationship("Arrange", backref = "room_user", lazy = "dynamic",  cascade="all, delete-orphan")
    # 添加"role_id"解决1054, "Unknown column 'room_user.roleId' in 'field list'"
    roleId = db.Column('role_id', db.Integer)
    # , db.ForeignKey('role.role_id')

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.userId)

    def is_admin(self):
        print '-------roleId : %s' % str(self.roleId)
        return self.roleId == 2

    def __repr__(self):
        return "RoomUser:userId=%d,name=%s" % (self.userId, self.name)


# 角色实体，与用户一对多
class Role(db.Model):
    __tablename__ = 'role'

    roleId = db.Column('role_id', db.Integer, primary_key=True)
    roleType = db.Column('role_type', db.String(10))
    # users = db.relationship("RoomUser", backref = "role", lazy = "dynamic")

    def __repr__(self):
        return "Role:roleType=%s,roleId = %d" % (self.roleType, self.roleId)
