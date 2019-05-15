import pytest
import json
import sys
# import os 

# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import user_token
from config import topic
from config import create_topic_datas




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
    # elif ((tab != 'share') & (tab != 'job') & (tab != 'ask')):
    elif( tab not in ['share','job','ask']):
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
