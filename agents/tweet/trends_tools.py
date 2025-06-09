import http.client
import json
import os
from dotenv import load_dotenv
from urllib.parse import quote_plus
load_dotenv()

HAS_API_KEY = os.getenv("HASDATA_API_KEY")

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

        conn.request(
            "GET",
            f"/scrape/google-trends/search?q={encoded_topic}&geo=IN-DL&region=country&dataType=relatedQueries&date=now+7-d",
            headers=headers
        )

        res = conn.getresponse()
        data = res.read()
        json_data = json.loads(data.decode("utf-8"))

        top_queries = json_data.get('relatedQueries', {}).get('top', [])[:5]

        if not top_queries:
            return "No trending queries found."

        result_lines = [
            f"{idx}. {item.get('query', 'N/A')}: {{{item.get('extractedValue', 'N/A')}}}"
            for idx, item in enumerate(top_queries, 1)
        ]

        return "\n".join(result_lines)

    except Exception as e:
        return f"Error occurred: {str(e)}"



          



#conn.request("GET", "/scrape/google-trends/search?q=Ai&geo=IN-DL&region=country&dataType=relatedQueries&date=now+7-d", headers=headers)
#conn.request("GET", "/scrape/google-trends/search?q=Coffee&geo=IN-DL&region=country&dataType=relatedTopics&date=now+7-d&cat=0", headers=headers)


# Extract rising and top queries
# rising_queries = data['relatedQueries'].get('rising', [])
# top_queries = data['relatedQueries'].get('top', [])

# # Helper function to print query data
# def print_queries(title, queries):
#     print(f"\n--- {title.upper()} ---")
#     for i, item in enumerate(queries, 1):
#         query = item.get('query', 'N/A')
#         value = item.get('value', 'N/A')
#         extracted_value = item.get('extractedValue', 'N/A')
#         link = item.get('link', 'N/A')
#         print(f"{i}. Query: {query}\n   Value: {value}\n   Extracted Value: {extracted_value}\n   Link: {link}\n")

# # Print each section
# #print_queries("Rising", rising_queries)
# print_queries("Top", top_queries)

# import http.client

# conn = http.client.HTTPSConnection("api.hasdata.com")

# headers = {
#     'x-api-key': "acc83333-7d23-402e-9816-31470d47e947",
#     'Content-Type': "application/json"
# }

# conn.request("GET", "/scrape/google-trends/search?q=Ai&geo=IN-DL&region=country&dataType=relatedQueries&date=now+7-d", headers=headers)
# #conn.request("GET", "/scrape/google-trends/search?q=Coffee&geo=IN-DL&region=country&dataType=relatedTopics&date=now+7-d&cat=0", headers=headers)

# res = conn.getresponse()
# data = res.read()

# print(data.decode("utf-8"))

# ans = data.decode("utf-8")

# import json
# data = json.loads(ans)

# # Extract rising and top queries
# rising_queries = data['relatedQueries'].get('rising', [])
# top_queries = data['relatedQueries'].get('top', [])

# # Helper function to print query data
# def print_queries(title, queries):
#     print(f"\n--- {title.upper()} ---")
#     for i, item in enumerate(queries, 1):
#         query = item.get('query', 'N/A')
#         value = item.get('value', 'N/A')
#         extracted_value = item.get('extractedValue', 'N/A')
#         link = item.get('link', 'N/A')
#         print(f"{i}. Query: {query}\n   Value: {value}\n   Extracted Value: {extracted_value}\n   Link: {link}\n")

# # Print each section
# #print_queries("Rising", rising_queries)
# print_queries("Top", top_queries)