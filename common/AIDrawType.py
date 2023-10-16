from enum import Enum

class AIDrawStyleEnum(Enum):
    EXPLORATION = '探索无限'
    ANCIENT_STYLE = '古风'
    ANIME = '二次元'
    REALISTIC = '写实风格'
    UKIYO_E = '浮世绘'
    LOW_POLY = 'low poly'
    FUTURISTIC = '未来主义'
    PIXEL_ART = '像素风格'
    CONCEPTUAL_ART = '概念艺术'
    CYBERPUNK = '赛博朋克'
    LOLITA_STYLE = '洛丽塔风格'
    BAROQUE_STYLE = '巴洛克风格'
    SURREALISM = '超现实主义'
    WATERCOLOR = '水彩画'
    STEAMPUNK = '蒸汽波艺术'
    OIL_PAINTING = '油画'
    CARTOON = '卡通画'

class AIDrawRadioEnum(Enum):
    RATIO_1_1 = "1:1"
    RATIO_3_2 = "3:2"
    RATIO_2_3 = "2:3"
