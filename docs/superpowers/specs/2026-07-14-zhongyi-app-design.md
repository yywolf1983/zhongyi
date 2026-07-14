# 中医App架构设计文档

## 1. 项目概述

本项目旨在开发一个中医知识应用，包含经典辨证论治、针灸针方、中药方剂等核心内容，支持知识点之间的相互关联查询，并提供古中医专业术语与现代医学概念的对照解释。数据采用JSON格式存储，结构设计考虑多方关联性。

### 1.1 目标平台
- Web端（HTML5/CSS/JavaScript）
- Android端（后续扩展）

### 1.2 核心功能
- 辨证论治系统：八纲辨证、脏腑辨证、六经辨证等
- 针灸针方库：穴位查询、针灸处方、经络理论
- 中药方剂库：中药功效、经典方剂、配伍原则
- 知识关联图谱：证-方-药-针-穴位的多方关联查询
- 现代对照解释：中医术语与现代医学概念对比

---

## 2. 架构设计

### 2.1 整体架构

```
┌─────────────────────────────────────────────────────────────────────┐
│                           UI层                                      │
├───────────┬───────────┬───────────┬───────────┬────────────────────┤
│ 辨证模块  │ 针灸模块  │ 方剂模块  │ 知识图谱  │   搜索/导航         │
└───────────┴───────────┴───────────┴───────────┴────────────────────┘
                              │
┌─────────────────────────────────────────────────────────────────────┐
│                        业务逻辑层                                    │
├──────────────────┬─────────────────────────────────────────────────┤
│   数据管理器      │              关联查询服务                         │
│ (DataManager)    │  (RelationService)                               │
│ - 加载JSON       │  - 证→方→药查询                                  │
│ - 缓存数据       │  - 证→针→穴位查询                                 │
│ - 新增/编辑      │  - 中药→功效→证查询                               │
│                 │  - 现代对照查询                                    │
└──────────────────┴─────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────────────────┐
│                          数据层                                      │
├─────────────────────────────────────────────────────────────────────┤
│         JSON文件存储（assets/data/*.json）                           │
└─────────────────────────────────────────────────────────────────────┘
```

### 2.2 核心实体模型

| 实体 | 描述 | 核心属性 |
|------|------|----------|
| **Syndrome** | 证型 | ID、名称、分类、辨证要点、病机分析、现代对照 |
| **Medicine** | 中药 | ID、名称、性味归经、功效主治、用法用量、现代药理 |
| **Acupoint** | 穴位 | ID、名称、归经、位置描述、解剖位置、主治病症 |
| **Formula** | 方剂 | ID、名称、来源、组成、功效、适应症、现代应用 |
| **NeedlePrescription** | 针方 | ID、名称、穴位组成、功效、适应症 |
| **Treatment** | 治疗方法 | ID、名称、分类、治疗原则、适用证型 |
| **Meridian** | 经络 | ID、名称、分类、循行路线、主治概要 |
| **Effect** | 功效 | ID、名称、描述、适用证型 |

### 2.3 关联关系模型

```
证 ────── 治（辨证论治）
  │
  ├─── 方剂（证-方对应）
  │       │
  │       └─── 中药（方剂组成）
  │
  └─── 针方（证-针对应）
          │
          └─── 穴位（针方取穴）

穴位 ────── 经络（归属关系）
中药 ────── 功效（具有关系）
功效 ────── 证（治疗关系）
```

---

## 3. 数据结构设计

### 3.1 数据文件清单

| 文件 | 内容 | 说明 |
|------|------|------|
| `syndromes.json` | 证型数据 | 核心辨证数据 |
| `medicines.json` | 中药数据 | 中药基本信息 |
| `acupoints.json` | 穴位数据 | 穴位详细信息 |
| `formulas.json` | 方剂数据 | 方剂组成和应用 |
| `needle_prescriptions.json` | 针方数据 | 针灸处方 |
| `treatments.json` | 治疗方法 | 治疗原则和方法 |
| `meridians.json` | 经络数据 | 经络循行和主治 |
| `effects.json` | 功效数据 | 中药功效定义 |
| `modern_mapping.json` | 现代对照 | 中医-现代医学对照 |

