import { useState, useCallback, useEffect } from 'react'

const KEY = 'recent_views'
const MAX = 12

/**
 * 最近浏览 hook：记录用户最近查看的实体（证型/方剂/中药/穴位/针方等）。
 * 持久化到 localStorage，供首页「最近浏览」展示。
 * 由 AppContext 调用一次并向下共享，保证多模块写入后首页实时刷新。
 */
export function useRecent() {
  const [recent, setRecent] = useState([])

  useEffect(() => {
    try {
      const raw = localStorage.getItem(KEY)
      if (raw) {
        const parsed = JSON.parse(raw)
        if (Array.isArray(parsed)) setRecent(parsed)
      }
    } catch {
      /* ignore corrupted data */
    }
  }, [])

  const addRecent = useCallback((entry) => {
    if (!entry || !entry.id || !entry.type) return
    setRecent((prev) => {
      const next = [
        entry,
        ...prev.filter((e) => !(e.type === entry.type && e.id === entry.id))
      ].slice(0, MAX)
      try {
        localStorage.setItem(KEY, JSON.stringify(next))
      } catch {
        /* quota exceeded - ignore */
      }
      return next
    })
  }, [])

  const clearRecent = useCallback(() => {
    setRecent([])
    try {
      localStorage.removeItem(KEY)
    } catch {
      /* ignore */
    }
  }, [])

  return { recent, addRecent, clearRecent }
}
