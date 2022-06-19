# -*- coding: utf-8 -*-
# @Date    : 2022-02-19 20:53:54
# @Author  : SKD

import git
import time
import requests
import os
import random
import pandas as pd
import math
import xgboost as xgb
from sklearn.metrics import *
import re
from bs4 import BeautifulSoup, NavigableString, Tag
import json
import logging
from datetime import datetime
from flask import Flask, g, jsonify, make_response, request
from flask_cors import CORS
from flask_httpauth import HTTPBasicAuth
from flask_sqlalchemy import SQLAlchemy
# from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import Serializer
from itsdangerous import BadSignature, SignatureExpired
from passlib.apps import custom_app_context

from flask_sqlalchemy import SQLAlchemy
#引入SQLAlchemy,它是一个很强大的关系型数据库框架
db = SQLAlchemy()

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

# r'/*' 是通配符，让本服务器所有的 URL 都允许跨域请求
CORS(app, resources=r'/*')
app.config['SECRET_KEY'] = 'hard to guess string'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_RECORD_QUERIES'] = True
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
#     os.path.join(basedir, 'data.sqlite')

app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:skd1116@localhost:3306/flasktest?charset=utf8mb4"
#如果设置成 True (默认情况)，Flask-SQLAlchemy 将会追踪对象的修改并且发送信号。这需要额外的内存， 如果不必要的可以禁用它。
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db.init_app(app)
auth = HTTPBasicAuth()
CSRF_ENABLED = True
app.debug = True

headers={
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
    # "Cookie": ""
}
def get_repo_name(repoid):
    if (repoid==1):
        return "FFmpeg"
    elif (repoid==2):
        return "ImageMagick"
    elif (repoid==3):
        return "jenkins"
    elif (repoid==4):
        return "linux"
    elif (repoid==5):
        return "moodle"
    elif (repoid==6):
        return "openssl"
    elif (repoid==7):
        return "php-src"
    elif (repoid==8):
        return "phpmyadmin"
    elif (repoid==9):
        return "qemu"
    elif (repoid==10):
        return "wireshark"

def get_rank(df, sortby, ascending=False):
    gb = df.groupby('cve')
    l = []
    for item1, item2 in gb:
        item2 = item2.reset_index()
        item2 = item2.sort_values(sortby + ['commit_id'], ascending=ascending)
        item2 = item2.reset_index(drop=True).reset_index()
        l.append(item2[['index', 'level_0']])

    df = pd.concat(l)
    df['rank'] = df['level_0']+1
    df = df.sort_values(['index'], ascending=True).reset_index(drop=True)
    return df['rank']

# name: /[\u4e00-\u9fa5]/
# phone: /^1[34578]\d{9}$/
# class: /[a-zA-Z0-9_\u4e00-\u9fa5]+/
# email: /^\w+@\w+\.\w+$/


# @auth.verify_password
# def verify_password(name_or_token, password):
#     print("1:",password)
#     if not name_or_token:
#         return False
#     name_or_token = re.sub(r'^"|"$', '', name_or_token)
#     admin = Admin.verify_auth_token(name_or_token)
#     if not admin:
#         admin = Admin.query.filter_by(name=name_or_token).first()
#         if not admin or not admin.verify_password(password):
#             return False
#     g.admin = admin
#     return True


# @app.route('/api/login', methods=['POST'])
# # @auth.login_required
# def get_auth_token():
#     token = g.admin.generate_auth_token()
#     print("1242")
#     return jsonify({'code': 200, 'msg': "登录成功", 'token': token.decode('ascii'), 'name': g.admin.name})
#
#
# @app.route('/api/setpwd', methods=['POST'])
# # @auth.login_required
# def set_auth_pwd():
#     data = json.loads(str(request.data, encoding="utf-8"))
#     admin = Admin.query.filter_by(name=g.admin.name).first()
#     if admin and admin.verify_password(data['oldpass']) and data['confirpass'] == data['newpass']:
#         admin.hash_password(data['newpass'])
#         return jsonify({'code': 200, 'msg': "密码修改成功"})
#     else:
#         return jsonify({'code': 500, 'msg': "请检查输入"})

