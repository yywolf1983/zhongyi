import sqlite3, sys
con = sqlite3.connect('db/zhongyi.db'); con.row_factory = sqlite3.Row; c = con.cursor()
rows = c.execute("SELECT id,name FROM needle_prescriptions WHERE subcategory IS NULL OR TRIM(subcategory) = ''").fetchall()
todo = []
for r in rows:
    ind = c.execute('SELECT value FROM needle_prescriptions_indications WHERE parent_id=? ORDER BY rowid LIMIT 1', (r['id'],)).fetchone()
    if ind and ind['value'].strip():
        sc = ind['value'].strip()
        todo.append((r['id'], r['name'], sc))
        print(f"  {r['id']} {r['name']} -> subcategory={sc}")
    else:
        print(f"  SKIP {r['id']} {r['name']} (no indication)")
if '--apply' in sys.argv:
    for fid, _, sc in todo:
        c.execute('UPDATE needle_prescriptions SET subcategory=? WHERE id=?', (sc, fid))
    con.commit()
    print('APPLIED', len(todo))
