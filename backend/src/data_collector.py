"""
데이터 수집 모듈
FinanceDataReader를 이용한 환율 데이터 수집
"""

import FinanceDataReader as fdr
import pandas as pd
from datetime import datetime, timedelta
from typing import Optional


class FXDataCollector:
    """환율 데이터 수집 클래스"""
    
    def __init__(self):
        """초기화"""
        pass
    
    def fetch_exchange_rate(
        self,
        currency_code: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        period_years: int = 5
    ) -> pd.DataFrame:
        """
        환율 데이터 수집
        
        Args:
            currency_code: 통화 코드 (예: 'USD/KRW')
            start_date: 시작일 (YYYY-MM-DD), None이면 period_years 사용
            end_date: 종료일 (YYYY-MM-DD), None이면 오늘
            period_years: 조회 기간 (년 단위), start_date가 None일 때 사용
            
        Returns:
            pandas.DataFrame: 환율 데이터
        """
        try:
            # 종료일 설정
            if end_date is None:
                end_date = datetime.now().strftime('%Y-%m-%d')
            
            # 시작일 설정
            if start_date is None:
                start = datetime.now() - timedelta(days=period_years * 365)
                start_date = start.strftime('%Y-%m-%d')
            
            # 데이터 수집
            df = fdr.DataReader(currency_code, start_date, end_date)
            
            # 데이터 검증
            if df is None or df.empty:
                raise ValueError(f"No data found for {currency_code}")
            
            # 데이터 전처리
            df = self._preprocess_data(df)
            
            return df
            
        except Exception as e:
            raise Exception(f"Failed to fetch data for {currency_code}: {str(e)}")
    
    def _preprocess_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        데이터 전처리
        
        Args:
            df: 원본 데이터프레임
            
        Returns:
            pandas.DataFrame: 전처리된 데이터프레임
        """
        # 인덱스를 Date 컬럼으로 변환
        if isinstance(df.index, pd.DatetimeIndex):
            df = df.reset_index()
            # 인덱스 이름이 없으면 'Date'로 설정
            if df.columns[0] == 0 or df.columns[0] == 'index':
                df.columns = ['Date'] + list(df.columns[1:])
        
        # Date 컬럼 확인 및 생성
        if 'Date' not in df.columns:
            # 첫 번째 컬럼이 날짜 형식이면 Date로 변경
            if pd.api.types.is_datetime64_any_dtype(df.iloc[:, 0]):
                df.columns = ['Date'] + list(df.columns[1:])
            else:
                raise ValueError("Date column not found in data")
        
        # Date 컬럼을 datetime 타입으로 변환
        df['Date'] = pd.to_datetime(df['Date'])
        
        # 날짜 기준 정렬
        df = df.sort_values('Date')
        
        # 결측치 처리 (forward fill, backward fill)
        df = df.ffill().bfill()
        
        # 인덱스 리셋
        df = df.reset_index(drop=True)
        
        return df
    
    def get_multiple_currencies(
        self,
        currency_codes: list,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        period_years: int = 5
    ) -> dict:
        """
        여러 통화의 환율 데이터를 한번에 수집
        
        Args:
            currency_codes: 통화 코드 리스트
            start_date: 시작일
            end_date: 종료일
            period_years: 조회 기간
            
        Returns:
            dict: {currency_code: DataFrame} 형태의 딕셔너리
        """
        result = {}
        
        for code in currency_codes:
            try:
                df = self.fetch_exchange_rate(
                    code,
                    start_date,
                    end_date,
                    period_years
                )
                result[code] = df
            except Exception as e:
                print(f"Warning: Failed to fetch {code}: {str(e)}")
                continue
        
        return result
