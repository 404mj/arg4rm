SET SESSION FOREIGN_KEY_CHECKS=0;

/* Drop Tables */

DROP TABLE if exists arrange;
DROP TABLE if exists role;
DROP TABLE if exists room;
DROP TABLE if exists room_user;




/* Create Tables */

CREATE TABLE arrange(
	arr_id int not null AUTO_INCREMENT,
	create_time datetime not null,
	start_time datetime,
	end_time datetime,
	-- 该计划包含的使用人数
	use_num int,
	-- 联系人，关联到user表
	user_id int not null,
	-- 该计划使用的房间号，关联到room表
	rm_id int not null,
	PRIMARY KEY (arr_id)
);


CREATE TABLE role (
    role_id int not null AUTO_INCREMENT,
    role_type VARCHAR(10) not null,
    PRIMARY KEY (role_id)
);


CREATE TABLE room(
	rm_id int not null AUTO_INCREMENT,
	rm_num VARCHAR(10),
	capacity int,
	PRIMARY KEY (rm_id)
);

CREATE TABLE room_user(
	user_id int not null AUTO_INCREMENT,
	user_name VARCHAR(15),
	-- 用户的角色，关联到role表
	role_id int not null,
	PRIMARY KEY (user_id)
);

--准备第一组role数据
insert into role values (1,'use'),(2,'manage');

--增加email字段
alter table room_user add COLUMN email vaarchar(25);

--增加密码字段
alter table room_user add column password varchar(50);

--增加管理源用户admin-admin
insert into room_user values (4,'admin',2,'admin@bjut.edu.cn', '17dde7811f1b41d1d6bb5f0b4eecba2d');

--增加arrange测试数据
insert into arrange (create_time, start_time, end_time, use_num, user_id, rm_id) values ('2016-11-1 08:20:00', '2016-11-3 08:00:00', '2016-11-3 12:00:00', 50, 5, 1);
insert into arrange (create_time, start_time, end_time, use_num, user_id, rm_id) values ('2016-10-30 09:25:00', '2016-11-3 13:00:00', '2016-11-3 14:00:00', 70, 5, 1);
insert into arrange (create_time, start_time, end_time, use_num, user_id, rm_id) values ('2016-11-2 10:10:00', '2016-11-3 15:00:00', '2016-11-3 18:00:00', 20, 5, 1);
insert into arrange (create_time, start_time, end_time, use_num, user_id, rm_id) values ('2016-11-2 18:20:00', '2016-11-3 08:00:00', '2016-11-3 12:00:00', 90, 5, 2);
insert into arrange (create_time, start_time, end_time, use_num, user_id, rm_id) values ('2016-11-1 13:00:00', '2016-11-4 08:00:00', '2016-11-3 11:00:00', 40, 5, 1);
	-- select * from arrange where create_time > '2016-11-01 13:00:00'
-- 	+--------+---------------------+---------------------+---------------------+---------+---------+-------+
-- | arr_id | create_time         | start_time          | end_time            | use_num | user_id | rm_id |
-- +--------+---------------------+---------------------+---------------------+---------+---------+-------+
-- |      3 | 2016-11-02 10:10:00 | 2016-11-03 15:00:00 | 2016-11-03 18:00:00 |      20 |       5 |     1 |
-- |      4 | 2016-11-02 18:20:00 | 2016-11-03 08:00:00 | 2016-11-03 12:00:00 |      90 |       5 |     2 |
-- +--------+---------------------+---------------------+---------------------+---------+---------+-------+
-- 2 rows in set (0.01 sec)
