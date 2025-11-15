import os, csv, random
from datetime import datetime, timedelta
os.makedirs("data", exist_ok=True)

MERCHANTS = {
  'rent': ['Sunrise Apartments','Oakwood Homes'],
  'utilities': ['City Electric','PureWater','GasWorks'],
  'groceries': ['Trader Joes','Whole Foods','Walmart','Costco'],
  'dining': ['Chipotle','Starbucks','Cafe Roma'],
  'transport': ['Uber','Lyft','Shell','Exxon'],
  'shopping': ['Amazon','Target','Best Buy'],
  'entertainment': ['AMC','Netflix','Spotify','Hulu'],
  'subscriptions': ['Netflix','Spotify','iCloud'],
  'healthcare': ['Walgreens','CVS','City Clinic'],
  'other': ['Misc Store'],
  'income': ['ACME Corp','Payouts Inc']
}

BASE = {
  'light':    dict(income=3500, rent=1200, utilities=150, groceries=250, dining=120, transport=80,  shopping=120, entertainment=80,  subscriptions=30,  healthcare=50,  other=40),
  'moderate': dict(income=4500, rent=1600, utilities=180, groceries=400, dining=250, transport=140, shopping=250, entertainment=150, subscriptions=45,  healthcare=80,  other=80),
  'heavy':    dict(income=5200, rent=1800, utilities=220, groceries=550, dining=450, transport=220, shopping=500, entertainment=300, subscriptions=60,  healthcare=120, other=150)
}

def gen(profile, months=2):
  path = f"data/{profile}.csv"
  with open(path, "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(['txn_id','date','account','merchant','description','amount','category','subcategory','channel','is_recurring','is_income'])
    today = datetime.today().date().replace(day=1)
    tid=1
    for m in range(months):
      start = (today - timedelta(days=30*m)).replace(day=1)
      # income biweekly
      for i in range(2):
        inc = round(BASE[profile]['income'] * random.uniform(0.95,1.05)/2, 2)
        w.writerow([tid, start + timedelta(days=2+i*14),'Checking', random.choice(MERCHANTS['income']),'Paycheck', inc, 'income','salary','ach',1,1]); tid+=1
      # rent monthly
      w.writerow([tid, start + timedelta(days=1),'Checking', random.choice(MERCHANTS['rent']),'Monthly Rent', -BASE[profile]['rent'], 'rent','housing','ach',1,0]); tid+=1
      # utilities
      w.writerow([tid, start + timedelta(days=random.randint(3,10)),'Checking', random.choice(MERCHANTS['utilities']),'Utility Bill', -BASE[profile]['utilities'], 'utilities','bill','ach',1,0]); tid+=1
      # subscriptions (3)
      for _ in range(3):
        w.writerow([tid, start + timedelta(days=random.randint(1,28)),'Credit', random.choice(MERCHANTS['subscriptions']),'Subscription', -round(BASE[profile]['subscriptions']*random.uniform(0.9,1.2),2),'subscriptions','media','card',1,0]); tid+=1
      # random spend
      cats = ['groceries','dining','transport','shopping','entertainment','healthcare','other']
      n = {'light':25,'moderate':45,'heavy':75}[profile]
      for _ in range(n):
        c = random.choice(cats)
        amt = -round(BASE[profile][c] * random.uniform(0.15,0.6), 2)
        w.writerow([tid, start + timedelta(days=random.randint(1,28)), random.choice(['Checking','Credit']),
                    random.choice(MERCHANTS[c]), f'{c} purchase', amt, c,'general', random.choice(['card','pos']),0,0]); tid+=1
  print("Wrote", path)

if __name__ == "__main__":
  for p in ['light','moderate','heavy']:
    gen(p)
