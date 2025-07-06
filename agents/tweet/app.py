import streamlit as st
import json
from search_tools import Content_Search
from tweet import print_text_tweet, print_image_tweet
from trends_tools import trending_searches_on_google
from simplify import topic_selection, generate_hastags
import re
import tempfile
import os
import shutil

def main():
    st.set_page_config(page_title="Tweet with Trends Agent", layout="wide")
    st.title("🐦 Tweet with Trends Agent")

    # --- Sidebar: User Profile Editor ---
    st.sidebar.header("🧑‍💻 User Profile")
    default_profile = {
        "age_range": "19-20",
        "profession": "software engineer",
        "interests": ["AI", "fitness", "travel"],
        "about": "A humorous person pursuing software engineering currently as a student with a passion for AI, fitness, and travel. Loves to learn and share knowledge about what I learn.",
    }

    profile_str = st.sidebar.text_area(
        "Edit your user profile (JSON format):",
        value=json.dumps(default_profile, indent=4),
        height=200
    )

    try:
        user_profile = json.loads(profile_str)
        st.sidebar.success("Profile loaded successfully.")
    except Exception:
        st.sidebar.error("Invalid JSON. Please fix the format.")
        return

    # Writer mode (sidebar)
    is_writer = st.sidebar.radio("✍️ Are you a writer?", ["No", "Yes"], index=0)
    show_trending_block = None

    want_suggestions = None
    if is_writer == "Yes":
        want_suggestions = st.sidebar.radio("💡 Want suggestions from trending topics?", ["No", "Yes"], index=1)

        # Main UI form
        
        if is_writer == "Yes" and want_suggestions == "Yes":
            # Show topic input and allow topic trend fetch
            topic = st.sidebar.text_input("🔍 Enter a topic for trending search:")
            show_trending_block = True
        else:
            topic = None
            show_trending_block = False

    else:
        topic = st.sidebar.text_input("🔍 Enter a topic for trending search:")
        show_trending_block = True
        
    go_clicked = False  # Ensure it's defined

    if "trends" not in st.session_state:
        st.session_state["trends"] = ""

    if topic or is_writer == "Yes":
        # Load or refresh topics
        if ('topics_list' not in st.session_state or st.session_state.get("last_topic") != topic) and show_trending_block:
            with st.spinner("Fetching trending topics..."):
                trends = trending_searches_on_google(topic)
                st.session_state["topics_list"] = [
                    re.sub(r'^\d+\.\s*', '', line.strip())
                    for line in trends.strip().split('\n') if line.strip()
                ]
                st.session_state["trends"] = trends
                st.session_state["last_topic"] = topic

        topics_list = st.session_state["topics_list"]

        if ("selected_topic" not in st.session_state) and is_writer == "No":
            with st.spinner("Selecting relevant topic..."):
                st.session_state["selected_topic"] = topic_selection(trends, user_profile) or topics_list[0]

            if "topic_dropdown" not in st.session_state:
                st.session_state["topic_dropdown"] = st.session_state["selected_topic"]

        if is_writer == "No":
            with st.form(key="topic_form"):
                col1, col2 = st.columns([4, 1])
                with col1:
                    selected_index = topics_list.index(st.session_state["selected_topic"]) if st.session_state["selected_topic"] in topics_list else 0
                    selected = st.radio(
                        "Select a topic from the list, best matching is already slected",
                        options=topics_list,
                        index=selected_index,
                        key="selected_trend",
                        help="Click to select a topic you resonate with.",
                        horizontal=True
                    )
                    st.session_state["selected_topic"] = str(selected)
                    st.session_state["topic_dropdown"] = st.session_state["selected_topic"]

                with col2:
                    st.write("")
                    go_clicked = st.form_submit_button("GO")

        elif is_writer == "Yes":
            go_clicked = st.button("GO")
    # --- GO Clicked ---
    if go_clicked:
        st.session_state["tweet_generated"] = False

        if is_writer == "Yes":
            # Use existing text from st.text_area (already set earlier)
            tweet_text = st.session_state.get("topic_dropdown", "")
            st.session_state["final_tweet"] = st.session_state["trends"]
        else:
            # Generate tweet using selected trend/topic
            st.session_state["tweet_content"] = Content_Search(str(st.session_state["topic_dropdown"]), user_profile)
            st.session_state["hashtags"] = generate_hastags(st.session_state["tweet_content"])
            st.session_state["final_tweet"] = st.session_state["tweet_content"] + f" {st.session_state['hashtags']}"
            st.session_state["selected_topic"] = st.session_state["topic_dropdown"]

        st.session_state["tweet_generated"] = True
        if "Image" is not st.session_state:
            st.session_state["Image"] = False


    # --- Display Tweet Editor & Image Option ---
    if st.session_state.get("tweet_generated"):
        tweet_text = st.session_state["final_tweet"]
        st.subheader("✍️ Final Tweet Content")
        edited_tweet = st.text_area("Edit your tweet (max 280 characters):", value=tweet_text, key="tweet_editor")
        st.session_state["edited_tweet"] = edited_tweet

        if len(str(edited_tweet)) > 280:
            st.warning("Tweet exceeds 280 characters.")

        st.subheader("🖼️ Add Image (Optional)")
        image_option = st.radio("Do you want to add an image?", ["No", "Yes"], horizontal=True, key="add_image_option")

        image_urls = []
        if image_option == "Yes":
            number = st.number_input("How many images?", min_value=1, max_value=4, step=1, key="image_count")

            uploaded_files = st.file_uploader(
                "Upload image(s):",
                accept_multiple_files=(number > 1),
                type=["png", "jpg", "jpeg"],
                key="image_uploads"
            )

            image_urls = []
            temp_dir = None

            if uploaded_files:
                temp_dir = tempfile.mkdtemp()
                files_to_process = uploaded_files if isinstance(uploaded_files, list) else [uploaded_files]

                for uploaded_file in files_to_process:
                    file_path = os.path.join(temp_dir, uploaded_file.name)
                    with open(file_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())
                    image_urls.append(file_path)

                if number == 1 and len(image_urls) == 1:
                    image_urls = image_urls[0]

            st.session_state["Image"] = True

        if st.button("🚀 Post Tweet"):
            if image_option == "Yes" and image_urls:
                print_image_tweet(edited_tweet, image_urls, multiple=isinstance(image_urls, list) and len(image_urls) > 1)
            else:
                print_text_tweet(edited_tweet)

            if st.session_state.get("Image") and image_urls and temp_dir:
                shutil.rmtree(temp_dir)
                st.success("✅ Tweet posted successfully with image(s)!")
            else:
                st.success("✅ Tweet posted successfully!")

if __name__ == "__main__":
    main()
