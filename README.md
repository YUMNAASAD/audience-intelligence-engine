# Pakistan Social Audience & Campaign Intelligence Engine
Clustering-based web app that finds what a Pakistani fashion audience wants, which posts are unusual, and what the marketing team should do next.

## Features
1. Content performance (reels vs photos vs influencer posts...)
2. Comment clustering (TF-IDF character n-grams + KMeans; works on English and Roman Urdu)
3. Anomaly detection (Isolation Forest, compared within the same content type)
4. Audience segments by language and need
5. Rule-based, evidence-driven recommendations

## Run
```
pip install -r requirements.txt
python generate_data.py
streamlit run app.py
```
## Data
Demo data is **simulated** (labeled `data_source=simulated`). Real data must be collected only through permitted methods and platform terms.
