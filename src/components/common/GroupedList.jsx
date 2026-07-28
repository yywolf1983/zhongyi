import { useState, useMemo } from 'react'
import { cloneElement } from 'react'
import EmptyState from './EmptyState.jsx'

/**
 * 搜索命中关键词高亮。
 * 仅当文本本身包含查询词时高亮（拼音/代码命中不强行高亮标题）。
 */
export function Highlight({ text, query }) {
  const t = (text ?? '').toString()
  const q = (query ?? '').trim()
  if (!q) return t
  const idx = t.toLowerCase().indexOf(q.toLowerCase())
  if (idx === -1) return t
  return (
    <>
      {t.slice(0, idx)}
      <mark className="hl">{t.slice(idx, idx + q.length)}</mark>
      {t.slice(idx + q.length)}
    </>
  )
}

/**
 * 通用分组列表：按 getGroup 分组，每组渲染吸顶组标题，组内渲染卡片；
 * 整体保留"加载更多"分页，避免长列表一次性渲染卡顿。
 * 用法同 EntityList，额外传入 getGroup（与可选 groupLabel）。
 */
export default function GroupedList({
  items = [],
  getGroup,
  groupLabel,
  sortGroups = false,
  renderItem,
  getKey,
  pageSize = 30,
  step = 30,
  emptyMessage = '暂无数据',
  emptyIcon = '🔍',
  className = '',
}) {
  const [visible, setVisible] = useState(pageSize)

  const groups = useMemo(() => {
    if (!items || items.length === 0) return []
    const map = new Map()
    for (const it of items) {
      const g = (getGroup ? getGroup(it) : null) ?? '其他'
      if (!map.has(g)) map.set(g, [])
      map.get(g).push(it)
    }
    let keys = Array.from(map.keys())
    if (sortGroups) {
      keys = keys.sort((a, b) => String(a).localeCompare(String(b), 'zh-Hans-CN'))
    }
    return keys.map((k) => ({
      key: k,
      label: groupLabel ? groupLabel(k) : k,
      items: map.get(k),
    }))
  }, [items, getGroup, groupLabel, sortGroups])

  const flat = useMemo(() => {
    const arr = []
    for (const g of groups) {
      arr.push({ type: 'header', group: g })
      for (const it of g.items) arr.push({ type: 'item', item: it, group: g })
    }
    return arr
  }, [groups])

  const shown = flat.slice(0, visible)
  const hasMore = visible < flat.length
  const loadMore = () => setVisible((v) => Math.min(v + step, flat.length))

  if (!items || items.length === 0) {
    return <EmptyState message={emptyMessage} icon={emptyIcon} />
  }

  return (
    <div className={className}>
      <div className="grouped-list">
        {shown.map((node) => {
          if (node.type === 'header') {
            return (
              <div key={`gh-${node.group.key}`} className="list-group-header">
                <span className="list-group-label">{node.group.label}</span>
                <span className="list-group-count">{node.group.items.length}</span>
              </div>
            )
          }
          const el = renderItem(node.item)
          return getKey ? cloneElement(el, { key: getKey(node.item) }) : el
        })}
      </div>
      {hasMore && (
        <div className="load-more-wrap">
          <button className="load-more-btn" type="button" onClick={loadMore}>
            加载更多（剩余 {flat.length - visible}）
          </button>
        </div>
      )}
    </div>
  )
}