@app.route('/api/CommitPage', methods=['GET'])
def get_gitcommit_list():
    page = request.args.get('page', 1, type=int)
    des = request.args.get('des', 1, type=str)
    repoid =request.args.get('repoid',0,type=int)
    if (des == ""):
        if (repoid==0):
            ret = db.session.execute(" SELECT sum(commit_num) from repo")
        else:
            reponame=get_repo_name(repoid)
            ret = db.session.execute(" SELECT sum(commit_num) from repo where repo_name=\'{}\'".format(reponame))
    else:
        if(repoid==0):
            ret = db.session.execute(" select count(*) from totalcommit where totalcommit.description like \'%{}%\'".format(des))
        else:
            reponame=get_repo_name(repoid)
            ret = db.session.execute(
                " select count(*) from totalcommit where repo_name=\'{}\' totalcommit.description like \'%{}%\'".format(reponame,des))
    cds = ret.fetchall()
    L = int(cds[0][0])
    page_size = 20
    print("L:",L)
    if (des == ""):
        if(repoid==0):
            ret = db.session.execute(" select * from totalcommit limit {},20".format((page-1)*20))
        else:
            reponame=get_repo_name(repoid)
            ret = db.session.execute(" select * from totalcommit where repo_name=\'{}\' limit {},20".format(reponame,(page - 1) * 20))
    else:
        if(repoid==0):
            ret = db.session.execute(" select * from totalcommit where totalcommit.description like \'%{}%\' limit {},20".format(des,(page - 1) * 20))
        else:
            ret = db.session.execute(
                " select * from totalcommit where repo_name=\'{}\' totalcommit.description like \'%{}%\' limit {},20".format(
                    reponame,des, (page - 1) * 20))
    cds = ret.fetchall()
    columns = ["commit_id","repo_name","author","description","commit_time"]
    list=[]
    for u in cds:
        result = {}
        for i in range(5):
            result[columns[i]] =u[i+1]
        list.append(result)
    return jsonify({
        'code': 200,
        'total': L,
        'page_size': page_size,
        'infos': list
    })

@app.route('/api/CVEPage', methods=['GET'])
def get_gitCVE_list():
    page = request.args.get('page', 1, type=int)
    cve=request.args.get('CVE',1,type=str)
    repoid=request.args.get('repoid',0,type=int)
    if (cve==""):
        if (repoid==0):
            ret = db.session.execute(" select count(*) from cve")
        else:
            reponame=get_repo_name(repoid)
            ret = db.session.execute(" select count(*) from cve where repo_name=\'{}\'".format(reponame))
    else:
        if (repoid==0):
            ret = db.session.execute(" select count(*) from cve where CVE_id  like \'%{}%\'".format(cve))
        else:
            reponame=get_repo_name(repoid)
            ret = db.session.execute(" select count(*) from cve where repo_name==\'{}\' and CVE_id  like \'%{}%\'".format(reponame,cve))
    cds = ret.fetchall()
    L = cds[0][0]
    page_size = 20
    print("L:",L)
    if (cve == ""):
        if (repoid==0):
            ret = db.session.execute(" SELECT a.CVE_id,b.Description,a.repo_name,a.cvetime,a.patch_gitcommit,a.score,a.S_des,a.cwe_id,a.cwe_name,b.Status,b.Phase from cve a,all_cve b where a.`CVE_id`=b.`CVE_id` limit {},20".format((page-1)*20))
        else:
            reponame=get_repo_name(repoid)
            ret = db.session.execute(
                " SELECT a.CVE_id,b.Description,a.repo_name,a.cvetime,a.patch_gitcommit,a.score,a.S_des,a.cwe_id,a.cwe_name,b.Status,b.Phase from cve a,all_cve b where a.`CVE_id`=b.`CVE_id` and a.`repo_name`=\'{}\' limit {},20".format(
                    reponame,(page - 1) * 20))
    else:
        if (repoid==0):
            ret = db.session.execute(" SELECT a.CVE_id,b.Description,a.repo_name,a.cvetime,a.patch_gitcommit,a.score,a.S_des,a.cwe_id,a.cwe_name,b.Status,b.Phase from cve a,all_cve b where a.`CVE_id`=b.`CVE_id` and a.`CVE_id` like \'%{}%\' limit {},20".format(cve,(page-1)*20))
        else:
            reponame=get_repo_name(repoid)
            ret = db.session.execute(
                " SELECT a.CVE_id,b.Description,a.repo_name,a.cvetime,a.patch_gitcommit,a.score,a.S_des,a.cwe_id,a.cwe_name,b.Status,b.Phase from cve a,all_cve b where a.`CVE_id`=b.`CVE_id` and a.`repo_name`=\'{}\' and a.`CVE_id` like \'%{}%\' limit {},20".format(
                    reponame,cve, (page - 1) * 20))
    cds = ret.fetchall()
    columns = ["CVE_id","Description","repo_name","cvetime","patch_gitcommit","score","S_des","cwe_id","cwe_name","Status","Phase"]
    list=[]
    for u in cds:
        result = {}
        for i in range(len(columns)):
            result[columns[i]] =u[i]
        list.append(result)
    return jsonify({
        'code': 200,
        'total': L,
        'page_size': page_size,
        'infos': list
    })

