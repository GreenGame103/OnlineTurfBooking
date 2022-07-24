from flask import Flask, render_template, request, redirect,session
import datetime
from DBConnection import Db
from email.mime import image
import os
import smtplib
from email.mime.text import MIMEText
from flask_mail import Mail



app = Flask(__name__)
app.secret_key="abc"

@app.route('/a')
def a():
    return render_template('admin/index.html')

@app.route('/logout')
def logout():
    session['lin']=""
    return redirect('/')

@app.route('/')
def firstpage():
    return render_template('firstpage.html')




@app.route('/fp',methods=['get','post'])
def fp():
    if request.method=="POST":
        db=Db()
        email = request.form['textfield']
        qry = db.selectOne("select * from login where user_name='" + email + "'")
        # print(qry)
        # otpvalue = random.randint(0000, 9999)
        if qry is not None:
            pswd = qry['password']

            try:
                gmail = smtplib.SMTP('smtp.gmail.com', 587)

                gmail.ehlo()

                gmail.starttls()

                gmail.login('greengameturf@gmail.com', 'green@game')

            except Exception as e:
                print("Couldn't setup email!!" + str(e))

            msg = MIMEText("Your Password is " + pswd)

            msg['Subject'] = 'Verification'

            msg['To'] = email

            msg['From'] = 'greengameturf@gmail.com'

            try:

                gmail.send_message(msg)

            except Exception as e:

                print("COULDN'T SEND EMAIL", str(e))
            return '''<script>alert("Mail Send successfully");window.location='/login'</script>'''
        else:
            return '''<script>alert("No such Mail");window.location='/login'</script>'''


    return render_template('fp.html')





@app.route('/login',methods=['get','post'])
def login():
    if request.method=='POST':
        db = Db()
        username = request.form['textfield']
        password = request.form['textfield2']
        res=db.selectOne("select * from login where user_name='"+username+"'and password='"+password+"'")

        # print(res)
        if res is not None:
            session['lid']=res['login_id']
            session['lin']="lin"
            if res['type'] == 'admin':
                return '''<script>alert('login successfull');window.location="/admin_home"</script>'''
            elif res['type'] =='manager':
                ss=db.selectOne("select * from prop where prop_id='"+str(session['lid'])+"'")
                session['pname']=ss['name']
                session['pimg']=ss['image']
                session['pmail']=ss['mail']
                return '''<script>alert('login successfull');window.location="/manager_home"</script>'''
            elif res['type'] =='user':
                ss = db.selectOne("select * from user where user_id='" + str(session['lid']) + "'")
                session['uname'] = ss['name']
                session['uimg'] = ss['image']
                session['umail'] = ss['mail']
                return '''<script>alert('login successfull');window.location="/user_home"</script>'''

            else:
                return '''<script>alert('not found');window.location="/"</script>'''
        else:
            return '''<script>alert('not found');window.location="/"</script>'''
    else:
        return render_template('login_index.html')


@app.route('/view_feedback')
def view_feedback():
    if session['lin']=="lin":
        db=Db()
        res=db.select("select * from feedback,user where user.user_id=feedback.user_id")
        return render_template('admin/view feedback.html',data=res)
    else:
        return redirect('/')


@app.route('/admin_home')
def admin_home():
    if session['lin'] == "lin":
        return render_template('admin/admin_home.html')
        # return render_template('admin/aa.html')
    else:
        return redirect('/')


@app.route('/view_prop')
def view_prop():
    if session['lin'] == "lin":
        db=Db()
        res=db.select("select * from prop")
        return render_template('admin/view prop.html',data=res)
    else:
        return redirect('/')

@app.route('/view_rating/<tid>')
def view_rating(tid):
    if session['lin'] == "lin":

        db=Db()
        res=db.select("select * from rating,user where user.user_id=rating.user_id and rating.turf_id='"+tid+"'")
        return render_template('admin/view rating.html',data=res)
    else:
        return redirect('/')


@app.route('/view_user')
def view_user():
    if session['lin'] == "lin":

        db = Db()
        res = db.select("select * from user")
        return render_template('admin/view user.html', data=res)
    else:
        return redirect('/')


@app.route('/view_turf')
def view_turf():
    if session['lin'] == "lin":

        db = Db()
        res = db.select("select * from turf,prop where turf.prop_id=prop.prop_id")
        return render_template('admin/view turf.html', data=res)
    else:
        return redirect('/')


# @app.route('/prop_reg',methods=['post','get'])
# def prop_reg():
#     return render_template('manager/prop reg.html')

