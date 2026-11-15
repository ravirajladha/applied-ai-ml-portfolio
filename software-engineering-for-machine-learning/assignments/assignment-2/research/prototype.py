# RESEARCH CODE - this is the first draft, kept on purpose as a "before" exhibit.
# It works, but everything is hardcoded, nothing is reusable, there is no
# validation, no logging, no error handling and no tests.
# See ecom/ for the production version of the same idea.
import os, sys, json
import pandas as pd
import numpy   as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import *

df = pd.read_csv( "data/sessions_train.csv" )
print(df.head())

# quick and dirty cleanup
df['avg_item_price'] = df['avg_item_price'].fillna(0)
df["pages_per_minute"]=df["pages_viewed"]/(df["session_duration_min"]+1)
df["cart_value"] = df["cart_items"]*df["avg_item_price"]
df["has_cart"]=(df["cart_items"]>0).astype(int)
d = pd.get_dummies(df["device"])
df = pd.concat([df,d],axis=1)

X = df[["pages_viewed","session_duration_min","cart_items","avg_item_price","is_returning_user","discount_applied","pages_per_minute","cart_value","has_cart","desktop","mobile","tablet"]]
y = df["converted"]

X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.2)   # no seed -> different numbers every run
m = LogisticRegression(max_iter=500)
m.fit(X_train,y_train)   # note: forgot to scale here, but scaled in the notebook - which one is right?
p = m.predict(X_test)
print("accuracy", accuracy_score(y_test,p))
print("f1", f1_score(y_test,p))

# tried this too, left it in
#m2 = RandomForestClassifier()
#m2.fit(X_train,y_train)

# scoring a new session - copy pasted feature order, easy to get wrong
new = [[12,8.5,2,799.0,1,0,1.26,1598.0,1,0,1,0]]
print("prediction:", m.predict(new))