@app.route('/api/GetCommitPieChart', methods=['GET'])
# @auth.login_required
def getcommitPieChart():
    # ret = db.session.execute("select repo_name,count(*) from totalcommit GROUP BY repo_name")
    ret = db.session.execute("select repo_name,commit_num from repo")
    cds = ret.fetchall()
    columns=["repo_name","commit_num"]
    total=0
    list=[]
    repo=[]
    for u in cds:
        result={}
        for i in range(len(columns)):
            result[columns[i]]=u[i]
        repo.append(u[0])
        total+=u[1]
        list.append(result)

    return jsonify({'code': 200, 'value': list, 'total': total,'repo':repo})

@app.route('/api/GetCVEPieChart', methods=['GET'])
# @auth.login_required
def getCVEPieChart():
    ret = db.session.execute("select repo_name,count(*) from cve GROUP BY repo_name")
    cds = ret.fetchall()
    columns=["repo_name","num"]
    total=0
    list=[]
    repo = []
    for u in cds:
        result={}
        for i in range(len(columns)):
            result[columns[i]]=u[i]
        repo.append(u[0])
        total+=u[1]
        list.append(result)

    return jsonify({'code': 200, 'value': list, 'total': total,'repo':repo})

@app.route('/api/GetCVEYearLineChart', methods=['GET'])
# @auth.login_required
def getCVEyearLineChart():
    ret = db.session.execute("SELECT left(cvetime,4),count(*) from cve GROUP BY left(cvetime,4)")
    cds = ret.fetchall()
    total=0
    list=[]
    time = []
    for u in cds:
        list.append(u[1])
        time.append(u[0])
        total+=u[1]

    return jsonify({'code': 200, 'value': list, 'total': total,'time':time})

@app.route('/api/GetCVEWatchChart', methods=['GET'])
# @auth.login_required
def getCVEWatchChart():
    ret = db.session.execute("SELECT avg(score),count(*) from cve where score!=0")
    cds = ret.fetchall()
    for u in cds:
        score=u[0]
        num=u[1]
    score=round(score,2)
    return jsonify({'code': 200, 'score': score, 'num': num})

@app.route('/api/GetCVECircleChart', methods=['GET'])
# @auth.login_required
def getCVECircleChart():
    ret = db.session.execute("SELECT S_des,count(*) from cve GROUP BY S_des ORDER BY field(S_des,\'CRITICAL\',\'HIGH\',\'MEDIUM\',\'LOW\',\'NONE\')")
    cds = ret.fetchall()
    columns = ["name","value"]
    total = 0
    list = []
    name=[]
    for u in cds:
        result = {}
        for i in range(len(columns)):
            result[columns[i]] = u[i]
        total += u[1]
        name.append(u[0])
        list.append(result)
    return jsonify({'code': 200, 'value': list, 'total': total,'name':name})

@app.route('/api/GetCVESquareChart', methods=['GET'])
# @auth.login_required
def getCVESquareChart():
    ret = db.session.execute("select cwe_name,count(*) from cve GROUP BY cwe_name ORDER BY count(*) desc LIMIT 10")
    cds = ret.fetchall()
    columns = ["name","value"]
    total = 0
    list = []
    name=[]
    for u in cds:
        result = {}
        for i in range(len(columns)):
            result[columns[i]] = u[i]
        total += u[1]
        name.append(u[0])
        list.append(result)
    return jsonify({'code': 200, 'value': list, 'total': total,'name':name})

