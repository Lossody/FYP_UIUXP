from application.login_model import Login_Entry
import pytest
from flask import json

#======================================================================
# This section test to see if user can be added into database using API 
#======================================================================

@pytest.mark.parametrize('api_register',[
    ['User_1','123456','C'],
    ['User_2','333333','S'],
    ['User_3','654321','E']
])
def test_api_register(client,api_register,capsys):
    with capsys.disabled():
        data1 = {
            'username': api_register[0],
            'password': api_register[1],
            'position': api_register[2],
        }
        response = client.post("/api/register_complete",
        data = json.dumps(data1),
        content_type = "application/json")
        assert response.status_code == 200
        assert response.headers['Content-Type'] == "application/json"
        response_body = json.loads(response.get_data(as_text=True))
        assert response_body['id']
