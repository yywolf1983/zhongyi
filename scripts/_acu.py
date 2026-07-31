import sqlite3
con = sqlite3.connect('db/zhongyi.db'); con.row_factory = sqlite3.Row; c = con.cursor()
for t in ['acupoints_indications','acupoints_classic_excerpts']:
    print(t, '列:', [r[1] for r in c.execute(f"PRAGMA table_info({t})")])
    n = c.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
    print('  记录数:', n)
# 覆盖统计
ids = [r['id'] for r in c.execute("SELECT id FROM acupoints")]
for t in ['acupoints_indications','acupoints_classic_excerpts']:
    cols = [r[1] for r in c.execute(f"PRAGMA table_info({t})")]
    vcol = 'value' if 'value' in cols else cols[-1]
    rows = c.execute(f"SELECT parent_id FROM {t}").fetchall()
    s = set(r['parent_id'] for r in rows)
    print(f'{t} 覆盖: {sum(1 for i in ids if i in s)}/418')
# 样本
print('\nclassic_excerpts 样本:')
for r in c.execute("SELECT a.name, e.* FROM acupoints_classic_excerpts e JOIN acupoints a ON e.parent_id=a.id LIMIT 3"):
    print('  ', dict(r))
con.close()