@app.route('/api/GetNewCVETable', methods=['GET'])
# @auth.login_required
def getNewCVETable():
    ret = db.session.execute("select CVE_id,repo_name,score,cwe_id,cwe_name,cvetime from cve ORDER BY cvetime desc LIMIT 10")
    cds = ret.fetchall()
    columns = ["CVE_id","repo_name","score","cwe_id","cwe_name","cvetime"]
    list = []
    for u in cds:
        result = {}
        for i in range(len(columns)):
            result[columns[i]] = u[i]
        list.append(result)
    return jsonify({'code': 200, 'CVEs': list})

@app.route('/api/GetSingalCVE', methods=['GET'])
def getSingalCVE():
    CVE = request.args.get('CVE',type=str)
    ret = db.session.execute(" SELECT a.CVE_id,b.Description,a.repo_name,a.cvetime,a.patch_gitcommit,a.score,a.S_des,a.cwe_id,a.cwe_name from cve a,all_cve b where a.`CVE_id`=b.`CVE_id` and a.`CVE_id`=\'{}\'".format(CVE))
    cds = ret.fetchall()
    columns = ["CVE_id","Description","repo_name","cvetime","patch_gitcommit","score","S_des","cwe_id","cwe_name"]
    list=[]
    for u in cds:
        result = {}
        for i in range(len(columns)):
            result[columns[i]] =u[i]
        list.append(result)
        c=u[6]
        cve=u[0]
    # print(list)
    return jsonify({
        'code': 200,
        'CVEinfos': list[0],
        'color': c,
        'cve':cve
    })

@app.route('/api/Predict', methods=['GET'])
def getPredict():
    CVE = request.args.get('CVE',type=str)
    # CVE = "CVE-2000-1254"
    #准备数据
    forrank = ['cve', 'commit_id', 'label']
    feature1_cols = ['addcnt', 'delcnt', 'totalcnt', 'issue_cnt', 'web_cnt', 'bug_cnt', 'cve_cnt', 'time_dis',
                     'inter_token_cwe_cnt', 'inter_token_cwe_ratio', 'vuln_commit_tfidf', 'cve_match',
                     'bug_match', 'func_match', 'filepath_match', 'file_match', 'likehood', 'vuln_type_1', 'vuln_type2',
                     'vuln_type3', 'mess_shared_ratio', 'mess_max', 'mess_sum', 'mess_mean', 'mess_var',
                     'code_shared_num', 'code_shared_ratio', 'code_max', 'code_sum', 'code_mean', 'code_var']
    vuln_cols = ['vuln_emb' + str(i) for i in range(32)]
    cmt_cols = ['cmt_emb' + str(i) for i in range(32)]
    columns = forrank + feature1_cols + vuln_cols + cmt_cols
    Col = "{}".format([a for a in columns])
    Col = Col.replace('[', '')
    Col = Col.replace(']', '')
    Col = Col.replace('\'', '')
    # print(Col)
    ret = db.session.execute("SELECT {} from vc_feature WHERE cve=\'{}\'".format(Col, CVE))
    cds = ret.fetchall()
    list = []
    length = []
    for u in cds:
        result = {}
        for i in range(len(columns)):
            result[columns[i]] = u[i]
        list.append(result)
        length.append(len(list) - 1)
    test = pd.DataFrame(list, index=length)
    #预测

    param = {
        'max_depth': 5,
        'eta': 0.05,
        'verbosity': 1,
        'random_state': 2021,
        'objective': 'binary:logistic',
        'tree_method': 'gpu_hist'
    }

    def myFeval(preds, dtrain):
        labels = dtrain.get_label()
        return 'error', math.sqrt(mean_squared_log_error(preds, labels))

    # print("XGBoost 预测")

    model = xgb.Booster({'nthread': 4})  # init model
    model.load_model('patchmatch.model')  #导入模型
    print(test)
    result = test[['cve', 'commit_id', 'label']]
    result.loc[:, 'prob_xgb'] = 0
    X_test = test[feature1_cols + vuln_cols + cmt_cols]# load data
    predict = model.predict(xgb.DMatrix(X_test))

    result.loc[X_test.index, 'prob_xgb'] = predict
    print(predict)

    result['rank_xgb'] = get_rank(result, ['prob_xgb'])
    result.sort_values('rank_xgb',inplace=True)
    result=result[:][:20]

    # result.to_csv("rank_test.csv", index=False)
    list = []
    for row in result.itertuples():
        # print(row)
        print(row[2],row[4],row[5])
        ret = db.session.execute(" select * from totalcommit where commit_id=\'{}\'".format(row[2]))
        cds = ret.fetchall()
        columns = ["commit_id", "repo_name", "author", "description", "commit_time"]
        result = {}
        for i in range(5):
            result[columns[i]] = cds[0][i + 1]
        result["prob_xgb"]=row[4]
        result["rank_xgb"]=row[5]
        list.append(result)


    return jsonify({
        'code': 200,
        'commitlist': list
    })

