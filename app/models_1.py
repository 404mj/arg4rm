# _*_ coding: utf-8 _*_
from app import Base, db
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
'''
ORM实体类
2016-11-07
zsx
TODO: 没有使用flask-sqlalchemy的db方式，不知道可不可以？
'''


class Arrange(Base):
    __tablename__ = 'arrange'

    arrId = Column('arr_id', Integer, nullable=False,  primary_key=True)
    createTime = Column('create_time', DateTime, nullable=False)
    startTime = Column('start_time', DateTime)
    endTime = Column('end_time', DateTime)
    useNum = Column('use_num', Integer)
    userId = Column(Integer, ForeignKey('room_user.user_id'))
    rmId = Column(Integer, ForeignKey('room.rm_id'))

    def __repr__(self):
        return "arrange:start_time=%s, rm_id=%d" % (self.startTime, self.roomId)


class Room(db.Model):
    __tablename__ = 'room'

    rmId = Column('rm_id', Integer, nullable=False, primary_key=True)
    rmNum = Column('rm_num', String(10))
    capacity = Column('capacity', Integer)
    arranges = relationship("Arrange", backref="room", lazy="dynamic")

    def __repr__(self):
        return "room:rmNum= %s,rmId=%d" % (self.rmNum, self.rmId)


class RoomUser(Base):
    __tablename__ = 'room_user'

    userId = Column('user_id', Integer, nullable=False, primary_key=True)
    name = Column('user_name', String(15), nullable=False)
    arranges = relationship("Arrange", backref=False, lazy="dynamic")
    roleId = Column(Integer, ForeignKey('role.role_id'))

    def __repr__(self):
        return "RoomUser:userId=%d,name=%s" % (self.userId, self.name)


class Role(Base):
    __tablename__ = 'role'

    roleId = Column('role_id', Integer, nullable=False, primary_key=True)
    roleType = Column('role_type', String(10))
    users = relationship("RoomUser", backref="role", lazy="dynamic")

    def __repr__(self):
        return "Role:roleType=%s,roleId = %d" % (self.roleType, self.roleId)
