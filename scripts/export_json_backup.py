#!/usr/bin/env python3
"""从 zhongyi.db 反向导出全部 9 张表的嵌套 JSON 备份。

规则：
- 主表标量列直接保留。
- 凡存在子表 `{table}_{field}`，该字段一律从子表还原为列表（子表为空时退回主表标量真实值）。
  这样可避免当初导入时把"列表字段"误存进主表标量列的 Python repr 垃圾串进入备份。
- 子表若仅含 `value` 列 -> 字符串列表；否则 -> 对象列表（其余列即对象字段）。
- 行顺序按 rowid（即原始 JSON 顺序）还原。
"""
import sqlite3, json, os

DB = "db/zhongyi.db"
OUT = "assets/data_backup"

FILES = {
    "syndromes": "syndromes.json",
    "medicines": "medicines.json",
    "acupoints": "acupoints.json",
    "formulas": "formulas.json",
    "needle_prescriptions": "needle_prescriptions.json",
    "treatments": "treatments.json",
    "meridians": "meridians.json",
    "effects": "effects.json",
    "modern_mapping": "modern_mapping.json",
}


def child_tables(cur, table):
    """返回 {suffix: [col, ...]} 仅含非 parent_id 的列。用前缀过滤避免 LIKE 通配符歧义。"""
    out = {}
    names = [r[0] for r in cur.execute("SELECT name FROM sqlite_master WHERE type='table'")]
    for name in names:
        if name != table and name.startswith(table + "_"):
            cols = [r[1] for r in cur.execute(f"PRAGMA table_info({name})")]
            out[name[len(table) + 1:]] = [c for c in cols if c != "parent_id"]
    return out


def main():
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    os.makedirs(OUT, exist_ok=True)

    for table, fname in FILES.items():
        main_cols = [r[1] for r in cur.execute(f"PRAGMA table_info({table})")]
        childs = child_tables(cur, table)
        list_fields = set(childs.keys())

        rows = cur.execute(f"SELECT * FROM {table} ORDER BY rowid").fetchall()
        out = []
        for row in rows:
            obj = {}
            for c in main_cols:
                if c in list_fields:
                    continue  # 由子表还原
                v = row[c]
                obj[c] = v
            for suffix, cols in childs.items():
                child = f"{table}_{suffix}"
                crows = cur.execute(
                    f"SELECT * FROM {child} WHERE parent_id=? ORDER BY rowid",
                    (row["id"],),
                ).fetchall()
                if crows:
                    if cols == ["value"]:
                        obj[suffix] = [r["value"] for r in crows]
                    else:
                        obj[suffix] = [{k: r[k] for k in cols} for r in crows]
                else:
                    # 子表为空：退回主表标量真实值（非列表 repr）
                    obj[suffix] = row[suffix] if suffix in main_cols else None
            out.append(obj)

        path = os.path.join(OUT, fname)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(out, f, ensure_ascii=False, indent=2)
        print(f"{fname:28s} {len(out):5d} 条  -> {path}")

    con.close()
    print("\n完成：全部 9 表 JSON 备份已写入", OUT)


if __name__ == "__main__":
    main()
