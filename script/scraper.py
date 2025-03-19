from scraper_functions import scrape_reddit
import math

POST_LIMIT = 1000

subraddit_name = "india"
db_name = f"{subraddit_name}.db"

# num_post = math.ceil(POST_LIMIT//30)

num_post_scrap = scrape_reddit(subraddit_name, db_name, POST_LIMIT)
print(f"Scraped {num_post_scrap} posts from r/{subraddit_name}")