@app.route('/prop_reg',methods=['post','get'])
def prop_reg ():

    if request.method == "POST":
        name=request.form['n']
        mail=request.form['textfield7']
        ph=request.form['textfield3']
        post= request.form['post']
        pla= request.form['pla']
        pin = request.form['pin']
        hname= request.form['hname']
        password=request.form['textfield6']
        cpassword=request.form['textfield17']
        img=request.files['fileField']
        date=datetime.datetime.now().strftime("%y%m%d-%H%M%S")
        img.save(r'C:\Users\VIMAL JAIN\PycharmProjects\online turf booking\static\pic\\'+date+'.jpg')

        ss='/static/pic/'+date+'.jpg'
        print(password,cpassword)
        db=Db()
        if password==cpassword:
            q=db.selectOne("select * from login WHERE user_name='"+mail+"'")
            if q:
                return '''<script>alert('user name already exists');window.location="/"</script>'''
            res=db.insert("insert into login values('','"+mail+"','"+password+"','manager')")
            db.insert("insert into prop values('"+str(res)+"','"+name+"','"+mail+"','"+ph+"','"+str(ss)+"','"+hname+"','"+pla+"','"+post+"','"+pin+"')")
            return '''<script>alert('successfully registered');window.location="/"</script>'''
        else:
            return '''<script>alert('Password Mismatch');window.location="/"</script>'''


    else:
        return render_template('manager/prop reg.html')


@app.route('/view_manager_profile')
def view_manager_profile():
    if session['lin'] == "lin":
        db = Db()
        res = db.selectOne("select * from prop WHERE prop_id='"+str(session['lid'])+"'")
        return render_template('manager/view and update profile.html',data=res)
    else:
        return redirect('/')





@app.route('/update_manager_profile', methods=['GET', 'POST'])
def update_manager_profile():
    if session['lin'] == "lin":

        if request.method == "POST":
                name = request.form['n']
                mail = request.form['textfield7']
                ph = request.form['textfield3']
                post = request.form['post']
                pla = request.form['pla']
                pin = request.form['pin']
                hname = request.form['hname']
                img = request.files['fileField']
                date = datetime.datetime.now().strftime("%y%m%d-%H%M%S")
                img.save(r"C:\Users\VIMAL JAIN\PycharmProjects\online turf booking\static\pic\\" + date + '.jpg')

                ss = "/static/pic/" + date + '.jpg'
                db = Db()
                if request.files!=None:
                    if img.filename!="":
                            db.update("update prop set name='"+name+"',mail='"+mail+"',ph_no='"+ph+"',image='"+str(ss)+"',place='"+pla+"',post='"+post+"',pin='"+pin+"',hname='"+hname+"' where prop_id='"+str(session['lid'])+"'")
                            return '''<script>alert('success');window.location="/view_manager_profile"</script>'''

                    else:
                        db.update( "update prop set name='" + name + "',mail='" + mail + "',ph_no='" + ph + "',place='" + pla + "',post='" + post + "',pin='" + pin + "',hname='" + hname + "' where prop_id='" + str(session['lid']) + "'")
                        return '''<script>alert('success ');window.location="/view_manager_profile"</script>'''

                else:
                    db.update( "update prop set name='" + name + "',mail='" + mail + "',ph_no='" + ph + "',place='" + pla + "',post='" + post + "',pin='" + pin + "',hname='" + hname + "' where prop_id='" + str(session['lid']) + "'")
                    return '''<script>alert('success ');window.location="/view_manager_profile"</script>'''
        else:
            db = Db()
            res = db.selectOne("select * from prop WHERE prop_id='" + str(session['lid']) + "'")
            return render_template("manager/update manager profile.html", data=res)
    else:
        return redirect('/')


@app.route('/booking_table')
def booking_table():
    if session['lin'] == "lin":
        db=Db()
        res=db.select("select * from booking,user,turf where user.user_id=booking.user_id and booking.turf_id=turf.turf_id and booking.turf_id=turf.turf_id and turf.prop_id='" + str(session['lid']) + "'")
        return render_template('manager/booking_table.html',data=res)
    else:
        return redirect('/')


@app.route('/tournament_creation',methods=['post','get'])
def tournament_creation():
  if session['lin'] == "lin":
    if request.method == "POST":
        turf=request.form['select']
        tournamentname = request.form['textfield']
        qry=db.select("select * from turf where prop_id='"+str(session['lid'])+"'")
        return render_template('manager/tournament creation.html',data=qry)
  else:
      return redirect('/')


@app.route('/tournament_request')
def tournament_request():
    if session['lin'] == "lin":
        db = Db()
        res = db.select("select  * from turf,tournament,tournament_request1,user where tournament_request1.tournament_id=tournament.tournament_id and tournament_request1.user_id=user.user_id and tournament.turf_id=turf.turf_id AND turf.prop_id='"+str(session['lid'])+"'  ")
        return render_template('manager/tournament request.html',data=res)
    else:
        return redirect('/')


