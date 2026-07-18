/**
 * 通用详情区块组件
 * 统一三个详情页大量重复的 <div className="section"><h2 className="section-title">...</h2>...</div> 结构。
 *
 * 用法：
 *   <DetailSection title="主治病症">
 *     <div className="tag-list">...</div>
 *   </DetailSection>
 *
 *   // 次要区块（现代应用等）
 *   <DetailSection title="现代应用" secondary>...</DetailSection>
 *
 *   // 中西对照标题样式 + 锚点 id
 *   <DetailSection title="中西对照" mapping id="sec-mapping">...</DetailSection>
 *
 * 约定：当没有内容需要展示时，调用处应直接不渲染本组件（保持既有条件渲染逻辑）。
 */
export default function DetailSection({
  title,
  id,
  secondary = false,
  mapping = false,
  children
}) {
  return (
    <div className={`section${secondary ? ' secondary' : ''}`} id={id}>
      <h2 className={`section-title${mapping ? ' mapping-title' : ''}`}>{title}</h2>
      {children}
    </div>
  )
}
