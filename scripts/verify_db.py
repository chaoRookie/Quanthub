"""
数据库验证脚本：检查数据库完整性和数据质量

使用方法：
    python manage.py shell
    >>> exec(open('scripts/verify_db.py').read())
"""

import os
import sys
import django

# 设置 Django 环境
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from backend.models import User, MarketDataDaily, Strategy, StrategyVersion, BacktestRecord
from datetime import date
from decimal import Decimal

def verify_database():
    """执行数据库验证"""
    
    print("=" * 50)
    print("QuantHub 数据库验证报告")
    print("=" * 50)
    
    # 1. 检查用户表
    print("\n[1/5] 检查用户表...")
    user_count = User.objects.count()
    print(f"  用户总数: {user_count}")
    
    # 2. 检查行情数据表
    print("\n[2/5] 检查日线行情表...")
    total_records = MarketDataDaily.objects.count()
    print(f"  总记录数: {total_records:,} 条")
    
    # 检查特定股票数据
    ping_an = MarketDataDaily.objects.filter(ts_code='000001.SZ')
    print(f"  平安银行(000001.SZ)数据: {ping_an.count()} 天")
    
    # 检查最新数据日期
    if total_records > 0:
        latest_date = MarketDataDaily.objects.order_by('-trade_date').first().trade_date
        print(f"  最新数据日期: {latest_date}")
    
    # 3. 检查策略表
    print("\n[3/5] 检查策略表...")
    strategy_count = Strategy.objects.count()
    print(f"  策略总数: {strategy_count}")
    
    # 4. 检查版本表
    print("\n[4/5] 检查版本表...")
    version_count = StrategyVersion.objects.count()
    print(f"  版本总数: {version_count}")
    
    # 5. 测试 unique_together 约束
    print("\n[5/5] 测试数据完整性约束...")
    try:
        # 尝试插入重复数据
        test_data = MarketDataDaily(
            ts_code='TEST.SZ',
            trade_date=date(2024, 1, 1),
            open=Decimal('10.00'),
            high=Decimal('10.50'),
            low=Decimal('9.80'),
            close=Decimal('10.20'),
            pre_close=Decimal('9.90'),
            vol=Decimal('1000000'),
            amount=Decimal('102000')
        )
        test_data.save()
        
        # 再次插入相同数据（应该失败）
        duplicate_data = MarketDataDaily(
            ts_code='TEST.SZ',
            trade_date=date(2024, 1, 1),
            open=Decimal('11.00'),
            high=Decimal('11.50'),
            low=Decimal('10.80'),
            close=Decimal('11.20'),
            pre_close=Decimal('10.90'),
            vol=Decimal('2000000'),
            amount=Decimal('224000')
        )
        duplicate_data.save()
        
        print("  ✗ unique_together 约束未生效（不应该到达这里）")
        
    except Exception as e:
        if "unique" in str(e).lower() or "duplicate" in str(e).lower():
            print("  ✓ unique_together 约束正常工作")
        else:
            print(f"  ？ 发生其他错误: {e}")
    
    # 清理测试数据
    MarketDataDaily.objects.filter(ts_code='TEST.SZ').delete()
    
    print("\n" + "=" * 50)
    print("验证完成！")
    print("=" * 50)

if __name__ == "__main__":
    verify_database()
