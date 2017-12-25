# -*- coding: utf-8 -*-
from nimin import app
from flask import Flask, render_template, session, redirect, url_for, request, g, flash, send_from_directory,abort
from mylib import PostList,Post
from random import randint as randint

def preVeri(request):
    if request.form.get('new',type=int)==2:
        author=0
    else:
        author = session.get('name')
    if not author:
        preName=['红','橙','黄','绿','银','蓝','靛','紫','青','黑','白','灰','褐','棕','赤','黛','茶','缥','玄','粉','金','绀','铅','赭','橡','曙','草','柳','藤']
        secName=['杯','杖','剑','书','笔','钥','刃','影','冰','瓶','门','帆','盾','庭','蔓','狗','果','馆','棺','楼','路','岭','鹿','旅','庐','键','菊','戒','枪','雪','星','箱','网','碟','月','原','雨']
        author = preName[randint(0,28)]+'色的'+secName[randint(0,36)]+str(randint(10,99))
        session.permanent = True
        session['name'] = author
    img = request.form.get('img')
    content = request.form.get('content')
    quote = request.form.get('quote',type=int)
    section = request.form.get('section',type=int)
    owner = request.form.get('owner',type=int)
    ip = request.headers.get('X-Real-IP')
    tid=Post().newPost(author,img,quote,content,section,ip,owner)
    return tid

#异常处理
@app.errorhandler(500)
def page_error(e):
    return render_template('error.html'), 500
@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html'), 404
@app.errorhandler(403)
def page_not_found(e):
    return render_template('error403.html'), 403

#自动关闭数据库连接
@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'db'):
        g.db.close()

@app.route('/')
def index():
    return redirect(url_for('page',pid = 1,sid=0))

@app.route('/p<int:sid>/<int:pid>', methods=['POST','GET'])
def page(sid,pid):
    if request.method == "POST":
        tid = preVeri(request)
        return redirect(url_for('posts',tid = tid,pid=1))
    curPage = PostList(section=sid,pid=pid)
    if curPage.getAl():
        return render_template('page.html',results = curPage.results, pagn = curPage.pagn,sid=sid)
    abort(404)

@app.route('/t/<int:tid>/<int:pid>', methods=['POST','GET'])
def posts(tid,pid):
    if request.method == "POST":
        tid = preVeri(request)
        return redirect(url_for('posts',tid = tid,pid=pid))
    curArti = Post(id=tid)
    if curArti.getIt(pid=pid):
        return render_template('article.html',curArti = curArti)
    abort(404)

@app.route('/dt/<int:tid>/<int:pid>')
def dire(tid,pid):
    curArti = Post(id=tid)
    pg = curArti.getPg(pid=pid)
    return redirect("/t/"+str(tid)+"/"+str(pg)+"#rep"+str(pid))

@app.route('/del/<int:tid>')
def dele(tid):
    if session.get('log'):
        Post().dele(tid)
    return "Success"

@app.route('/robots.txt')
def static_from_root():
    return send_from_directory(app.static_folder, request.path[1:])