from search_tools import Content_Search
from tweet import print_text_tweet, print_image_tweet
from trends_tools import trending_searches_on_google
from simplify import topic_selection, generate_hastags

user_profile = {
    "age_range": "19-20",
    "profession": "software engineer",
    "interests": ["AI", "fitness", "travel"],
    "about": "A humorous person pursuing software engineering currently as a student with a passion for AI, fitness, and travel. Loves to learn and share knowledge about what I learn.",
}

def main():
    # == Basic User Interaction ==
    print("Welcome to the Tweet with Trends Agent and I hope you filled user profile in the code and filled all environment variables in .env file")
    topic = input("Enter a topic to search for trending tweets: ")

    # Fetching trending tweets based on the topic
    print("\nFetching trending tweets...\n")
    trends = trending_searches_on_google(topic)
    print("Trending Searches on Google:")
    print(trends)

    # Selecting a topic based on user profile and trending keywords
    print("\nSelecting a relevant topic for your tweet...\n")
    selected_topic = topic_selection(trends, user_profile)
    print(f"Selected Topic: {selected_topic}")

    # researching content for the selected topic and tweet generation
    print("\nResearching content for the selected topic...\n")
    tweet_content = Content_Search(selected_topic, user_profile)
    print(f"Generated Tweet Content: {tweet_content}")

    # Validating the tweet content
    if len(tweet_content) > 280:
        print("The tweet content is too long. Please try again.")
        return
    
    # Generating hashtags for the tweet
    hashtags = generate_hastags(tweet_content)
    tweet_content += f" {hashtags}"
    print(f"Final Tweet Content with Hashtags: {tweet_content}")

    # Asking user for agreement on the generated tweet content
    print("\nReview the generated tweet content:")
    print("Do you agree with the generated tweet content? (yes/cancel/edit)")
    user_agreement = input().strip().lower()
    if user_agreement == 'cancel':
        print("Please try again with a different topic.")
        return
    elif user_agreement == 'edit':
        print("Please edit the tweet content:")
        tweet_content = input().strip()
        if len(tweet_content) > 280:
            print("The edited tweet content is still too long. Please try again.")
            return
    
    # Everything looks good, let's check for images
    print("\nDo you want to add an image to your tweet? (yes/no)")
    add_image = input().strip().lower()

    if add_image.lower() == 'yes':
        number = int(input("Please provide the number of images: "))
    
        if number == 1:
            image_url = input("Please provide the image URL: ").strip()
            image_urls = image_url  # Wrap in a list
            print_image_tweet(tweet_content, image_urls)
        
        elif number > 1:
            input_urls = input("Please provide the image URLs separated by commas: ").strip()
            image_urls = [url.strip() for url in input_urls.split(',') if url.strip()]
            print_image_tweet(tweet_content, image_urls, multiple=True)

        else:
            print("No images will be added to the tweet.")
            ask = input("Do you want to tweet the content without images? (yes/no): ").strip().lower()
            if ask == 'yes':
                print_text_tweet(tweet_content)
            else:
                print("Please try again with a different topic.")

    else:
        print_text_tweet(tweet_content)
    
    print("thank you for using the Tweet with Trends Agent! Your tweet has been posted successfully.")
    
if __name__ == "__main__":
    main()
    
    









