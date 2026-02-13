"""
시각화 모듈
Plotly를 이용한 환율 그래프 생성
"""

import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
from typing import Dict, List, Optional
from datetime import datetime


class FXVisualizer:
    """환율 시각화 클래스"""
    
    def __init__(self, config: Dict):
        """
        초기화
        
        Args:
            config: 그래프 설정 딕셔너리
        """
        self.config = config
    
    def create_trend_chart(
        self,
        df: pd.DataFrame,
        currency_name: str,
        currency_symbol: str,
        ma_config: Dict,
        statistics: Dict,
        price_column: str = 'Close'
    ) -> go.Figure:
        """
        환율 트렌드 차트 생성
        
        Args:
            df: 분석된 환율 데이터프레임
            currency_name: 통화명
            currency_symbol: 통화 심볼 (예: USD/KRW)
            ma_config: 이동평균 설정
            statistics: 통계 정보
            price_column: 가격 컬럼명
            
        Returns:
            plotly.graph_objects.Figure: 생성된 차트
        """
        fig = go.Figure()
        
        # 원본 환율 데이터
        fig.add_trace(go.Scatter(
            x=df['Date'],
            y=df[price_column],
            mode='lines',
            name='환율',
            line=dict(
                color=self.config.get('original_color', '#2C3E50'),
                width=self.config.get('line_width', 2)
            ),
            hovertemplate='%{x|%Y-%m-%d}<br>환율: %{y:,.2f}원<extra></extra>'
        ))
        
        # 이동평균선들
        for ma_name, ma_info in ma_config.items():
            if ma_name in df.columns:
                fig.add_trace(go.Scatter(
                    x=df['Date'],
                    y=df[ma_name],
                    mode='lines',
                    name=ma_info['label'],
                    line=dict(
                        color=ma_info['color'],
                        width=ma_info.get('line_width', 1)  # 각 이동평균의 line_width 사용, 기본값 1
                    ),
                    hovertemplate='%{x|%Y-%m-%d}<br>' + ma_info['label'] + ': %{y:,.2f}원<extra></extra>'
                ))
        
        # Pandas 3.0 호환성을 위해 Timestamp를 Python datetime으로 변환
        max_date = statistics['max']['date']
        min_date = statistics['min']['date']
        if hasattr(max_date, 'to_pydatetime'):
            max_date = max_date.to_pydatetime()
        if hasattr(min_date, 'to_pydatetime'):
            min_date = min_date.to_pydatetime()
        
        # 최고점 표시
        fig.add_trace(go.Scatter(
            x=[max_date],
            y=[statistics['max']['price']],
            mode='markers+text',
            name='최고점',
            marker=dict(color='red', size=10, symbol='triangle-up'),
            text=[f"최고: {statistics['max']['price']:,.2f}원"],
            textposition='top center',
            hovertemplate='최고점<br>%{x|%Y-%m-%d}<br>%{y:,.2f}원<extra></extra>'
        ))
        
        # 최저점 표시
        fig.add_trace(go.Scatter(
            x=[min_date],
            y=[statistics['min']['price']],
            mode='markers+text',
            name='최저점',
            marker=dict(color='blue', size=10, symbol='triangle-down'),
            text=[f"최저: {statistics['min']['price']:,.2f}원"],
            textposition='bottom center',
            hovertemplate='최저점<br>%{x|%Y-%m-%d}<br>%{y:,.2f}원<extra></extra>'
        ))
        
        # 현재 환율 마커 추가 (수직선 대신)
        # Pandas 3.0 호환성을 위해 Timestamp를 Python datetime으로 변환
        current_date = statistics['current']['date']
        if hasattr(current_date, 'to_pydatetime'):
            current_date = current_date.to_pydatetime()
        
        fig.add_trace(go.Scatter(
            x=[current_date],
            y=[statistics['current']['price']],
            mode='markers+text',
            name='현재',
            marker=dict(color='green', size=12, symbol='diamond'),
            text=[f"현재: {statistics['current']['price']:,.2f}원"],
            textposition='middle right',
            hovertemplate='현재<br>%{x|%Y-%m-%d}<br>%{y:,.2f}원<extra></extra>'
        ))
        
        # 날짜 범위 계산 (좌우 여백 추가)
        date_range = (df['Date'].max() - df['Date'].min()).days
        padding_days = int(date_range * 0.02)  # 전체 범위의 2% 여백
        x_range_start = df['Date'].min() - pd.Timedelta(days=padding_days)
        x_range_end = df['Date'].max() + pd.Timedelta(days=padding_days)
        
        # 레이아웃 설정
        fig.update_layout(
            title=dict(
                text=f"{currency_name} 환율 트렌드 및 이동평균",
                font=dict(size=24, color='#2C3E50'),
                x=0.5,
                xanchor='center'
            ),
            xaxis=dict(
                title='',  # X축 제목 제거
                showgrid=True,
                gridwidth=1,
                gridcolor='LightGray',
                tickformat='%Y-%m-%d',
                range=[x_range_start, x_range_end]  # 좌우 여백 추가
            ),
            yaxis=dict(
                title=currency_symbol,  # 통화 심볼 표시
                showgrid=True,
                gridwidth=1,
                gridcolor='LightGray',
                tickformat=',.0f'
            ),
            hovermode='x unified',
            autosize=True,  # 자동 크기 조정
            height=self.config.get('height', 600),
            margin=dict(l=60, r=20, t=80, b=40),  # 여백 조정
            legend=dict(
                x=0.01,
                y=0.99,
                bgcolor='rgba(255, 255, 255, 0.8)',
                bordercolor='Gray',
                borderwidth=1
            ),
            plot_bgcolor='white',
            paper_bgcolor='white'
        )
        
        return fig
    
    def create_summary_html(
        self,
        statistics: Dict,
        currency_name: str
    ) -> str:
        """
        요약 정보 HTML 생성
        
        Args:
            statistics: 통계 정보
            currency_name: 통화명
            
        Returns:
            str: HTML 문자열
        """
        html = f"""
        <div style="text-align: center; margin: 18px 0; padding: 18px; background-color: #f8f9fa; border-radius: 10px;">
            <h2 style="color: #2C3E50; margin-bottom: 18px;">{currency_name} 요약 정보</h2>
            <div style="display: flex; justify-content: space-around; flex-wrap: wrap;">
                <div style="margin: 9px; padding: 13px; background-color: white; border-radius: 8px; min-width: 200px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                    <h3 style="color: #e74c3c; margin: 0;">최고 환율</h3>
                    <p style="font-size: 24px; font-weight: bold; margin: 9px 0;">{statistics['max']['price']:,.2f}원</p>
                    <p style="color: #7f8c8d; margin: 0;">{statistics['max']['formatted_date']}</p>
                </div>
                <div style="margin: 9px; padding: 13px; background-color: white; border-radius: 8px; min-width: 200px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                    <h3 style="color: #3498db; margin: 0;">최저 환율</h3>
                    <p style="font-size: 24px; font-weight: bold; margin: 9px 0;">{statistics['min']['price']:,.2f}원</p>
                    <p style="color: #7f8c8d; margin: 0;">{statistics['min']['formatted_date']}</p>
                </div>
                <div style="margin: 9px; padding: 13px; background-color: white; border-radius: 8px; min-width: 200px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                    <h3 style="color: #27ae60; margin: 0;">현재 환율</h3>
                    <p style="font-size: 24px; font-weight: bold; margin: 9px 0;">{statistics['current']['price']:,.2f}원</p>
                    <p style="color: #7f8c8d; margin: 0;">{statistics['current']['formatted_date']}</p>
                </div>
            </div>
        </div>
        """
        return html
    
    def save_to_html(
        self,
        fig: go.Figure,
        summary_html: str,
        output_path: str,
        title: str = "FX Trend Dashboard"
    ):
        """
        HTML 파일로 저장
        
        Args:
            fig: Plotly Figure 객체
            summary_html: 요약 정보 HTML
            output_path: 출력 파일 경로
            title: 페이지 제목
        """
        # 현재 시간
        generated_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # 전체 HTML 구성
        html_content = f"""
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #f5f5f5;
        }}
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            padding: 18px;
        }}
        .header {{
            text-align: center;
            padding: 36px 18px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-radius: 10px;
            margin-bottom: 27px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}
        .header h1 {{
            margin: 0;
            font-size: 36px;
        }}
        .chart-container {{
            background-color: white;
            padding: 18px;
            border-radius: 10px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            margin-bottom: 27px;
            width: 100%;
        }}
        .chart-container > div {{
            width: 100% !important;
        }}
        .footer {{
            text-align: center;
            padding: 18px;
            color: #7f8c8d;
            font-size: 14px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>💱 {title}</h1>
            <p>환율 트렌드 및 이동평균 분석 대시보드</p>
        </div>
        
        {summary_html}
        
        <div class="chart-container">
            {fig.to_html(include_plotlyjs='cdn', full_html=False, config={'responsive': True})}
        </div>
        
        <div class="footer">
            <p>데이터 출처: FinanceDataReader</p>
            <p>생성 일시: {generated_time}</p>
            <p>© 2026 FX Trend Dashboard</p>
        </div>
    </div>
</body>
</html>
"""
        
        # 파일로 저장
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"HTML 파일이 생성되었습니다: {output_path}")
