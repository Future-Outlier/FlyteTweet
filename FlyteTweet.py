import os
from flytekit import ImageSpec, task, workflow
from flytekitplugins.chatgpt import ChatGPTTask
import requests
from bs4 import BeautifulSoup
import tweepy

# Configure through environment variables
OPENAI_ORG = os.environ.get("OPENAI_ORG")
BEARER_TOKEN = os.environ.get("BEARER_TOKEN")
CONSUMER_KEY = os.environ.get("CONSUMER_KEY")
CONSUMER_SECRET = os.environ.get("CONSUMER_SECRET")
ACCESS_TOKEN = os.environ.get("ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.environ.get("ACCESS_TOKEN_SECRET")

chatgpt_job = ChatGPTTask(
    name="chatgpt",
    config={
        "openai_organization": OPENAI_ORG,
        "chatgpt_conf": {
            "model": "gpt-4",
            "temperature": 0.7,
        },
    },
)

@task
def get_article(url: str) -> str:
    # Sanitize and validate the URL if needed
    response = requests.get(url)
    response.raise_for_status()  # raise an exception for HTTP errors

    soup = BeautifulSoup(response.text, "html.parser")
    texts = soup.stripped_strings
    all_text = " ".join(texts)
    message = (f"You are a FlyteTweet Bot. I want to summarize this article and introduce "
               f"to Flyte Users. You don't need to handle the tweetapi, just focus on the "
               f"summary. Make the return message in 100 characters, this is a Tweet Message. "
               f"Make sure the return message starts from 'Let's check the latest blog from Flyte!' "
               f"{all_text}")

    return message

@task
def tweet(text: str):
    client = tweepy.Client(
        bearer_token=BEARER_TOKEN,
        consumer_key=CONSUMER_KEY,
        consumer_secret=CONSUMER_SECRET,
        access_token=ACCESS_TOKEN,
        access_token_secret=ACCESS_TOKEN_SECRET,
    )
    client.create_tweet(text=text)

@workflow
def wf(url: str):
    message = get_article(url=url)
    message = chatgpt_job(message=message)
    tweet(text=message)

if __name__ == "__main__":
    wf("https://flyte.org/blog/getting-started-with-large-language-models-key-things-to-know")
