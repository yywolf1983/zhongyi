#!/bin/bash

set -eo pipefail

APP_NAME="中医辨证论治系统"
APP_ID="com.zhongyi.app"
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
NODE_MODULES="$PROJECT_DIR/node_modules"
NPM_BIN="$NODE_MODULES/.bin"
DATA_DIR="$PROJECT_DIR/assets/data"
DOCS_DIR="$PROJECT_DIR/docs"
ANDROID_DIR="$PROJECT_DIR/android"
DIST_DIR="$PROJECT_DIR/dist"
APK_OUT_DIR="/Users/yy/Desktop/back/dapk"

print_banner() {
  echo ""
  echo "╔══════════════════════════════════════════════════════════════════════╗"
  echo "║                        $APP_NAME                                   ║"
  echo "║                    构建与管理脚本                                   ║"
  echo "╚══════════════════════════════════════════════════════════════════════╝"
  echo ""
}

print_help() {
  print_banner
  echo "用法: $0 [命令]"
  echo ""
  echo "  开发环境:"
  echo "    dev              启动开发服务器 (默认端口: 5173)"
  echo "    dev --port 8080  启动开发服务器 (指定端口)"
  echo "    dev --host       启动开发服务器 (允许外部访问)"
  echo ""
  echo "  构建:"
  echo "    build            生产环境构建（Web）"
  echo "    build:dev        开发环境构建（Web）"
  echo "    build:analyze    构建并分析包大小"
  echo "    build:clean      清理构建产物"
  echo ""
  echo "  Android 构建:"
  echo "    android:setup    初始化 Android 项目（首次使用）"
  echo "    android:build    Web 构建 + 同步到 Android"
  echo "    android:sync     仅同步 Web 产物到 Android"
  echo "    android:open     在 Android Studio 中打开项目"
  echo "    android:install  编译并安装到已连接设备"
  echo "    android:run      构建+安装并启动 App"
  echo "    android:clean    清理 Android 构建产物"
  echo ""
  echo "  预览:"
  echo "    preview          预览构建结果 (默认端口: 5173)"
  echo "    preview --port 8080 预览构建结果 (指定端口)"
  echo ""
  echo "  依赖管理:"
  echo "    install          安装所有依赖"
  echo "    install:clean    清理并重新安装依赖"
  echo "    update           更新依赖版本"
  echo "    audit            检查依赖安全问题"
  echo ""
  echo "  数据管理:"
  echo "    data:count       统计数据条目数量"
  echo "    data:check       检查数据完整性和关联关系"
  echo "    data:summary     生成数据统计文档"
  echo "    data:validate    验证数据关联引用的有效性"
  echo ""
  echo "  代码质量:"
  echo "    lint             运行代码检查"
  echo "    format           格式化代码"
  echo ""
  echo "  其他:"
  echo "    help             显示此帮助信息"
  echo "    version          显示版本信息"
  echo "    clean            清理所有缓存和构建产物"
  echo ""
}

print_version() {
  print_banner
  echo "版本: $(cat "$PROJECT_DIR/package.json" | grep '"version"' | cut -d'"' -f4)"
  echo "项目: $(cat "$PROJECT_DIR/package.json" | grep '"name"' | cut -d'"' -f4)"
  echo ""
}

check_node() {
  if ! command -v node &> /dev/null; then
    echo "❌ 错误: 未找到 Node.js，请先安装 Node.js"
    echo "下载地址: https://nodejs.org/"
    exit 1
  fi
  
  NODE_VERSION=$(node --version | cut -d'v' -f2)
  echo "✅ Node.js 版本: $NODE_VERSION"
  
  if ! command -v npm &> /dev/null; then
    echo "❌ 错误: 未找到 npm"
    exit 1
  fi
  
  NPM_VERSION=$(npm --version)
  echo "✅ npm 版本: $NPM_VERSION"
}

check_dependencies() {
  if [ ! -d "$NODE_MODULES" ]; then
    echo "⚠️  未检测到 node_modules，正在安装依赖..."
    run_install
  fi
}

run_install() {
  echo "📦 安装依赖..."
  cd "$PROJECT_DIR" && npm install
  echo "✅ 依赖安装完成"
}

run_install_clean() {
  echo "🧹 清理旧依赖..."
  rm -rf "$NODE_MODULES"
  rm -f "$PROJECT_DIR/package-lock.json"
  echo "📦 重新安装依赖..."
  cd "$PROJECT_DIR" && npm install
  echo "✅ 依赖重新安装完成"
}

