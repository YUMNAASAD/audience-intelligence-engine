# Pakistan Social Audience & Campaign Intelligence Engine

**Live app:** [https://pakistan-audience-engine.streamlit.app/](https://pakistan-audience-engine.streamlit.app/)

A clustering-based analytics project for a Pakistani fashion (lawn suit) brand. It analyses social media posts and comments to find **what the audience wants**, **which posts behave unusually**, and **what the marketing team should do next**.

> **Data note:** the demo dataset is **simulated** (every row has `data_source = simulated`). See [DATA_SOURCES.md](DATA_SOURCES.md).

## Business questions

1. Which content types attract the most attention?
2. What does the audience ask for in comments (price, delivery, discounts, availability...)?
3. Which posts are unusual compared with similar posts?
4. How do audience segments differ by language and need?
5. What actions should the marketing team take?

## Methods

| Task | Method |
|---|---|
| Content performance | Engagement rate = (likes + comments + shares) / views x 100 |
| Comment grouping | TF-IDF on character n-grams + KMeans clustering |
| Unusual posts | Isolation Forest, compared within the same content type |
| Recommendations | Rule-based, driven by cluster sizes and engagement results |

Character n-grams are used because Roman Urdu has no fixed spelling (e.g. *kitna / kitnaa / ketna*).

## Key results (simulated data)

- **Reels** have the highest engagement rate (about 7.6%); **Product Photos** the lowest (about 4.0%). Reels lead on all three platforms.
- Platforms and campaigns differ only slightly (about 5.5% to 5.8%).
- 71% of comments are in Roman Urdu and 29% in English.
- The largest comment groups concern **discounts/sales, delivery and price**.
- Discount comments are most frequent under Sale Announcements; fabric questions under Product Photos; praise under Influencer Posts.
- The Isolation Forest flagged **80 of 2,000 posts** (4%) as unusual, including posts with very high engagement and posts with many comments but few likes.

## Project structure

- `generate_data.py` - generates the simulated posts and comments
- `engine.py` - analysis functions (metrics, clustering, anomaly detection, recommendations)
- `app.py` - Streamlit dashboard with 5 tabs
- `notebooks/` - step-by-step analysis notebooks (01 to 04)
- `data/` - CSV data files
- `DATA_SOURCES.md` - data provenance (simulated vs real)

## How to run

    pip install -r requirements.txt
    python generate_data.py
    streamlit run app.py

To run the notebooks, also install `ipykernel` and `matplotlib` and open them in VS Code or Jupyter.

## Limitations

- The data is simulated, so findings show the method working, not real market behaviour.
- Cluster names are generated from frequent words and can be unclear because common Roman Urdu words such as "hai" are not removed.
- Recommendations are rule-based and should be checked by a human.
- The anomaly detector depends on the `contamination` setting (40, 80 or 160 posts at 2%, 4%, 8%).

## Future work

- Replace simulated data with real, permitted data (e.g. brand-owned analytics).
- Add a Roman Urdu stop-word list and better cluster naming.
- Add sentiment analysis and A/B-test tracking.
- Deploy the dashboard online.
