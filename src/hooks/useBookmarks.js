import { useState, useEffect, useCallback } from 'react'

const STORAGE_KEY = 'zhongyi_bookmarks'

export function useBookmarks() {
  const [bookmarks, setBookmarks] = useState(() => {
    try {
      const stored = localStorage.getItem(STORAGE_KEY)
      return stored ? JSON.parse(stored) : []
    } catch {
      return []
    }
  })

  useEffect(() => {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(bookmarks))
    } catch { /* ignore */ }
  }, [bookmarks])

  const addBookmark = useCallback((item) => {
    setBookmarks(prev => {
      if (prev.find(b => b.id === item.id && b.type === item.type)) {
        return prev
      }
      return [{ ...item, bookmarkedAt: new Date().toISOString() }, ...prev]
    })
  }, [])

  const removeBookmark = useCallback((id, type) => {
    setBookmarks(prev => prev.filter(b => !(b.id === id && b.type === type)))
  }, [])

  const isBookmarked = useCallback((id, type) => {
    return bookmarks.some(b => b.id === id && b.type === type)
  }, [bookmarks])

  const getBookmarksByType = useCallback((type) => {
    if (!type) return bookmarks
    return bookmarks.filter(b => b.type === type)
  }, [bookmarks])

  return {
    bookmarks,
    addBookmark,
    removeBookmark,
    isBookmarked,
    getBookmarksByType
  }
}
