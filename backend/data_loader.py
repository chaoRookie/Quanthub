"""
数据加载脚本：从 Tushare 拉取股票数据并存入数据库

使用方法：
    python manage.py shell
    >>> from backend.data_loader import load_market_data
    >>> load_market_data(start_year=2020, end_year=2024)
"""

import tushare as ts
import os
from datetime import datetime
from decimal import Decimal
from backend.models import MarketDataDaily
from django.db import transaction

# 从环境变量读取 Tushare Token（更安全）
TUSHARE_TOKEN = os.environ.get('TUSHARE_TOKEN', '')

if not TUSHARE_TOKEN:
    print("⚠️ 警告: TUSHARE_TOKEN 环境变量未设置")
    print("请设置环境变量: set TUSHARE_TOKEN=你的token")
    print("或者直接修改本文件第11行")


def init_tushare():
    """初始化 Tushare API"""
    ts.set_token(TUSHARE_TOKEN)
    return ts.pro_api()

def load_market_data(start_year=2020, end_year=2024, batch_size=100):
    """
    加载市场数据到数据库
    
    参数:
        start_year: 开始年份
        end_year: 结束年份
        batch_size: 每批处理的股票数量
    """
    pro = init_tushare()
    
    # 1. 获取所有股票列表
    print("正在获取股票列表...")
    stock_list = pro.stock_basic(exchange='', list_status='L', fields='ts_code,name')
    total_stocks = len(stock_list)
    print(f"共获取到 {total_stocks} 只股票")
    
    # 2. 按年份循环
    for year in range(start_year, end_year + 1):
        start_date = f"{year}0101"
        end_date = f"{year}1231"
        print(f"\n处理 {year} 年数据...")
        
        # 3. 按股票分批处理
        for i in range(0, total_stocks, batch_size):
            batch_stocks = stock_list[i:i+batch_size]
            batch_data = []
            
            for idx, stock in batch_stocks.iterrows():
                ts_code = stock['ts_code']
                try:
                    # 调用 Tushare API 获取日线数据
                    df = pro.daily(
                        ts_code=ts_code,
                        start_date=start_date,
                        end_date=end_date
                    )
                    
                    if df.empty:
                        continue
                    
                    # 数据清洗：转换为 Django 模型实例
                    for _, row in df.iterrows():
                        # 跳过空值数据
                        if row.isnull().any():
                            continue
                        
                        batch_data.append(MarketDataDaily(
                            ts_code=row['ts_code'],
                            trade_date=datetime.strptime(str(row['trade_date']), '%Y%m%d').date(),
                            open=Decimal(str(row['open'])),
                            high=Decimal(str(row['high'])),
                            low=Decimal(str(row['low'])),
                            close=Decimal(str(row['close'])),
                            pre_close=Decimal(str(row['pre_close'])),
                            vol=Decimal(str(row['vol'])),
                            amount=Decimal(str(row['amount']))
                        ))
                    
                    print(f"  已处理 {ts_code} ({idx+1}/{len(batch_stocks)})")
                    
                except Exception as e:
                    print(f"  ⚠️ {ts_code} 获取失败: {e}")
                    continue
            
            # 4. 批量插入数据库 (高效！)
            if batch_data:
                try:
                    MarketDataDaily.objects.bulk_create(
                        batch_data,
                        ignore_conflicts=True  # 忽略重复数据
                    )
                    print(f"  ✓ 成功插入 {len(batch_data)} 条数据")
                except Exception as e:
                    print(f"  ✗ 批量插入失败: {e}")
            
            print(f"批次 {i//batch_size + 1}/{(total_stocks + batch_size - 1)//batch_size} 完成")
    
    print(f"\n✅ 数据加载完成！共处理 {end_year - start_year + 1} 年数据")

if __name__ == "__main__":
    print("请在 Django shell 中运行此脚本：")
    print("  python manage.py shell")
    print("  >>> from backend.data_loader import load_market_data")
    print("  >>> load_market_data()")
