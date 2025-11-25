// src/pages/EditorPage.jsx
import React, { useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import Editor from '@monaco-editor/react';
import { Play } from 'lucide-react';

const EditorPage = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [code, setCode] = useState(`# QuantHub Workspace: ${id}
# You can modify the code here

import backtrader as bt

# ... Your Strategy Logic ...
`);

  const handleBacktest = () => {
    // 实际项目中，这里会调用后端 API (Celery 任务)
    // 这里我们直接模拟“任务提交成功”，跳转到结果页
    console.log("Submitting code:", code);
    navigate(`/result/${id}`); 
  };

  return (
    <div className="h-[calc(100vh-64px)] flex flex-col">
      {/* 顶部工具栏 */}
      <div className="h-14 bg-gray-900 border-b border-gray-800 flex items-center justify-between px-6">
        <div className="flex items-center gap-2 text-gray-300">
           <span className="text-gray-500">Workspace /</span>
           <span>{id}</span>
        </div>
        <div className="flex gap-3">
          <button className="px-4 py-2 text-sm text-gray-300 bg-gray-800 rounded hover:bg-gray-700">Save</button>
          <button 
            onClick={handleBacktest}
            className="px-4 py-2 text-sm font-bold bg-green-500 text-black rounded hover:bg-green-600 flex items-center gap-2"
          >
            <Play size={16} />
            Run Backtest
          </button>
        </div>
      </div>

      {/* 编辑器区域 */}
      <div className="flex-1 bg-[#1e1e1e]">
        <Editor 
          height="100%" 
          defaultLanguage="python" 
          theme="vs-dark"
          value={code}
          onChange={(val) => setCode(val)}
          options={{
            fontSize: 14,
            minimap: { enabled: true },
            scrollBeyondLastLine: false,
          }}
        />
      </div>
    </div>
  );
};

export default EditorPage;