import pytest
from config import user_token
from config import topic


#12. 测试未读消息数
def test_unreadmsg_list():
    res = topic.get_num_unreadmessage(user_token)
    jsdata = res.json()
    assert res.status_code == 200
    assert jsdata['success'] == True

#13. 测试消息列表
@pytest.mark.parametrize('mdrender', ['false', 'true'])
def test_message_list(mdrender):
    res = topic.get_all_message(user_token, mdrender=mdrender)
    jsdata = res.json()
    assert res.status_code == 200
    # 测试mdrender渲染效果一致
    if(mdrender == 'true'):
        has_read_messages = jsdata['data']['has_read_messages']
        if len(has_read_messages) != 0:
            for msg in has_read_messages:
                res_content = msg['reply']['content']
                assert res_content.startswith('<div')
                assert res_content.endswith('</div>')

        hasnot_read_messages = jsdata['data']['hasnot_read_messages']
        if len(has_read_messages) != 0:
            for msg in has_read_messages:
                res_content = msg['reply']['content']
                assert res_content.startswith('<div')
                assert res_content.endswith('</div>')



# 14. 测试标记消息全部已读
def test_mark_allmsg():
    res = topic.post_mark_allmessage(user_token)
    jsdata = res.json()
    assert res.status_code == 200
    assert jsdata['success'] == True

# 15. 测试标记消息单个已读
def test_mark_message():
    res = topic.post_mark_onemessage(user_token, message_id='58ec7d39da8344a81eee0c14')
    jsdata = res.json()
    assert res.status_code == 200
    assert jsdata['success'] == True