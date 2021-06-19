import sys
import time
from concurrent.futures import TimeoutError
from google.cloud import pubsub_v1

# Create a topic called "ticker"
PROJECT_ID = 'pub-sub-experimentation'

# Specify how long to wait before stopping subscribe
TIMEOUT = 5


def pull_async(subscriber, subscription_path):  
  def callback(msg):
    print("Received message:", subscription_path, msg)
    msg.ack()

  future = subscriber.subscribe(subscription_path, callback)
  
  try:
    future.result(timeout=TIMEOUT)
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
      print("Received message:", subscription_path, msg.message)

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

  args = sys.argv[1:]

  with pubsub_v1.SubscriberClient() as subscriber: 

    if (len(args) < 1):
      print ("Please supply a subscription name")
      return

    subscription_path = subscriber.subscription_path(PROJECT_ID, args[0])
    pull_async(subscriber, subscription_path)

    #pull_sync(subscriber, subscription_path)

main()
   