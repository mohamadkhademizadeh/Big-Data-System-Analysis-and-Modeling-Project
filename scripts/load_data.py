import json, orjson
from datetime import datetime, timezone
from pymongo import MongoClient, InsertOne
import pandas as pd
from tqdm import tqdm
from config import *
from scripts.utils_text import extract_hashtags, extract_mentions

def parse_date(s):
    # Accept ISO strings or "YYYY-MM-DD HH:MM:SS"
    try:
        return datetime.fromisoformat(s.replace("Z","+00:00")).astimezone(timezone.utc)
    except Exception:
        return datetime.strptime(s, "%Y-%m-%d %H:%M:%S").replace(tzinfo=timezone.utc)

def to_doc(row: dict):
    created = parse_date(row["created_at"])
    hashtags, hashtags_lc = extract_hashtags(row.get("text",""))
    mentions = extract_mentions(row.get("text",""))
    doc = {
        "_id": str(row["id"]),
        "created_at": created,
        "date_ymd": created.date().isoformat(),
        "month_ym": f"{created.year:04d}-{created.month:02d}",
        "text": row.get("text"),
        "lang": row.get("lang"),
        "user": {
            "user_id": str(row.get("user_id")),
            "screen_name": row.get("user_screen_name"),
        },
        "metrics": {
            "retweet_count": int(row.get("retweet_count") or 0),
            "favorite_count": int(row.get("favorite_count") or 0),
            "reply_count": int(row.get("reply_count") or 0),
            "quote_count": int(row.get("quote_count") or 0),
        },
        "entities": {
            "hashtags": hashtags,
            "hashtags_lc": hashtags_lc,
            "mentions": mentions
        },
        "place": {
            "full_name": row.get("place_full_name"),
            "country_code": row.get("country_code")
        }
    }
    lon, lat = row.get("lon"), row.get("lat")
    if lon not in (None, "") and lat not in (None, ""):
        doc["geo"] = {"type":"Point","coordinates":[float(lon), float(lat)]}
    return doc

def load_jsonl(path):
    with open(path, "rb") as f:
        for line in f:
            if not line.strip():
                continue
            row = orjson.loads(line)
            yield row

def load_csv(path):
    df = pd.read_csv(path, low_memory=False)
    for _, r in df.iterrows():
        row = {k: r.get(v) for k,v in CSV_MAPPING.items()}
        yield row

def main():
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    coll = db[COLL_TWEETS]
    source = load_jsonl(INPUT_PATH) if DATA_FORMAT == "jsonl" else load_csv(INPUT_PATH)
    buffer, n = [], 0
    for row in tqdm(source, desc="Loading"):
        try:
            doc = to_doc(row)
            buffer.append(InsertOne(doc))
            if len(buffer) >= BATCH_SIZE:
                coll.bulk_write(buffer, ordered=False)
                buffer.clear()
        except Exception as e:
            print("Skip row due to error:", e)
        n += 1
    if buffer:
        coll.bulk_write(buffer, ordered=False)
    print(f"Ingested ~{n} rows.")

if __name__ == "__main__":
    main()
