"""
FX Trend Dashboard 설정 파일
"""

# 지원 통화 설정
CURRENCIES = {
    'USD/KRW': {
        'symbol': 'USD/KRW',
        'name': '미국 달러',
        'fdr_code': 'USD/KRW'
    },
    'JPY/KRW': {
        'symbol': 'JPY/KRW',
        'name': '일본 엔화',
        'fdr_code': 'JPY/KRW'
    },
    'EUR/KRW': {
        'symbol': 'EUR/KRW',
        'name': '유로화',
        'fdr_code': 'EUR/KRW'
    },
    'USD/BRL': {
        'symbol': 'USD/BRL',
        'name': '브라질 헤알 (USD기준)',
        'fdr_code': 'USD/BRL'
    }
}

# 기본 설정
DEFAULT_CURRENCY = 'USD/KRW'
DEFAULT_PERIOD_YEARS = 5  # 그래프에 표시할 기간
MA_WARMUP_YEARS = 3  # 이동평균 계산을 위한 추가 기간 (최대 MA 기간)

# 이동평균 설정 (Bloomberg Terminal: 다크 배경에 잘 보이는 색상)
MOVING_AVERAGES = {
    'MA3M': {
        'days': 60,
        'label': '3개월 이동평균',
        'color': '#ff6b6b',
        'line_width': 1
    },
    'MA1Y': {
        'days': 250,
        'label': '1년 이동평균',
        'color': '#5dd0f5',
        'line_width': 1
    },
    'MA3Y': {
        'days': 750,
        'label': '3년 이동평균',
        'color': '#7ee787',
        'line_width': 1
    }
}

# 그래프 설정 (Bloomberg Terminal Style)
GRAPH_CONFIG = {
    'width': 1200,
    'height': 600,
    'line_width': 2.5,
    'original_color': '#ffa726'
}

# 출력 설정
OUTPUT_DIR = 'docs'
OUTPUT_FILENAME = 'index.html'
