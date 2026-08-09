#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""药物精简（第二阶段）：
1) 别名合并：把冷僻别名药物重定向到常用药（保留常用药，删除别名主表+子表，
   组成 formulas_ingredients 中引用别名的 medicine_id/name 改为常用药）。
2) 冷僻/残缺删除：核心字段全空且非别名的药物直接删除；其在方剂组成中的引用行一并删除。
引用处理原则由 REF_KEEP 决定。
用法: python3 scripts/trim_medicines.py   (默认 db/zhongyi.db)
"""
import sqlite3
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "db", "zhongyi.db")

# 别名药物 id -> 常用药 id（合并，组成重定向）
ALIAS_MAP = {
    "medicine_609": "medicine_514",  # 薯蓣 -> 山药
    "medicine_587": "medicine_254",  # 天门冬 -> 天冬
    "medicine_605": "medicine_044",  # 橘皮 -> 陈皮
    "medicine_607": "medicine_319",  # 葱 -> 葱白
    "medicine_615": "medicine_004",  # 生姜汁 -> 生姜
    "medicine_592": "medicine_041",  # 大附子 -> 附子
    "medicine_594": "medicine_041",  # 天雄 -> 附子
    "medicine_619": "medicine_145",  # 川椒 -> 花椒
    "medicine_595": "medicine_566",  # 干地黄 -> 地黄
    "medicine_612": "medicine_347",  # 茵陈蒿 -> 茵陈
    "medicine_616": "medicine_227",  # 诃梨勒 -> 诃子
}

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

    alias_ids = set(ALIAS_MAP.keys())
    redirect_rows = 0
    alias_del_main = 0
    alias_del_child = 0
    plain_del_main = 0
    plain_del_child = 0
    plain_del_ing = 0

    # ---- 1. 别名合并 ----
    for del_id, keep_id in ALIAS_MAP.items():
        del_name = name_by_id.get(del_id)
        keep_name = name_by_id.get(keep_id)
        if del_name is None or keep_name is None:
            print(f"  跳过(目标缺失): {del_id} -> {keep_id}")
            continue
        # 组成重定向
        rows = cur.execute(
            "SELECT parent_id, name FROM formulas_ingredients WHERE medicine_id=?", (del_id,)
        ).fetchall()
        for r in rows:
            cur.execute(
                "UPDATE formulas_ingredients SET medicine_id=?, name=? "
                "WHERE parent_id=? AND medicine_id=?",
                (keep_id, keep_name, r["parent_id"], del_id),
            )
            redirect_rows += 1
        for t in MED_CHILD_TABLES:
            alias_del_child += cur.execute(
                f"DELETE FROM {t} WHERE parent_id=?", (del_id,)
            ).rowcount
        cur.execute("DELETE FROM medicines WHERE id=?", (del_id,))
        alias_del_main += 1
        print(f"  合并别名: {del_name}({del_id}) -> {keep_name}({keep_id}), 组成重定向 {len(rows)} 条")

    # ---- 2. 冷僻/残缺删除：核心字段全空 且 不在别名集合中 ----
    full_empty = cur.execute(
        """SELECT id FROM medicines WHERE
           (CASE WHEN indications IS NULL OR TRIM(indications)='' THEN 1 ELSE 0 END)+
           (CASE WHEN dosage IS NULL OR TRIM(dosage)='' THEN 1 ELSE 0 END)+
           (CASE WHEN usage IS NULL OR TRIM(usage)='' THEN 1 ELSE 0 END)+
           (CASE WHEN flavor IS NULL OR TRIM(flavor)='' THEN 1 ELSE 0 END)+
           (CASE WHEN nature IS NULL OR TRIM(nature)='' THEN 1 ELSE 0 END)+
           (CASE WHEN meridian IS NULL OR TRIM(meridian)='' THEN 1 ELSE 0 END) >= 4"""
    ).fetchall()
    for r in full_empty:
        did = r["id"]
        if did in alias_ids:
            continue
        dname = name_by_id.get(did, did)
        # 删除组成引用行
        plain_del_ing += cur.execute(
            "DELETE FROM formulas_ingredients WHERE medicine_id=?", (did,)
        ).rowcount
        for t in MED_CHILD_TABLES:
            plain_del_child += cur.execute(
                f"DELETE FROM {t} WHERE parent_id=?", (did,)
            ).rowcount
        cur.execute("DELETE FROM medicines WHERE id=?", (did,))
        plain_del_main += 1

    con.commit()

    # 校验
    orphan = cur.execute(
        "SELECT COUNT(*) FROM formulas_ingredients fi LEFT JOIN medicines m ON fi.medicine_id=m.id "
        "WHERE m.id IS NULL"
    ).fetchone()[0]
    remaining = cur.execute("SELECT COUNT(*) FROM medicines").fetchone()[0]
    con.close()

    print(f"\n别名合并: 删主表 {alias_del_main}, 删子表 {alias_del_child}, 组成重定向 {redirect_rows}")
    print(f"冷僻删除: 删主表 {plain_del_main}, 删子表 {plain_del_child}, 删组成行 {plain_del_ing}")
    print(f"校验 formulas_ingredients 孤儿引用: {orphan} (应为0)")
    print(f"medicines 剩余: {remaining}")


if __name__ == "__main__":
    main()
