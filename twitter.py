from pprint import pprint
import twitter
import tweepy
import schedule
import time

API_KEY             = "iSS54YjOPjxrY3qxhZqarY30E"
API_SECRET          = "yVKi9NlGLGbP2v3gLAWJ2ZgJUzovlmWPyZORmzwnHrCFac7WGF"
BEARER_TOKEN        ="AAAAAAAAAAAAAAAAAAAAABCgeQEAAAAAeL13JUfh0KBwzKibmwJQbhLPvp8%3Dj6nHZ6NSWgcuUtlWbvfjp6NsmtiO2NlWn4zTzk8bzXjry9fO4x"
ACCESS_TOKEN        ="3242100708-w30GLvPiUH0xQ1G4N7wq6yZwSjAo1qYlDaffU4Q"
ACCESS_TOKEN_SECRET ="tK0Y0tlAZ5xYq37Bu0FFfQjEtK1N8MxwdrrjauDbaFMhw"

message="Hello World"

def main():
    schedule.every(1).minutes.do(CreateTweet, message=message)
    while True:
        schedule.run_pending()
        time.sleep(1)
    
def ClientInfo():
    client = tweepy.Client( consumer_key=API_KEY,
                             consumer_secret=API_SECRET, 
                             access_token=ACCESS_TOKEN, 
                             access_token_secret=ACCESS_TOKEN_SECRET)
    return client

def CreateTweet(message):
    tweet = ClientInfo().create_tweet(text=message)
    return tweet



if __name__ == "__main__":
    main()