run_update() {
  echo "🔄 更新依赖..."
  cd "$PROJECT_DIR" && npm update
  echo "✅ 依赖更新完成"
}

run_audit() {
  echo "🔍 检查依赖安全问题..."
  cd "$PROJECT_DIR" && npm audit
}

run_dev() {
  check_dependencies
  echo "🚀 启动开发服务器..."
  cd "$PROJECT_DIR"
  if [ "$1" = "--host" ]; then
    npm run dev -- --host
  elif [ "$1" = "--port" ]; then
    npm run dev -- --port "$2"
  else
    npm run dev
  fi
}

run_build() {
  check_dependencies
  echo "🔨 生产环境构建..."
  cd "$PROJECT_DIR" && npm run build
  echo "✅ 构建完成，输出目录: $PROJECT_DIR/dist"
}

run_build_dev() {
  check_dependencies
  echo "🔨 开发环境构建..."
  cd "$PROJECT_DIR" && npm run build -- --mode development
  echo "✅ 开发构建完成"
}

run_build_analyze() {
  check_dependencies
  echo "🔍 构建并分析包大小..."
  cd "$PROJECT_DIR" && npm run build -- --analyze
  echo "✅ 构建分析完成"
}

run_build_clean() {
  echo "🧹 清理构建产物..."
  rm -rf "$PROJECT_DIR/dist"
  rm -rf "$PROJECT_DIR/.vite"
  echo "✅ 构建产物清理完成"
}

run_preview() {
  check_dependencies
  echo "👁️  预览构建结果..."
  cd "$PROJECT_DIR"
  if [ "$1" = "--port" ]; then
    npm run preview -- --port "$2"
  else
    npm run preview
  fi
}

run_lint() {
  check_dependencies
  echo "📋 运行代码检查..."
  cd "$PROJECT_DIR"
  if command -v eslint &> /dev/null; then
    eslint .
  elif [ -x "$NPM_BIN/eslint" ]; then
    "$NPM_BIN/eslint" .
  else
    echo "⚠️  未安装 eslint，跳过代码检查"
  fi
}

run_format() {
  check_dependencies
  echo "✨ 格式化代码..."
  cd "$PROJECT_DIR"
  if command -v prettier &> /dev/null; then
    prettier --write .
  elif [ -x "$NPM_BIN/prettier" ]; then
    "$NPM_BIN/prettier" --write .
  else
    echo "⚠️  未安装 prettier，跳过代码格式化"
  fi
}

run_clean() {
  echo "🧹 清理所有缓存和构建产物..."
  rm -rf "$PROJECT_DIR/dist"
  rm -rf "$PROJECT_DIR/.vite"
  rm -rf "$PROJECT_DIR/node_modules/.cache"
  echo "✅ 清理完成"
}

