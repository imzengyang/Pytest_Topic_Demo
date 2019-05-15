from all_api.api_topics import Topics
from tools.data_tools import get_csv_data


topic = Topics()
user_name = 'user12'
user_token = 'df375d8b-0bf8-4a8e-9265-63dfa2012644'
create_topic_datas = get_csv_data('test_data/create_topics_data.csv')
collected_topic = []