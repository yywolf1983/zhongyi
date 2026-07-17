import { createPortal } from 'react-dom'

// 浮动返回按钮：通过 Portal 渲染到 document.body，
// 彻底脱离页面内容层（尤其是 .page-enter 的 opacity 动画合成层），
// 避免在移动端 WebView 中渲染成半透明。
export default function FloatingBackButton({ onClick, label = '返回' }) {
  return createPortal(
    <button className="back-fab" onClick={onClick} aria-label={label}>
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
        <polyline points="15 18 9 12 15 6"></polyline>
      </svg>
    </button>,
    document.body
  )
}
