# pubsub-sample

This is just a simple demo of publishing messags to a pubsub topic and then running a subscriber to pull the data. There are 2 ways to subscribe: `async` and `sync`. Both methods are included in the subscriber.py. Just comment/uncomment the appropriate lines.

## Pre-requisites
Create a topic `ticker` and subscriber `ticker-sub`

## Virtual Environment

Create the virtual environment
```
> virtualenv venv
```

Activate the venv
```
> source venv/bin/activate
```

Deactivate venv
```
> deactivate
```

## Install dependencies
```
pip install --upgrade google-cloud-pubsub
```

## Running it all
```
python publisher.py
python subscriber.py
```