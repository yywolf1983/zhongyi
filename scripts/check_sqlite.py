#!/usr/bin/env python3
"""对 db/zhongyi.db 做全量引用完整性 / 一致性 / 覆盖校验，输出中文报告。
用法: python3 scripts/check_sqlite.py
"""
import os
import sqlite3

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB = os.path.join(ROOT, "db", "zhongyi.db")
con = sqlite3.connect(DB)
con.row_factory = sqlite3.Row
cur = con.cursor()
TABLES = ["syndromes", "medicines", "acupoints", "formulas",
          "needle_prescriptions", "treatments", "meridians", "effects", "modern_mapping"]


def q(sql):
    return cur.execute(sql).fetchall()


def line(c="="):
    print(c * 60)


print("数据库:", DB)
line()

# ---------- 一、悬空引用（list 子表引用其他表） ----------
print("一、悬空引用（list 子表字段引用了不存在的 id）")
line()
REF_MATRIX = [
    ("formulas_ingredients", "medicine_id", "medicines", "id"),
    ("formulas_effect_ids", "value", "effects", "id"),
    ("formulas_syndrome_ids", "value", "syndromes", "id"),
    ("formulas_related_syndromes", "value", "syndromes", "id"),
    ("needle_prescriptions_acupoints", "acupoint_id", "acupoints", "id"),
    ("needle_prescriptions_related_syndromes", "value", "syndromes", "id"),
    ("medicines_effect_ids", "value", "effects", "id"),
    ("medicines_meridian_ids", "value", "meridians", "id"),
    ("effects_related_medicines", "value", "medicines", "id"),
    ("effects_related_formulas", "value", "formulas", "id"),
    ("effects_related_syndromes", "value", "syndromes", "id"),
    ("syndromes_related_effects", "value", "effects", "id"),
    ("syndromes_related_formulas", "value", "formulas", "id"),
    ("syndromes_related_needle", "value", "needle_prescriptions", "id"),
    ("syndromes_related_treatments", "value", "treatments", "id"),
    ("meridians_related_acupoints", "value", "acupoints", "id"),
    ("meridians_related_syndromes", "value", "syndromes", "id"),
    ("treatments_related_formulas", "value", "formulas", "id"),
    ("treatments_related_needle", "value", "needle_prescriptions", "id"),
    ("treatments_related_syndromes", "value", "syndromes", "id"),
]
total = 0
for child, fk, tgt, tk in REF_MATRIX:
    sql = (f'SELECT c.parent_id, c.{fk} FROM "{child}" c '
           f'LEFT JOIN "{tgt}" t ON c.{fk}=t.{tk} '
           f'WHERE c.{fk} IS NOT NULL AND c.{fk}<>\'\' AND t.{tk} IS NULL')
    rows = q(sql)
    total += len(rows)
    if rows:
        print(f"\n[ {child}.{fk} -> {tgt} ] 命中 {len(rows)}")
        for r in rows[:20]:
            print("   ", dict(r))
print(f"\n>>> list 引用悬空合计: {total}")

# ---------- 标量引用 ----------
print("\n" + "=" * 60)
print("二、标量引用悬空（acupoints.meridian_id / modern_mapping.related_syndrome）")
print("=" * 60)
SCALAR_REFS = [
    ("acupoints", "meridian_id", "meridians", "id"),
    ("modern_mapping", "related_syndrome", "syndromes", "id"),
]
stotal = 0
for tbl, fk, tgt, tk in SCALAR_REFS:
    sql = (f'SELECT t.id, t.{fk} FROM "{tbl}" t '
           f'LEFT JOIN "{tgt}" s ON t.{fk}=s.{tk} '
           f'WHERE t.{fk} IS NOT NULL AND t.{fk}<>\'\' AND s.{tk} IS NULL')
    rows = q(sql)
    stotal += len(rows)
    if rows:
        print(f"\n[ {tbl}.{fk} -> {tgt} ] 命中 {len(rows)}")
        for r in rows[:20]:
            print("   ", dict(r))
print(f"\n>>> 标量引用悬空合计: {stotal}")

# ---------- 名称一致性 ----------
print("\n" + "=" * 60)
print("三、名称一致性（子表 name 与引用表规范名）")
print("=" * 60)
consistency = [
    ("方剂组成 name 与药材库不一致",
     "SELECT fi.parent_id, fi.medicine_id, fi.name AS 组成名, m.name AS 药材库名 "
     "FROM formulas_ingredients fi JOIN medicines m ON fi.medicine_id=m.id WHERE fi.name<>m.name"),
    ("针方穴位 name 与穴位库不一致",
     "SELECT na.parent_id, na.acupoint_id, na.name AS 针方名, a.name AS 穴位库名 "
     "FROM needle_prescriptions_acupoints na JOIN acupoints a ON na.acupoint_id=a.id WHERE na.name<>a.name"),
]
cm = 0
for name, sql in consistency:
    rows = q(sql)
    cm += len(rows)
    print(f"\n[ {name} ] 命中 {len(rows)}")
    for r in rows[:20]:
        print("   ", dict(r))
print(f"\n>>> 名称不一致合计: {cm}")

# ---------- id 重复 ----------
print("\n" + "=" * 60)
print("四、id 重复")
print("=" * 60)
id_dup = 0
for tbl in TABLES:
    rows = q(f'SELECT id, COUNT(*) c FROM "{tbl}" GROUP BY id HAVING COUNT(*)>1')
    if rows:
        id_dup += len(rows)
        print(f"{tbl} id 重复: {len(rows)}", [dict(r) for r in rows[:10]])
print(">>> id 重复合计:", id_dup)

# ---------- name 空 ----------
print("\n" + "=" * 60)
print("五、主表 name 空")
print("=" * 60)
for tbl in TABLES:
    rows = q(f'SELECT id, "name" FROM "{tbl}" WHERE "name" IS NULL OR "name"=\'\'')
    if rows:
        print(f"{tbl}.name 空: {len(rows)}", [dict(r) for r in rows[:10]])

# ---------- 覆盖统计 ----------
print("\n" + "=" * 60)
print("六、方剂来源覆盖统计")
print("=" * 60)
print("方剂总数:", q("SELECT COUNT(*) c FROM formulas")[0]["c"])
print("source 含'伤寒':", q("SELECT COUNT(*) c FROM formulas WHERE source LIKE '%伤寒%'")[0]["c"])
print("source 含'金匮':", q("SELECT COUNT(*) c FROM formulas WHERE source LIKE '%金匮%'")[0]["c"])
print("\n各表记录数:")
for tbl in TABLES:
    print(f"  {tbl}: {q(f'SELECT COUNT(*) c FROM {tbl}')[0]['c']}")

con.close()
print("\n校验完成。")
