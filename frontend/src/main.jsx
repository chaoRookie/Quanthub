import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './app.jsx'  // 引用你的 app.jsx
import './index.css'         // 引用样式

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)