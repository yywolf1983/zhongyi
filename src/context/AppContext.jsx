import { createContext, useContext } from 'react'
import { useBookmarks } from '../hooks/useBookmarks'

const AppContext = createContext(null)

export function AppProvider({ children }) {
  const bookmarkHook = useBookmarks()

  return (
    <AppContext.Provider value={{ ...bookmarkHook }}>
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
