import { useState, useMemo, cloneElement } from 'react'
import EmptyState from './EmptyState.jsx'

/**
 * 通用分页列表组件
 * 解决长列表（中药/功效/穴位/方剂数百~上千条）一次性渲染全部 DOM 导致的
 * 手机滚动卡顿与内存占用问题：仅渲染当前可见的 pageSize 条，点击「加载更多」增量展开。
 *
 * 用法：
 *   <EntityList
 *     items={medicines}
 *     pageSize={24}
 *     getKey={(m) => m.id}
 *     renderItem={(item) => (
 *       <div key={item.id} className="list-item medicine" onClick={...}>
 *         <div className="list-item-title">{item.name}</div>
 *       </div>
 *     )}
 *   />
 *
 * 注意：renderItem 返回的元素需自带 key（如上例的 key={item.id}）。
 */
export default function EntityList({
  items = [],
  renderItem,
  getKey,
  pageSize = 24,
  step = 24,
  emptyMessage = '暂无数据',
  emptyIcon = '🔍',
  className = ''
}) {
  const [visible, setVisible] = useState(pageSize)

  const shown = useMemo(
    () => (items || []).slice(0, visible),
    [items, visible]
  )
  const hasMore = visible < (items?.length || 0)

  const loadMore = () => {
    setVisible((v) => Math.min(v + step, items.length))
  }

  if (!items || items.length === 0) {
    return <EmptyState message={emptyMessage} icon={emptyIcon} />
  }

  return (
    <div className={className}>
      <div className="list-container">
        {shown.map((item) => {
          const el = renderItem(item)
          return getKey ? cloneElement(el, { key: getKey(item) }) : el
        })}
      </div>
      {hasMore && (
        <div className="load-more-wrap">
          <button className="load-more-btn" onClick={loadMore} type="button">
            加载更多（剩余 {items.length - visible}）
          </button>
        </div>
      )}
    </div>
  )
}
