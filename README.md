# 中医辨证论治系统

一个面向中医学习与实践的知识类移动优先（Mobile-First）Web 应用，覆盖**证型、针灸、方剂、中药**等核心内容，并提供全文检索、知识图谱、中西医对照与收藏功能。基于 React + Vite 构建，并通过 Capacitor 打包为 Android 原生应用。

## 功能特性

- **证型辨证**：浏览中医证型，查看病机、治法、代表方剂与针灸方案。
- **针灸模块**：穴位定位与主治、针方、针灸处方，含经络归属与现代解剖对照。
- **方剂 / 中药**：方剂组成、功效、适应症、用法，以及单味中药的性味归经与主治。
- **全文搜索**：跨证型、方剂、中药、穴位等实体的关键词检索与分类聚合。
- **知识图谱**：以可视化关系图呈现实体（证型、方剂、中药、穴位等）之间的关联。
- **现代对照**：中医概念与现代医学术语的映射解读，辅助理解。
- **收藏夹**：本地收藏常用条目，随时回看。
- **移动端体验**：响应式布局、安全区适配、暗色模式、滚动回顶、Android 返回键与状态栏适配。

## 技术栈

| 分类 | 选型 |
| --- | --- |
| 前端框架 | React 18 + React DOM 18 |
| 构建工具 | Vite 5 |
| 路由 | React Router 6 |
| 原生桥接 | Capacitor 8（`@capacitor/android`、`@capacitor/app`、`@capacitor/status-bar`） |
| 样式 | 原生 CSS + CSS 变量设计令牌（支持暗色模式） |
| 数据 | SQLite 数据库（`db/zhongyi.db`，端侧由 `sql.js` 加载 `public/zhongyi.db`） |

## 目录结构

```
zhongyi/
├── index.html              # 应用入口 HTML
├── vite.config.js          # Vite 配置（base './'，@ -> /src 别名）
├── capacitor.config.json   # Capacitor 配置（appId: com.zhongyi.app）
├── android/                # Capacitor 生成的 Android 原生工程
├── db/
│   └── zhongyi.db          # 开发用 SQLite 数据库（业务数据单一来源）
├── public/
│   ├── zhongyi.db          # 运行用 SQLite 数据库（DataManager 经 sql.js 加载）
│   └── sql-wasm.wasm       # sql.js WebAssembly 运行时
├── assets/
│   └── data_backup/        # 由 SQLite 反向导出的 JSON 备份（仅供留档/审阅）
├── src/
│   ├── main.jsx            # React 渲染入口
│   ├── index.css           # 全局样式与设计令牌（含暗色模式）
│   ├── web/
│   │   └── App.jsx         # 路由、布局、数据加载、Capacitor 原生适配
│   ├── components/
│   │   ├── common/         # Header / Navigation / 全局搜索 / 错误边界等
│   │   ├── syndrome/       # 证型模块
│   │   ├── acupuncture/    # 针灸模块（穴位 / 针方 / 处方）
│   │   ├── formula/        # 方剂 / 中药模块
│   │   ├── search/         # 搜索模块
│   │   ├── knowledge/      # 知识图谱 + 现代对照
│   │   └── bookmarks/      # 收藏模块
│   ├── context/            # 全局状态（AppContext）
│   ├── hooks/              # 自定义 Hooks
│   └── services/           # 数据服务（DataManager 等）
└── scripts/                # 数据处理 / 构建辅助脚本
```

## 快速开始

### 环境要求

- Node.js 18+（建议 LTS）
- npm 9+

### 安装依赖

```bash
npm install
```

### 本地开发

```bash
npm run dev
```

启动后终端会输出本地访问地址（默认 `http://localhost:5173/`）。

### 构建生产包

```bash
npm run build
```

产物输出到 `dist/` 目录（Capacitor 的 `webDir` 即指向此处）。

### 本地预览构建产物

```bash
npm run preview
```

## 移动端 / Android

本项目通过 Capacitor 打包为 Android 应用，Web 资源构建后同步进原生工程：

```bash
# 1. 构建 Web 资源
npm run build

# 2. 同步到 Android 工程
npx cap sync android

# 3. 用 Android Studio 打开并运行，或直接构建 APK
npx cap open android
```

关键原生适配（见 `src/web/App.jsx`）：

- **状态栏**：进入应用时设置 Android 状态栏背景色与深色样式。
- **返回键**：监听 `backButton`，首页退出应用、其它页面返回上一页。

## 设计说明

- **配色**：采用「霁青蓝 + 琥珀金」的雅致书院风冷调配色，全部颜色通过 `:root` 中的 CSS 变量统一管理。
- **暗色模式**：跟随系统 `prefers-color-scheme`，在 `src/index.css` 的暗色媒体查询中覆盖设计令牌。
- **移动优先**：以窄屏为基准设计，通过媒体查询适配大屏与安全区（`env(safe-area-inset-*)`）。

## 数据说明

业务数据统一存放在 **SQLite 数据库** `db/zhongyi.db`（开发副本）与 `public/zhongyi.db`（应用运行副本，二者应保持同步）。应用启动时，`src/services/DataManager` 通过 `sql.js`（`public/sql-wasm.wasm`）在浏览器端加载 `public/zhongyi.db`，并将扁平表（含 `{表}_{字段}` 子表）物化为嵌套对象供各模块使用。

修改数据请直接操作 `db/zhongyi.db`，再同步到 `public/zhongyi.db` 并重新构建；如需 JSON 审阅/留档，可运行 `scripts/export_json_backup.py` 反向导出至 `assets/data_backup/`。数据质量与一致性检查见 `scripts/`（`analyze_data.py`、`check_sqlite.py`、`clean_data.py`）。

## 许可证

内部学习 / 演示用途。如需商用或二次分发，请确认相关中医内容的版权与合规要求。
