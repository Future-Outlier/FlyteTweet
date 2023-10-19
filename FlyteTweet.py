from flytekit import ImageSpec, task, workflow
from flytekitplugins.chatgpt import ChatGPTTask

chatgpt_job = ChatGPTTask(
    name="chatgpt",
    config={
        "openai_organization": "org-NayNG68kGnVXMJ8Ak4PMgQv7",
        "chatgpt_conf": {
            "model": "gpt-4",
            "temperature": 0.7,
        },
    },
)

@task
def get_article(
    url: str = "https://flyte.org/blog/getting-started-with-large-language-models-key-things-to-know",
) -> str:
    import requests
    from bs4 import BeautifulSoup

    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    texts = soup.stripped_strings
    all_text = " ".join(texts)
    message = f"You are a FlyteTweet Bot.\n\
                I want to summarize this article and introduce to Flyte Users.\n\
                You don't need to handle the tweetapi, just focus on the summary.\n\
                Make the return message in 100 characters, this is a Tweet Message.\n\
                Make sure the return message starts from 'Let's check the latest blog from Flyte!'\n\
                {all_text}"

    return message


@task
def tweet(text: str):
    import tweepy
    print("@@@ text:", text)
    client = tweepy.Client(
        bearer_token="AAAAAAAAAAAAAAAAAAAAAA1XqgEAAAAA1hfKvJHzlCSuY2dVtcrh11%2BhirE%3D6xAO4XMwAnxUd991uObQ3kNmyPWvgCL8XbsNt5qFpWs8DHzHE5",
        consumer_key="Pdte2Po2e6XmiWmTPYsmm0s42",
        consumer_secret="5lniLAidFkcKAmfGrI9br6BLqCnU53XcQYZv7FnMP5rRg2MPyn",
        access_token="1714653527858159616-TRtxqsqAb0STZaeAO3C6WTzqZ1OkmQ",
        access_token_secret="pLsEQDOjn9MSXVOSaM3DJ409f28dgDdBJkN1FkpIbp9BJ",
    )
    client.create_tweet(text=text)


@workflow
def wf(
    url: str = "https://flyte.org/blog/getting-started-with-large-language-models-key-things-to-know",
):
    message = get_article(url=url)
    message = chatgpt_job(message=message)
    tweet(text=message)


if __name__ == "__main__":
    wf()
