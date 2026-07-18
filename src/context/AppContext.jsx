import { createContext, useContext } from 'react'
import { useBookmarks } from '../hooks/useBookmarks'
import { useRecent } from '../hooks/useRecent'

const AppContext = createContext(null)

export function AppProvider({ children }) {
  const bookmarkHook = useBookmarks()
  const recentHook = useRecent()

  return (
    <AppContext.Provider value={{ ...bookmarkHook, ...recentHook }}>
      {children}
    </AppContext.Provider>
  )
}

export function useAppContext() {
  const context = useContext(AppContext)
  if (!context) {
    throw new Error('useAppContext must be used within AppProvider')
  }
  return context
}
