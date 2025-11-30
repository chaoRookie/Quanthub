"""
Django Admin 配置
提供可视化数据库管理界面
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, MarketDataDaily, Strategy, StrategyVersion, BacktestRecord

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """用户管理"""
    list_display = ('username', 'email', 'is_staff', 'date_joined')
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    search_fields = ('username', 'email')

@admin.register(MarketDataDaily)
class MarketDataDailyAdmin(admin.ModelAdmin):
    """日线行情管理"""
    list_display = ('ts_code', 'trade_date', 'open', 'high', 'low', 'close', 'vol')
    list_filter = ('trade_date',)
    search_fields = ('ts_code',)
    date_hierarchy = 'trade_date'
    ordering = ('-trade_date', 'ts_code')
    
    # 只读字段（防止误修改历史数据）
    readonly_fields = ('ts_code', 'trade_date', 'open', 'high', 'low', 'close', 'pre_close', 'vol', 'amount')
    
    # 每页显示数量
    list_per_page = 50

@admin.register(Strategy)
class StrategyAdmin(admin.ModelAdmin):
    """策略仓库管理"""
    list_display = ('title', 'user', 'is_public', 'created_at', 'get_version_count')
    list_filter = ('is_public', 'created_at')
    search_fields = ('title', 'description', 'user__username')
    date_hierarchy = 'created_at'
    raw_id_fields = ('user', 'fork_from')  # 大数据量时使用搜索框
    
    def get_version_count(self, obj):
        """显示版本数量"""
        return obj.versions.count()
    get_version_count.short_description = '版本数'

@admin.register(StrategyVersion)
class StrategyVersionAdmin(admin.ModelAdmin):
    """代码版本管理"""
    list_display = ('strategy', 'version_tag', 'commit_message', 'created_at', 'get_code_preview')
    list_filter = ('created_at',)
    search_fields = ('strategy__title', 'version_tag', 'commit_message')
    date_hierarchy = 'created_at'
    raw_id_fields = ('strategy',)
    
    # 代码内容很长，在列表里只显示前50个字符
    def get_code_preview(self, obj):
        """代码预览"""
        return obj.code_content[:50] + '...' if len(obj.code_content) > 50 else obj.code_content
    get_code_preview.short_description = '代码预览'
    
    # 代码内容字段使用文本框显示
    fieldsets = (
        ('基本信息', {
            'fields': ('strategy', 'version_tag', 'commit_message')
        }),
        ('代码内容', {
            'fields': ('code_content',),
            'classes': ('wide',)  # 宽屏显示
        }),
    )

@admin.register(BacktestRecord)
class BacktestRecordAdmin(admin.ModelAdmin):
    """回测结果管理"""
    list_display = ('strategy_version', 'annual_return', 'max_drawdown', 'sharpe_ratio', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('strategy_version__strategy__title',)
    date_hierarchy = 'created_at'
    raw_id_fields = ('strategy_version',)
    
    # JSON字段使用 JSONField widget 显示
    fieldsets = (
        ('绩效指标', {
            'fields': ('strategy_version', 'annual_return', 'max_drawdown', 'sharpe_ratio')
        }),
        ('详细数据', {
            'fields': ('chart_data', 'trade_log'),
            'classes': ('collapse',)  # 默认折叠
        }),
    )
    
    # 设置颜色高亮（年化收益为正显示绿色，为负显示红色）
    def annual_return(self, obj):
        from django.utils.html import format_html
        if obj.annual_return > 0:
            return format_html('<span style="color: green;">+{}%</span>', obj.annual_return)
        else:
            return format_html('<span style="color: red;">{}%</span>', obj.annual_return)
    annual_return.short_description = '年化收益率'

# 自定义 Admin 站点标题
admin.site.site_header = 'QuantHub 管理后台'
admin.site.site_title = 'QuantHub Admin'
admin.site.index_title = '欢迎使用 QuantHub 数据管理系统'
