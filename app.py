from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
# from send_mail import send_mail

app = Flask(__name__)

ENV = 'prod'

if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = ''
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://kuuwkzrcubexsf:18c924cf3abf84471d37c2bdd8460c3644fca2a3d94d7620f0d0b2a3fb44e653@ec2-34-200-94-86.compute-1.amazonaws.com:5432/d12gum4pr39dlr'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Feedback(db.Model):
    __tablename__ = 'feedback'
    id = db.Column(db.Integer, primary_key=True)
    customer = db.Column(db.String(200), unique=True)
    dealer = db.Column(db.String(200))
    rating = db.Column(db.Integer)
    comments = db.Column(db.Text())

    def __init__(self, customer, dealer, rating, comments):
        self.customer = customer
        self.dealer = dealer
        self.rating = rating
        self.comments = comments


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        customer = request.form['customer']
        dealer = request.form['dealer']
        rating = request.form['rating']
        comments = request.form['comments']
        print(customer, dealer, rating, comments)
        if customer == '' or dealer == '':
            return render_template('index.html', message='Please enter required fields')
        if db.session.query(Feedback).filter(Feedback.customer == customer).count() == 0:
            data = Feedback(customer, dealer, rating, comments)
            db.session.add(data)
            db.session.commit()
            # send_mail(customer, dealer, rating, comments)
            return render_template('success.html')
        return render_template('index.html', message='You have already submitted feedback')
    
@app.route('/view', methods=['POST'])
def view():
    if request.method == 'POST':
        num_rows = db.session.query(Feedback).count()
        if num_rows == 0:
            return render_template('allFeedbacks.html', message='No record exists')
        feedbacks = Feedback.query.all()
        return render_template('allFeedbacks.html', msg=feedbacks)

@app.route('/back', methods=['POST'])
def back():
    if request.method == 'POST':
        return render_template('index.html')

@app.route('/clear', methods=['POST'])
def clear():
    if request.method == 'POST':
        try:
            num_rows_deleted = db.session.query(Feedback).delete()
            db.session.commit()
        except:
            db.session.rollback()
        
        if num_rows_deleted == 0:
            return render_template('allFeedbacks.html', message='No record exists')
        return render_template('allFeedbacks.html', message='Successfully deleted')

if __name__ == '__main__':
    app.run()
