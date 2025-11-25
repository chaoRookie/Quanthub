// src/pages/HomePage.jsx
import React from 'react';
import { useNavigate } from 'react-router-dom';
import { TrendingUp, Activity, Zap, Layers } from 'lucide-react'; // 图标库

const HomePage = () => {
  const navigate = useNavigate();

  // 模拟四个经典策略数据
  const strategies = [
    { id: 'dual-ma', name: 'Dual MA Strategy', return: '+125.4%', icon: <TrendingUp className="text-orange-500" />, color: 'text-green-400' },
    { id: 'bitcoin', name: 'Bitcoin Trend', return: '+48.7%', icon: <Activity className="text-yellow-500" />, color: 'text-green-400' },
    { id: 'breakout', name: 'Breakout Strategy', return: '+98.1%', icon: <Zap className="text-orange-400" />, color: 'text-green-400' },
    { id: 'pairs', name: 'Pairs Trading', return: '+36.5%', icon: <Layers className="text-blue-400" />, color: 'text-green-400' },
  ];

  return (
    <div className="max-w-6xl mx-auto px-6 py-12">
      {/* 顶部 Banner 文字 */}
      <div className="mb-16 mt-8">
        <h1 className="text-6xl font-bold text-white mb-6 leading-tight">
          Algo Trading <br />
          <span className="text-gray-400">for Everyone</span>
        </h1>
        <button className="px-6 py-3 border border-gray-600 rounded-lg hover:bg-gray-800 transition text-gray-300">
          Start Backtesting
        </button>
      </div>

      {/* 经典模型卡片区域 */}
      <h2 className="text-xl text-gray-400 mb-6">Classic Models</h2>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {strategies.map((strat) => (
          <div 
            key={strat.id}
            onClick={() => navigate(`/strategy/${strat.id}`)} // 点击跳转到详情页
            className="bg-gray-900 border border-gray-800 rounded-xl p-6 cursor-pointer hover:border-green-500 hover:shadow-lg hover:shadow-green-900/20 transition-all duration-300 group"
          >
            <div className="flex items-center gap-3 mb-4">
              <div className="p-2 bg-gray-800 rounded-lg">{strat.icon}</div>
              <span className="font-medium text-gray-200">{strat.name}</span>
            </div>
            <div className={`text-4xl font-bold ${strat.color} mb-4`}>
              {strat.return}
            </div>
            {/* 模拟一个小走势图 */}
            <div className="h-12 w-full bg-gray-800/50 rounded overflow-hidden relative">
               <div className="absolute bottom-0 left-0 w-full h-full bg-gradient-to-t from-green-500/10 to-transparent"></div>
               <svg className="w-full h-full text-green-500 fill-none stroke-current stroke-2" viewBox="0 0 100 20">
                 <path d="M0 15 Q 20 18, 40 10 T 100 5" />
               </svg>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default HomePage;