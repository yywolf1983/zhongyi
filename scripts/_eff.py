import sqlite3
con = sqlite3.connect('db/zhongyi.db'); con.row_factory = sqlite3.Row; c = con.cursor()
rows = c.execute("SELECT id,name,description,auto_desc FROM effects WHERE description IS NULL OR TRIM(description)=''").fetchall()
print('effects 缺 description:', len(rows))
for r in rows:
    print(f"  {r['id']} | {r['name']} | auto_desc={r['auto_desc']}")
con.close()
