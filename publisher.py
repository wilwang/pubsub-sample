import base64
import json
from google.cloud import pubsub_v1

# Create a topic called "ticker"
PROJECT_ID = 'pub-sub-experimentation'
TOPIC_ID = 'ticker'

def main():
  publisher = pubsub_v1.PublisherClient()
  topic = publisher.topic_path(PROJECT_ID, TOPIC_ID)
    
  for x in range(20):
    data = {}
    data['symbol'] = 'GOOG'
    data['price'] = x
    json_data = json.dumps(data)

    future = publisher.publish(topic, json_data.encode('utf-8'))
    message_id = future.result()

    print (json_data)

main()