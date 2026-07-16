#!/usr/bin/env python3
import json
import os

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'assets', 'data')

ALLOWED_ASPECTS = {
    '症状', '核心症状', '病因', '病理', '病理机制', '病理意义', '机制', '病机',
    '功效', '主治', '组成', '治法', '治则', '西医对应', '临床表现',
    '卫分证', '气分证', '营分证', '血分证', '上焦', '中焦', '下焦'
}

def load(name):
    with open(os.path.join(DATA_DIR, name), 'r', encoding='utf-8') as f:
        return json.load(f)

def save(name, data):
    with open(os.path.join(DATA_DIR, name), 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def to_text(v):
    if v is None:
        return ''
    if isinstance(v, list):
        return '；'.join(str(x).strip() for x in v if str(x).strip())
    return str(v).strip()

def norm_classic(s):
    if not s:
        return ''
    s = s.strip()
    if not s.startswith('《'):
        s = '《' + s
    if not s.endswith('》'):
        s = s + '》'
    return s

def syndrome_classic(s):
    cats = s.get('category', []) or []
    name = s.get('name', '') or ''
    cls_text = ' '.join(s.get('classification', []) or [])
    blob = name + cls_text
    if '六经辨证' in cats:
        return '《伤寒论》'
    if '卫气营血辨证' in cats or '三焦辨证' in cats:
        return '《温病条辨》'
    if '经络辨证' in cats:
        return '《针灸甲乙经》'
    if '脏腑辨证' in cats:
        if any(k in blob for k in ['脾', '胃', '脾胃']):
            return '《脾胃论》'
        return '《金匮要略》'
    if '气血津液辨证' in cats:
        return '《金匮要略》'
    if '八纲辨证' in cats:
        return '《伤寒论》'
    if '病因辨证' in cats or '六淫辨证' in cats:
        return '《黄帝内经》'
    if '病机辨证' in cats:
        return '《黄帝内经》'
    return '《黄帝内经》'

def clean_rows(rows):
    if not rows:
        return []
    out = []
    seen = set()
    for r in rows:
        if not isinstance(r, dict):
            continue
        aspect = (r.get('aspect') or '').strip()
        tcm = to_text(r.get('tcm')).strip()
        western = to_text(r.get('western')).strip()
        if not aspect or aspect not in ALLOWED_ASPECTS:
            continue
        if not tcm:
            continue
        if aspect in seen:
            continue
        seen.add(aspect)
        out.append({
            'aspect': aspect,
            'tcm': tcm,
            'western': western,
            'classic': norm_classic(r.get('classic')) if r.get('classic') else ''
        })
    return out

def build_syndrome_comparison(s, classic):
    rows = []
    path = to_text(s.get('pathogenesis')).strip()
    if path:
        rows.append({'aspect': '病机', 'tcm': path, 'western': '', 'classic': classic})
    diag = s.get('diagnosis_points') or []
    if isinstance(diag, list) and diag:
        rows.append({'aspect': '核心症状', 'tcm': '、'.join(str(x).strip() for x in diag if str(x).strip()),
                     'western': '', 'classic': classic})
    mm = s.get('modern_medicine') or []
    if isinstance(mm, list) and mm:
        txt = '、'.join(str(x).strip() for x in mm if str(x).strip())
        rows.append({'aspect': '西医对应', 'tcm': txt,
                     'western': '现代医学对应：' + txt, 'classic': classic})
    return rows

def main():
    syndromes = load('syndromes.json')
    formulas = load('formulas.json')
    medicines = load('medicines.json')
    mappings = load('modern_mapping.json')

    syn_classic_map = {}
    empty_before = 0
    filled = 0
    for s in syndromes:
        classic = syndrome_classic(s)
        syn_classic_map[s['id']] = classic
        comp = s.get('comparison')
        if not isinstance(comp, list) or len(comp) == 0:
            empty_before += 1
            comp = build_syndrome_comparison(s, classic)
            if comp:
                filled += 1
        else:
            comp = clean_rows(comp)
            for r in comp:
                if not r.get('classic'):
                    r['classic'] = classic
        s['comparison'] = comp
    save('syndromes.json', syndromes)
    print('证型: %d 条，原空 comparison %d 条，本次派生填充 %d 条' % (len(syndromes), empty_before, filled))

    f_done = 0
    for f in formulas:
        classic = norm_classic(f.get('source')) or '《伤寒论》'
        rows = []
        effects = to_text(f.get('effects'))
        pe = to_text(f.get('pharmacological_effect'))
        ind = to_text(f.get('indications'))
        ma = to_text(f.get('modern_applications'))
        if effects:
            rows.append({'aspect': '功效', 'tcm': effects, 'western': pe, 'classic': classic})
        if ind:
            rows.append({'aspect': '主治', 'tcm': ind, 'western': ma, 'classic': classic})
        rows = clean_rows(rows)
        if rows:
            f['comparison'] = rows
            f_done += 1
    save('formulas.json', formulas)
    print('方剂: %d 条，生成 comparison %d 条（经典取 source）' % (len(formulas), f_done))

    for m in medicines:
        if not (m.get('classic') or '').strip():
            m['classic'] = '《本草纲目》'
    save('medicines.json', medicines)
    print('中药: %d 条，加 classic 出处' % len(medicines))

    mm_done = 0
    for mm in mappings:
        rs = mm.get('related_syndrome') or ''
        classic = syn_classic_map.get(rs, '')
        if not classic:
            cat = mm.get('category', '') or ''
            if cat == '症状':
                classic = '《伤寒论》'
            elif cat == '疾病':
                classic = '《金匮要略》'
            elif cat == '心理':
                classic = '《黄帝内经》'
            else:
                classic = '《黄帝内经》'
        comp = clean_rows(mm.get('comparison') or [])
        for r in comp:
            if not r.get('classic'):
                r['classic'] = classic
        mm['comparison'] = comp
        mm_done += 1
    save('modern_mapping.json', mappings)
    print('中西对照: %d 条，挂经典出处' % mm_done)

if __name__ == '__main__':
    main()
