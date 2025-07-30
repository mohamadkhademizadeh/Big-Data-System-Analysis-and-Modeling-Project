# Title
Analyzing a Large-Scale COVID-19 Twitter Dataset with MongoDB (2022–2023)

## 1. System Overview
- MongoDB architecture: document store, replica sets, sharding
- Consistency model: tunable R/W concern; linearizable reads on primary
- Query language: find, aggregation; text & geo search

## 2. Dataset
- Real-world tweet-like schema (text, user, time, metrics, geo)
- ETL: normalization of hashtags/mentions; derived fields `date_ymd`, `month_ym`

## 3. Conceptual Model (UML)
- Tweet, User, Hashtag, Mention with relationships

## 4. Physical Model
- One document per tweet
- Embedded arrays for hashtags/mentions
- 2dsphere location; indexes: time, hashtag+time, user+time, text, geo

## 5. Deployment
- Docker single-node replica set
- Indexing strategy; shard key options for scale-out

## 6. Queries & Insights (Live Demo)
- Daily volume (trend)
- Top hashtags (overall & per-month)
- Hashtag engagement (avg likes/RTs)
- User activity
- Geo bounding-box counts
- Text search: "vaccine rollout"

## 7. Results & Discussion
- Topic dynamics over time
- Regional heterogeneity
- Trade-offs: write amplification vs. denormalization; shard key choices

## 8. Future Work
- Sentiment classification
- Bot detection signals
- Change-point detection on timelines