@app.route('/api/CheckCommit', methods=['GET'])
# @auth.login_required
def update_CVE_Commit():
    Commit_id = request.args.get('Commit_id', type=str)
    CVE_id = request.args.get('CVE_id', type=str)
    print("ss:"+Commit_id)
    print(CVE_id)
    # return jsonify({'code': 200, 'msg': "更新成功"})
    if Commit_id:
        ret = db.session.execute("update cve set patch_gitcommit=\'{0}\' where CVE_id= \'{1}\'".format(Commit_id,CVE_id))
        print(ret)
        return jsonify({'code': 200, 'msg': "更新成功"})
    else:
        return jsonify({'code': 500, 'msg': "未知错误"})

@app.route('/api/test', methods=['GET'])
def gettest():
    CVE = "CVE-2000-1254"
    #现阶段先随机生成
    # ran=random.randint(1, 5000)

    forrank = ['cve', 'commit_id', 'label']
    feature1_cols = ['addcnt', 'delcnt', 'totalcnt', 'issue_cnt', 'web_cnt', 'bug_cnt', 'cve_cnt', 'time_dis',
                     'inter_token_cwe_cnt', 'inter_token_cwe_ratio', 'vuln_commit_tfidf', 'cve_match',
                     'bug_match', 'func_match', 'filepath_match', 'file_match', 'likehood', 'vuln_type_1', 'vuln_type2',
                     'vuln_type3', 'mess_shared_ratio', 'mess_max', 'mess_sum', 'mess_mean', 'mess_var',
                     'code_shared_num', 'code_shared_ratio', 'code_max', 'code_sum', 'code_mean', 'code_var']
    vuln_cols = ['vuln_emb' + str(i) for i in range(32)]
    cmt_cols = ['cmt_emb' + str(i) for i in range(32)]
    columns = forrank + feature1_cols + vuln_cols + cmt_cols
    Col="{}".format([a for a in columns])
    Col=Col.replace('[','')
    Col=Col.replace(']', '')
    Col=Col.replace('\'','')
    print(Col)
    ret = db.session.execute("SELECT {} from vc_feature WHERE cve=\'{}\'".format(Col, CVE))
    cds = ret.fetchall()
    list=[]
    length=[]
    for u in cds:
        result = {}
        for i in range(len(columns)):
            result[columns[i]] =u[i]
        list.append(result)
        length.append(len(list)-1)
    df=pd.DataFrame(list,index=length)
    print(df)
    return jsonify({
        'code': 200,
        'commitlist': list
    })

@app.route('/api/GetNewCommitTable', methods=['GET'])
# @auth.login_required
def getNewCommitTable():
    ret = db.session.execute("select * from totalcommit LIMIT 10")
    cds = ret.fetchall()
    columns = ["commit_id", "repo_name", "author", "description", "commit_time"]
    list = []
    for u in cds:
        result = {}
        for i in range(len(columns)):
            result[columns[i]] = u[i+1]
        list.append(result)
    return jsonify({'code': 200, 'Commits': list})

@app.route('/api/GetCommitPieChart', methods=['GET'])
# @auth.login_required
def getCommitPieChart():
    ret = db.session.execute("select repo_name,commit_num from repo ")
    cds = ret.fetchall()
    columns=["repo_name","commit_num"]
    total=0
    list=[]
    repo = []
    for u in cds:
        result={}
        for i in range(len(columns)):
            result[columns[i]]=u[i]
        repo.append(u[0])
        total+=u[1]
        list.append(result)

    return jsonify({'code': 200, 'value': list, 'total': total,'repo':repo})

