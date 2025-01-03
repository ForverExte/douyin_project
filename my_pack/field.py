from enum import Enum


class SearchChannelType(Enum):
    """搜索频道类型"""
    GENERAL = "aweme_general"  # 综合
    VIDEO = "aweme_video_web"  # 视频
    USER = "aweme_user_web"  # 用户
    LIVE = "aweme_live"  # 直播


class SearchSortType(Enum):
    """搜索排序类型"""
    GENERAL = 0  # 综合排序
    MOST_LIKE = 1  # 最多点赞
    LATEST = 2  # 最新发布


class PublishTimeType(Enum):
    """发布时间类型"""
    UNLIMITED = 0  # 不限
    ONE_DAY = 1  # 一天内
    ONE_WEEK = 7  # 一周内
    SIX_MONTH = 180  # 半年内