### 3.2 实体数据结构

#### 3.2.1 Syndrome（证型）

```json
{
  "id": "syndrome_001",
  "name": "风寒感冒",
  "pinyin": "Feng Han Gan Mao",
  "category": ["八纲辨证", "病因辨证"],
  "classification": ["表证", "寒证"],
  "diagnosis_points": ["恶寒重，发热轻", "无汗", "鼻塞流清涕", "脉浮紧"],
  "pathogenesis": "风寒之邪侵袭肌表，卫气被遏，营阴郁滞",
  "modern_medicine": ["普通感冒", "急性上呼吸道感染"],
  "modern_explanation": "风寒感冒相当于现代医学中的普通感冒，由病毒感染引起的上呼吸道炎症反应",
  "related_formulas": ["formula_001", "formula_002"],
  "related_needle": ["needle_001"],
  "related_treatments": ["treatment_001"],
  "related_effects": ["effect_001"]
}
```

**字段说明：**
| 字段 | 类型 | 说明 |
|------|------|------|
| id | string | 唯一标识符 |
| name | string | 证型名称 |
| pinyin | string | 拼音 |
| category | array | 辨证方法分类 |
| classification | array | 八纲分类（表/里、寒/热、虚/实、阴/阳） |
| diagnosis_points | array | 辨证要点 |
| pathogenesis | string | 病机分析 |
| modern_medicine | array | 现代医学对应疾病 |
| modern_explanation | string | 现代医学解释 |
| related_formulas | array | 关联方剂ID列表 |
| related_needle | array | 关联针方ID列表 |
| related_treatments | array | 关联治疗方法ID列表 |
| related_effects | array | 关联功效ID列表 |

#### 3.2.2 Medicine（中药）

```json
{
  "id": "medicine_001",
  "name": "麻黄",
  "pinyin": "Ma Huang",
  "latin_name": "Ephedrae Herba",
  "category": "解表药",
  "subcategory": "辛温解表药",
  "nature": "温",
  "taste": ["辛", "微苦"],
  "meridian_tropism": ["肺经", "膀胱经"],
  "effects": ["发汗解表", "宣肺平喘", "利水消肿"],
  "indications": ["风寒感冒", "咳嗽气喘", "风水水肿"],
  "usage": "煎服，2-9g",
  "contraindications": ["体虚多汗者慎用", "高血压患者慎用", "孕妇慎用"],
  "modern_pharmacology": ["发汗作用：促进汗腺分泌", "平喘作用：舒张支气管", "利尿作用：增加尿量"],
  "related_effects": ["effect_001", "effect_002"],
  "related_formulas": ["formula_001"]
}
```

**字段说明：**
| 字段 | 类型 | 说明 |
|------|------|------|
| id | string | 唯一标识符 |
| name | string | 中药名称 |
| pinyin | string | 拼音 |
| latin_name | string | 拉丁名 |
| category | string | 中药分类 |
| subcategory | string | 中药亚分类 |
| nature | string | 药性（寒/热/温/凉/平） |
| taste | array | 药味（辛/甘/酸/苦/咸） |
| meridian_tropism | array | 归经 |
| effects | array | 功效描述 |
| indications | array | 主治病症 |
| usage | string | 用法用量 |
| contraindications | array | 禁忌 |
| modern_pharmacology | array | 现代药理作用 |
| related_effects | array | 关联功效ID列表 |
| related_formulas | array | 关联方剂ID列表 |

#### 3.2.3 Acupoint（穴位）

```json
{
  "id": "acupoint_001",
  "name": "足三里",
  "pinyin": "Zu San Li",
  "code": "ST36",
  "meridian": "足阳明胃经",
  "meridian_id": "meridian_003",
  "location": "在小腿外侧，犊鼻下3寸，胫骨前嵴外1横指处",
  "location_description": "屈膝，在犊鼻穴下3寸，胫骨前嵴外1横指处取穴",
  "anatomy": "在胫骨前肌、趾长伸肌之间",
  "indications": ["胃痛", "腹胀", "消化不良", "呕吐", "泄泻", "下肢痿痹", "心悸", "失眠"],
  "methods": ["直刺1-2寸", "可灸"],
  "modern_anatomy": "浅层布有腓肠外侧皮神经。深层有腓深神经和胫前动、静脉",
  "modern_applications": ["消化系统疾病", "运动系统疾病", "心血管系统疾病"],
  "related_syndromes": ["syndrome_002", "syndrome_005"],
  "related_needle": ["needle_002"]
}
```