@app.route('/view_tournament')
def view_tournament():
    if session['lin'] == "lin":
        db = Db()
        # res = db.select("select turf.turf_name,turf.latitude,turf.Longitude,tournament.* from tournament,turf where tournament.turf_id=turf.turf_id AND turf.prop_id='"+str(session['lid'])+"' ")
        res = db.select("select turf.turf_name,turf.latitude,turf.Longitude,tournament.* from tournament,turf where tournament.turf_id=turf.turf_id AND turf.prop_id='"+str(session['lid'])+"' ")
        return render_template('manager/view_tournament.html',data=res)
    else:
        return redirect('/')




@app.route('/tournament_sheduling/<id>',methods=['post','get'])
def tournament_sheduling(id):
    if session['lin'] == "lin":
        if request.method == "POST":
            date = request.form['textfield']
            time = request.form['textfield2']
            gametype=request.form['select']
            team1=request.form['select2']
            team2=request.form['select3']
            bre=request.form['textfield3']
            db =Db()
            db.insert("insert into tournament_shedule values('','"+str(id)+"','"+date+"','"+time+"','"+gametype+"','"+team1+"','"+team2+"','"+bre+"','pending','pending')")
            return '''<script>alert('successfully registered');window.location="/view_tournament"</script>'''
        else:
            ab = Db()
            qry = ab.select("select * from turf ")
            return render_template('manager/tournament scheduling.html',data=qry)
    else:
        return redirect('/')




@app.route('/view_schedule/<tid>')
def view_schedule(tid):
    if session['lin'] == "lin":
        db = Db()
        res = db.select("select * from tournament_shedule where  tournament_id='"+tid+"'")
        return render_template('manager/view schedule.html', data=res)
    else:
        return redirect('/')



@app.route('/winner/<t1>/<t2>/<sid>',methods=['get','post'])
def winner(t1,t2,sid):
    if session['lin'] == "lin":
        if request.method=="POST":
            trid=request.form['checkbox']
            db = Db()
            q=db.selectOne("select * from tournament_shedule where schedule_id='"+sid+"'")
            if q:
                gt=q['gametype']
                tid=q['tournament_id']
                if gt=='Finals':
                    db.update("update tournament_shedule set winner='"+trid+"',status='winner is set' where schedule_id='"+sid+"' ")
                    # q=db.selectOne("select * from winner_list where tournament_id='"+str(tid)+"'")
                    db.insert("insert into winner_list values('','"+str(tid)+"','"+trid+"')")
                    return '''<script>alert('winner updated');window.location="/view_tournament"</script>'''
                else:
                    db.update("update tournament_shedule set winner='" + trid + "',status='winner is set' where schedule_id='" + sid + "' ")
                    return '''<script>alert('winner updated');window.location="/view_tournament"</script>'''
        return render_template('manager/set_winner.html', data=t1,data1=t2)
    else:
        return redirect('/')



@app.route('/update_schedule/<id>',methods=['post','get'])
def update_schedule(id):
    if session['lin'] == "lin":
        if request.method == "POST":
            date = request.form['textfield']
            time = request.form['textfield2']
            gametype=request.form['select']
            team1=request.form['select2']
            team2=request.form['select3']
            bre=request.form['textfield3']
            db =Db()

            db.update("update tournament_shedule set starting_date='"+date+"',time='"+time+"',gametype='"+gametype+"',team_1='"+team1+"',team_2='"+team2+"',break='"+bre+"' where schedule_id='"+id+"'")
            return '''<script>alert('successfully updated');window.location="/view_tournament"</script>'''
        else:
            ab = Db()
            qry = ab.selectOne("select * from tournament_shedule where schedule_id='"+id+"' ")
            tid=qry['tournament_id']
            gt=qry['gametype']
            if gt=='Finals':
                qry1 = ab.select("select tournament_request1.*,tournament_shedule.status as ts from tournament_request1,tournament_shedule where tournament_request1.tournament_id=tournament_shedule.tournament_id and tournament_request1.status='accepted' and tournament_request1.tournament_id='"+str(tid)+"' and tournament_shedule.status='winner is set' and tournament_shedule.winner=tournament_request1.team_name  group by tournament_request_id  ")
            else:
                qry1 = ab.select("select tournament_request1.*,tournament_shedule.status as ts from tournament_request1,tournament_shedule where tournament_request1.tournament_id=tournament_shedule.tournament_id and tournament_request1.status='accepted' and tournament_request1.tournament_id='" + str(tid) + "'   group by tournament_request_id")
                qry1 = ab.select("select tournament_request1.*,tournament_shedule.status as ts from tournament_request1,tournament_shedule where tournament_request1.tournament_id=tournament_shedule.tournament_id and tournament_request1.status='accepted' and tournament_request1.tournament_id='" + str(tid) + "'   group by tournament_request_id")

            return render_template('manager/update scheduling.html',data=qry,data1=qry1)
    else:
        return redirect('/')





