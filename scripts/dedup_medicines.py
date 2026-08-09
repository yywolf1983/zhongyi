#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""药物去重：删除仅差"生"前缀的纯别名记录（生X -> X）。
保留更规范常用、无"生"前缀的一条；把被删记录的引用重定向到保留条。
用法: python3 scripts/dedup_medicines.py   (默认 db/zhongyi.db)
"""
import sqlite3
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "db", "zhongyi.db")

# (待删除的生X id, 保留的X id)
PAIRS = [
    ("medicine_025", "medicine_566"),  # 生地黄 -> 地黄
    ("medicine_528", "medicine_056"),  # 生艾叶 -> 艾叶
    ("medicine_541", "medicine_156"),  # 生侧柏叶 -> 侧柏叶
    ("medicine_546", "medicine_506"),  # 生荷叶 -> 荷叶
    ("medicine_624", "medicine_189"),  # 生竹茹 -> 竹茹
]

MED_CHILD_TABLES = [
    "medicines_classic_excerpts",
    "medicines_contraindications",
    "medicines_effect_ids",
    "medicines_effects",
    "medicines_flavor",
    "medicines_indications",
    "medicines_meridian",
    "medicines_meridian_ids",
    "medicines_usage",
]


def main():
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    cur = con.cursor()

    name_by_id = {r["id"]: r["name"] for r in cur.execute("SELECT id, name FROM medicines")}

    total_redirect = 0
    total_del_child = 0
    total_del_main = 0

    for del_id, keep_id in PAIRS:
        del_name = name_by_id.get(del_id)
        keep_name = name_by_id.get(keep_id)
        if del_name is None or keep_name is None:
            print(f"  跳过（id 不存在）: 删{del_id} 留{keep_id}")
            continue

        # 1) 重定向 formulas_ingredients 引用
        rows = cur.execute(
            "SELECT parent_id, name FROM formulas_ingredients WHERE medicine_id=?",
            (del_id,),
        ).fetchall()
        for r in rows:
            cur.execute(
                "UPDATE formulas_ingredients SET medicine_id=?, name=? WHERE parent_id=? AND medicine_id=?",
                (keep_id, keep_name, r["parent_id"], del_id),
            )
            total_redirect += 1
        print(f"  重定向 {del_name}->{keep_name}: formulas_ingredients {len(rows)} 条")

        # 2) 删除子表记录
        for t in MED_CHILD_TABLES:
            c = cur.execute(f"DELETE FROM {t} WHERE parent_id=?", (del_id,)).rowcount
            total_del_child += c

        # 3) 删除主表记录
        cur.execute("DELETE FROM medicines WHERE id=?", (del_id,))
        total_del_main += 1
        print(f"  删除主表: {del_name}({del_id})")

    con.commit()

    # 校验：是否有 formulas_ingredients 仍指向已删 id
    orphan = cur.execute(
        "SELECT COUNT(*) FROM formulas_ingredients fi "
        "LEFT JOIN medicines m ON fi.medicine_id=m.id "
        "WHERE m.id IS NULL"
    ).fetchone()[0]
    con.close()

    print(f"\n完成。重定向 {total_redirect} 条, 删子表 {total_del_child} 条, 删主表 {total_del_main} 条")
    print(f"校验 formulas_ingredients 孤儿引用: {orphan} (应为0)")


if __name__ == "__main__":
    main()
