import pytest
import json
import sys
import os 

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from all_api.api_topics import Topics
from tools import data_tools

topic = Topics()
user_name = 'user12'
user_token = 'df375d8b-0bf8-4a8e-9265-63dfa2012644'
create_topic_datas = data_tools.get_csv_data('test_data/create_topics_data.csv')
collected_topic = []

# *****************    工具   ******************
@pytest.fixture
def get_topic_id():
    res = topic.post_create_topic(user_token, 'title test xxx', 'ask', 'content test xxxxxx')
    jsdata = res.json()
    return jsdata['topic_id']

# *****************    测试用例   ******************
#1. 测试主题首页
@pytest.mark.parametrize('tab, limit, mdrender', [('ask', '1', 'false'), ('share', '10', 'false'), ('share', '8', 'true')])
def test_home_topics(tab, limit, mdrender):
    res = topic.get_home_topics(tab=tab, limit=limit, mdrender=mdrender)
    jsdata = res.json()
    # 测试请求数据条数是否与请求参数limit一致
    assert len(jsdata['data']) <= int(limit) 
    for item in jsdata['data']:
        # 测试数据类型是否与请求参数ask一致
        assert item['tab'] == tab
        # 测试数据渲染效果是否与请求参数mdrender一致
        if mdrender == 'true':
            assert (item['content']).startswith('<div')
            assert (item['content']).endswith('</div>')

# 2. 测试主题详情
@pytest.mark.parametrize('mdrender', ['false', 'true', 'false'])
def test_topic_detail(mdrender, get_topic_id):
    res = topic.get_topic_detail(user_token, topic_id=get_topic_id, mdrender=mdrender)
    jsdata = res.json()
    realdata = jsdata['data']
    # 测试数据的topic_id是否与参数一致
    assert realdata['id'] == get_topic_id
    # 测试数据渲染效果是否与请求参数mdrender一致
    if mdrender == 'true':
            assert (realdata['content']).startswith('<div')
            assert (realdata['content']).endswith('</div>')

# 3. 测试新建主题
@pytest.mark.parametrize('title, tab, content', create_topic_datas)
def test_create_topic(title, tab, content):
    res = topic.post_create_topic(user_token, title, tab, content)
    jsdata = res.json()
    if len(title) < 5:
        # 测试标题字数太多或太少
        assert res.status_code == 400
        assert jsdata['error_msg'] == '标题字数太多或太少'
    elif ((tab != 'share') & (tab != 'job') & (tab != 'ask')):
        assert res.status_code == 400
        assert jsdata['error_msg'] == '必须选择一个版块'
    else: 
        assert res.status_code == 200

# 4. 测试编辑主题
@pytest.mark.parametrize('title, tab, content', [('happy', 'ask', 'happy content'), ('sad', 'share', 'sad content xxx')])
def test_edit_topic(get_topic_id, title, tab, content):
    res = topic.post_edit_topic(user_token, title, tab, content, get_topic_id)
    jsdata = res.json()
    # 测试编辑接口是否调取成功
    assert res.status_code == 200 
    # 测试topic_id是否一致
    if jsdata['success'] == 'true':
        res_topicid = jsdata['topic_id']
        assert res_topicid == get_topic_id

# 5. 测试收藏主题
def test_collect_topic(get_topic_id):
    res = topic.post_collect_theme(user_token, get_topic_id)
    jsdata = res.json()
    collected_topic.append(get_topic_id)
    print('vvvvvvvvv', collected_topic)
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
    assert res.status_code == 200
    is_contain = False
    if(len(collected_topic)):
        assert len(jsdata['data']) != 0
        for item in jsdata['data']:
            if item['id'] == collected_topic[0]:
                is_contain = True
                break
    assert is_contain

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