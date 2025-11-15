import pandas as pd

KW = {
  'rent':'rent','apartment':'rent','uber':'transport','lyft':'transport','shell':'transport','exxon':'transport',
  'amazon':'shopping','netflix':'subscriptions','hulu':'subscriptions','spotify':'subscriptions',
  'grocery':'groceries','whole foods':'groceries','trader joes':'groceries','walmart':'groceries',
  'walgreens':'healthcare','cvs':'healthcare','chipotle':'dining','starbucks':'dining','restaurant':'dining','movie':'entertainment'
}

def guess_category(desc: str) -> str:
  d = str(desc).lower()
  for k,v in KW.items():
    if k in d: return v
  return 'other'

def ensure_category(df: pd.DataFrame) -> pd.DataFrame:
  if 'category' not in df.columns:
    df['category'] = df['description'].apply(guess_category)
  return df
