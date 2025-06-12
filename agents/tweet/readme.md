# Tweet with Trends Agent

A Python-based agent that helps you generate engaging, trending, and personalized tweets using AI, Google Trends, and web research. The agent researches trending topics, crafts tweet content tailored to your profile, and can post directly to Twitter.

## Features

- **Trending Topic Discovery:** Fetches trending Google searches for a given topic.
- **Personalized Tweet Generation:** Uses your profile (age, profession, interests) to select relevant topics and generate tweet content.
- **Web Research:** Summarizes web content to enrich tweets.
- **Hashtag Generation:** Suggests relevant hashtags for your tweet.
- **Direct Tweeting:** Posts text or image tweets to Twitter via the Twitter API.

## Project Structure

- `main.py` — Main entry point; handles user interaction and tweet workflow.
- `trends_tools.py` — Fetches trending Google searches using the HasData API.
- `search_tools.py` — Performs web research and content summarization.
- `browser_tools.py` — Scrapes and summarizes website content.
- `simplify.py` — Selects topics and generates hashtags using LLMs.
- `tweet.py` — Handles Twitter API authentication and posting.
- `requirements.txt` — Python dependencies.

## Setup

1. **Clone the repository** and install dependencies:
   ```sh
   pip install -r requirements.txt
   ```

2. **Set up environment variables** in a `.env` file:
   - `OPENAI_API_KEY`
   - `SERPER_API_KEY`
   - `HASDATA_API_KEY`
   - `TWITTER_API_KEY`, `TWITTER_API_SECRET_KEY`, `TWITTER_BEARER_TOKEN`, `TWITTER_ACCESS_TOKEN`, `TWITTER_ACCESS_TOKEN_SECRET`

3. **Edit your user profile** in `main.py` to personalize tweet generation.

## Usage

Run the main script:
```sh
python main.py
```
- Enter a topic to search for trending tweets.
- Review and approve the generated tweet.
- The agent can post the tweet directly to your Twitter account.

## Notes

- Requires valid API keys for OpenAI, HasData, Serper, and Twitter.
- Make sure your Twitter app has the necessary permissions for posting.