@app.route('/delete_schedule/<tid>')
def delete_schedule(tid):
    if session['lin'] == "lin":
        db=Db()
        res=db.delete("delete from tournament_shedule where schedule_id='"+tid+"'")
        return '''<script>alert("Deleted successfully");window.location='/view_tournament'</script>'''
    else:
        return redirect('/')






@app.route('/turf_management',methods=['post','get'])
def turf_management():
    if session['lin'] == "lin":
        if request.method == "POST":

            turfname = request.form['textfield']
            la= request.form['la']
            lo= request.form['lo']
            ph= request.form['textfield2']
            details=request.form['textarea2']
            price = request.form['textfield3']
            time = request.form['textfield4']
            members = request.form['select']
            img = request.files['fileField']
            date = datetime.datetime.now().strftime("%y%m%d-%H%M%S")
            img.save(r'C:\Users\VIMAL JAIN\PycharmProjects\online turf booking\static\pic\\' + date + '.jpg')
            ss = '/static/pic/' + date + '.jpg'

            db=Db()
            db.insert("insert into turf values('','"+turfname+"','"+la+"','"+lo+"','"+ph+"','"+str(session['lid'])+"','"+str(ss)+"','"+details+"','"+price+"','"+time+"','"+members+"')")
            return '''<script>alert('successfully registered');window.location="/manager_home"</script>'''
        else:
            return render_template('manager/turf management.html')
    else:
        return redirect('/')



@app.route('/manager_view_turf')
def manager_view_turf():
    if session['lin'] == "lin":
        db = Db()
        res = db.select("select * from turf where  prop_id='"+str(session['lid'])+"'")
        return render_template('manager/view turf.html', data=res)
    else:
        return redirect('/')



@app.route('/manager_view_rating/<tid>')
def manager_view_rating(tid):
    if session['lin'] == "lin":
        db=Db()
        res=db.select("select * from rating,user where user.user_id=rating.user_id and rating.turf_id='"+tid+"'")
        return render_template('manager/view rating.html',data=res)
    else:
        return redirect('/')




@app.route('/delete_turf/<tid>')
def delete_turf(tid):
    if session['lin'] == "lin":
        if session['lin'] == "lin":
            db=Db()
            res=db.delete("delete from turf where turf_id='"+tid+"'")
            res=db.delete("delete from rating where turf_id='"+tid+"'")
            return '''<script>alert("Deleted successfully");window.location='/manager_view_turf'</script>'''
        else:
            return redirect('/')
    else:
        return redirect('/')




@app.route('/view_turfpayment/<tid>')
def view_turfpayment(tid):
    if session['lin'] == "lin":
        db = Db()
        res = db.select("select * from turfpayment,turf where turf.turf_id=turfpayment.turfid and  turf.prop_id='"+str(session['lid'])+"' and turfpayment.turfid='"+tid+"'")
        return render_template('manager/view turf payment.html',data=res)
    else:
        return redirect('/')




@app.route('/view_tpayment')
def view_tpayment():
    if session['lin'] == "lin":
        db = Db()
        res = db.select("select * from tpayment")
        return render_template('manager/view tpayment.html',data=res)
    else:
        return redirect('/')




@app.route('/view_request')
def view_request():
    if session['lin'] == "lin":
        db = Db()
        res = db.select("select * from turf,booking,user where booking.turf_id=turf.turf_id and booking.user_id=user.user_id and turf.prop_id='"+str(session['lid'])+"' ")
        return render_template('manager/view request.html',data=res)
    else:
        return redirect('/')


@app.route('/manager_home')
def manager_home():
    if session['lin'] == "lin":
        return render_template('manager/manager_home.html')
    else:
        return redirect('/')



@app.route('/view_m_feedback')
def view_m_feedback():
    if session['lin'] == "lin":
        db=Db()
        res=db.select("select * from feedback,user where user.user_id=feedback.user_id")
        return render_template('manager/view feedback.html',data=res)
    else:
        return redirect('/')


@app.route('/view_m_rating')
def view_m_rating():
    if session['lin'] == "lin":
        db=Db()
        res=db.select("select * from rating,user,turf where user.user_id=rating.user_id and rating.turf_id=turf.turf_id")
        return render_template('manager/view rating.html',data=res)
    else:
        return redirect('/')


@app.route('/accept_booking/<bid>')
def accept_booking(bid):
    if session['lin'] == "lin":
        db=Db()
        db.update("update booking set status='accepted' where booking_id='"+bid+"'")
        return '''<script>alert('success');window.location="/view_request"</script>'''
    else:
        return redirect('/')


