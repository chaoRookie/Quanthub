// src/App.jsx
import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import HomePage from './pages/HomePage';
import StrategyDetailPage from './pages/StrategyDetailPage';
import EditorPage from './pages/EditorPage';
import ResultPage from './pages/ResultPage';

// 简单的顶部导航栏组件
const Navbar = () => (
  <nav className="bg-gray-900 border-b border-gray-800 px-6 py-4 flex justify-between items-center text-white">
    <div className="flex items-center gap-2">
      {/* 模拟Logo */}
      <div className="w-6 h-6 bg-gradient-to-r from-blue-500 to-green-400 rounded-full"></div>
      <span className="text-xl font-bold tracking-tight">QuantHub</span>
    </div>
    <div className="flex gap-6 text-sm text-gray-400">
      <span className="hover:text-white cursor-pointer">Home</span>
      <span className="hover:text-white cursor-pointer">The Workspace</span>
      <div className="w-8 h-8 bg-gray-700 rounded-full flex items-center justify-center text-xs">金</div>
    </div>
  </nav>
);

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-black text-gray-100 font-sans selection:bg-green-500 selection:text-black">
        <Navbar />
        <Routes>
          <Route path="/" element={<HomePage />} />
          {/* 策略详情页，:id 代表策略的名称 */}
          <Route path="/strategy/:id" element={<StrategyDetailPage />} />
          {/* 编辑器页面 */}
          <Route path="/editor/:id" element={<EditorPage />} />
          {/* 结果页面 */}
          <Route path="/result/:id" element={<ResultPage />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;