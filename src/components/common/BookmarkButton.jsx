import { useAppContext } from '../../context/AppContext'

export default function BookmarkButton({ item, type }) {
  const { isBookmarked, addBookmark, removeBookmark } = useAppContext()
  const bookmarked = isBookmarked(item.id, type)

  const handleClick = (e) => {
    e.stopPropagation()
    if (bookmarked) {
      removeBookmark(item.id, type)
    } else {
      addBookmark({ ...item, type })
    }
  }

  return (
    <button
      className="bookmark-btn"
      onClick={handleClick}
      title={bookmarked ? '取消收藏' : '添加收藏'}
    >
      {bookmarked ? '★' : '☆'}
    </button>
  )
}
