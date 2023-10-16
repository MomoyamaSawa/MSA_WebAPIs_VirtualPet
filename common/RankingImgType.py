from enum import Enum

class RankingImgType(Enum):
    ALL = "all"
    ILLUST = "illust"
    UGOIRA = "ugoira"
    MANGA = "manga"

class RankingImgMode(Enum):
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    ROOKIE = "rookie"
    ORIGINAL = "original"
    MALE = "male"
    FEMALE = "female"
    DAILY_R18 = "daily_r18"
    WEEKLY_R18 = "weekly_r18"
    MALE_R18 = "male_r18"
    FEMALE_R18 = "female_r18"
    R18G = "r18g"