@app.route('/reject_booking/<bid>')
def reject_booking(bid):
    if session['lin'] == "lin":
        db=Db()
        q = db.selectOne("select * from booking where booking_id='" + bid + "' ")
        p = q['amount']
        uid = q['user_id']
        tid = q['turf_id']
        q1 = db.selectOne("select * from card where cardid='1'")
        b = q1['balance']
        am = float(b) - float(p)
        # print(am)
        q2 = db.selectOne("select * from card where cardid='2'")
        b1 = q2['balance']
        am1 = float(b1) + float(p)
        print(am1)
        db.update("update card set balance='" + str(am) + "' where cardid=1")
        db.update("update card set balance='" + str(am1) + "' where cardid=2")
        q1 = db.selectOne("select * from turfpayment where turfid='" + str(tid) + "' and userid='" + str(uid) + "'  ")
        rr = q1['tupayid']
        db.delete("delete from turfpayment where tupayid='" + str(rr) + "'")
        db.update("update booking set status='rejected' where booking_id='" + bid + "'")
        return '''<script>alert('success');window.location="/view_request"</script>'''
    else:
        return redirect('/')


@app.route('/reject_tournament_request/<bid>')
def reject_tournament_request(bid):
    if session['lin'] == "lin":
        db=Db()
        q=db.selectOne("select * from tournament_request1,tournament where tournament.tournament_id=tournament_request1.tournament_id and tournament_request_id='"+bid+"' ")
        p=q['price']
        uid=q['user_id']
        tid=q['tournament_id']
        q1=db.selectOne("select * from card where cardid='1'")
        b=q1['balance']
        am=float(b) - float(p)
        # print(am)
        q2 = db.selectOne("select * from card where cardid='2'")
        b1 = q2['balance']
        am1 = float(b1) + float(p)
        print(am1)
        db.update("update card set balance='" + str(am) + "' where cardid=1")
        db.update("update card set balance='"+ str(am1) + "' where cardid=2")
        q1=db.selectOne("select * from tpayment where tid='"+str(tid)+"' and userid='"+str(uid)+"'  ")
        rr=q1['tpay']
        db.delete("delete from tpayment where tpay='"+str(rr)+"'")
        db.update("update tournament_request1 set status='reject' where tournament_request_id='"+bid+"'")

        return '''<script>alert('success');window.location="/tournament_request"</script>'''
    else:
        return redirect('/')


@app.route('/accept_tournament_request/<bid>')
def accept_tournament_request(bid):
    if session['lin'] == "lin":
        db=Db()
        db.update("update tournament_request1 set status='accepted' where tournament_request_id='"+bid+"'")
        return '''<script>alert('success');window.location="/tournament_request"</script>'''
    else:
        return redirect('/')


@app.route('/user_reg',methods=['post','get'])
def user_reg ():
    if request.method == "POST":
        name=request.form['n']
        mail=request.form['textfield7']
        ph=request.form['textfield3']
        post= request.form['post']
        pla= request.form['pla']
        pin = request.form['pin']
        hname= request.form['hname']
        password=request.form['textfield6']
        cpassword=request.form['textfield17']
        img=request.files['fileField']
        date=datetime.datetime.now().strftime("%y%m%d-%H%M%S")
        img.save(r'C:\Users\VIMAL JAIN\PycharmProjects\online turf booking\static\pic\\'+date+'.jpg')

        ss='/static/pic/'+date+'.jpg'
        print(password,cpassword)
        db=Db()
        if password==cpassword:
            q=db.selectOne("select * from login WHERE user_name='"+mail+"'")
            if q:
                return '''<script>alert('user name already exists');window.location="/"</script>'''
            res=db.insert("insert into login values('','"+mail+"','"+password+"','user')")
            db.insert("insert into user values('"+str(res)+"','"+name+"','"+mail+"','"+ph+"','"+str(ss)+"','"+pla+"','"+post+"','"+pin+"','"+hname+"')")
            return '''<script>alert('successfully registered');window.location="/"</script>'''
        else:
            return '''<script>alert('Password Mismatch');window.location="/"</script>'''


    else:
        return render_template('user/user_reg.html')

@app.route('/user_home')
def user_home():
    if session['lin'] == "lin":
        return render_template('user/user home.html')
    else:
        return redirect('/')



@app.route('/view_profile')
def view_profile():
    if session['lin'] == "lin":
        db = Db()
        res = db.selectOne("select * from user WHERE user_id='"+str(session['lid'])+"'")
        return render_template('user/view and update profile.html',data=res)
    else:
        return redirect('/')



