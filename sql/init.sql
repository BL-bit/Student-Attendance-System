-- 学生考勤管理系统数据库
CREATE DATABASE IF NOT EXISTS student_attendance DEFAULT CHARACTER SET utf8mb4;
USE student_attendance;

-- 管理员表
CREATE TABLE admin(
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(30) NOT NULL UNIQUE,
    password VARCHAR(30) NOT NULL,
    name VARCHAR(20) NOT NULL
);

-- 教师表
CREATE TABLE teacher(
    tid INT PRIMARY KEY AUTO_INCREMENT,
    t_username VARCHAR(30) NOT NULL UNIQUE,
    t_password VARCHAR(30) NOT NULL,
    t_name VARCHAR(20) NOT NULL,
    t_course VARCHAR(50)
);

-- 学生表
CREATE TABLE student(
    sid VARCHAR(20) PRIMARY KEY,
    s_name VARCHAR(20) NOT NULL,
    s_class VARCHAR(30) NOT NULL,
    s_password VARCHAR(30) DEFAULT '123456'
);

-- 考勤记录表
CREATE TABLE attendance(
    aid INT PRIMARY KEY AUTO_INCREMENT,
    sid VARCHAR(20) NOT NULL,
    sign_date DATE NOT NULL,
    sign_time TIME,
    status ENUM('正常','迟到','缺勤') DEFAULT '正常',
    FOREIGN KEY (sid) REFERENCES student(sid)
);

-- 请假表
CREATE TABLE leave_apply(
    lid INT PRIMARY KEY AUTO_INCREMENT,
    sid VARCHAR(20) NOT NULL,
    leave_start DATE NOT NULL,
    leave_end DATE NOT NULL,
    reason TEXT,
    audit_status ENUM('待审核','通过','驳回') DEFAULT '待审核',
    FOREIGN KEY (sid) REFERENCES student(sid)
);

-- 测试数据
INSERT INTO admin(username,password,name) VALUES ('admin','admin123','系统管理员');
INSERT INTO teacher(t_username,t_password,t_name,t_course) VALUES ('teacher1','t123456','张老师','Python程序设计');
INSERT INTO student(sid,s_name,s_class) VALUES ('221090232','胡洋','计科2201'),('221090125','郑伯滨','计科2201');