@app.route('/api/AddNewCVE', methods=['GET'])
def add_newCVE():
    cve = request.args.get('CVE', 1, type=str)
    repoid = request.args.get('repoid', 1, type=int)
    page = 'https://cve.mitre.org/cgi-bin/cvename.cgi?name=' + cve
    res = requests.get(url=page, headers=headers)
    cvetime = re.search('<td><b>([0-9]{8})</b></td>', res.text).group(1)

    page = 'https://nvd.nist.gov/vuln/detail/' + cve
    res = requests.get(url=page, headers=headers)
    try:
        links = []
        soup = BeautifulSoup(res.text, 'lxml')
        tbody = soup.find(attrs={'data-testid': "vuln-hyperlinks-table"}).tbody
        for tr in tbody.children:
            if isinstance(tr, NavigableString): continue
            tds = tr.findAll('td')
            if 'Patch' in tds[1].text:
                links.append(tds[0].a['href'])
        tbody = soup.find(attrs={'data-testid': "vuln-CWEs-table"}).tbody
        for tr in tbody.children:
            if isinstance(tr, NavigableString): continue
            tds = tr.findAll('td')
            cwe_id=tds[0].text
            cwe_id=cwe_id.replace("\n",'')
            cwe_name = tds[1].text
        tbody = soup.find(attrs={'data-testid': "vuln-cvss3-panel-score-na"})
        if tbody is None:
            tbody = soup.find(attrs={'data-testid': "vuln-cvss3-panel-score"})
            if tbody is None:
                tbody = soup.find(attrs={'data-testid': "vuln-cvss3-cna-panel-score"})
                score = tbody.string
            else:
                score = tbody.string
            strlist = score.split(" ")
            score=float(strlist[0])
            S_des=strlist[1]

        else:
            S_des = "NONE"
            score = 0
    except Exception as e:
        logging.info(page + " ")

    reponame=get_repo_name(repoid)
    print(cve)
    print(repoid)
    print(reponame)
    print(cvetime)
    print(links)
    print(cwe_id)
    print(cwe_name)
    print(score)
    print(S_des)
    ret=db.session.execute("insert into cve( CVE_id,repo_name,repo_id,cvetime,score,S_des,cwe_id,cwe_name) values ( \'{}\',\'{}\',{} ,\'{}\',{},\'{}\',\'{}\',\'{}\')".format(cve,reponame,repoid,cvetime,score,S_des,cwe_id,cwe_name))
    ret = db.session.execute(
        "update repo set cve_num =(select count(*) from cve where repo_name=\'{}\')where repo_name= \'{}\'".format(
            reponame,reponame))
    # print(ret.cursor())
    return jsonify({
        'code': 200,
        'infos': "ok henshin"
    })

@app.route('/api/AddNewCommit', methods=['GET'])
def add_newCommit():
    print("start")
    repoid = request.args.get('repoid', 1, type=int)
    reponame=get_repo_name(repoid)
    ret = db.session.execute(" SELECT latest_commit from repo where repo_name=\'{}\'".format(reponame))
    cds=ret.fetchall()
    commit_id = str(cds[0][0])
    repo = git.Repo('D:/skd/study/Vulnerabilities/data/gitrepo/{}'.format(reponame))
    i=0
    latestcommit=""
    print("ssss",commit_id)
    listcommit=[]
    for item in repo.iter_commits():
        commit = repo.commit(str(item))
        print("right now",commit)
        if (i==0):
            latestcommit=str(item)

        if(str(item)==commit_id):
            print("waell")
            break
        else:

            author=commit.author
            description=commit.message
            committime=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(commit.committed_date))
            print(commit)
            # print(reponame)
            # print(author)
            # print(description)
            print(committime)
            listcommit.append(str(item))
            ret = db.session.execute(
                "INSERT into totalcommit(commit_id,repo_name,author,description,commit_time) values (\'{}\',\'{}\',\'{}\',\'{}\',\'{}\')".format(
                    str(item), reponame, author, description, committime))

        i+=1
        if(i==11):
            break
    print(latestcommit)
    if i==0:
        print("error")
        return jsonify({
            'code': 500,
            'infos': "error",
            'nums':0
        })
    else:
        ret = db.session.execute(
            "update repo set commit_num =(select count(*) from totalcommit where repo_name=\'{}\')where repo_name= \'{}\'".format(
                reponame, reponame))
        ret = db.session.execute(
            "update repo set latest_commit =\'{}\'where repo_name= \'{}\'".format(
                latestcommit, reponame))
        print("complete")
        print(listcommit)
        return jsonify({
            'code': 200,
            'infos': "complete",
            'nums':i,
            'commits': listcommit
        })


# @auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)


if __name__ == '__main__':
    db.create_all()
    app.run(host='0.0.0.0',debug=True)