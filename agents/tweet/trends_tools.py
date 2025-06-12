import http.client
import json
import os
from dotenv import load_dotenv
from urllib.parse import quote_plus
load_dotenv()

HAS_API_KEY = os.getenv("HASDATA_API_KEY")
top = 5

def trending_searches_on_google(topic: str) -> str:
    """
    Returns the top 5 trending Google searches in the IN-DL region for the given topic.
    Format: '1. <query>: {<value>}'
    """
    encoded_topic = quote_plus(topic)
    try:
        conn = http.client.HTTPSConnection("api.hasdata.com")
        headers = {
            'x-api-key': str(HAS_API_KEY),
            'Content-Type': "application/json"
        }

        # Here ypu can change location, relatedTopics, relatedQueries, time, etc.
        # https://app.hasdata.com/apis/21 from this link you can know more about the API and its parameters
        conn.request(
            "GET",
            f"/scrape/google-trends/search?q={encoded_topic}&geo=IN-DL&region=country&dataType=relatedQueries&date=now+7-d",
            headers=headers
        )

        res = conn.getresponse()
        data = res.read()
        json_data = json.loads(data.decode("utf-8"))

        top_queries = json_data.get('relatedQueries', {}).get('top', [])[:top]

        if not top_queries:
            return "No trending queries found."

        result_lines = [
            #f"{idx}. {item.get('query', 'N/A')}: {{{item.get('extractedValue', 'N/A')}}}" # For extractedValue
            f"{idx}. {item.get('query', 'N/A')}" # For query only
            for idx, item in enumerate(top_queries, 1)
        ]

        return "\n".join(result_lines)

    except Exception as e:
        return f"Error occurred: {str(e)}"



          



#conn.request("GET", "/scrape/google-trends/search?q=Ai&geo=IN-DL&region=country&dataType=relatedQueries&date=now+7-d", headers=headers)
#conn.request("GET", "/scrape/google-trends/search?q=Coffee&geo=IN-DL&region=country&dataType=relatedTopics&date=now+7-d&cat=0", headers=headers)

