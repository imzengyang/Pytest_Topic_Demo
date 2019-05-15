import pytest
# *****************    工具   ******************
from config import topic
from config import user_token

@pytest.fixture(scope="module")
def get_topic_id():
    res = topic.post_create_topic(user_token, 'title test xxx', 'ask', 'content test xxxxxx')
    jsdata = res.json()
    return jsdata['topic_id']