count_data() {
  echo "📊 数据统计:"
  echo ""
  
  local total=0
  
  for file in "$DATA_DIR"/*.json; do
    if [ -f "$file" ]; then
      local filename=$(basename "$file")
      local count=$(cat "$file" | python3 -c "import sys,json; print(len(json.load(sys.stdin)))")
      local type=$(echo "$filename" | cut -d'.' -f1 | sed 's/_/ /g')
      printf "  %-25s %3d 条\n" "$type:" "$count"
      total=$((total + count))
    fi
  done
  
  echo ""
  printf "  %-25s %3d 条\n" "总计:" "$total"
}

check_data() {
  echo "🔍 检查数据完整性..."
  echo ""
  
  local errors=0
  
  for file in "$DATA_DIR"/*.json; do
    if [ -f "$file" ]; then
      local filename=$(basename "$file")
      echo "检查 $filename..."
      
      if ! python3 -c "import sys,json; json.load(sys.stdin)" < "$file"; then
        echo "  ❌ JSON 格式错误"
        errors=$((errors + 1))
      else
        echo "  ✅ JSON 格式正确"
      fi
    fi
  done
  
  echo ""
  
  if [ "$errors" -eq 0 ]; then
    echo "✅ 所有数据文件格式正确"
  else
    echo "❌ 发现 $errors 个错误"
    exit 1
  fi
}

validate_data_references() {
  echo "🔍 验证数据关联引用..."
  echo ""
  
  python3 << 'EOF'
import os
import json

data_dir = 'assets/data'

all_data = {}
all_ids = {}

for filename in sorted(os.listdir(data_dir)):
    if filename.endswith('.json'):
        filepath = os.path.join(data_dir, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        prefix = filename.replace('.json', '').replace('modern_mapping', 'mapping')
        all_data[prefix] = data
        for item in data:
            all_ids[item['id']] = item

reference_fields = [
    'related_formulas', 'related_needle', 'related_treatments', 'related_effects',
    'related_syndromes', 'related_acupoints', 'related_medicines', 'related_meridians',
    'related_acupoint', 'related_medicine', 'related_formula', 'related_syndrome',
    'medicine_id', 'acupoint_id', 'meridian_id'
]

errors = []
for prefix, data in all_data.items():
    for item in data:
        item_id = item['id']
        for field in reference_fields:
            if field in item:
                values = item[field]
                if not isinstance(values, list):
                    values = [values]
                for ref_id in values:
                    if ref_id not in all_ids:
                        errors.append(f"  ❌ {item_id} 的 {field} 引用了不存在的 ID: {ref_id}")

if errors:
    for error in errors:
        print(error)
    print(f"\n❌ 发现 {len(errors)} 个无效引用")
    exit(1)
else:
    print("✅ 所有数据引用有效")
EOF
}

generate_summary() {
  echo "📝 生成数据统计文档..."
  cd "$PROJECT_DIR"
  python3 - << 'EOF'
import os
import json

data_dir = 'assets/data'
docs_dir = 'docs'

if not os.path.exists(docs_dir):
    os.makedirs(docs_dir)

summary = []
summary.append('# 中医辨证论治系统 - 数据统计')
summary.append('')
summary.append('## 数据概览')
summary.append('')
summary.append('| 数据类型 | 文件路径 | 数量 |')
summary.append('| :--- | :--- | :---: |')

total = 0
for filename in sorted(os.listdir(data_dir)):
    if filename.endswith('.json'):
        filepath = os.path.join(data_dir, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        count = len(data)
        total += count
        data_type = filename.replace('.json', '').replace('_', ' ')
        summary.append(f'| {data_type} | [{filename}](assets/data/{filename}) | {count} |')

summary.append(f'| **合计** | - | **{total}** |')
summary.append('')
summary.append('## 详细数据列表')
summary.append('')

for filename in sorted(os.listdir(data_dir)):
    if filename.endswith('.json'):
        filepath = os.path.join(data_dir, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        data_type = filename.replace('.json', '').replace('_', ' ')
        summary.append(f'### {data_type}')
        summary.append('')
        summary.append('| ID | 名称 | 拼音 |')
        summary.append('| :--- | :--- | :--- |')
        for item in data:
            name = item.get('name', '')
            pinyin = item.get('pinyin', '')
            summary.append(f'| {item["id"]} | {name} | {pinyin} |')
        summary.append('')

summary.append('## 数据关联关系')
summary.append('')
summary.append('### 核心关联')
summary.append('- 证型 → 方剂、针方、治疗方法、功效')
summary.append('- 方剂 → 中药、功效、证型')
summary.append('- 中药 → 功效、方剂')
summary.append('- 穴位 → 经络、证型、针方')
summary.append('- 针方 → 穴位、证型')
summary.append('- 经络 → 穴位')
summary.append('- 治疗方法 → 证型、方剂、针方')
summary.append('- 现代医学对照 → 证型、中药、穴位、方剂')
summary.append('')

with open(os.path.join(docs_dir, 'data-summary.md'), 'w', encoding='utf-8') as f:
    f.write('\n'.join(summary))

print(f'✅ 数据统计文档已生成: docs/data-summary.md')
print(f'   总计: {total} 条数据')
EOF
}

# ====================
# Android 相关
# ====================

check_java() {
  if ! command -v java &> /dev/null; then
    echo "❌ 错误: 未找到 Java，请安装 JDK 17+"
    echo "下载地址: https://adoptium.net/"
    exit 1
  fi
  echo "✅ Java: $(java -version 2>&1 | head -1)"
}

check_android_sdk() {
  if [ -z "$ANDROID_HOME" ] && [ -z "$ANDROID_SDK_ROOT" ]; then
    echo "⚠️  警告: 未设置 ANDROID_HOME 或 ANDROID_SDK_ROOT"
    echo "   请确保 Android SDK 已安装并设置环境变量"
    echo ""
    # 尝试自动检测
    if [ -d "$HOME/Library/Android/sdk" ]; then
      export ANDROID_HOME="$HOME/Library/Android/sdk"
      echo "✅ 自动检测到 Android SDK: $ANDROID_HOME"
    elif [ -d "$HOME/Downloads/android-sdk" ]; then
      export ANDROID_HOME="$HOME/Downloads/android-sdk"
      echo "✅ 自动检测到 Android SDK: $ANDROID_HOME"
    elif [ -d "$HOME/Android/Sdk" ]; then
      export ANDROID_HOME="$HOME/Android/Sdk"
      echo "✅ 自动检测到 Android SDK: $ANDROID_HOME"
    else
      echo "⚠️  未找到 Android SDK，Android 命令可能无法正常执行"
    fi
  else
    SDK="${ANDROID_HOME:-$ANDROID_SDK_ROOT}"
    echo "✅ Android SDK: $SDK"
    export ANDROID_HOME="$SDK"
  fi
  # 确保 local.properties 中的 SDK 路径正确
  if [ -n "$ANDROID_HOME" ] && [ -f "$ANDROID_DIR/local.properties" ]; then
    echo "sdk.dir=$ANDROID_HOME" > "$ANDROID_DIR/local.properties"
    echo "✅ local.properties 已同步 SDK 路径: $ANDROID_HOME"
  fi
}

check_adb() {
  if command -v adb &> /dev/null; then
    echo "✅ adb: $(adb --version | head -1)"
  else
    echo "⚠️  未找到 adb，无法安装到设备"
  fi
}

# 在 cap sync 后重新应用国内镜像源（cap sync 会重写 cordova 插件的 build.gradle）
apply_china_mirrors_after_sync() {
  local cordova_build_gradle="$ANDROID_DIR/capacitor-cordova-android-plugins/build.gradle"
  if [ -f "$cordova_build_gradle" ]; then
    # 如果已包含国内源则跳过
    if grep -q "maven.aliyun.com" "$cordova_build_gradle" 2>/dev/null; then
      return 0
    fi
    # 在 buildscript repositories 块中插入国内源（在 google() 前）
    perl -i -pe 's|(buildscript \{\s*\n\s*repositories \{\s*\n)(\s*google\(\))|$1        maven { url '\''https://maven.aliyun.com/repository/google'\'' }\n        maven { url '\''https://maven.aliyun.com/repository/public'\'' }\n        maven { url '\''https://maven.aliyun.com/repository/gradle-plugin'\'' }\n$2|' "$cordova_build_gradle" 2>/dev/null || true
    # 在模块 repositories 块中插入国内源
    perl -i -pe 's|^(repositories \{\s*\n)(\s*google\(\))|$1    maven { url '\''https://maven.aliyun.com/repository/google'\'' }\n    maven { url '\''https://maven.aliyun.com/repository/public'\'' }\n$2|' "$cordova_build_gradle" 2>/dev/null || true
    echo "✅ 国内镜像源已应用到 cordova 插件"
  fi
}

install_capacitor() {
  echo "📦 安装 Capacitor 依赖..."
  cd "$PROJECT_DIR"
  npm install --save @capacitor/core @capacitor/cli @capacitor/android 2>&1 | tail -3
  echo "✅ Capacitor 依赖安装完成"
}

run_android_setup() {
  print_banner
  echo "🔧 初始化 Android 项目..."
  echo ""

  check_node
  check_java
  check_android_sdk

  # 安装 Capacitor
  if ! grep -q '"@capacitor/core"' "$PROJECT_DIR/package.json"; then
    install_capacitor
  else
    echo "✅ Capacitor 已安装"
  fi

  # 先构建 Web
  echo ""
  echo "🔨 构建 Web 应用..."
  run_build

  # 初始化 Capacitor Android 平台
  echo ""
  echo "📱 初始化 Android 平台..."
  cd "$PROJECT_DIR"

  if [ ! -d "$ANDROID_DIR" ]; then
    npx cap add android 2>&1
    echo "✅ Android 平台已添加"

    # 更新 capacitor.config.json
    if [ -f "$PROJECT_DIR/capacitor.config.json" ]; then
      # 确保 appId 正确
      cat > "$PROJECT_DIR/capacitor.config.json" << 'CONFEOF'
{
  "appId": "com.zhongyi.app",
  "appName": "中医辨证论治系统",
  "webDir": "dist",
  "bundledWebRuntime": false,
  "server": {
    "androidScheme": "https"
  }
}
CONFEOF
      echo "✅ capacitor.config.json 已配置"
    fi
  else
    echo "✅ Android 平台已存在，跳过创建"
  fi

  # 同步 Web 到 Android
  echo ""
  echo "🔄 同步 Web 到 Android..."
  npx cap sync android 2>&1
  apply_china_mirrors_after_sync

  echo ""
  echo "✅ Android 初始化完成！"
  echo ""
  echo "📱 下一步:"
  echo "   ./build.sh android:open    在 Android Studio 中打开"
  echo "   ./build.sh android:run     构建并安装到设备"
}

run_android_build() {
  print_banner
  echo "📱 Android 构建（Web + Sync + APK）..."
  echo ""

  check_node
  check_java
  check_android_sdk

  # 构建 Web
  echo "🔨 构建 Web 应用..."
  run_build

  # 同步到 Android
  echo ""
  echo "🔄 同步 Web 产物到 Android..."
  cd "$PROJECT_DIR"

  if [ ! -d "$ANDROID_DIR" ]; then
    echo "❌ 错误: 未找到 Android 项目目录"
    echo "   请先运行: $0 android:setup"
    exit 1
  fi

  npx cap sync android 2>&1
  apply_china_mirrors_after_sync

  echo ""
  echo "✅ Web → Android 同步完成"
  echo ""

  # 自动编译 APK
  echo "🔨 编译 APK (Debug)..."
  cd "$ANDROID_DIR"
  chmod +x ./gradlew 2>/dev/null || true

  # 导出 ANDROID_HOME 确保 Gradle 能找到 SDK
  if [ -n "$ANDROID_HOME" ]; then
    export ANDROID_HOME
  fi

  # 运行 Gradle 构建
  set +o pipefail
  local gradle_result=0
  ./gradlew assembleDebug 2>&1 || gradle_result=$?
  set -o pipefail

  if [ $gradle_result -ne 0 ]; then
    echo ""
    echo "❌ APK 编译失败（退出码: $gradle_result）"
    echo "   请检查上面的错误信息"
    exit 1
  fi

  echo ""
  echo "✅ APK 编译成功！"
  copy_apk

  echo ""
  echo "📱 下一步:"
  echo "   ./build.sh android:install  安装到设备"
  echo "   ./build.sh android:run      构建安装并启动"
}

run_android_sync() {
  echo "🔄 同步 Web 产物到 Android..."
  cd "$PROJECT_DIR"

  if [ ! -d "$ANDROID_DIR" ]; then
    echo "❌ 错误: 未找到 Android 项目，请先运行 android:setup"
    exit 1
  fi

  npx cap sync android 2>&1
  apply_china_mirrors_after_sync
  echo "✅ 同步完成"
}

run_android_open() {
  echo "📱 在 Android Studio 中打开项目..."
  cd "$PROJECT_DIR"

  if [ ! -d "$ANDROID_DIR" ]; then
    echo "❌ 错误: 未找到 Android 项目，请先运行 android:setup"
    exit 1
  fi

  npx cap open android 2>&1
}

run_android_install() {
  print_banner
  echo "📱 编译并安装 Android APK..."
  echo ""

  check_adb

  # 确认有设备连接
  DEVICES=$(adb devices 2>/dev/null | grep -v "List" | grep "device$" | wc -l | tr -d ' ')
  if [ "$DEVICES" -eq 0 ]; then
    echo "❌ 错误: 未检测到已连接的 Android 设备"
    echo "   请确保:"
    echo "   1. 设备已通过 USB 连接并开启 USB 调试"
    echo "   2. 运行 adb devices 确认设备已授权"
    exit 1
  fi
  echo "✅ 检测到 $DEVICES 台设备"

  # 确保 Android 项目已初始化
  if [ ! -d "$ANDROID_DIR" ]; then
    echo "❌ 错误: 未找到 Android 项目，请先运行 android:setup"
    exit 1
  fi

  # 构建 + 同步
  echo ""
  echo "🔨 构建发布版 APK..."
  cd "$ANDROID_DIR"

  # 使用 Gradle 构建
  if [ -f "./gradlew" ]; then
    chmod +x ./gradlew
    [ -n "$ANDROID_HOME" ] && export ANDROID_HOME
    ./gradlew assembleDebug 2>&1
  else
    echo "❌ 错误: 未找到 gradlew，Android 项目可能损坏"
    echo "   请重新运行: $0 android:setup"
    exit 1
  fi

  # 安装 APK
  APK_PATH=$(find "$ANDROID_DIR/app/build/outputs/apk/debug" -name "*.apk" 2>/dev/null | head -1)
  if [ -z "$APK_PATH" ]; then
    echo "❌ 错误: APK 构建失败，未找到产物"
    exit 1
  fi

  echo ""
  echo "📲 安装 APK 到设备..."
  adb install -r "$APK_PATH" 2>&1

  echo ""
  echo "✅ 安装完成！"

  # 复制 APK
  copy_apk
}

run_android_run() {
  print_banner
  echo "📱 构建安装并启动 App..."
  echo ""

  # 构建 + 同步
  check_node
  echo "🔨 构建 Web 应用..."
  run_build

  cd "$PROJECT_DIR"
  if [ ! -d "$ANDROID_DIR" ]; then
    echo "❌ 错误: 未找到 Android 项目，请先运行 android:setup"
    exit 1
  fi

  echo "🔄 同步 Web 到 Android..."
  npx cap sync android 2>&1
  apply_china_mirrors_after_sync

  # 安装
  check_adb
  DEVICES=$(adb devices 2>/dev/null | grep -v "List" | grep "device$" | wc -l | tr -d ' ')
  if [ "$DEVICES" -eq 0 ]; then
    echo "❌ 错误: 未检测到已连接的 Android 设备"
    exit 1
  fi

  echo "🔨 编译 APK..."
  cd "$ANDROID_DIR"
  chmod +x ./gradlew 2>/dev/null || true
  [ -n "$ANDROID_HOME" ] && export ANDROID_HOME
  ./gradlew assembleDebug 2>&1

  APK_PATH=$(find "$ANDROID_DIR/app/build/outputs/apk/debug" -name "*.apk" 2>/dev/null | head -1)
  if [ -z "$APK_PATH" ]; then
    echo "❌ 错误: APK 构建失败"
    exit 1
  fi

  echo "📲 安装并启动..."
  adb install -r "$APK_PATH" 2>&1

  # 启动 App
  echo "🚀 启动 App..."
  adb shell am start -n "$APP_ID/.MainActivity" 2>&1

  echo "✅ App 已启动！"

  # 复制 APK
  copy_apk
}

run_android_clean() {
  echo "🧹 清理 Android 构建产物..."
  if [ -d "$ANDROID_DIR" ]; then
    cd "$ANDROID_DIR"
    if [ -f "./gradlew" ]; then
      chmod +x ./gradlew
      ./gradlew clean 2>&1 | tail -2
    fi
    rm -rf app/build
    echo "✅ Android 构建产物清理完成"
  else
    echo "⚠️  未找到 Android 项目目录"
  fi
}

# 自动复制 APK 到输出目录
copy_apk() {
  local apk_path=$(find "$ANDROID_DIR/app/build/outputs/apk/debug" -name "*.apk" 2>/dev/null | head -1)
  if [ -z "$apk_path" ]; then
    echo "⚠️  未找到 APK 产物，跳过复制"
    return 1
  fi

  mkdir -p "$APK_OUT_DIR"
  cp "$apk_path" "$APK_OUT_DIR/zhongyi.apk"
  echo "📋 APK 已复制到: $APK_OUT_DIR/zhongyi.apk"
  return 0
}

main() {
  case "${1:-help}" in
    help)
      print_help
      ;;
    version)
      print_version
      ;;
    install)
      check_node
      run_install
      ;;
    install:clean)
      check_node
      run_install_clean
      ;;
    update)
      check_node
      run_update
      ;;
    audit)
      check_node
      run_audit
      ;;
    dev)
      check_node
      run_dev "$2" "$3"
      ;;
    build)
      check_node
      run_build
      ;;
    build:dev)
      check_node
      run_build_dev
      ;;
    build:analyze)
      check_node
      run_build_analyze
      ;;
    build:clean)
      run_build_clean
      ;;
    # Android
    android:setup)
      run_android_setup
      ;;
    android:build)
      run_android_build
      ;;
    android:sync)
      run_android_sync
      ;;
    android:open)
      run_android_open
      ;;
    android:install)
      run_android_install
      ;;
    android:run)
      run_android_run
      ;;
    android:clean)
      run_android_clean
      ;;
    preview)
      check_node
      run_preview "$2" "$3"
      ;;
    lint)
      check_node
      run_lint
      ;;
    format)
      check_node
      run_format
      ;;
    clean)
      run_clean
      ;;
    data:count)
      count_data
      ;;
    data:check)
      check_data
      ;;
    data:validate)
      validate_data_references
      ;;
    data:summary)
      generate_summary
      ;;
    *)
      echo "❌ 未知命令: $1"
      echo "使用 '$0 help' 查看可用命令"
      exit 1
      ;;
  esac
}

main "$@"