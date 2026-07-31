import sqlite3
con = sqlite3.connect('db/zhongyi.db'); con.row_factory = sqlite3.Row; c = con.cursor()
for f in ['note','beginner_note','advanced_clinical_note','pharmacological_effect','modern_applications','usage','source']:
    n = c.execute(f"SELECT COUNT(*) FROM formulas WHERE {f} IS NULL OR TRIM({f})=''").fetchone()[0]
    print(f'{f}: 空 {n}/490')
# beginner_note 为空的，看是否都有 indication/组成 可生成
empty = c.execute("SELECT id,name FROM formulas WHERE beginner_note IS NULL OR TRIM(beginner_note)=''").fetchall()
print('beginner_note 空:', len(empty))
con.close()
