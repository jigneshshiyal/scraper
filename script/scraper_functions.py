import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from database_functions import insert_post, create_database
from tqdm import tqdm

# 📌 Scrape and Store Posts in Database
def scrape_reddit(subreddit, db_name,post_limit):
    create_database(db_name)

    base_url = f"https://old.reddit.com/r/{subreddit}/"
    headers = {"User-Agent": "Mozilla/5.0"}
    next_page = base_url

    num_posts = 0
    print(post_limit)
    while num_posts < post_limit:
        response = requests.get(next_page, headers=headers)
        if response.status_code != 200:
            print("Failed to fetch data")
            break

        soup = BeautifulSoup(response.text, "html.parser")

        # Extract posts
        for post in soup.find_all("div", class_="thing"):
            title = post.find("a", class_="title").text
            link = urljoin(base_url, post.find("a", class_="title")["href"])
            votes = post.find("div", class_="score unvoted")
            votes = votes.text if votes else "0"
            comments = post.find("a", string=lambda text: text and "comment" in text.lower())
            comments = comments.text if comments else "0 comments"
            author = post.find("a", class_="author")
            author = author.text if author else "Unknown"
            date = post.find("time")["datetime"] if post.find("time") else "Unknown"

            # Insert into database
            id = insert_post(title, link, votes, comments, author, date, db_name)
            print(num_posts)
            if id!=None:
                num_posts += 1
                print(num_posts)

        # Find the next page button
        next_button = soup.find("span", class_="next-button")
        if next_button:
            next_page = next_button.find("a")["href"]
        else:
            break  # No more pages
    return num_posts