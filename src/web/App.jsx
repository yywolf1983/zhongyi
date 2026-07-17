import { useEffect, useState, useCallback } from 'react'
import { BrowserRouter, Routes, Route, useLocation, useNavigate } from 'react-router-dom'
import { AppProvider } from '../context/AppContext'
import Header from '../components/common/Header'
import Navigation from '../components/common/Navigation'
import GlobalSearchBar from '../components/common/GlobalSearchBar'
import ErrorBoundary from '../components/common/ErrorBoundary'
import { DataManager } from '../services/DataManager'
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
          await StatusBar.setBackgroundColor({ color: '#161b20' })
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

// 应用启动时初始化数据，显示加载状态
function DataLoader({ children }) {
  const [dataState, setDataState] = useState('loading')
  const [errorMsg, setErrorMsg] = useState('')

  useEffect(() => {
    // 如果数据已有状态（比如 other component 已经 init），直接使用
    if (DataManager.isReady) {
      setDataState('ready')
      return
    }
    if (DataManager.state === 'ready' && DataManager.error) {
      setDataState('degraded')
      setErrorMsg(DataManager.error)
      return
    }

    const unsub = DataManager.onStateChange((state, err) => {
      if (state === 'ready') {
        setDataState(err ? 'degraded' : 'ready')
        setErrorMsg(err || '')
      } else if (state === 'error') {
        setDataState('error')
        setErrorMsg(err || '未知错误')
      }
    })

    // 延迟调用 init，避免阻塞首屏渲染
    const timer = setTimeout(() => {
      DataManager.init()
    }, 0)

    return () => {
      clearTimeout(timer)
      unsub()
    }
  }, [])

  const handleRetry = useCallback(() => {
    setDataState('loading')
    setErrorMsg('')
    DataManager.reload()
  }, [])

  if (dataState === 'loading') {
    return (
      <div style={{
        display: 'flex', flexDirection: 'column', alignItems: 'center',
        justifyContent: 'center', minHeight: '50vh', padding: '40px 20px'
      }}>
        <div className="loading-spinner" style={{
          width: '40px', height: '40px', border: '3px solid var(--color-border)',
          borderTopColor: 'var(--color-primary)', borderRadius: '50%',
          animation: 'spin 0.8s linear infinite', marginBottom: '16px'
        }} />
        <p style={{ color: 'var(--color-text-hint)', fontSize: '0.95rem' }}>
          {children.props?.loadingText || '正在加载数据...'}
        </p>
      </div>
    )
  }

  if (dataState === 'error') {
    return (
      <div style={{
        display: 'flex', flexDirection: 'column', alignItems: 'center',
        justifyContent: 'center', minHeight: '50vh', padding: '40px 20px',
        textAlign: 'center'
      }}>
        <div style={{ fontSize: '3rem', marginBottom: '16px' }}>⚠️</div>
        <h2 style={{ marginBottom: '8px', color: 'var(--color-text-primary)' }}>数据加载失败</h2>
        <p style={{ color: 'var(--color-text-hint)', maxWidth: '360px', marginBottom: '24px', fontSize: '0.9rem' }}>
          应用数据未能成功加载，请重试。
        </p>
        <button
          onClick={handleRetry}
          style={{
            padding: '10px 32px', background: 'var(--color-primary)', color: 'var(--color-text-on-primary)',
            border: 'none', borderRadius: '8px', fontSize: '1rem', cursor: 'pointer'
          }}
        >
          重试
        </button>
      </div>
    )
  }

  // ready / degraded 状态都渲染子组件
  return children
}

function Layout({ children }) {
  useCapacitorNative()

  return (
    <div className="app-container">
      <Header />
      <GlobalSearchBar />
      <Navigation />
      <main className="main-content">
        <div className="page-enter">
          <ErrorBoundary>
            <DataLoader>{children}</DataLoader>
          </ErrorBoundary>
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
          <Route element={<Layout><AcupunctureModule /></Layout>} path="/acupuncture/acu-presc/:acuPrescId" />
          <Route element={<Layout><AcupunctureModule /></Layout>} path="/acupuncture/presc/:prescId" />
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