**字段说明：**
| 字段 | 类型 | 说明 |
|------|------|------|
| id | string | 唯一标识符 |
| name | string | 穴位名称 |
| pinyin | string | 拼音 |
| code | string | 穴位代码（如ST36） |
| meridian | string | 所属经络名称 |
| meridian_id | string | 所属经络ID |
| location | string | 位置描述 |
| location_description | string | 详细取穴方法 |
| anatomy | string | 中医解剖位置 |
| indications | array | 主治病症 |
| methods | array | 针灸方法 |
| modern_anatomy | string | 现代解剖位置 |
| modern_applications | array | 现代应用领域 |
| related_syndromes | array | 关联证型ID列表 |
| related_needle | array | 关联针方ID列表 |

#### 3.2.4 Formula（方剂）

```json
{
  "id": "formula_001",
  "name": "麻黄汤",
  "pinyin": "Ma Huang Tang",
  "category": "解表剂",
  "subcategory": "辛温解表",
  "source": "《伤寒论》",
  "author": "张仲景",
  "composition": [
    {"medicine_id": "medicine_001", "name": "麻黄", "dose": "9g", "role": "君"},
    {"medicine_id": "medicine_002", "name": "桂枝", "dose": "6g", "role": "臣"},
    {"medicine_id": "medicine_003", "name": "杏仁", "dose": "6g", "role": "佐"},
    {"medicine_id": "medicine_004", "name": "甘草", "dose": "3g", "role": "使"}
  ],
  "effects": ["发汗解表", "宣肺平喘"],
  "indications": ["外感风寒表实证：恶寒发热，无汗而喘，头痛身痛，舌苔薄白，脉浮紧"],
  "usage": "水煎服，温覆取微汗",
  "modern_applications": ["感冒", "支气管炎", "哮喘", "过敏性鼻炎"],
  "modern_explanation": "麻黄汤具有发汗、平喘、抗炎等作用，现代常用于治疗呼吸道感染性疾病",
  "related_syndromes": ["syndrome_001"],
  "related_effects": ["effect_001", "effect_003"]
}
```

**字段说明：**
| 字段 | 类型 | 说明 |
|------|------|------|
| id | string | 唯一标识符 |
| name | string | 方剂名称 |
| pinyin | string | 拼音 |
| category | string | 方剂分类 |
| subcategory | string | 方剂亚分类 |
| source | string | 来源书籍 |
| author | string | 作者 |
| composition | array | 组成（含药名、剂量、君臣佐使） |
| effects | array | 功效描述 |
| indications | array | 适应症 |
| usage | string | 用法 |
| modern_applications | array | 现代应用 |
| modern_explanation | string | 现代医学解释 |
| related_syndromes | array | 关联证型ID列表 |
| related_effects | array | 关联功效ID列表 |

#### 3.2.5 NeedlePrescription（针方）

```json
{
  "id": "needle_001",
  "name": "感冒针方",
  "category": "解表",
  "acupoints": [
    {"acupoint_id": "acupoint_005", "name": "风池", "method": "捻转泻法"},
    {"acupoint_id": "acupoint_006", "name": "大椎", "method": "提插泻法"},
    {"acupoint_id": "acupoint_007", "name": "合谷", "method": "捻转泻法"},
    {"acupoint_id": "acupoint_008", "name": "列缺", "method": "捻转补法"}
  ],
  "effects": ["疏风解表", "宣肺通窍"],
  "indications": ["感冒", "头痛", "鼻塞"],
  "modern_applications": ["上呼吸道感染", "过敏性鼻炎"],
  "related_syndromes": ["syndrome_001"]
}
```

**字段说明：**
| 字段 | 类型 | 说明 |
|------|------|------|
| id | string | 唯一标识符 |
| name | string | 针方名称 |
| category | string | 分类 |
| acupoints | array | 穴位组成（含穴位ID、名称、操作方法） |
| effects | array | 功效描述 |
| indications | array | 适应症 |
| modern_applications | array | 现代应用 |
| related_syndromes | array | 关联证型ID列表 |

