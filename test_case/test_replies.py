import pytest
import json

from config import user_token
from config import topic



#8. 测试新建评论
@pytest.mark.parametrize('content, reply_id, topic_id', [('content0001', None, '5cda54824aac0b7d9436981e'), ('content0002', '5cda6b654aac0b7d94369837', '5cda54824aac0b7d9436981e')])
def test_create_comment(content, reply_id, topic_id):
    res = topic.post_create_comment(user_token, content, reply_id, topic_id)
    jsdata = res.json()
    assert res.status_code == 200
    # 测试返回结果中有评论id
    assert len(jsdata['reply_id']) != 0

# 9. 测试评论点赞
def test_comment_ups():
    res = topic.post_comment_ups(user_token, '5cda54824aac0b7d9436981e')
    jsdata = res.json()
    if jsdata['success'] == False:
        assert len(jsdata['error_msg']) != 0
    else:
        assert len(jsdata['action']) != 0