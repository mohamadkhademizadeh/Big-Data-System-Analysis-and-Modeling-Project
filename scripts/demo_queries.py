from pymongo import MongoClient
from config import MONGO_URI, DB_NAME, COLL_TWEETS

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
tweets = db[COLL_TWEETS]

def daily_counts():
    pipeline = [
        {"$group": {"_id": "$date_ymd", "count": {"$sum": 1}}},
        {"$sort": {"_id": 1}}
    ]
    return list(tweets.aggregate(pipeline))

def top_hashtags(limit=20, month=None):
    match = {"month_ym": month} if month else {}
    pipeline = [
        {"$match": match} if match else {"$match": {}},
        {"$unwind": "$entities.hashtags_lc"},
        {"$group": {"_id": "$entities.hashtags_lc", "freq": {"$sum": 1}}},
        {"$sort": {"freq": -1}},
        {"$limit": int(limit)}
    ]
    return list(tweets.aggregate(pipeline))

def hashtag_trend(tag, top_n_days=30):
    pipeline = [
        {"$match": {"entities.hashtags_lc": tag.lower()}},
        {"$group": {"_id": "$date_ymd", "count": {"$sum": 1}}},
        {"$sort": {"_id": 1}},
        {"$limit": int(top_n_days)}
    ]
    return list(tweets.aggregate(pipeline))

def user_activity(user_id, top_n=10):
    pipeline = [
        {"$match": {"user.user_id": str(user_id)}},
        {"$group": {"_id": "$month_ym", "posts": {"$sum": 1},
                    "retweets": {"$sum": "$metrics.retweet_count"},
                    "likes": {"$sum": "$metrics.favorite_count"}}},
        {"$sort": {"_id": 1}},
        {"$limit": int(top_n)}
    ]
    return list(tweets.aggregate(pipeline))

def geo_bbox(west, south, east, north):
    pipeline = [
        {"$match": {"geo": {"$geoWithin": {"$box": [[west, south],[east, north]]}}}},
        {"$group": {"_id": "$date_ymd", "count": {"$sum": 1}}},
        {"$sort": {"_id": 1}}
    ]
    return list(tweets.aggregate(pipeline))

def search_text(query, limit=10):
    cur = tweets.find({"$text": {"$search": query}},
                      {"score": {"$meta":"textScore"}, "text":1, "created_at":1, "user.screen_name":1})\
                .sort([("score", {"$meta":"textScore"})]).limit(int(limit))
    return list(cur)

def hashtag_engagement(top_n=20):
    pipeline = [
        {"$unwind": "$entities.hashtags_lc"},
        {"$group": {
            "_id": "$entities.hashtags_lc",
            "posts": {"$sum": 1},
            "avg_retweets": {"$avg": "$metrics.retweet_count"},
            "avg_likes": {"$avg": "$metrics.favorite_count"}
        }},
        {"$sort": {"avg_likes": -1}},
        {"$limit": int(top_n)}
    ]
    return list(tweets.aggregate(pipeline))

if __name__ == "__main__":
    print("Daily counts:", daily_counts())
    print("Top hashtags:", top_hashtags(limit=10))
    print("Trend #covid19:", hashtag_trend("covid19", top_n_days=60))
    print("User 1001 activity:", user_activity("1001"))
    print("Geo within N Italy bbox:", geo_bbox(6.62, 44.0, 13.0, 46.5))
    print("Search 'vaccine rollout':", search_text("vaccine rollout", limit=5))
    print("Hashtag engagement:", hashtag_engagement(10))
