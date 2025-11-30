from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    """
    用户表：直接继承 Django 自带的 AbstractUser
    包含字段：username, password, email, first_name, last_name, is_active, date_joined 等
    """
    pass

class MarketDataDaily(models.Model):
    """
    日线行情表：存储 Tushare 拉取的历史数据
    """
    ts_code = models.CharField(max_length=20, db_index=True, verbose_name="股票代码")
    trade_date = models.DateField(db_index=True, verbose_name="交易日期")
    
    # 使用 DecimalField 保证金额精度，严禁使用 Float
    open = models.DecimalField(max_digits=20, decimal_places=4, verbose_name="开盘价")
    high = models.DecimalField(max_digits=20, decimal_places=4, verbose_name="最高价")
    low = models.DecimalField(max_digits=20, decimal_places=4, verbose_name="最低价")
    close = models.DecimalField(max_digits=20, decimal_places=4, verbose_name="收盘价")
    pre_close = models.DecimalField(max_digits=20, decimal_places=4, verbose_name="昨收价")
    vol = models.DecimalField(max_digits=20, decimal_places=4, verbose_name="成交量(手)")
    amount = models.DecimalField(max_digits=20, decimal_places=4, verbose_name="成交额(千元)")

    class Meta:
        verbose_name = "日线行情"
        verbose_name_plural = verbose_name
        # 联合主键：同一只股票在同一天只能有一条记录
        unique_together = ('ts_code', 'trade_date')
        indexes = [
            models.Index(fields=['ts_code', 'trade_date']),
        ]
    
    def __str__(self):
        return f"{self.ts_code} - {self.trade_date}"

class Strategy(models.Model):
    """
    策略仓库表：相当于 GitHub 的 Repository
    """
    title = models.CharField(max_length=200, verbose_name="策略名称")
    description = models.TextField(blank=True, verbose_name="策略描述")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="strategies", verbose_name="作者")
    
    # Fork 机制：指向原策略
    fork_from = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name="forks", verbose_name="Fork自")
    
    is_public = models.BooleanField(default=True, verbose_name="是否公开")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        verbose_name = "策略仓库"
        verbose_name_plural = verbose_name
    
    def __str__(self):
        return self.title

class StrategyVersion(models.Model):
    """
    代码版本表：相当于 Git 的 Commit
    每次保存代码都是 Insert 新记录，实现版本控制
    """
    strategy = models.ForeignKey(Strategy, on_delete=models.CASCADE, related_name="versions", verbose_name="所属策略")
    version_tag = models.CharField(max_length=50, verbose_name="版本号") # e.g., "v1.0"
    code_content = models.TextField(verbose_name="代码内容")
    commit_message = models.CharField(max_length=500, verbose_name="提交说明")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="提交时间")

    class Meta:
        verbose_name = "策略版本"
        verbose_name_plural = verbose_name
        ordering = ['-created_at'] # 最新版本在前
    
    def __str__(self):
        return f"{self.strategy.title} - {self.version_tag}"

class BacktestRecord(models.Model):
    """
    回测结果表：记录某一个版本的运行结果
    """
    strategy_version = models.OneToOneField(StrategyVersion, on_delete=models.CASCADE, related_name="backtest_result", verbose_name="关联版本")
    
    # 核心绩效指标
    annual_return = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="年化收益率(%)")
    max_drawdown = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="最大回撤(%)")
    sharpe_ratio = models.DecimalField(max_digits=10, decimal_places=4, verbose_name="夏普比率")
    
    # 图表数据 (JSON)
    chart_data = models.JSONField(verbose_name="图表数据") # {"dates": [], "values": []}
    trade_log = models.JSONField(verbose_name="交易记录")   # [{"date": "...", "action": "buy", ...}]
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="回测时间")

    class Meta:
        verbose_name = "回测记录"
        verbose_name_plural = verbose_name
    
    def __str__(self):
        return f"{self.strategy_version} - {self.annual_return}%"
