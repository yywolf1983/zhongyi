import { useEffect, useState, useCallback } from 'react'
import { BrowserRouter, Routes, Route, useLocation, useNavigate } from 'react-router-dom'
import { AppProvider } from '../context/AppContext'
import Header from '../components/common/Header'
import Navigation from '../components/common/Navigation'
import GlobalSearchBar from '../components/common/GlobalSearchBar'
import SyndromeModule from '../components/syndrome/SyndromeModule'
import AcupunctureModule from '../components/acupuncture/AcupunctureModule'
import FormulaModule from '../components/formula/FormulaModule'
import SearchModule from '../components/search/SearchModule'
import KnowledgeGraph from '../components/knowledge/KnowledgeGraph'
import ModernMapping from '../components/knowledge/ModernMapping'
import BookmarksModule from '../components/bookmarks/BookmarksModule'

// 路由变化自动滚动到顶部
function ScrollToTop() {
  const { pathname } = useLocation()
  useEffect(() => {
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }, [pathname])
  return null
}

// 滚动到顶部按钮
function ScrollTopButton() {
  const [visible, setVisible] = useState(false)

  useEffect(() => {
    const onScroll = () => {
      setVisible(window.scrollY > 400)
    }
    window.addEventListener('scroll', onScroll, { passive: true })
    return () => window.removeEventListener('scroll', onScroll)
  }, [])

  const scrollToTop = () => {
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }

  return (
    <button
      className={`scroll-top-btn ${visible ? 'visible' : ''}`}
      onClick={scrollToTop}
      aria-label="回到顶部"
    >
      ↑
    </button>
  )
}

// Android 返回键处理 + 状态栏
function useCapacitorNative() {
  const navigate = useNavigate()
  const location = useLocation()

  useEffect(() => {
    // 设置 Android 状态栏颜色
    const setupStatusBar = async () => {
      try {
        const { StatusBar, Style } = await import('@capacitor/status-bar')
        if (window.Capacitor?.getPlatform() === 'android') {
          await StatusBar.setBackgroundColor({ color: '#1a3a1a' })
          await StatusBar.setStyle({ style: Style.Dark })
        }
      } catch {
        // StatusBar plugin not available on this platform
      }
    }

    // 处理 Android 返回键
    const setupBackButton = async () => {
      try {
        const { App } = await import('@capacitor/app')
        App.addListener('backButton', ({ canGoBack }) => {
          if (!canGoBack) {
            // 如果已经在首页，按返回键退出应用
            if (location.pathname === '/' || location.pathname === '/syndromes') {
              App.exitApp()
            } else {
              // 否则返回上一页
              navigate(-1)
            }
          }
        })
      } catch {
        // App plugin not available on this platform (web)
      }
    }

    setupStatusBar()
    setupBackButton()
  }, [navigate, location.pathname])
}

function Layout({ children }) {
  useCapacitorNative()

  return (
    <div className="app-container">
      <Header />
      <GlobalSearchBar />
      <main className="main-content">
        <Navigation />
        <div className="page-enter">
          {children}
        </div>
      </main>
      <ScrollTopButton />
    </div>
  )
}

export default function App() {
  return (
    <BrowserRouter>
      <AppProvider>
        <ScrollToTop />
        <Routes>
          <Route element={<Layout><SyndromeModule /></Layout>} path="/" />
          <Route element={<Layout><SyndromeModule /></Layout>} path="/syndromes" />
          <Route element={<Layout><SyndromeModule /></Layout>} path="/syndromes/:syndromeId" />
          <Route element={<Layout><AcupunctureModule /></Layout>} path="/acupuncture" />
          <Route element={<Layout><AcupunctureModule /></Layout>} path="/acupuncture/:acupointId" />
          <Route element={<Layout><AcupunctureModule /></Layout>} path="/acupuncture/needle/:needleId" />
          <Route element={<Layout><FormulaModule /></Layout>} path="/formulas" />
          <Route element={<Layout><FormulaModule /></Layout>} path="/formulas/:formulaId" />
          <Route element={<Layout><FormulaModule /></Layout>} path="/formulas/medicine/:medicineId" />
          <Route element={<Layout><SearchModule /></Layout>} path="/search" />
          <Route element={<Layout><KnowledgeGraph /></Layout>} path="/knowledge-graph" />
          <Route element={<Layout><KnowledgeGraph /></Layout>} path="/knowledge-graph/:entityType/:entityId" />
          <Route element={<Layout><ModernMapping /></Layout>} path="/modern-mapping" />
          <Route element={<Layout><BookmarksModule /></Layout>} path="/bookmarks" />
          <Route element={<Layout><SyndromeModule /></Layout>} path="*" />
        </Routes>
      </AppProvider>
    </BrowserRouter>
  )
}
