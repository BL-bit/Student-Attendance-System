import pymysql
from datetime import date, datetime

# 数据库连接配置
DB_CONFIG = {
    "host": "localhost",
    "port": 3306,
    "user": "root",
    "password": "123456",
    "database": "student_attendance",
    "charset": "utf8mb4"
}

def get_db_conn():
    """获取数据库连接"""
    return pymysql.connect(**DB_CONFIG)

# ========== 学生功能模块 ==========
def student_sign(sid: str):
    """学生签到"""
    conn = get_db_conn()
    cur = conn.cursor()
    today = date.today()
    now_time = datetime.now().time()
    # 判断是否已签到
    cur.execute("SELECT * FROM attendance WHERE sid=%s AND sign_date=%s", (sid, today))
    if cur.fetchone():
        print("今日已完成签到，无需重复操作！")
        cur.close()
        conn.close()
        return
    # 判断迟到：8:30之后算迟到
    status = "正常"
    if now_time > datetime.strptime("08:30:00", "%H:%M:%S").time():
        status = "迟到"
    sql = "INSERT INTO attendance(sid,sign_date,sign_time,status) VALUES(%s,%s,%s,%s)"
    cur.execute(sql, (sid, today, now_time, status))
    conn.commit()
    print(f"签到成功！当前状态：{status}")
    cur.close()
    conn.close()

def apply_leave(sid: str, start: str, end: str, reason: str):
    """提交请假申请"""
    conn = get_db_conn()
    cur = conn.cursor()
    sql = "INSERT INTO leave_apply(sid,leave_start,leave_end,reason) VALUES(%s,%s,%s,%s)"
    cur.execute(sql, (sid, start, end, reason))
    conn.commit()
    print("请假申请提交成功，等待教师审核！")
    cur.close()
    conn.close()

def query_my_attendance(sid: str):
    """学生查询自己考勤记录"""
    conn = get_db_conn()
    cur = conn.cursor()
    cur.execute("SELECT sign_date,sign_time,status FROM attendance WHERE sid=%s ORDER BY sign_date DESC", (sid,))
    res = cur.fetchall()
    print("===== 个人考勤记录 =====")
    for row in res:
        print(f"日期:{row[0]} 签到时间:{row[1]} 状态:{row[2]}")
    cur.close()
    conn.close()

# ========== 教师功能模块 ==========
def audit_leave(lid: int, audit_result: str):
    """教师审核请假单 audit_result: 通过/驳回"""
    conn = get_db_conn()
    cur = conn.cursor()
    sql = "UPDATE leave_apply SET audit_status=%s WHERE lid=%s"
    cur.execute(sql, (audit_result, lid))
    conn.commit()
    print(f"请假单{lid}审核完成，结果：{audit_result}")
    cur.close()
    conn.close()

def class_attendance_stat(class_name: str):
    """教师统计班级考勤"""
    conn = get_db_conn()
    cur = conn.cursor()
    sql = """
    SELECT s.sid,s.s_name,a.status,COUNT(a.aid) sign_count
    FROM student s LEFT JOIN attendance a ON s.sid=a.sid
    WHERE s.s_class=%s GROUP BY s.sid,s.s_name,a.status
    """
    cur.execute(sql, (class_name,))
    data = cur.fetchall()
    print(f"===== {class_name} 考勤统计 =====")
    for item in data:
        print(f"学号:{item[0]} 姓名:{item[1]} 考勤状态:{item[2]} 签到次数:{item[3]}")
    cur.close()
    conn.close()

# ========== 管理员功能模块 ==========
def add_student(sid: str, name: str, cls: str):
    """管理员新增学生"""
    conn = get_db_conn()
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO student(sid,s_name,s_class) VALUES(%s,%s,%s)", (sid, name, cls))
        conn.commit()
        print("学生新增成功！")
    except Exception as e:
        print("学号重复，新增失败！", e)
    cur.close()
    conn.close()

# ========== 程序交互入口 ==========
def main():
    print("===== 学生考勤管理系统 =====")
    print("1.学生签到  2.提交请假  3.查询个人考勤")
    print("4.教师审核请假  5.班级考勤统计  6.管理员新增学生")
    op = input("请输入功能编号：")
    if op == "1":
        sid = input("输入学生学号：")
        student_sign(sid)
    elif op == "2":
        sid = input("学号：")
        s = input("请假开始日期(yyyy-mm-dd)：")
        e = input("请假结束日期(yyyy-mm-dd)：")
        r = input("请假原因：")
        apply_leave(sid, s, e, r)
    elif op == "3":
        sid = input("学号：")
        query_my_attendance(sid)
    elif op == "4":
        lid = int(input("请假单ID："))
        res = input("审核结果(通过/驳回)：")
        audit_leave(lid, res)
    elif op == "5":
        cls = input("班级名称：")
        class_attendance_stat(cls)
    elif op == "6":
        sid = input("学生学号：")
        name = input("学生姓名：")
        cls = input("班级：")
        add_student(sid, name, cls)
    else:
        print("输入错误！")

if __name__ == "__main__":
    main()