import os

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/?replicaSet=rs0")
DB_NAME = os.getenv("DB_NAME", "covid_twitter")
COLL_TWEETS = os.getenv("COLL_TWEETS", "tweets")
BATCH_SIZE = int(os.getenv("BATCH_SIZE", "5000"))

# Toggle for datasets: "jsonl" or "csv"
DATA_FORMAT = os.getenv("DATA_FORMAT", "jsonl")
INPUT_PATH = os.getenv("INPUT_PATH", "scripts/sample_data.jsonl")  # replace with your dataset path

# If CSV fields differ, map them here
CSV_MAPPING = {
    "id": "id",
    "user_id": "user_id",
    "user_screen_name": "user_screen_name",
    "created_at": "created_at",
    "text": "text",
    "lang": "lang",
    "retweet_count": "retweet_count",
    "favorite_count": "favorite_count",
    "reply_count": "reply_count",
    "quote_count": "quote_count",
    "place_full_name": "place_full_name",
    "country_code": "country_code",
    "lon": "lon",
    "lat": "lat"
}
