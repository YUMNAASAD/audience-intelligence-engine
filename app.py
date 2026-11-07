import streamlit as st, pandas as pd
import engine as E
st.set_page_config(page_title="Audience & Campaign Intelligence Engine",layout="wide")
st.title("Pakistan Social Audience & Campaign Intelligence Engine")
p,c=E.load(); p=E.add_metrics(p)
st.sidebar.header("Filters")
pf=st.sidebar.multiselect("Platform",sorted(p.platform.unique()),default=sorted(p.platform.unique()))
cp=st.sidebar.multiselect("Campaign",sorted(p.campaign.unique()),default=sorted(p.campaign.unique()))
p=p[p.platform.isin(pf)&p.campaign.isin(cp)]; c=c[c.post_id.isin(p.post_id)]
if "simulated" in set(p.data_source): st.warning("Demo uses SIMULATED data. Replace data/*.csv with real permitted data.")
k=st.sidebar.slider("Number of comment clusters",3,12,8)
perf=E.content_performance(p); cc=E.cluster_comments(c,k); an=E.find_anomalies(p)
t1,t2,t3,t4,t5=st.tabs(["1. Content","2. Audience wants","3. Unusual posts","4. Audience segments","5. Next steps"])
with t1:
    st.subheader("Which content attracts attention?"); st.dataframe(perf); st.bar_chart(perf.avg_engagement_rate)
with t2:
    st.subheader("What does the audience want?"); st.bar_chart(cc.cluster_name.value_counts())
    for n in cc.cluster_name.unique():
        with st.expander(n): st.write(cc[cc.cluster_name==n].comment_text.drop_duplicates().head(6).tolist())
with t3:
    st.subheader("Posts that differ from comparable posts"); st.dataframe(an[an.anomaly].sort_values("anomaly_score",ascending=False)
      [["post_id","platform","campaign","content_type","views","likes","comments_count","engagement_rate","anomaly_score"]])
with t4:
    st.subheader("Segments by language and need"); st.dataframe(pd.crosstab(cc.cluster_name,cc.language_type))
with t5:
    st.subheader("Recommended actions")
    for r in E.recommendations(cc,perf): st.markdown("- "+r)