#### 3.2.6 Treatment（治疗方法）

```json
{
  "id": "treatment_001",
  "name": "辛温解表法",
  "category": "解表法",
  "principle": "发散风寒，解除表证",
  "indications": ["风寒感冒", "风寒咳嗽", "风寒头痛"],
  "methods": ["药物治疗：麻黄汤、桂枝汤", "针灸治疗：风池、大椎、合谷", "艾灸治疗：风门、肺俞"],
  "modern_explanation": "辛温解表法通过促进汗腺分泌、改善微循环、增强免疫力来治疗风寒感冒",
  "related_syndromes": ["syndrome_001"],
  "related_formulas": ["formula_001", "formula_002"],
  "related_needle": ["needle_001"]
}
```

#### 3.2.7 Meridian（经络）

```json
{
  "id": "meridian_001",
  "name": "手太阴肺经",
  "pinyin": "Shou Tai Yin Fei Jing",
  "category": "十二正经",
  "yin_yang": "阴",
  "element": "金",
  "path": "起于中焦，下络大肠，还循胃口，上膈属肺。从肺系，横出腋下，下循臑内，行少阴、心主之前，下肘中，循臂内上骨下廉，入寸口，上鱼，循鱼际，出大指之端",
  "main_points": ["中府", "云门", "天府", "侠白", "尺泽", "孔最", "列缺", "经渠", "太渊", "鱼际", "少商"],
  "indications": ["咳嗽", "气喘", "咽喉肿痛", "胸痛", "肩背痛"],
  "related_acupoints": ["acupoint_008", "acupoint_009"],
  "related_syndromes": ["syndrome_001"]
}
```

#### 3.2.8 Effect（功效）

```json
{
  "id": "effect_001",
  "name": "发汗解表",
  "description": "发散表邪，解除表证的治疗作用",
  "mechanism": "通过药物的辛温发散作用，促进人体汗腺分泌，使汗液排出，从而发散表邪",
  "indications": ["风寒感冒", "风热感冒", "表证"],
  "related_medicines": ["medicine_001", "medicine_002"],
  "related_formulas": ["formula_001"],
  "related_syndromes": ["syndrome_001"]
}
```

### 3.3 关联关系数据结构

#### 3.3.1 Modern Mapping（现代对照）

```json
{
  "id": "mapping_001",
  "chinese_term": "风寒感冒",
  "modern_term": "普通感冒",
  "category": "疾病",
  "explanation": "风寒感冒是中医术语，指因风寒之邪侵袭人体引起的感冒，相当于现代医学中的普通感冒，主要由病毒感染引起",
  "related_syndrome": "syndrome_001"
}
```

---

## 4. 前端架构设计

### 4.1 目录结构

```
zhongyi/
├── assets/
│   ├── data/
│   │   ├── syndromes.json
│   │   ├── medicines.json
│   │   ├── acupoints.json
│   │   ├── formulas.json
│   │   ├── needle_prescriptions.json
│   │   ├── treatments.json
│   │   ├── meridians.json
│   │   ├── effects.json
│   │   └── modern_mapping.json
│   ├── images/
│   │   └── acupoints/
│   └── icons/
├── src/
│   ├── components/
│   │   ├── syndrome/
│   │   │   ├── SyndromeList.jsx
│   │   │   ├── SyndromeDetail.jsx
│   │   │   └── SyndromeSearch.jsx
│   │   ├── acupuncture/
│   │   │   ├── AcupointList.jsx
│   │   │   ├── AcupointDetail.jsx
│   │   │   └── NeedlePrescription.jsx
│   │   ├── formula/
│   │   │   ├── FormulaList.jsx
│   │   │   ├── FormulaDetail.jsx
│   │   │   └── MedicineList.jsx
│   │   ├── knowledge/
│   │   │   ├── RelationGraph.jsx
│   │   │   └── ModernMapping.jsx
│   │   ├── search/
│   │   │   ├── GlobalSearch.jsx
│   │   │   ├── SearchResults.jsx
│   │   │   └── SearchSuggestions.jsx
│   │   └── common/
│   │       ├── Header.jsx
│   │       ├── Navigation.jsx
│   │       └── SearchBar.jsx
│   ├── services/
│   │   ├── DataManager.js
│   │   ├── RelationService.js
│   │   └── SearchService.js
│   ├── utils/
│   │   ├── helpers.js
│   │   └── fuzzySearch.js
│   ├── styles/
│   │   ├── main.css
│   │   └── responsive.css
│   ├── web/
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── index.html
│   └── native/
│       ├── App.jsx
│       ├── MainActivity.java
│       └── MainApplication.java
├── package.json
├── vite.config.js
└── metro.config.js
```

