import sqlite3, sys
con = sqlite3.connect('db/zhongyi.db'); con.row_factory = sqlite3.Row; c = con.cursor()

rows = c.execute("SELECT id,name,source,pharmacological_effect,beginner_note FROM formulas WHERE advanced_clinical_note IS NULL OR TRIM(advanced_clinical_note) = ''").fetchall()

for r in rows:
    fid = r['id']
    name = r['name']
    inds = [x['value'] for x in c.execute('SELECT value FROM formulas_indications WHERE parent_id=?', (fid,)).fetchall()]
    mods = [x['value'] for x in c.execute('SELECT value FROM formulas_modern_applications WHERE parent_id=?', (fid,)).fetchall()]
    pharm = (r['pharmacological_effect'] or '').strip()
    src = (r['source'] or '').strip()
    src_disp = src if (src.startswith('《') and src.endswith('》')) else (f'《{src}》' if src else '前人经验')

    parts = []
    parts.append(f'【临床应用】本方出自{src_disp}。')
    if inds:
        parts.append('主治' + '；'.join(inds) + '。')
    if mods:
        parts.append('现代临床常用于' + '、'.join(mods[:6]) + '等。')
    if pharm:
        # 取药理首句，避免过长
        p = pharm.split('。')[0].strip()
        if p:
            parts.append('药理研究提示' + p + '。')
    note = ''.join(parts)
    print(f'{fid} {name}')
    print('   ', note)
    print()

if '--apply' in sys.argv:
    for r in rows:
        fid = r['id']
        inds = [x['value'] for x in c.execute('SELECT value FROM formulas_indications WHERE parent_id=?', (fid,)).fetchall()]
        mods = [x['value'] for x in c.execute('SELECT value FROM formulas_modern_applications WHERE parent_id=?', (fid,)).fetchall()]
        pharm = (r['pharmacological_effect'] or '').strip()
        src = (r['source'] or '').strip()
        src_disp = src if (src.startswith('《') and src.endswith('》')) else (f'《{src}》' if src else '前人经验')
        parts = [f'【临床应用】本方出自{src_disp}。']
        if inds:
            parts.append('主治' + '；'.join(inds) + '。')
        if mods:
            parts.append('现代临床常用于' + '、'.join(mods[:6]) + '等。')
        if pharm:
            p = pharm.split('。')[0].strip()
            if p:
                parts.append('药理研究提示' + p + '。')
        note = ''.join(parts)
        c.execute('UPDATE formulas SET advanced_clinical_note=? WHERE id=?', (note, fid))
    con.commit()
    print('APPLIED', len(rows))
