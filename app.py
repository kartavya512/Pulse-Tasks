from flask import Flask,render_template,request,url_for,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
app = Flask(__name__)
#databse
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///PulseTasks.db"
app.config["SQLAlchemy_TRACK_MODIFICATIONS"]=False
db = SQLAlchemy(app)

class Tasks(db.Model):
    sno=db.Column(db.Integer,primary_key=True)
    task=db.Column(db.String(200),nullable=False)
    desc=db.Column(db.String(500),nullable=False)
    date=db.Column(db.DateTime,default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno}-{self.task}"
    
with app.app_context():
    db.create_all()

@app.route('/',methods=["GET",'POST'])
def hello_world():
    if(request.method=='POST'):
        
        
        task=request.form["task"]
       
        desc=request.form["desc"]
     
        tasks=Tasks(task=task,desc=desc)
        db.session.add(tasks)
        db.session.commit()
    alltasks=Tasks.query.all()
    
    return render_template('index.html',alltasks=alltasks)

@app.route('/update/<int:sno>',methods=["GET",'POST'])
def update(sno):
     
    if(request.method=='POST'):
        
        
        task=request.form["task"]
       
        desc=request.form["desc"]
        t=Tasks.query.filter_by(sno=sno).first()
        t.task=task
        t.desc=desc
        
        db.session.add(t)
        db.session.commit()
        return redirect('/')
    
    t=Tasks.query.filter_by(sno=sno).first()
    return render_template('update.html', t=t)
    


@app.route('/delete/<int:sno>')
def delete(sno):
   
    task=Tasks.query.filter_by(sno=sno).first()
   
    db.session.delete(task)
    db.session.commit()
    return redirect('/')

if __name__== '__main__':
    app.run(debug=True)