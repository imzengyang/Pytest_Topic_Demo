import requests
import json

class Topics(object):
    base_url = 'http://39.107.96.138:3000/api/v1'

    def __init__(self):
        print(self.base_url)

    # 用户登录
    def user_login(name='user12', password='123456'):
        url = self.base_url + '/sign'

    #1. 主题首页
    def get_home_topics(self, page=1, limit=20, mdrender=False, tab=None):
        url = self.base_url + '/topics'
        params = {'page':page, 'limit':limit, 'mdrender':mdrender, 'tab':tab}
        res = requests.get(url, params=params)
        return res

    #2. 主题详情
    def get_topic_detail(self, token, topic_id, mdrender=False):
        url = self.base_url + '/topic/{}'.format(topic_id)
        params = {'accesstoken':token, 'mdrender':mdrender} 
        res = requests.get(url, params=params)
        return res

    #3. 新建主题
    def post_create_topic(self, token, title, tab, content):
        url = self.base_url + '/topics'
        data = {'accesstoken':token, 'title':title, 'tab':tab, 'content':content}
        res = requests.post(url, data=data)
        return res

    #4. 编辑主题
    def post_edit_topic(self, token, title, tab, content, topic_id):
        url = self.base_url + '/topics/update'
        data = {'accesstoken':token, 'title':title, 'tab':tab, 'content':content, 'topic_id':topic_id}
        res = requests.post(url, data=data)
        return res

    #5. 收藏主题
    def post_collect_theme(self, token, topic_id):
        url = self.base_url + '/topic_collect/collect'
        data = {'accesstoken':token, 'topic_id':topic_id}
        res = requests.post(url, data)
        return res

    #6. 取消收藏
    def post_decollect_theme(self, token, topic_id):
        url = self.base_url + '/topic_collect/de_collect'
        data = {'accesstoken':token, 'topic_id':topic_id}
        res = requests.post(url, data)
        return res

    #7. 用户收藏列表
    def get_topic_collection(self, loginname):
        url = self.base_url + '/topic_collect/' + loginname
        res = requests.get(url)
        return res

    #8. 新建评论
    def post_create_comment(self, token, content, reply_id, topic_id):
        url = self.base_url + '/topic/{}/replies'.format(topic_id)
        data = {'accesstoken':token, 'content':content, 'reply_id':reply_id}
        res = requests.post(url, data=data)
        return res

    #9. 为评论点赞
    def post_comment_ups(self, token, reply_id):
        url = self.base_url + '/reply/{}/ups'.format(reply_id)
        res = requests.post(url, data={'accesstoken':token})
        return res

    #10. 用户详情
    def get_userinfo_detail(self, loginname):
        url = self.base_url + '/user/{}'.format(loginname)
        res = requests.get(url)
        return res
        
    #11. 验证token
    def post_verify_token(self, token):
        url = self.base_url + '/accesstoken'
        res = requests.post(url, data={'accesstoken':token})
        return res

    #12. 获取未读消息数
    def get_num_unreadmessage(self, token):
        url = self.base_url + '/message/count'
        params = {'accesstoken':token}
        res = requests.get(url, params)
        return res

    #13. 获取已读和未读消息
    def get_all_message(self, token, mdrender=False):
        url = self.base_url + '/messages'
        params = {'accesstoken':token, 'mdrender':mdrender}
        res = requests.get(url, params)
        return res

    #14. 标记全部已读
    def post_mark_allmessage(self, token):
        url = self.base_url + '/message/mark_all'
        res = requests.post(url, data={'accesstoken':token})
        return res

    #15.标记单个已读
    def post_mark_onemessage(self, token, message_id):
        url = self.base_url + '/message/mark_one/{}'.format(message_id)
        res = requests.post(url, data={'accesstoken':token})
        return res

if __name__ == "__main__":
    topic = Topics()
    res = topic.post_create_topic(token='df375d8b-0bf8-4a8e-9265-63dfa2012644', title='title', tab='ask', content='content')
    print(res.json())