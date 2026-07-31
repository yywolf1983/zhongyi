import sqlite3
con = sqlite3.connect('db/zhongyi.db'); con.row_factory = sqlite3.Row; c = con.cursor()
MULTI = {'解表药','清热药','泻下药','祛风湿药','利水渗湿药','止血药','活血化瘀药',
         '化痰止咳平喘药','安神药','平肝息风药','补益药','收涩药'}
bad = c.execute("SELECT id,name,category FROM medicines WHERE subcategory IS NULL OR TRIM(subcategory)=''").fetchall()
bad = [r for r in bad if r['category'] in MULTI]
print('多级大类仍缺子类:', len(bad))
for r in bad: print('  ', r['id'], r['name'], r['category'])
tot = c.execute("SELECT COUNT(*) FROM medicines WHERE subcategory IS NULL OR TRIM(subcategory)=''").fetchone()[0]
print('全部仍缺子类:', tot)
