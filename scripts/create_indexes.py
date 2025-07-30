from pymongo import MongoClient, ASCENDING, DESCENDING
from config import MONGO_URI, DB_NAME, COLL_TWEETS

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
coll = db[COLL_TWEETS]

# Time-based queries
coll.create_index([("created_at", DESCENDING)], name="ix_created_at_desc")

# Hashtag analytics (array index)
coll.create_index([("entities.hashtags_lc", ASCENDING), ("created_at", DESCENDING)],
                  name="ix_hashtag_time")

# User-centric queries
coll.create_index([("user.user_id", ASCENDING), ("created_at", DESCENDING)],
                  name="ix_user_time")

# Text search on tweet text (language-aware stemming)
coll.create_index([("text", "text")], default_language="english", name="ix_text")

# Geo queries
coll.create_index([("geo", "2dsphere")], name="ix_geo_2dsphere")

print("Indexes created.")