### 4.2 核心服务

#### 4.2.1 DataManager（数据管理器）

**职责：**
- 加载JSON数据文件
- 缓存数据到内存
- 提供数据增删改查接口
- 支持数据持久化（可选）

**接口：**
```javascript
class DataManager {
  async loadData(fileName)
  getAll(type)
  getById(type, id)
  search(type, keyword)
  fuzzySearch(type, keyword, options)
  add(type, data)
  update(type, id, data)
  delete(type, id)
}
```

**模糊搜索配置：**
```javascript
// options 参数
{
  fields: ['name', 'pinyin', 'indications'], // 搜索字段
  matchMode: 'contains', // 匹配模式: contains(包含), startsWith(前缀), exact(精确)
  caseSensitive: false, // 是否区分大小写
  fuzzy: true // 是否启用模糊匹配（允许错别字）
}
```

#### 4.2.2 RelationService（关联查询服务）

**职责：**
- 处理实体之间的关联查询
- 提供图式查询能力
- 支持多维度关联分析

**接口：**
```javascript
class RelationService {
  getFormulasBySyndrome(syndromeId)
  getMedicinesByFormula(formulaId)
  getAcupointsByNeedle(needleId)
  getNeedlesBySyndrome(syndromeId)
  getEffectsByMedicine(medicineId)
  getModernMapping(chineseTerm)
  getRelations(entityId, entityType)
}
```

#### 4.2.3 SearchService（全局搜索服务）

**职责：**
- 跨模块全局模糊搜索
- 搜索结果分类展示
- 搜索历史记录
- 搜索建议自动补全

**接口：**
```javascript
class SearchService {
  globalSearch(keyword)
  getSuggestions(keyword)
  getSearchHistory()
  addSearchHistory(keyword)
  clearSearchHistory()
}
```

**全局搜索结果结构：**
```javascript
{
  keyword: "感冒",
  results: {
    syndromes: [{ id: "syndrome_001", name: "风寒感冒", score: 0.95 }],
    formulas: [{ id: "formula_001", name: "麻黄汤", score: 0.88 }],
    medicines: [{ id: "medicine_001", name: "麻黄", score: 0.72 }],
    acupoints: [{ id: "acupoint_005", name: "风池", score: 0.65 }],
    needles: [{ id: "needle_001", name: "感冒针方", score: 0.90 }]
  },
  total: 5
}
```

---

## 5. 功能模块设计

### 5.1 辨证论治模块

**功能：**
- 证型列表展示
- 证型详细信息查看（辨证要点、病机分析）
- 关联方剂查询
- 关联针方查询
- 现代医学对照

**流程：**
```
选择证型 → 查看辨证要点 → 查看关联方剂/针方 → 查看现代对照
```

### 5.2 针灸模块

**功能：**
- 穴位列表展示（按经络分类）
- 穴位详细信息（位置、主治、解剖）
- 针方查询
- 经络浏览

**流程：**
```
选择经络 → 查看穴位列表 → 查看穴位详情 → 查看针方应用
```

### 5.3 方剂模块

**功能：**
- 方剂列表展示（按分类）
- 方剂详细信息（组成、功效、用法）
- 中药查询
- 配伍分析

**流程：**
```
选择方剂 → 查看组成 → 查看各中药详情 → 查看适应症
```

### 5.4 知识图谱模块

**功能：**
- 关联关系可视化
- 多维度查询
- 现代对照搜索

**流程：**
```
选择实体 → 展示关联图谱 → 点击关联实体 → 查看详情
```

