import pytest
import json

from config import topic
from config import user_token
from config import collected_topic
from config import user_name


# 5. 测试收藏主题
def test_collect_topic(get_topic_id):
    res = topic.post_collect_theme(user_token, get_topic_id)
    jsdata = res.json()
    collected_topic.append(get_topic_id)
    assert res.status_code == 200

# 6. 测试取消收藏主题
def test_cancel_collect(get_topic_id):
    res = topic.post_decollect_theme(user_token, get_topic_id)
    jsdata = res.json()
    assert res.status_code == 200

# 7. 测试收藏列表
def test_collect_list():
    res = topic.get_topic_collection(user_name)
    jsdata = res.json()
    print("jsdata==",jsdata)
    assert res.status_code == 200
    is_contain = False
    if(len(collected_topic)):
        assert len(jsdata['data']) != 0
        for item in jsdata['data']:
            if item['id'] == collected_topic[0]:
                is_contain = True
                break
    assert is_contain