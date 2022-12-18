# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from flask import Flask, render_template, request, session, redirect
import dao as DB
import json, os
from flask_apscheduler import APScheduler
from functools import wraps

ipaddr = 'localhost'
user = 'root'
password = 'microsys'
# DB.init_database(ip=ipaddr, usr=user, pwd=password)

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
app.config['SCHEDULER_API_ENABLED'] = True
scheduler = APScheduler()


@scheduler.task('cron', id='do_job', day='*', hour='23', minute='40', second='05')
def do_job():
    DB.multi_insert_data(ip=ipaddr, usr=user, pwd=password)


# 装饰器装饰多个视图函数
def wrapper(func):
    @wraps(func)  # 保存原来函数的所有属性,包括文件名
    def inner(*args, **kwargs):
        # 校验session
        if session.get("user"):
            ret = func(*args, **kwargs)
            return ret
        else:
            return redirect("/login")

    return inner


@app.route("/contract_law")
def get_contract_law():
    results = DB.rand_find_data(ip=ipaddr, usr=user, pwd=password)
    if len(results) == 0:
        return 'error'
    return render_template("contract_law.html", results=results)


@app.route("/labor_law")
def get_labor_law():
    results = DB.rand_find_data(ip=ipaddr, usr=user, pwd=password, law_name="laborLaw")
    if len(results) == 0:
        return 'error'
    return render_template("labor_law.html", results=results)


@app.route("/traffic_safety_law")
def get_traffic_safety_law():
    results = DB.rand_find_data(ip=ipaddr, usr=user, pwd=password, law_name="trafficSafetyLaw")
    if len(results) == 0:
        return 'error'
    return render_template("traffic_safety_law.html", results=results)


@app.route("/marriage_law")
def get_marriage_law():
    results = DB.rand_find_data(ip=ipaddr, usr=user, pwd=password, law_name="marriageLaw")
    if len(results) == 0:
        return 'error'
    return render_template("marriage_law.html", results=results)


@app.route("/succession_law")
def get_succession_law():
    results = DB.rand_find_data(ip=ipaddr, usr=user, pwd=password, law_name="successionLaw")
    if len(results) == 0:
        return 'error'
    return render_template("succession_law.html", results=results)


@app.route("/home")
def get_home():
    return render_template("home.html")


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == "GET":
        return render_template("login.html")
    else:
        data = json.loads(request.data)
        user_name = data.get("account")
        pwd = data.get("pwd")
        session["user"] = user_name
        results = DB.find_user(ip=ipaddr, usr=user, pwd=password, account=user_name, password=pwd)
        if len(results) == 0:
            return "error"
        else:
            return "ok"


@app.route("/register/", methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        data = json.loads(request.data)
        account = data.get("account")
        pwd = data.get("pwd")
        pwd1 = data.get("pwd1")
        telephone = data.get("telephone")
        print(account, pwd, pwd1, telephone)
        results = DB.find_is_exist(ip=ipaddr, usr=user, pwd=password, account=account, telephone=telephone)
        if len(results) != 0:
            return "error"
        else:
            DB.insert_user(ip=ipaddr, usr=user, pwd=password, account=account, password=pwd, passwd=pwd1,
                           telephone=telephone)
            return "ok"
    else:
        return render_template("register.html")


@app.route("/forget", methods=['GET', 'POST'])
def forget():
    if request.method == 'GET':
        return render_template("forget.html")
    else:
        data = json.loads(request.data)
        pwd = data.get("pwd")
        pwd1 = data.get("pwd1")
        telephone = data.get("telephone")
        results = DB.find_is_exist(ip=ipaddr, usr=user, pwd=password, telephone=telephone)
        if len(results) == 0:
            return "error"
        else:
            DB.update_user(ip=ipaddr, usr=user, pwd=password, password=pwd, passwd=pwd1,
                           telephone=telephone)
            return "ok"


@app.route("/my_leave")
@wrapper
def my_leave():
    if request.method == "GET":
        title = request.args.get("title")
        start_date = request.args.get("start_date")
        end_date = request.args.get("end_date")
        print(title)
        print(start_date)
        print(end_date)
        if (title == None) & (start_date == None) & (end_date == None):
            account = session.get("user")
            id = DB.find_user_id(ip=ipaddr, usr=user, pwd=password, account=account)
            results = DB.find_user_title(ip=ipaddr, usr=user, pwd=password, id=id)
            res_list = []
            for result in results:
                res_list.append(result)
            return render_template("my_leave.html", results=res_list)
        if (title != "") & ("NaN" not in start_date) & ("NaN" not in end_date):
            account = session.get("user")
            id = DB.find_user_id(ip=ipaddr, usr=user, pwd=password, account=account)
            results = DB.search_one_title(ip=ipaddr, usr=user, pwd=password, id=id, title=title, start=start_date, end=end_date)
            print(results)
            res_list = []
            for result in results:
                res_list.append(result)
            print(res_list)
            return res_list
        elif (title != "") | (("NaN" not in start_date) & ("NaN" not in end_date)):
            account = session.get("user")
            id = DB.find_user_id(ip=ipaddr, usr=user, pwd=password, account=account)
            results = DB.search_title(ip=ipaddr, usr=user, pwd=password, id=id, title=title, start=start_date,
                                          end=end_date)
            print(results)
            res_list = []
            for result in results:
                res_list.append(result)
            print(res_list)
            return res_list
        elif (title == "") & ("NaN" in start_date) & ("NaN" in end_date):
            return "ok"
        else:
            return "error"


@app.route("/publish_leave", methods=['GET', 'POST'])
@wrapper
def publish_leave():
    if request.method == "GET":
        return render_template("publish_leave.html")
    else:
        data = json.loads(request.data)
        title = data.get("title")
        content = data.get("content")
        is_public = data.get("is_public")
        account = session.get("user")
        DB.insert_leave(ip=ipaddr, usr=user, pwd=password, title=title, content=content, is_public=is_public,
                        account=account)
        return "ok"


@app.route("/public_leave")
def public_leave():
    results = DB.find_public_title(ip=ipaddr, usr=user, pwd=password)
    res_list = []
    for result in results:
        res_list.append(result)
    return render_template("public_leave.html", results=res_list)


@app.route("/relay_leave")
def relay_leave():
    return render_template("relay_leave.html")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    scheduler.init_app(app)
    scheduler.start()
    app.run()
