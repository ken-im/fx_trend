"""
분석 모듈
이동평균 계산 및 통계 분석
"""

import pandas as pd
import numpy as np
from typing import Dict, Tuple


class FXAnalyzer:
    """환율 분석 클래스"""
    
    def __init__(self):
        """초기화"""
        pass
    
    def calculate_moving_averages(
        self,
        df: pd.DataFrame,
        ma_periods: Dict[str, int],
        price_column: str = 'Close'
    ) -> pd.DataFrame:
        """
        이동평균 계산
        
        Args:
            df: 환율 데이터프레임
            ma_periods: 이동평균 기간 딕셔너리 {'MA3M': 60, 'MA1Y': 250, ...}
            price_column: 가격 컬럼명
            
        Returns:
            pandas.DataFrame: 이동평균이 추가된 데이터프레임
        """
        df = df.copy()
        
        for ma_name, period in ma_periods.items():
            df[ma_name] = df[price_column].rolling(window=period, min_periods=1).mean()
        
        return df
    
    def get_statistics(
        self,
        df: pd.DataFrame,
        price_column: str = 'Close'
    ) -> Dict:
        """
        환율 통계 정보 계산
        
        Args:
            df: 환율 데이터프레임
            price_column: 가격 컬럼명
            
        Returns:
            dict: 통계 정보 (최고/최저/현재 환율 및 날짜)
        """
        # 최고 환율
        max_idx = df[price_column].idxmax()
        max_price = df.loc[max_idx, price_column]
        max_date = df.loc[max_idx, 'Date']
        
        # 최저 환율
        min_idx = df[price_column].idxmin()
        min_price = df.loc[min_idx, price_column]
        min_date = df.loc[min_idx, 'Date']
        
        # 현재 환율 (가장 최근 날짜)
        current_idx = df['Date'].idxmax()
        current_price = df.loc[current_idx, price_column]
        current_date = df.loc[current_idx, 'Date']
        
        return {
            'max': {
                'price': max_price,
                'date': max_date,
                'formatted_date': max_date.strftime('%Y-%m-%d')
            },
            'min': {
                'price': min_price,
                'date': min_date,
                'formatted_date': min_date.strftime('%Y-%m-%d')
            },
            'current': {
                'price': current_price,
                'date': current_date,
                'formatted_date': current_date.strftime('%Y-%m-%d')
            }
        }
    
    def calculate_change_rate(
        self,
        df: pd.DataFrame,
        price_column: str = 'Close'
    ) -> pd.DataFrame:
        """
        변동률 계산
        
        Args:
            df: 환율 데이터프레임
            price_column: 가격 컬럼명
            
        Returns:
            pandas.DataFrame: 변동률이 추가된 데이터프레임
        """
        df = df.copy()
        
        # 일별 변동률 (%)
        df['daily_change'] = df[price_column].pct_change() * 100
        
        # 누적 변동률 (첫 날 대비 %)
        first_price = df[price_column].iloc[0]
        df['cumulative_change'] = ((df[price_column] - first_price) / first_price) * 100
        
        return df
    
    def analyze_trend(
        self,
        df: pd.DataFrame,
        ma_periods: Dict[str, int],
        price_column: str = 'Close'
    ) -> pd.DataFrame:
        """
        전체 분석 수행 (이동평균 + 통계)
        
        Args:
            df: 환율 데이터프레임
            ma_periods: 이동평균 기간
            price_column: 가격 컬럼명
            
        Returns:
            pandas.DataFrame: 분석 결과가 추가된 데이터프레임
        """
        # 이동평균 계산
        df = self.calculate_moving_averages(df, ma_periods, price_column)
        
        # 변동률 계산
        df = self.calculate_change_rate(df, price_column)
        
        return df
