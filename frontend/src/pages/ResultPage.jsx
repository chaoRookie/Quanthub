// src/pages/ResultPage.jsx
import React from 'react';
import ReactECharts from 'echarts-for-react'; // ECharts 的 React 封装

const ResultPage = () => {
  // 模拟图表配置
  const getOption = () => ({
    backgroundColor: 'transparent',
    tooltip: { trigger: 'axis' },
    grid: { left: '3%', right: '4%', bottom: '3%', containLabel: true },
    xAxis: {
      type: 'category',
      data: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
      axisLine: { lineStyle: { color: '#555' } }
    },
    yAxis: {
      type: 'value',
      splitLine: { lineStyle: { color: '#333' } },
      axisLine: { lineStyle: { color: '#555' } }
    },
    series: [
      {
        name: 'Strategy',
        type: 'line',
        smooth: true,
        data: [1000, 1120, 1080, 1350, 1400, 1550, 1680], // 模拟的净值曲线
        itemStyle: { color: '#10b981' }, // 绿色
        areaStyle: {
          color: {
            type: 'linear',
            x: 0, y: 0, x2: 0, y2: 1,
            colorStops: [{ offset: 0, color: 'rgba(16, 185, 129, 0.3)' }, { offset: 1, color: 'rgba(16, 185, 129, 0)' }]
          }
        }
      },
      {
        name: 'Benchmark',
        type: 'line',
        smooth: true,
        data: [1000, 1010, 1020, 1015, 1030, 1040, 1050],
        itemStyle: { color: '#ef4444' }, // 红色基准
        lineStyle: { type: 'dashed' }
      }
    ]
  });

  return (
    <div className="max-w-6xl mx-auto px-6 py-8">
      <h2 className="text-2xl font-bold text-white mb-6">Performance Report</h2>

      {/* 核心指标卡片 */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
        {[
          { label: 'Total Return', val: '+45.2%', color: 'text-green-400' },
          { label: 'Sharpe Ratio', val: '1.85', color: 'text-white' },
          { label: 'Max Drawdown', val: '-12.4%', color: 'text-red-400' },
          { label: 'Win Rate', val: '68%', color: 'text-white' }
        ].map((stat, i) => (
          <div key={i} className="bg-gray-900 border border-gray-800 p-6 rounded-xl">
            <div className="text-gray-400 text-sm mb-2">{stat.label}</div>
            <div className={`text-3xl font-bold ${stat.color}`}>{stat.val}</div>
          </div>
        ))}
      </div>

      {/* 图表区域 */}
      <div className="bg-gray-900 border border-gray-800 p-6 rounded-xl mb-8">
        <div className="text-white font-bold mb-4">Visual Analysis</div>
        <ReactECharts option={getOption()} style={{ height: '400px' }} />
      </div>

      {/* 底部模拟实盘按钮 */}
      <div className="flex justify-end">
        <button 
          onClick={() => alert('前端假装弹个窗：实盘连接模块正在开发中...')} 
          className="px-6 py-3 bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-bold"
        >
          Simulate Live Trading
        </button>
      </div>
    </div>
  );
};

export default ResultPage;