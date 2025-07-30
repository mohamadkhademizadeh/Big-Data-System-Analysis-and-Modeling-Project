# COVID Twitter Analytics on MongoDB

A university-style project showing end-to-end use of a distributed NoSQL system (MongoDB) on a large real-world dataset of COVID-related tweets.

## Quick start

```bash
# 1) Start services
./scripts/init.sh    # or: docker compose up -d

# 2) Python env
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# 3) Load your dataset (JSONL preferred)
export INPUT_PATH=/absolute/path/to/your.jsonl
export DATA_FORMAT=jsonl   # or csv
python scripts/load_data.py

# 4) Create indexes
python scripts/create_indexes.py

# 5) Run demo pipelines
python scripts/demo_queries.py
```

Mongo Express UI: http://localhost:8081 (admin/admin).

## Dataset format

Minimal fields:
- `id`, `created_at`, `text`, `user_id`, `user_screen_name`
Optional: `lang`, metric counts, `lon`/`lat`, `place_full_name`, `country_code`.

For CSVs, edit `CSV_MAPPING` in `config.py`.

## Models

- Conceptual UML in `models/conceptual_uml.md` (Mermaid).
- Physical model example document in `models/physical_model.json`.

## Scale-out notes

- Replica set enabled (single-node for dev).
- Suggested shard key if scaling: `{ month_ym: 1, user.user_id: "hashed" }`.
- Indexes: time, hashtag+time, user+time, text, geo.

## License

MIT — see LICENSE.
