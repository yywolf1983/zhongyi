import { useState } from 'react'

/**
 * 可折叠筛选分组：默认收起，仅显示「标签：当前选择 ▾」一行；
 * 点开才平铺内部筛选内容（通常是 tag-filter-bar 的 chips）。
 * 用于分类/子类等占用竖向空间较多的筛选区，兼顾「全部展示」与「不挤占列表」。
 */
export default function CollapsibleFilter({ label, summary, defaultOpen = false, children }) {
  const [open, setOpen] = useState(defaultOpen)

  return (
    <div className="filter-group">
      <button
        type="button"
        className="filter-group-toggle"
        aria-expanded={open}
        onClick={() => setOpen((o) => !o)}
      >
        <span className="filter-group-label">{label}</span>
        <span className="filter-group-summary">{summary}</span>
        <span className={`filter-group-chevron ${open ? 'open' : ''}`} />
      </button>
      {open && <div className="filter-group-body">{children}</div>}
    </div>
  )
}