@app.route('/update_profile', methods=['GET', 'POST'])
def update_profile():
    if session['lin'] == "lin":

        if request.method == "POST":
                name = request.form['n']
                mail = request.form['textfield7']
                ph = request.form['textfield3']
                post = request.form['post']
                pla = request.form['pla']
                pin = request.form['pin']
                hname = request.form['hname']
                img = request.files['fileField']
                date = datetime.datetime.now().strftime("%y%m%d-%H%M%S")
                img.save(r"C:\Users\VIMAL JAIN\PycharmProjects\online turf booking\static\pic\\" + date + '.jpg')

                ss = "/static/pic/" + date + '.jpg'
                db = Db()
                if request.files!=None:
                    if img.filename!="":
                            db.update("update user set name='"+name+"',mail='"+mail+"',ph_no='"+ph+"',image='"+str(ss)+"',place='"+pla+"',post='"+post+"',pin='"+pin+"',hname='"+hname+"' where user_id='"+str(session['lid'])+"'")
                            return '''<script>alert('success');window.location="/view_profile"</script>'''

                    else:
                        db.update( "update user set name='" + name + "',mail='" + mail + "',ph_no='" + ph + "',place='" + pla + "',post='" + post + "',pin='" + pin + "',hname='" + hname + "' where user_id='" + str(session['lid']) + "'")
                        return '''<script>alert('success ');window.location="/view_profile"</script>'''

                else:
                    db.update( "update user set name='" + name + "',mail='" + mail + "',ph_no='" + ph + "',place='" + pla + "',post='" + post + "',pin='" + pin + "',hname='" + hname + "' where user_id='" + str(session['lid']) + "'")
                    return '''<script>alert('success ');window.location="/view_profile"</script>'''



        else:
            db = Db()
            res = db.selectOne("select * from user WHERE user_id='" + str(session['lid']) + "'")
            return render_template("user/update profile.html", data=res)
    else:
        return redirect('/')


@app.route('/search_turf',methods=['get','post'])
def search_turf():
    if session['lin'] == "lin":
        if request.method=="POST":
            t=request.form['t']
            db = Db()
            res = db.select("select * from turf where turf_name LIKE '%"+t+"%'")
            return render_template('user/search_turf.html', data=res)

        db = Db()
        res = db.select("select * from turf")
        return render_template('user/search_turf.html',data=res)
    else:
        return redirect('/')


@app.route('/send_request/<a>',methods=['GET','post'])
def send_request(a):
    if session['lin'] == "lin":
        if request.method == "POST":
            member=request.form['select']
            date = request.form['textfield']
            time = request.form['select2']
            hr = request.form['radio']
            db=Db()
            if hr=='1400':
                time2=time.strip('AM').strip('PM')
                time3=int(time2)+1
            else:
                time2 = time.strip('AM').strip('PM')
                time3 = int(time2) + 2

            q = "select * from booking where turf_id='" + a + "' and date='" + date + "' and time between '" + str(time2) + "' and '" + str(time3) + "'"
            print(q)
            q1=db.selectOne(q)
            if q1:
                return '''<script>alert('This Hour is Already Reserved ');window.location="/search_turf"</script>'''

            return render_template("user/turfpayment.html",member=member,date=date,time=time,hr=hr,a=a)
        else:

            return render_template('user/send request .html')
    else:
        return redirect('/')



@app.route('/turfpay/<m>/<d>/<t>/<tid>',methods=['post','get'])
def turfpay(m,d,t,tid):
    if session['lin'] == "lin":
        db = Db()
        chn=request.form['hn']
        cn=request.form['cn']
        cvv=request.form['cvv']
        date=request.form['date']
        amt=request.form['price']
        z=db.selectOne("select * from card where cno='"+cn+"' and expiry='"+date+"' and chname='"+chn+"' and cvv='"+cvv+"' and userid='2'")
        if z:
            b=z['balance']
            if float(b)>float(amt):
                db.insert("insert into booking values('','"+str(session['lid'])+"','"+tid+"','"+m+"','"+d+"','"+t+"','"+amt+"','pending')")
                db.update("update card set balance=balance+'"+amt+"' where cardid=1")
                db.update("update card set balance=balance-'"+amt+"' where cardid=2")
                db.insert("insert into turfpayment values('','"+str(session['lid'])+"','"+tid+"','"+amt+"',curdate())")
                return '''<script>alert("Payment Successfull");window.location="/search_turf"</script>'''
            else:
                return '''<script>alert("Insufficient Balance");window.location="/search_turf"</script>'''
        else:
            return '''<script>alert("Account Doesn't Exists");window.location="/search_turf"</script>'''
    else:
        return redirect('/')









@app.route('/turf_booking_status')
def turf_booking_status():
    if session['lin'] == "lin":
        db = Db()
        res = db.select("select * from booking,turf where booking.turf_id=turf.turf_id and booking.user_id='"+str(session['lid'])+"'")
        return render_template('user/turf booking status.html',data=res)
    else:
        return redirect('/')



@app.route('/view_tournament_user')
def view_tournament_user():
    if session['lin'] == "lin":
        db = Db()
        res = db.select("select * from tournament ")
        return render_template('user/view tournament.html',data=res)
    else:
        return redirect('/')