### 5.5 搜索模块

**功能：**
- 全局模糊搜索（跨证型、中药、穴位、方剂、针方）
- 分类搜索结果展示
- 搜索建议自动补全
- 搜索历史记录
- 搜索结果排序（按匹配度）

**流程：**
```
输入关键词 → 实时搜索建议 → 选择搜索 → 展示分类结果 → 点击查看详情
```

**模糊搜索算法：**
- **包含匹配**：关键词包含在字段中即可命中（如"风"可匹配"风寒感冒"、"风池"）
- **拼音匹配**：支持拼音搜索（如"ma huang"可匹配"麻黄"）
- **模糊容错**：允许错别字（使用编辑距离算法）
- **权重排序**：名称匹配权重 > 拼音匹配 > 描述匹配

**搜索字段配置：**
| 实体类型 | 搜索字段 |
|----------|----------|
| 证型 | name, pinyin, diagnosis_points, indications |
| 中药 | name, pinyin, latin_name, effects, indications |
| 穴位 | name, pinyin, code, location, indications |
| 方剂 | name, pinyin, source, composition[].name, indications |
| 针方 | name, pinyin, acupoints[].name, indications |

---

## 6. 扩展设计

### 6.1 数据新增机制

**设计原则：**
- 支持用户自定义新增数据
- 新增数据与原有数据隔离存储
- 支持数据导出/导入

**实现方式：**
- 默认数据存储在`assets/data/`目录下的JSON文件中（只读）
- 用户新增数据存储在浏览器localStorage中（Web端）或SQLite数据库中（Android端）
- DataManager优先加载默认数据，再合并用户数据
- 支持将用户数据导出为JSON文件，也支持导入JSON文件

### 6.2 跨平台架构

**技术方案：React Native**
- 使用React Native + React Native Web实现一套代码同时支持Web和Android
- Web端：通过Vite构建，数据存储使用localStorage
- Android端：通过React Native构建，数据存储使用SQLite
- 核心业务逻辑（DataManager、RelationService）复用

**优势：**
- 一套代码，多端运行
- 共享核心服务逻辑
- 原生体验（Android端）
- 快速开发迭代

---

## 7. 技术栈

| 层级 | Web端 | Android端 |
|------|-------|-----------|
| 框架 | React + React Native Web | React Native |
| 样式 | Tailwind CSS + React Native StyleSheet | React Native StyleSheet + NativeWind |
| 数据存储 | JSON文件 + localStorage | JSON文件 + SQLite |
| 图表库 | D3.js / Recharts | Recharts |
| 构建工具 | Vite | Metro |
| 数据库 | - | react-native-sqlite-storage |

---

## 8. 开发计划

### Phase 1：数据模型与基础架构
- 定义JSON数据结构
- 创建示例数据
- 实现DataManager服务
- 实现RelationService服务

### Phase 2：核心功能模块
- 辨证论治模块开发
- 针灸模块开发
- 方剂模块开发

### Phase 3：知识图谱与对照
- 知识图谱可视化
- 现代对照功能
- 搜索功能优化

### Phase 4：完善与优化
- 数据新增功能
- UI优化
- 性能优化

---

## 9. 附录

### 9.1 ID命名规范

```
证型: syndrome_XXX
中药: medicine_XXX
穴位: acupoint_XXX
方剂: formula_XXX
针方: needle_XXX
治疗: treatment_XXX
经络: meridian_XXX
功效: effect_XXX
对照: mapping_XXX
```

### 9.2 辨证方法分类

- 八纲辨证
- 脏腑辨证
- 六经辨证
- 卫气营血辨证
- 三焦辨证
- 病因辨证
- 气血津液辨证

### 9.3 中药分类

- 解表药
- 清热药
- 泻下药
- 祛风湿药
- 化湿药
- 利水渗湿药
- 温里药
- 理气药
- 消食药
- 驱虫药
- 止血药
- 活血祛瘀药
- 化痰止咳平喘药
- 安神药
- 平肝息风药
- 开窍药
- 补虚药
- 收涩药
- 涌吐药
- 解毒杀虫燥湿止痒药
- 拔毒化腐生肌药
