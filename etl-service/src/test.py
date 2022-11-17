import json
from main import app

EVENT = {
    "sleep_duration": "8",
    "heart_rate": '60',
    "efficiency": '50',
    "latency": "3",
    "rem_duration": "2",
    "deep_duration": "2",
    "light_duration": "4",
    "wake_up_count": "12",
    "sleep_quality_score": "90"
}

USER_SETTINGS = {
    "id": "123",
    "DateOfBirth": "ddmmyy",
    "Height": "6,3",
    "Weight": "100lbs",
    "Gender": "male"
}



def test_add_user_event():
    parameters = EVENT
    response = app.test_client().post('/add_user_event', json=parameters)
    assert response.status_code == 200


def test_get_user_events():
    response = app.test_client().get('/get_user_events?id=123')
    assert response.status_code == 200



def test_get_user_hrv_data():
    response = app.test_client().get('/get_user_hrv_data?id=123')
    assert response.status_code == 200


def test_add_user_settings():
    parameters = USER_SETTINGS
    response = app.test_client().post('/add_user_settings', json=parameters)
    assert response.status_code == 200


def test_get_user_settings():
    response = app.test_client().get('/get_user_settings?id=123')
    assert response.status_code == 200