@app.route('/tournament_request_user/<tid>/<p>',methods=['post','get'])
def tournament_request_user(tid,p):
    if session['lin'] == "lin":
        db = Db()
        if request.method == "POST":
            teamname = request.form['textfield']
            db = Db()
            q = db.selectOne("select * from tournament_request1 where team_name='"+teamname+"' and status='accepted'")
            if q:
                return '''<script>alert('Team Name Already Exists..!!!');window.location="/view_tournament_user"</script>'''
            return render_template("user/payment.html",tn=teamname,p=p,tid=tid)
            # db = Db()
            # q=db.selectOne("select * from tournament_request1 where user_id='"+str(session['lid'])+"' and tournament_id='"+tid+"'")
            # if q:
            #     return '''<script>alert('Already Requested');window.location="/view_tournament_user"</script>'''
            # db.insert("insert into tournament_request1 VALUES ('','"+str(session['lid'])+"','"+tid+"','"+teamname+"',curdate(),'pending')")
            # return '''<script>alert('successfully requested');window.location="/view_tournament_user"</script>'''
        else:
            return render_template('user/tournament request.html')
    else:
        return redirect('/')



@app.route('/tpay/<tn>/<tid>',methods=['post','get'])
def tpay(tn,tid):
    if session['lin'] == "lin":
        db = Db()
        chn=request.form['hn']
        cn=request.form['cn']
        cvv=request.form['cvv']
        date=request.form['date']
        amt=request.form['price']
        z=db.selectOne("select * from card where cno='"+cn+"' and expiry='"+date+"' and chname='"+chn+"' and cvv='"+cvv+"' and userid='2'")
        if z:
            b=z['balance']
            if float(b)>float(amt):
                q = db.selectOne("select * from tournament_request1 where user_id='" + str(session['lid']) + "' and tournament_id='" + tid + "'")
                if q:
                    return '''<script>alert('Already Requested');window.location="/view_tournament_user"</script>'''
                db.insert("insert into tournament_request1 VALUES ('','" + str(session['lid']) + "','" + tid + "','" + tn + "',curdate(),'pending')")
                db.update("update card set balance=balance+'"+amt+"' where cardid=1")
                db.update("update card set balance=balance-'"+amt+"' where cardid=2")
                db.insert("insert into tpayment values('','"+str(session['lid'])+"','"+tid+"',curdate(),'"+amt+"')")
                return '''<script>alert("Payment Successfull");window.location="/view_tournament_user"</script>'''
            else:
                return '''<script>alert("Insufficient Balance");window.location="/view_tournament_user"</script>'''
        else:
            return '''<script>alert("Account Doesn't Exists");window.location="/view_tournament_user"</script>'''
    else:
        return redirect('/')



@app.route('/send_partner/<tid>',methods=['GET','POST'])
def send_partner(tid):
    if session['lin'] == "lin":
        # db = Db()
        if request.method == "POST":
            member=request.form['textfield']
            db = Db()
            db.insert("insert into partner_request VALUES ('','"+tid+"','"+member+"','pending')")
            return '''<script>alert('successfully requested');window.location="/turf_booking_status"</script>'''
        else:
            return render_template('user/send partner.html')
    else:
        return redirect('/')


@app.route('/view_partner_req_status/<bid>', methods=['GET', 'POST'])
def view_partner_req_status(bid):
    if session['lin'] == "lin":
        db=Db()
        q=db.select("select * from pr_user,partner_request,user where pr_user.user_id=user.user_id and pr_user.partner_id=partner_request.partner_id and partner_request.booking_id='"+bid+"'")
        return render_template('user/view_partner_req_status.html',data=q)
    else:
        return redirect('/')


@app.route('/req_partner/<pid>', methods=['GET', 'POST'])
def req_partner(pid):
    if session['lin'] == "lin":

        db = Db()
        q=db.selectOne("select * from pr_user where partner_id='"+pid+"' and user_id='"+str(session['lid'])+"'")
        if q:
            return '''<script>alert('Already a member');window.location="/view_partner_req"</script>'''
        else:

            db.update("update partner_request set members=members-'1' where partner_id='"+pid+"'")
            a=db.insert("insert into pr_user values('','"+pid+"', '"+str(session['lid'])+"')")
            return '''<script>alert('You are a member now...!11');window.location="/view_partner_req"</script>'''
    else:
        return redirect('/')


@app.route('/view_partner_req', methods=['GET', 'POST'])
def view_partner_req():
    if session['lin'] == "lin":
        db = Db()
        a=db.select("select partner_request.members as m,partner_request.partner_id,booking.*,turf.*,user.* from partner_request,booking,turf,user where partner_request.members!='0' and booking.user_id=user.user_id and  booking.booking_id=partner_request.booking_id and booking.turf_id=turf.turf_id and partner_request.status='pending' and booking.user_id!='"+str(session['lid'])+"'")
        return render_template('user/partner search.html',b=a)
    else:
        return redirect('/')


