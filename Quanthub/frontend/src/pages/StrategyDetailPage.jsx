// src/pages/StrategyDetailPage.jsx
import React from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { GitFork, Star, User } from 'lucide-react';
import Editor from '@monaco-editor/react'; // 引入代码编辑器组件只读模式

const StrategyDetailPage = () => {
  const { id } = useParams();
  const navigate = useNavigate();

  // 模拟源代码
  const codeString = `
# QuantHub Original Strategy: ${id}
import backtrader as bt

class MyStrategy(bt.Strategy):
    params = (('period', 15),)

    def __init__(self):
        self.sma = bt.indicators.SMA(
            self.data.close, 
            period=self.params.period
        )

    def next(self):
        if self.sma > self.data.close:
            self.buy()
        elif self.sma < self.data.close:
            self.sell()
`;

  return (
    <div className="max-w-7xl mx-auto px-6 py-8">
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        
        {/* 左侧：策略源代码展示 */}
        <div className="lg:col-span-2">
          <div className="flex items-center justify-between mb-6">
            <div>
              <h2 className="text-3xl font-bold text-white capitalize">{id.replace('-', ' ')}</h2>
              <p className="text-gray-400 mt-1">The Origin Strategy</p>
            </div>
            <div className="flex gap-2">
                <span className="px-3 py-1 bg-gray-800 rounded text-xs text-gray-300">Trend</span>
                <span className="px-3 py-1 bg-gray-800 rounded text-xs text-gray-300">Low Risk</span>
            </div>
          </div>

          <div className="bg-[#1e1e1e] rounded-xl border border-gray-700 overflow-hidden h-[500px]">
            <div className="flex justify-between items-center px-4 py-2 bg-[#2d2d2d] border-b border-gray-700">
               <span className="text-xs text-gray-400">main.py</span>
               <span className="text-xs text-gray-500 cursor-pointer hover:text-white">Copy</span>
            </div>
            <Editor 
              height="100%" 
              defaultLanguage="python" 
              defaultValue={codeString} 
              theme="vs-dark"
              options={{ readOnly: true, minimap: { enabled: false } }}
            />
          </div>
        </div>

        {/* 右侧：社区 Forks 列表 */}
        <div className="lg:col-span-1">
           <h3 className="text-xl font-bold text-white mb-6">Top Forks by Community</h3>
           
           <div className="space-y-4">
             {/* 模拟列表项 */}
             {[
               { user: 'Michael', strategy: 'MACD Enhanced', apy: '+98.7%' },
               { user: 'Emily', strategy: 'RSI Optimized', apy: '+76.2%' },
               { user: 'Alex', strategy: 'Volatility Adj.', apy: '+54.8%' },
             ].map((item, idx) => (
               <div key={idx} className="bg-gray-900 border border-gray-800 p-4 rounded-lg flex items-center justify-between group hover:border-green-500 transition">
                 <div className="flex items-center gap-3">
                   <div className="w-8 h-8 rounded-full bg-gray-700 flex items-center justify-center">
                     <User size={16} />
                   </div>
                   <div>
                     <div className="text-white text-sm font-medium">{item.strategy}</div>
                     <div className="text-gray-500 text-xs">{item.user}</div>
                   </div>
                 </div>
                 <div className="text-green-400 font-bold text-sm">{item.apy}</div>
               </div>
             ))}
           </div>

           {/* 核心操作按钮：Fork */}
           <div className="mt-8 p-6 bg-gray-900 rounded-xl border border-gray-800 text-center">
             <p className="text-gray-400 text-sm mb-4">Want to improve this strategy?</p>
             <button 
               onClick={() => navigate(`/editor/${id}-fork-${Date.now()}`)} // 核心动作：跳转编辑器
               className="w-full py-3 bg-green-500 hover:bg-green-600 text-black font-bold rounded-lg flex items-center justify-center gap-2 transition"
             >
               <GitFork size={18} />
               Fork & Edit
             </button>
           </div>
        </div>

      </div>
    </div>
  );
};

export default StrategyDetailPage;