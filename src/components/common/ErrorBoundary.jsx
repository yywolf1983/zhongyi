import { Component } from 'react'

export default class ErrorBoundary extends Component {
  constructor(props) {
    super(props)
    this.state = { hasError: false, error: null }
  }

  static getDerivedStateFromError(error) {
    return { hasError: true, error }
  }

  componentDidCatch(error, info) {
    console.error('[ErrorBoundary] 捕获渲染错误:', error, info)
  }

  handleRetry = () => {
    this.setState({ hasError: false, error: null })
  }

  render() {
    if (this.state.hasError) {
      return (
        <div style={{
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          minHeight: '60vh',
          padding: '40px 20px',
          textAlign: 'center'
        }}>
          <div style={{ fontSize: '3rem', marginBottom: '16px' }}>⚠️</div>
          <h2 style={{ marginBottom: '8px', color: '#333' }}>
            {this.props.title || '页面加载出错'}
          </h2>
          <p style={{ color: '#888', maxWidth: '360px', marginBottom: '24px', fontSize: '0.9rem' }}>
            {this.props.message || '数据加载失败，请检查网络连接后重试。'}
          </p>
          <button
            onClick={this.handleRetry}
            style={{
              padding: '10px 32px',
              background: '#4a9c8c',
              color: '#fff',
              border: 'none',
              borderRadius: '8px',
              fontSize: '1rem',
              cursor: 'pointer'
            }}
          >
            重试
          </button>
          {this.props.showDetail && this.state.error && (
            <details style={{ marginTop: '24px', color: '#999', fontSize: '0.8rem', maxWidth: '400px' }}>
              <summary style={{ cursor: 'pointer', marginBottom: '8px' }}>错误详情</summary>
              <pre style={{ textAlign: 'left', whiteSpace: 'pre-wrap', wordBreak: 'break-all' }}>
                {this.state.error?.message || String(this.state.error)}
              </pre>
            </details>
          )}
        </div>
      )
    }

    return this.props.children
  }
}
