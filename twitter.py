from pprint import pprint
import twitter
import tweepy

API_KEY             = "rg14vbOkkd7HK25j7oQaqZ92B"
API_SECRET          = "GyBYdS5VMXvBt6ObBxGyOqwKErV3FExHIL27R33FyZzQ0d8y4K"
BEARER_TOKEN        ="AAAAAAAAAAAAAAAAAAAAABCgeQEAAAAAgMP3CQoUrrfI4tjQiMJJ%2B1yBB7E%3DXslOTvgcmkVD2U7FgtvdaNk3lJagb3hVheRgbmJQ3OQlSeyZEp"
ACCESS_TOKEN        ="3242100708-QrfqLMs3a0zZuq7hv9At7MV3ukHY60IuOGyDnpS"
ACCESS_TOKEN_SECRET ="t1pKgjcog8ys5L21s0zV6KiaOI0TJ3WRAp07hKcpE9UxK"

message="Hellow World"

def main():
    client = tweepy.Client(consumer_key=API_KEY, consumer_secret=API_SECRET, access_token=ACCESS_TOKEN, access_token_secret=ACCESS_TOKEN_SECRET)
    client.create_tweet(text=message)



if __name__ == "__main__":
    main()


