from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

model=ChatOpenAI(model="gpt-4o")

def topic_selection(treding_keywords, user_profile) -> str:
    """
    Select a relevant topic for a tweet based on trending keyword data and user profile.
    
    Args:
        treding_keywords (str): A list of trending keywords with their scores.
        user_profile (dict): A dictionary containing user profile information such as age range, profession, and interests.
        
    Returns:
        str: The generated tweet content.
    """

    system_prompt = (
        f"You are a helpful twitter post creator fot user age range {user_profile['age_range']}, "
        f"working as a {user_profile['profession']} and he is {user_profile['about']} interested in {', '.join(user_profile['interests'])}. "
        "Your task is to generate engaging and relevant tweets based on the user's interests and profession. "
        "You will be provided with a list of trending topics with score(range of 0-100), choose the one topic accouting relevance to the user profile and trends."
        "and you should choose one topic from the list that can be used to make tweets that are informative, entertaining, and aligned with the user's profile. "
        "One return the chosen topic from the list, no preamble, no explanation, just the topic itself. "
    )

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "Following are the trending keyword with score : \n{input}\n"),
    ])

    chain = prompt | model

    result = chain.invoke({"input": treding_keywords},)
    return str(result.content)

def generate_hastags(tweet_content):
    """
    Generate hashtags for a given tweet content.
    
    Args:
        tweet_content (str): The content of the tweet.
        
    Returns:
        str: A string of hashtags relevant to the tweet content.
    """
    
    system_prompt = (
        "You are a helpful assistant that generates relevant hashtags for tweets. "
        "Given the tweet content, create a list of 3-4 hashtags that are relevant and popular. "
        "The hashtags should be concise and related to the main topics of the tweet and total resposne not exceed 20 characters."
        "Return only the hashtags, separated by commas, without any additional text or explanation."
    )

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{tweet_content}"),
    ])

    chain = prompt | model

    result = chain.invoke({"tweet_content": tweet_content},)
    return result.content