@app.route('/view_winner')
def view_winner():
    if session['lin'] == "lin":
        db = Db()
        res = db.select("select * from winner_list,tournament WHERE winner_list.tournament_id=tournament.tournament_id")
        return render_template('user/view winner list.html', data=res)
    else:
        return redirect('/')



@app.route('/add_rating/<tid>',methods=['post','get'])
def add_rating(tid):
    if session['lin'] == "lin":
        db = Db()
        if request.method == "POST":
            r = request.form['textarea']
            db = Db()
            db.insert("insert into rating VALUES ('','"+str(session['lid'])+"',curdate(),'"+r+"','"+tid+"')")
            return '''<script>alert('successfully rated');window.location="/search_turf"</script>'''
        else:
            return render_template('user/add rating.html')
    else:
        return redirect('/')




@app.route('/add_feedback/<tid>',methods=['post','get'])
def add_feedback(tid):
    if session['lin'] == "lin":
        db = Db()
        if request.method == "POST":
            r = request.form['textarea']
            db = Db()
            db.insert("insert into feedback VALUES ('','"+str(session['lid'])+"',curdate(),'"+r+"')")
            return '''<script>alert('send successfully ');window.location="/search_turf"</script>'''
        else:
            return render_template('user/add feedback.html')
    else:
        return redirect('/')





@app.route('/partner_search')
def partner_search():
    if session['lin'] == "lin":
        db = Db()
        res = db.select("select * from winner_list,tournament")
        return render_template('user/partner search.html', data=res)
    else:
        return redirect('/')

@app.route('/tournament_status')
def tournament_status():
    if session['lin'] == "lin":
        db = Db()
        res = db.select("select * from tournament,tournament_request1 WHERE tournament_request1.tournament_id=tournament.tournament_id and tournament_request1.user_id='"+str(session['lid'])+"'")
        return render_template('user/tournament booking status.html', data=res)
    else:
        return redirect('/')



@app.route('/user_view_schedule/<tid>',methods=['post','get'])
def user_view_schedule(tid):
    if session['lin'] == "lin":
        db = Db()
        res = db.select("select * from tournament_shedule WHERE tournament_id='"+tid+"'")
        return render_template('user/view schedule.html', data=res)
    else:
        return redirect('/')





@app.route('/view_fr')
def view_fr():
    if session['lin'] == "lin":
        db = Db()
        res = db.select("select * from rating,user,turf where rating.user_id=user.user_id and rating.turf_id=turf.turf_id")
        res1 = db.select("select * from feedback,user where feedback.user_id=user.user_id ")
        return render_template('user/view rating and feedback.html', r=res,f=res1)
    else:
        return redirect('/')




@app.route('/public_home')
def public_home():
        return render_template('public/public home.html')





@app.route('/view_rf')
def view_rf():
        db = Db()
        res = db.select("select * from rating,user,turf where rating.user_id=user.user_id and rating.turf_id=turf.turf_id")
        res1 = db.select("select * from feedback,user where feedback.user_id=user.user_id ")
        return render_template('public/view rating and feedback.html', r=res,f=res1)


@app.route('/view_turf_facilities')
def view_turf_facilities():
        db = Db()
        res = db.select("select * from turf")
        return render_template('public/facilities_turf.html',data=res)




@app.route('/change_password',methods=['GET','POST'])
def change_password():
    if request.method=='POST':
        current=request.form['textfield1']
        new = request.form['textfield2']
        confirm=request.form['textfield3']
        if new==confirm:
            db=Db()
            q=db.selectOne("select * from login where login_id='"+str(session['lid'])+"'and password='"+current+"'")
            if q:
                db.update("update login set password='"+new+"' where login_id='"+str(session['lid'])+"'")
                return  '''<script>alert("password changed");window.location="/"</script>'''
            else:
                return '''<script>alert("invalid user");window.location="/change_password"</script>'''
        else:
            return '''<script>alert("password mismatch");window.location="/change_password"</script>'''
    else:
        return render_template('user/user_change_password.html')


@app.route('/change_m_password',methods=['GET','POST'])
def change_m_password():
    if request.method=='POST':
        current=request.form['textfield1']
        new = request.form['textfield2']
        confirm=request.form['textfield3']
        if new==confirm:
            db=Db()
            q=db.selectOne("select * from login where login_id='"+str(session['lid'])+"'and password='"+current+"'")
            if q:
                db.update("update login set password='"+new+"' where login_id='"+str(session['lid'])+"'")
                return  '''<script>alert("password changed");window.location="/"</script>'''
            else:
                return '''<script>alert("invalid user");window.location="/change_password"</script>'''
        else:
            return '''<script>alert("password mismatch");window.location="/change_password"</script>'''
    else:
        return render_template('manager/manager_change_password.html')


if __name__ == '__main__':
    app.run()
