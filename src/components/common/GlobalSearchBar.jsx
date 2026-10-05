import { useState, useEffect, useRef, useCallback } from 'react'
import { useNavigate } from 'react-router-dom'
import { SearchService } from '../../services/SearchService.js'
import { navigateToEntity } from '../../services/EntityRoute.js'

export default function GlobalSearchBar() {
  const navigate = useNavigate()
  const wrapperRef = useRef(null)
  const [keyword, setKeyword] = useState('')
  const [suggestions, setSuggestions] = useState([])
  const [showSuggestions, setShowSuggestions] = useState(false)
  const [activeIndex, setActiveIndex] = useState(-1)

  // 点击外部关闭建议
  useEffect(() => {
    const handleClickOutside = (e) => {
      if (wrapperRef.current && !wrapperRef.current.contains(e.target)) {
        setShowSuggestions(false)
      }
    }
    document.addEventListener('mousedown', handleClickOutside)
    return () => document.removeEventListener('mousedown', handleClickOutside)
  }, [])

  // 输入即搜：debounce 获取建议
  useEffect(() => {
    if (!keyword.trim()) {
      setSuggestions([])
      setShowSuggestions(false)
      setActiveIndex(-1)
      return
    }
    const timer = setTimeout(() => {
      const list = SearchService.getSuggestions(keyword)
      setSuggestions(list)
      setShowSuggestions(list.length > 0)
      setActiveIndex(-1)
    }, 150)
    return () => clearTimeout(timer)
  }, [keyword])

  const doSearch = useCallback(() => {
    if (!keyword.trim()) return
    setShowSuggestions(false)
    navigate(`/search?q=${encodeURIComponent(keyword.trim())}`)
  }, [keyword, navigate])

  const handleSubmit = (e) => {
    e.preventDefault()
    doSearch()
  }

  const handleSuggestionClick = (suggestion) => {
    setShowSuggestions(false)
    if (suggestion.id) {
      navigateToEntity(navigate, suggestion.type, suggestion.id)
    } else {
      setKeyword(suggestion.name)
      navigate(`/search?q=${encodeURIComponent(suggestion.name)}`)
    }
  }

  // 键盘导航：上下切换高亮、回车跳转、Esc 关闭
  const handleKeyDown = (e) => {
    if (!showSuggestions || suggestions.length === 0) return
    if (e.key === 'ArrowDown') {
      e.preventDefault()
      setActiveIndex((i) => (i + 1) % suggestions.length)
    } else if (e.key === 'ArrowUp') {
      e.preventDefault()
      setActiveIndex((i) => (i <= 0 ? suggestions.length - 1 : i - 1))
    } else if (e.key === 'Enter') {
      if (activeIndex >= 0 && activeIndex < suggestions.length) {
        e.preventDefault()
        handleSuggestionClick(suggestions[activeIndex])
      }
    } else if (e.key === 'Escape') {
      setShowSuggestions(false)
    }
  }

  return (
    <div className="global-search-wrapper" ref={wrapperRef}>
      <form className="global-search-bar" onSubmit={handleSubmit}>
        <input
          type="text"
          className="global-search-input"
          placeholder="搜索证型、中药、穴位、方剂、针方、中西对照..."
          value={keyword}
          onChange={(e) => setKeyword(e.target.value)}
          onKeyDown={handleKeyDown}
          onFocus={() => {
            if (suggestions.length > 0) setShowSuggestions(true)
          }}
        />
        <button type="submit" className="global-search-btn">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
            <circle cx="11" cy="11" r="8"/>
            <line x1="21" y1="21" x2="16.65" y2="16.65"/>
          </svg>
          搜索
        </button>
      </form>

      {showSuggestions && suggestions.length > 0 && (
        <div className="search-suggestions global-suggestions-dropdown">
          <div className="suggestions-header">搜索建议</div>
          <div className="suggestions-list">
            {suggestions.map((suggestion, index) => (
              <div
                key={`${suggestion.type}-${suggestion.id}-${index}`}
                className={`suggestion-item ${index === activeIndex ? 'active' : ''}`}
                onClick={() => handleSuggestionClick(suggestion)}
                onMouseEnter={() => setActiveIndex(index)}
              >
                <span className="suggestion-name">{suggestion.name}</span>
                <span className="suggestion-type">{suggestion.type}</span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}
