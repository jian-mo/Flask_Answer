from os import abort

from flask import Flask, render_template, request, url_for,redirect


from client import post_client as cl

app = Flask(__name__)
app.debug = True


HOST = '0.0.0.0'
PORT = 100
PREFIX = '/'

@app.route('/',methods=["GET","POST"])
def client_start():
    question_url=url_for(".client_main")

    if request.method=="GET":
        return render_template("client_start.html")
    if request.method=="POST":
        if request.form.get("Choices") is not None:
            print "redirected"
            return redirect(question_url,code=307)
        else:

            print request.args
            uid=request.form.get("uid",None)
            cid=request.form.get("cid",None)
            print "uid,cid=",uid,cid
            resp=cl.JsonParser(cl.star_planning(cl.url_start,uid,cid))

            return render_template('client_main.html',
                               qid=resp.questionID,
                               uid=uid,
                               url=question_url,
                               questions=resp.question,
                               choices=resp.choices_text,transitionText=resp.transitionText)

@app.route('/main',methods=["GET","POST"])

def client_main():
    question_url=url_for(".client_main")
    if request.method == "GET":
        return render_template('client_main.html',
                               qid='',
                               uid='',
                               url=question_url,
                               questions="",
                               choices=["yes","no"])
    elif request.method == "POST":
        print "redirect took"
        uid=request.form.get("uid",None)
        qid=request.form.get("qid",None)
        choice=request.form.get("Choices",None)
        print "choice is ",choice
        rdata=cl.post_answer('http://127.0.0.1/post_conv/',uid,qid,choice)
        print "answer ok"
        pdata=cl.JsonParser(rdata)
        return render_template('client_main.html',uid=uid,qid=pdata.questionID,url=question_url,questions=pdata.question,transitionText=pdata.transitionText,
                               choices=pdata.choices_text)
    pass


# @app.route('/client/question/',methods=['POST'])
# def client_question():
#     if not request.args:
#         pass
#     else:
#         uid=request.args.get("uid")
#         qid=request.args.get("qid")
#         choice=request.args.get("choice")
#         rdata=cl.post_answer(url_for(".post"),uid,qid,choice)
#         pdata=cl.JsonParser(rdata)
#         return render_template('client_main.html',qid="",uid="",url=question_url)

if __name__ == '__main__':
    app.run(
        host=HOST,
        port=PORT
    )