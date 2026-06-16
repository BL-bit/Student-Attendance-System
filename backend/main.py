import pymysql
from datetime import date, datetime
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # 允许前端跨域访问

# 数据库配置
DB_CONFIG = {
    "host": "localhost",
    "port": 3306,
    "user": "root",
    "password": "123456",
    "database": "student_attendance",
    "charset": "utf8mb4"
}

def get_db_conn():
    return pymysql.connect(**DB_CONFIG)

# ===================== 登录接口 =====================
@app.route("/api/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    pwd = data.get("password")
    role = data.get("role")
    conn = get_db_conn()
    cur = conn.cursor()
    if role == "student":
        cur.execute("SELECT s_name FROM student WHERE sid=%s AND s_password=%s", (username, pwd))
        res = cur.fetchone()
    elif role == "teacher":
        cur.execute("SELECT t_name FROM teacher WHERE t_username=%s AND t_password=%s", (username, pwd))
        res = cur.fetchone()
    elif role == "admin":
        cur.execute("SELECT name FROM admin WHERE username=%s AND password=%s", (username, pwd))
        res = cur.fetchone()
    else:
        return jsonify({"code": 400, "msg": "角色错误"})
    cur.close()
    conn.close()
    if res:
        return jsonify({"code": 200, "msg": "登录成功", "name": res[0]})
    else:
        return jsonify({"code": 401, "msg": "账号或密码错误"})

# ===================== 学生接口 =====================
# 签到
@app.route("/api/sign", methods=["POST"])
def sign():
    sid = request.json.get("sid")
    conn = get_db_conn()
    cur = conn.cursor()
    today = date.today()
    now_time = datetime.now().time()
    cur.execute("SELECT sid FROM student WHERE sid=%s", (sid,))
    if not cur.fetchone():
        cur.close()
        conn.close()
        return jsonify({"code": 400, "msg": "学号不存在"})
    cur.execute("SELECT * FROM attendance WHERE sid=%s AND sign_date=%s", (sid, today))
    if cur.fetchone():
        cur.close()
        conn.close()
        return jsonify({"code": 400, "msg": "今日已签到"})
    status = "正常"
    if now_time > datetime.strptime("08:30:00", "%H:%M:%S").time():
        status = "迟到"
    cur.execute("INSERT INTO attendance(sid,sign_date,sign_time,status) VALUES(%s,%s,%s,%s)",(sid,today,now_time,status))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"code":200,"msg":f"签到成功，状态：{status}"})

# 提交请假
@app.route("/api/leave/apply", methods=["POST"])
def leave_apply():
    d = request.json
    sid = d["sid"]
    s = d["start"]
    e = d["end"]
    r = d["reason"]
    conn = get_db_conn()
    cur = conn.cursor()
    cur.execute("INSERT INTO leave_apply(sid,leave_start,leave_end,reason) VALUES(%s,%s,%s,%s)",(sid,s,e,r))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"code":200,"msg":"请假申请提交成功，等待审核"})

# 查询个人考勤
@app.route("/api/attendance/my", methods=["POST"])
def my_attendance():
    sid = request.json.get("sid")
    conn = get_db_conn()
    cur = conn.cursor()
    cur.execute("SELECT sign_date,sign_time,status FROM attendance WHERE sid=%s ORDER BY sign_date DESC",(sid,))
    data = cur.fetchall()
    cur.close()
    conn.close()
    list_data = []
    for item in data:
        list_data.append({
            "date": str(item[0]),
            "time": str(item[1]),
            "status": item[2]
        })
    return jsonify({"code":200,"data":list_data})

# ===================== 教师接口 =====================
# 审核请假
@app.route("/api/leave/audit", methods=["POST"])
def audit_leave():
    lid = request.json["lid"]
    res = request.json["result"]
    conn = get_db_conn()
    cur = conn.cursor()
    cur.execute("UPDATE leave_apply SET audit_status=%s WHERE lid=%s",(res,lid))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"code":200,"msg":"审核完成"})

# 班级考勤统计
@app.route("/api/attendance/class", methods=["POST"])
def class_stat():
    cls = request.json["cls"]
    conn = get_db_conn()
    cur = conn.cursor()
    sql = """
    SELECT s.sid,s.s_name,a.status,COUNT(a.aid) sign_count
    FROM student s LEFT JOIN attendance a ON s.sid=a.sid
    WHERE s.s_class=%s GROUP BY s.sid,s.s_name,a.status
    """
    cur.execute(sql,(cls,))
    data = cur.fetchall()
    cur.close()
    conn.close()
    res_list = []
    for i in data:
        res_list.append({
            "sid":i[0],
            "name":i[1],
            "status":i[2],
            "count":i[3]
        })
    return jsonify({"code":200,"data":res_list})

# ===================== 管理员接口 =====================
@app.route("/api/student/add", methods=["POST"])
def add_student():
    d = request.json
    sid = d["sid"]
    name = d["name"]
    cls = d["cls"]
    conn = get_db_conn()
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO student(sid,s_name,s_class) VALUES(%s,%s,%s)",(sid,name,cls))
        conn.commit()
        msg = "新增学生成功"
    except Exception as e:
        msg = "学号已存在，新增失败"
    cur.close()
    conn.close()
    return jsonify({"code":200,"msg":msg})

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
