const baseUrl = "http://127.0.0.1:5000/api";

// 登录
async function login(){
    const role = document.getElementById("role").value;
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;
    const res = await fetch(`${baseUrl}/login`,{
        method:"POST",
        headers:{"Content-Type":"application/json"},
        body:JSON.stringify({username,password,role})
    }).then(r=>r.json());
    document.getElementById("msg").innerText = res.msg;
    if(res.code === 200){
        localStorage.setItem("user",username);
        if(role === "student") location.href = "student.html";
        else if(role === "teacher") location.href = "teacher.html";
        else location.href = "admin.html";
    }
}

// 学生签到
async function sign(){
    const sid = localStorage.getItem("user");
    const res = await fetch(`${baseUrl}/sign`,{
        method:"POST",
        headers:{"Content-Type":"application/json"},
        body:JSON.stringify({sid})
    }).then(r=>r.json());
    alert(res.msg);
}

// 学生提交请假
async function submitLeave(){
    const sid = localStorage.getItem("user");
    const start = document.getElementById("leaveStart").value;
    const end = document.getElementById("leaveEnd").value;
    const reason = document.getElementById("leaveReason").value;
    const res = await fetch(`${baseUrl}/leave/apply`,{
        method:"POST",
        headers:{"Content-Type":"application/json"},
        body:JSON.stringify({sid,start,end,reason})
    }).then(r=>r.json());
    alert(res.msg);
}

// 查询个人考勤
async function getMyAttendance(){
    const sid = localStorage.getItem("user");
    const res = await fetch(`${baseUrl}/attendance/my`,{
        method:"POST",
        headers:{"Content-Type":"application/json"},
        body:JSON.stringify({sid})
    }).then(r=>r.json());
    let html = "<table class='table'><tr><th>日期</th><th>签到时间</th><th>状态</th></tr>";
    res.data.forEach(item=>{
        html += `<tr><td>${item.date}</td><td>${item.time}</td><td>${item.status}</td></tr>`;
    })
    html += "</table>";
    document.getElementById("attendanceTable").innerHTML = html;
}

// ========== 教师端功能 ==========
// 审核请假
async function auditLeave() {
    const lid = document.getElementById("leaveId").value;
    const result = document.getElementById("auditResult").value;
    const res = await fetch(`${baseUrl}/leave/audit`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ lid, result })
    }).then(r => r.json());
    document.getElementById("auditMsg").innerText = res.msg;
}

// 查询班级考勤统计
async function getClassAttendance() {
    const cls = document.getElementById("className").value;
    const res = await fetch(`${baseUrl}/attendance/class`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ cls })
    }).then(r => r.json());

    let html = `<table class="table table-striped">
        <tr><th>学号</th><th>姓名</th><th>考勤状态</th><th>签到次数</th></tr>`;
    res.data.forEach(item => {
        html += `<tr>
            <td>${item.sid}</td>
            <td>${item.name}</td>
            <td>${item.status}</td>
            <td>${item.count}</td>
        </tr>`;
    });
    html += `</table>`;
    document.getElementById("classTable").innerHTML = html;
}

// ========== 管理员端功能 ==========
async function addNewStudent() {
    const sid = document.getElementById("newSid").value;
    const name = document.getElementById("newName").value;
    const cls = document.getElementById("newClass").value;
    const res = await fetch(`${baseUrl}/student/add`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ sid, name, cls })
    }).then(r => r.json());
    document.getElementById("adminMsg").innerText = res.msg;
}