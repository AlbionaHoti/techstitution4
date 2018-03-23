from flask import Flask, render_template, request, redirect, url_for
from flask_pymongo import PyMongo
from bson import ObjectId

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'albi'
mongo = PyMongo(app)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        # Query to retrieve data from DB
        audits = mongo.db.audit.find()
        return render_template('index.html', audits=audits)
    elif request.method == 'POST':
        data = request.form
        accident = data['accident']  # Getting audit name
        airprox = data['airprox']  # Getting audit ref num value
        incident = data['incident']
        infringement = data['infringement']
        occurrenceposition = data['occurrenceposition']
        optionFLALT = data['optionFLALT']
        # inputdate = data['date']

        # Query for inserting into DB
        mongo.db.audit.insert({
            "accident": accident,
            "airprox": airprox,
            "incident": incident,
            "infringement": infringement,
            "occurrenceposition": occurrenceposition,
            "optionFLALT": optionFLALT
            # "inputdate" : inputdate
        })
        return ("Success")


@app.route('/audit/<string:audit_id>', methods=['GET', 'POST'])
def show(audit_id):
    if request.method == 'GET':
        # Query to get specific audit
        audit = mongo.db.audit.find_one({"_id": ObjectId(audit_id)})

        return render_template('show.html', audit=audit)


# Editing audit
@app.route('/edit/audit/<string:audit_id>', methods=['GET', 'POST'])
def edit(audit_id):
	if request.method == 'GET':
		# Query to get specific audit

		audit = mongo.db.audit.find_one({"_id": ObjectId(audit_id)})

		return render_template('edit.html', audit=audit)
	elif request.method == 'POST':
		try:
			edit_data = request.form
			mongo.db.audit.update({"_id": ObjectId(audit_id)}, {'$set': {
				"accident": edit_data['accident'],
				"airprox": edit_data['airprox'],
				"incident": edit_data['incident'],
				"infringement": edit_data['infringement'],
				"occurrenceposition": edit_data['occurrenceposition'],
				"optionFLALT": edit_data['optionFLALT']
			}})
		except Exception as e:
			return str(e)
	return redirect(url_for("show", audit_id=audit_id))


# Delete the specific audit
@app.route('/audit/delete/<string:audit_id>', methods=['GET', 'POST'])
def delete(audit_id):
    if request.method == 'GET':
        # Query to delete specific audit
        mongo.db.audit.remove({"_id": ObjectId(audit_id)})
        return redirect(url_for("index", audit_id=audit_id))


if __name__ == '__main__':
    app.run(port=5000, host='0.0.0.0', debug=True)

# Terminal
# show dbs
# use techstitution4
# db.audit.find().pretty()
