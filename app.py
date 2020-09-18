import time

from flask import Flask,render_template,request
import Config
from config import LiveFunc
from config import SearchWorkpage
from config import WorkpageFunc
app = Flask(__name__)
configs = Config.config()



@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/search/users')
def search_users():
    configs = Config.config()
    return configs.HEADERS
@app.route('/verlive',methods=["POST",'GET'])
def verify_live():
    if request.method == 'GET':
        return render_template("index.html")
    else:
        url =  request.form.get("live_url")
        print(url)
        SP = LiveFunc.LiveFunc(url)
        result = SP.startplay()
        if result ==1:
            return "正在直播"
        else:
            return "直播停止"


@app.route('/live/like',methods=['POST','GET'])
def like_live():
    if request.method == 'GET':
        return render_template("index3.html")
    if request.method == "POST":
        num = request.form.get("click_num")
        url = request.form.get('live_url')
        SP = LiveFunc.LiveFunc(url)
        for i in range(int(num)):
            SP.livelike()
            time.sleep(1)
        return "点赞完"



@app.route('/search/workpages',methods=["POST",'GET'])
def search_workpage():
    if request.method == 'GET':
        return render_template("index2.html")
    if request.method == 'POST':
        text = request.form.get('search_text')
        page = request.form.get('search_page')
        print(type(page))
        SW = SearchWorkpage.SearchWorkpage(text,int(page))
        tiems = SW.search_workpage(SW.sig_data)
        str = ''
        for i in tiems:
            str = str+i
        return str

@app.route('/workpage/like',methods=['POST','GET'])
def like_workpage():
    if request.method == 'GET':
        return render_template('workpage.html')
    if request.method == "POST":
        url = request.form.get('page_url')
        oper = request.form.get("operator")
        WF = WorkpageFunc.WorkpageFunc(url)
        cc = WF.Workpgelike()
        return cc






if __name__ == '__main__':
    app.run(debug=True)
