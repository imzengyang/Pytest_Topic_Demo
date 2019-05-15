import pytest
import json

from config import topic
from config import user_token


# 10. 测试用户详情
@pytest.mark.parametrize('username', ['user1', 'user2', 'user3', 'user12'])
def test_user_detail(username):
    res = topic.get_userinfo_detail(username)
    jsdata = res.json()
    loginname = jsdata['data']['loginname']
    assert loginname == username

#11. 测试accesstoken正确性
def test_verify_token():
    res = topic.post_verify_token(user_token)
    jsdata = res.json()
    assert res.status_code == 200
    assert jsdata['success'] == True