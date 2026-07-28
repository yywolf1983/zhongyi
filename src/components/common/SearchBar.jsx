import { useCallback } from 'react'

/**
 * 通用搜索栏：用于各模块列表的"标题模糊搜索"。
 * 受控组件，由父级持有 state 并负责实际的列表过滤逻辑。
 */
export default function SearchBar({ value, onChange, placeholder = '搜索标题…' }) {
  const clear = useCallback(() => onChange(''), [onChange])
  return (
    <div className="module-search-bar">
      <span className="module-search-icon" aria-hidden>🔍</span>
      <input
        type="text"
        className="module-search-input"
        placeholder={placeholder}
        value={value}
        onChange={(e) => onChange(e.target.value)}
      />
      {value && (
        <button
          type="button"
          className="module-search-clear"
          onClick={clear}
          aria-label="清除搜索"
        >
          ✕
        </button>
      )}
    </div>
  )
}
