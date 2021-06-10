import time
from concurrent.futures import TimeoutError
from google.cloud import pubsub_v1

# Create a topic called "ticker"
PROJECT_ID = 'pub-sub-experimentation'
SUB_ID = 'ticker-sub'


def pull_async(subscriber, subscription_path):  
  def callback(msg):
    print("Received message:", msg.data)
    msg.ack()

  future = subscriber.subscribe(subscription_path, callback)
  
  try:
    future.result(timeout=5)
  except TimeoutError:
    print ('I''m tired of waiting')
    future.cancel()

def pull_sync(subscriber, subscription_path):
  def pull(subscriber, subscription_path):
    response = subscriber.pull(
      request={
        "subscription": subscription_path,
        "max_messages": 1, # can return up to this number of messages per pull
      }
    )
    return response 

  response = pull(subscriber, subscription_path)  
  while len(response.received_messages) > 0:
    for msg in response.received_messages:
      print("Received message:", msg.message.data)

    ack_ids = [msg.ack_id for msg in response.received_messages]
    subscriber.acknowledge(
      request={
        "subscription": subscription_path,
        "ack_ids": ack_ids,
      }
    )
    response = pull(subscriber, subscription_path)

    time.sleep(0.1)

def main():
  with pubsub_v1.SubscriberClient() as subscriber:  
    subscription_path = subscriber.subscription_path(PROJECT_ID, SUB_ID)  

    pull_async(subscriber, subscription_path)
    #pull_sync(subscriber, subscription_path)

main()
   