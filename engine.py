import numpy as np, pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.ensemble import IsolationForest
def load():
    return pd.read_csv("data/posts.csv"), pd.read_csv("data/comments.csv")
def add_metrics(p):
    p=p.copy(); v=p.views.clip(lower=1)
    p["engagement_rate"]=(p.likes+p.comments_count+p.shares)/v*100
    return p
def content_performance(p):
    return (p.groupby("content_type").agg(posts=("post_id","count"),avg_likes=("likes","mean"),
      avg_comments=("comments_count","mean"),avg_shares=("shares","mean"),avg_engagement_rate=("engagement_rate","mean"))
      .round(2).sort_values("avg_engagement_rate",ascending=False))
def cluster_comments(c,k=8):
    vec=TfidfVectorizer(analyzer="char_wb",ngram_range=(2,4),lowercase=True)  # char n-grams cope with Roman Urdu spelling
    X=vec.fit_transform(c.comment_text.str.lower())
    km=KMeans(n_clusters=k,n_init=10,random_state=42).fit(X); c=c.copy(); c["cluster"]=km.labels_
    wvec=TfidfVectorizer(stop_words="english",token_pattern=r"[a-zA-Z]{3,}")
    names={}
    for cl in range(k):
        txt=c[c.cluster==cl].comment_text
        try:
            M=wvec.fit_transform(txt); top=np.asarray(M.sum(0)).ravel().argsort()[::-1][:3]
            names[cl]=", ".join(wvec.get_feature_names_out()[top])
        except ValueError: names[cl]="misc"
    c["cluster_name"]=c.cluster.map(names); return c
def find_anomalies(p,contamination=0.04):
    p=add_metrics(p); v=p.views.clip(lower=1)
    F=pd.DataFrame({"like_r":p.likes/v,"com_r":p.comments_count/v,"share_r":p.shares/v,"logv":np.log1p(p.views)})
    F=F.groupby(p.content_type).transform(lambda s:(s-s.mean())/(s.std()+1e-9))  # compare with similar posts only
    iso=IsolationForest(contamination=contamination,random_state=42).fit(F)
    p["anomaly"]=iso.predict(F)==-1; p["anomaly_score"]=-iso.score_samples(F); return p
def recommendations(c,perf):
    share=c.cluster_name.value_counts(normalize=True)*100; recs=[]
    best=perf.index[0]; worst=perf.index[-1]
    recs.append(f"CONTENT: '{best}' has the highest engagement rate ({perf.avg_engagement_rate.iloc[0]}%). Make more of it; test whether '{worst}' needs a rework.")
    for name,pct in share.head(4).items():
        low=name.lower()
        if any(w in low for w in ["discount","sale","off","code"]): recs.append(f"PROMOTION ({pct:.0f}% of comments: {name}): Run a visible limited-time offer and pin the discount details.")
        elif any(w in low for w in ["delivery","order","time","days"]): recs.append(f"CUSTOMER SERVICE ({pct:.0f}%: {name}): Post delivery timelines in captions and auto-reply with tracking info.")
        elif any(w in low for w in ["price","rate","expensive"]): recs.append(f"PRICING ({pct:.0f}%: {name}): Put price in the caption; A/B test price-in-caption vs. inbox.")
        elif any(w in low for w in ["available","stock","size","karachi"]): recs.append(f"AVAILABILITY ({pct:.0f}%: {name}): Add size/city availability in a story highlight.")
        else: recs.append(f"INSIGHT ({pct:.0f}%: {name}): Review sample comments and decide a content or service response.")
    recs.append("TESTING: A/B test one change per campaign (e.g. price in caption) and compare engagement rate and comment mix.")
    return recs
