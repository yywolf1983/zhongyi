#!/usr/bin/env python3
"""全面数据质量分析（只读，不改数据）：
1) 字段填全率（每列非空比例）
2) 引用双向一致性缺口（可安全增补的方向）
3) 重名 / 空白 / 首尾空格 / 全角半角等格式问题
"""
import sqlite3, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB = os.path.join(ROOT, "db", "zhongyi.db")
con = sqlite3.connect(DB); con.row_factory = sqlite3.Row; cur = con.cursor()
TABLES = ["syndromes","medicines","acupoints","formulas","needle_prescriptions",
          "treatments","meridians","effects","modern_mapping"]

def childs(t):
    out={}
    for (n,) in cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE ?",(t+"\\_%",)):
        cols=[r[1] for r in cur.execute(f"PRAGMA table_info({n})")]
        out[n[len(t)+1:]]=[c for c in cols if c!="parent_id"]
    return out

# ---- 1. 字段填全率 ----
print("#"*70); print("# 一、字段填全率（空=None/''/纯空白）"); print("#"*70)
for t in TABLES:
    cols=[r[1] for r in cur.execute(f"PRAGMA table_info({t})")]
    n=cur.execute(f"SELECT COUNT(*) c FROM {t}").fetchone()["c"]
    print(f"\n## {t} ({n} 条)")
    ch=childs(t)
    for c in cols:
        if c=="id": continue
        empty=cur.execute(f'SELECT COUNT(*) c FROM {t} WHERE "{c}" IS NULL OR TRIM("{c}")=\'\'').fetchone()["c"]
        rate=100*(n-empty)/n if n else 0
        if rate<100:
            print(f"   {c:24s} 填全率 {rate:5.1f}%  空 {empty}")
    for suf,cc in ch.items():
        # 子表：统计有多少父记录完全没有该列表
        has=cur.execute(f"SELECT COUNT(DISTINCT parent_id) c FROM {t}_{suf}").fetchone()["c"]
        rate=100*has/n if n else 0
        print(f"   [列表]{suf:22s} 覆盖 {rate:5.1f}%  有数据的记录 {has}")

# ---- 2. 双向引用缺口 ----
print("\n"+"#"*70); print("# 二、双向引用缺口（A 引用 B，但 B 未反向引用 A）"); print("#"*70)
# 用集合计算。先收集所有 list 引用到内存（数据量小）
def collect_list_refs(t):
    """返回 {field: {parent_id: set(vals)}}"""
    res={}
    for suf,cc in childs(t).items():
        field=suf
        rows=cur.execute(f"SELECT parent_id, value FROM {t}_{suf}").fetchall() if "value" in cc else \
             cur.execute(f"SELECT parent_id, {cc[0]} AS v FROM {t}_{suf}").fetchall()
        d={}
        for r in rows:
            d.setdefault(r["parent_id"],set()).add(r["v"])
        res[field]=d
    return res

refs={t:collect_list_refs(t) for t in TABLES}

# 定义双向对：(A表, A引用字段, A引用目标表, B表, B反向字段)
BIDIR=[
 ("formulas","syndrome_ids","syndromes","syndromes","related_formulas"),
 ("formulas","related_syndromes","syndromes","syndromes","related_formulas"),
 ("formulas","effect_ids","effects","effects","related_formulas"),
 ("medicines","effect_ids","effects","effects","related_medicines"),
 ("effects","related_medicines","medicines","medicines","effect_ids"),
 ("effects","related_formulas","formulas","formulas","effect_ids"),
 ("effects","related_syndromes","syndromes","syndromes","related_effects"),
 ("syndromes","related_effects","effects","effects","related_syndromes"),
 ("syndromes","related_formulas","formulas","formulas","syndrome_ids"),
 ("syndromes","related_needle","needle_prescriptions","needle_prescriptions","related_syndromes"),
 ("syndromes","related_treatments","treatments","treatments","related_syndromes"),
 ("needle_prescriptions","related_syndromes","syndromes","syndromes","related_needle"),
 ("treatments","related_formulas","formulas","formulas","syndrome_ids"),
 ("treatments","related_needle","needle_prescriptions","needle_prescriptions","related_syndromes"),
 ("treatments","related_syndromes","syndromes","syndromes","related_treatments"),
 ("meridians","related_acupoints","acupoints","acupoints","meridian_id"),
]
for A,af,B,B2,bf in BIDIR:
    if af not in refs[A] or bf not in refs.get(B2,{}):
        continue
    a_map=refs[A][af]; b_map=refs[B2][bf]
    gap=0
    for pid,vals in a_map.items():
        for v in vals:
            bset=b_map.get(v,set())  # v 是目标表 id，b_map 以目标表 id 为键
            if pid not in bset:
                gap+=1
    if gap:
        print(f"   {A}.{af} -> {B}.{bf}: 反向缺失 {gap}")

# ---- 3. 重名 ----
print("\n"+"#"*70); print("# 三、主表 name 重复"); print("#"*70)
NAMECOL={"modern_mapping":"chinese_term"}
for t in TABLES:
    nc=NAMECOL.get(t,"name")
    rows=cur.execute(f'SELECT "{nc}" AS nm, COUNT(*) c FROM {t} GROUP BY "{nc}" HAVING COUNT(*)>1').fetchall()
    if rows:
        print(f"   {t}.{nc}: {len(rows)} 个重名", [dict(r) for r in rows[:10]])

# ---- 4. 格式问题 ----
print("\n"+"#"*70); print("# 四、格式问题（首尾空格 / 全角数字 / 多余标点）"); print("#"*70)
for t in TABLES:
    cols=[r[1] for r in cur.execute(f"PRAGMA table_info({t})")]
    for c in cols:
        if c=="id": continue
        ws=cur.execute(f'SELECT COUNT(*) c FROM {t} WHERE "{c}" IS NOT NULL AND ("{c}"<>TRIM("{c}") OR "{c}" LIKE "%  %")').fetchone()["c"]
        if ws: print(f"   {t}.{c}: 首尾/连续空格 {ws}")

con.close()
print("\n分析结束。")
