from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request
import psycopg2

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:root@localhost:5432/covid-records"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]= False
db = SQLAlchemy(app)

class records(db.Model): 
    nric = db.Column(db.VARCHAR, primary_key=True)
    firstName = db.Column(db.VARCHAR)
    lastName = db.Column(db.VARCHAR)
    phoneNumber = db.Column(db.INTEGER)
    address = db.Column(db.String(100))
    emailAddress = db.Column(db.VARCHAR)

    def __init__(self, nric, firstName, lastName, phoneNumber, address, emailAddress):
        self.nric = nric
        self.firstName = firstName
        self.lastName = lastName
        self.phoneNumber = phoneNumber
        self.address = address
        self.emailAddress = emailAddress

# Retrieve all patients' details 
@app.route("/")
def index():
    covid_records = records.query.all()
    return render_template('index.html', records= covid_records)

# Add new patient 
@app.route('/add_patient', methods=['POST', 'GET'])
def add_patient():
    result_message = ""
    if request.method == 'POST':
        nric = request.form["nric"]
        check_dups = records.query.filter_by(nric=nric).first()

        if (check_dups == None): 
            first_name = request.form["first_name"]
            last_name = request.form["last_name"]
            email_address = request.form["email_address"]
            address = request.form["address"]
            phone_number = request.form["phone_number"]

            entry = records(nric, first_name, last_name, phone_number, address, email_address)
            db.session.add(entry)
            db.session.commit()
            result_message = "Individual's record has been successfully added."
        else: 
            result_message = "This individual's record already exists."

    return render_template('add_patient.html', result_msg=result_message)

# Show patient's details 
@app.route('/show_patient', methods=['POST', 'GET'])
def show_patient():
    nric = request.args.get('nric')
    record = records.query.filter_by(nric=nric).first()
    firstName = record.firstName
    lastName = record.lastName
    emailAddress = record.emailAddress
    phoneNumber = record.phoneNumber
    address = str(record.address)
    return render_template('edit_patient.html', nric=nric, firstName=firstName, lastName=lastName, emailAddress=emailAddress, phoneNumber=phoneNumber, address=address)

# Update patient's details
@app.route('/edit_patient', methods=['POST', 'GET'])
def edit_patient():

    if request.method == 'POST':
        nric = request.form["nric"]
        firstName = request.form["first_name"]
        lastName = request.form["last_name"]
        emailAddress = request.form["email_address"]
        phoneNumber = request.form["phone_number"]
        address = request.form["address"]

        update_record = records.query.filter_by(nric=nric).first()

        update_record.firstName = firstName 
        update_record.lastName = lastName 
        update_record.nric = nric
        update_record.emailAddress = emailAddress 
        update_record.phoneNumber = phoneNumber 
        update_record.address = address 

        try: 
            db.session.commit()
            result_message = "Individual's record has been successfully updated."
        except: 
            result_message = "Updating of individual's record has been unsuccessful, please try again."

    return render_template('edit_patient.html', nric=nric, firstName=firstName, lastName=lastName, emailAddress=emailAddress, phoneNumber=phoneNumber, address=address, result_msg=result_message)

# Delete patient's record 
@app.route('/delete_patient', methods=['POST', 'GET'])
def delete_patient():
    nric = request.args.get('nric')
    records.query.filter_by(nric=nric).delete()
    db.session.commit()
    covid_records = records.query.all()
    return render_template('index.html', records=covid_records)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
