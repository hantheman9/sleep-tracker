from flask import Flask, json, request, jsonify
import firebase_admin
from firebase_admin import credentials, firestore
import json
import uuid
import os


#TODO
#parse xml files coming from applewatch application


app = Flask(__name__)

cred = credentials.Certificate('cred.json')
firebase_admin.initialize_app(cred)
db = firestore.client()


def add_data(collection, data):
    try:
        data.update({
            'timestamp': firestore.SERVER_TIMESTAMP
        })
        data_ref = db.collection(str(collection)).document(str(data['id']))
        data_ref.collection(u'data').document(str(uuid.uuid1())).set(data)
        return f'Successfully added data to {collection}', 200
    except:
        return f'Failed to add data to {collection}', 500


def get_latest_data(collection, user_id):
    try:
        events_collection = db.collection(str(collection)).document(user_id).collection(u'data').\
            order_by(u'timestamp', direction=firestore.Query.DESCENDING).\
            limit(1).stream()
        events = []
        for event in events_collection:
            events.append(event.to_dict())
        return jsonify(events), 200
    except:
        return f'Failed to get latest data from {collection}', 500


def get_data(collection, user_id, latest="false"):
    if latest == 'true':
        return get_latest_data(collection, user_id)
    try:
        events_collection = db.collection(str(collection)).document(user_id).collection(u'data').get()
        events = []
        for event in events_collection:
            events.append(event.to_dict())
        return jsonify(events), 200
    except:
        return f'Failed to get data from {collection}', 500


@app.route('/add_user_event', methods=['POST'])
def add_event():
    data = request.get_json()
    return add_data('events', data)


@app.route('/add_user_settings', methods=['POST'])
def add_user_settings():
    data = request.get_json()
    return add_data('users-settings', data)


@app.route('/get_user_settings', methods=['GET'])
def get_user_settings():
    user_id = request.args.get("id")
    return get_data('users-settings', user_id, request.args.get("latest"))

# Starting application on 8080 port
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))