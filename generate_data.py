"""Generates SIMULATED posts + comments for a lawn-suit brand demo.
Replace with real (permitted) data later. Output is labeled data_source='simulated'."""
import random, numpy as np, pandas as pd
random.seed(42); np.random.seed(42)
BRANDS=["Brand A","Brand B","Brand C"]; PLATFORMS=["Instagram","TikTok","Facebook"]
CAMPAIGNS=["Eid Collection","11.11 Sale","12.12 Sale","Winter Lawn"]
BASE={"Reel":1.6,"Product Photo":0.8,"Influencer Post":1.3,"Styling Video":1.1,"Sale Announcement":1.0}
T={"Price inquiry":["Price please?","Price kya hai?","Rate bata dein","Kitne ka hai ye suit?","price?"],
"Price complaint":["Price bohat zyada hai.","Itna mehnga kyun hai?","Too expensive for lawn","Rate bohat high hai"],
"Discount":["Any discount on this suit?","Sale kab lag rahi hai?","Discount code hai koi?","11.11 pe kitna off hoga?"],
"Delivery":["Delivery kitne din mein hogi?","Ordered last week, still waiting.","Order abhi tak nahi pohancha","Lahore delivery time?"],
"Availability":["Is this available in Karachi?","Stock mein hai?","Medium size available hai?","Islamabad store mein milega?"],
"Fabric":["Fabric kaisa hai?","Is it pure cotton lawn?","Quality achi hai ya nahi?","Colour fade to nahi hota?"],
"Praise":["Very beautiful dress!","Bohat khoobsurat!","Love this collection","Mashallah gorgeous"],
"Inbox request":["Inbox me details send kar dein.","DM details please","Inbox kardo price"]}
def weights(ctype,camp):
    w={k:1.0 for k in T}
    if "Sale" in camp or ctype=="Sale Announcement": w["Discount"]*=3; w["Price complaint"]*=1.5
    if ctype=="Influencer Post": w["Praise"]*=2.5; w["Inbox request"]*=2
    if ctype=="Product Photo": w["Fabric"]*=2.5; w["Availability"]*=2
    if camp=="Eid Collection": w["Delivery"]*=2.5
    return w
posts,comments=[],[]
for i in range(2000):
    pid=f"P{i+1:04d}"; ct=random.choice(list(BASE)); camp=random.choice(CAMPAIGNS); pf=random.choice(PLATFORMS)
    views=int(np.random.lognormal(10,0.6)*BASE[ct]); likes=int(views*np.random.uniform(.02,.06)*BASE[ct])
    cc=int(views*np.random.uniform(.002,.008)*BASE[ct]); sh=int(views*np.random.uniform(.001,.005))
    if random.random()<0.03:  # injected unusual posts
        likes*=random.choice([4,.15]); cc*=random.choice([6,.1])
    posts.append(dict(post_id=pid,brand=random.choice(BRANDS),platform=pf,campaign=camp,content_type=ct,
      product_category="Lawn suit",likes=int(likes),comments_count=int(cc),shares=sh,views=views,
      days_since_post=random.randint(1,30),data_source="simulated"))
    w=weights(ct,camp)
    for _ in range(3):
        t=random.choices(list(w),weights=list(w.values()))[0]; txt=random.choice(T[t])
        comments.append(dict(post_id=pid,comment_text=txt,true_topic=t,
          language_type="English" if txt.isascii() and any(x in txt for x in ["Price please","Any discount","Is this","Very beautiful","DM","Too expensive","Ordered","Love","Is it"]) else "Roman Urdu",
          data_source="simulated"))
pd.DataFrame(posts).to_csv("data/posts.csv",index=False); pd.DataFrame(comments).to_csv("data/comments.csv",index=False)
print(len(posts),"posts,",len(comments),"comments saved in data/")
