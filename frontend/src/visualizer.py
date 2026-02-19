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
        
        # 레이아웃 설정 (Bloomberg Terminal: 다크 배경, 대비되는 축/그리드/글자)
        fig.update_layout(
            title=dict(
                text=f"{currency_name} 환율 트렌드 및 이동평균",
                font=dict(size=20, color='#ffb86c'),
                x=0.5,
                xanchor='center'
            ),
            xaxis=dict(
                title='',
                showgrid=True,
                gridwidth=1,
                gridcolor='#484f58',
                linecolor='#586069',
                zerolinecolor='#586069',
                tickformat='%Y-%m-%d',
                range=[x_range_start, x_range_end],
                tickfont=dict(color='#e6edf3', size=11)
            ),
            yaxis=dict(
                title=currency_symbol,
                showgrid=True,
                gridwidth=1,
                gridcolor='#484f58',
                linecolor='#586069',
                zerolinecolor='#586069',
                tickformat=',.0f',
                tickfont=dict(color='#e6edf3', size=11)
            ),
            hovermode='x unified',
            autosize=True,
            height=self.config.get('height', 600),
            margin=dict(l=60, r=20, t=80, b=40),
            legend=dict(
                x=0.01,
                y=0.99,
                bgcolor='rgba(22, 27, 34, 0.9)',
                bordercolor='#484f58',
                borderwidth=1,
                font=dict(color='#e6edf3', size=11)
            ),
            plot_bgcolor='#1c2128',
            paper_bgcolor='#161b22',
            font=dict(family='Consolas, Monaco, Courier New, monospace', color='#e6edf3', size=11)
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
        <div style="text-align: center; margin: 18px 0; padding: 18px; background-color: #161b22; border: 1px solid #30363d; border-radius: 4px;">
            <div style="display: flex; justify-content: space-around; flex-wrap: wrap;">
                <div class="stat-high" style="margin: 9px; padding: 13px; border-radius: 4px; min-width: 200px;">
                    <h3 style="color: #ff6b6b; margin: 0;">최고 환율</h3>
                    <p style="font-size: 24px; font-weight: bold; margin: 9px 0; color: #ff8c00;">{statistics['max']['price']:,.2f}원</p>
                    <p style="color: #8b949e; margin: 0;">{statistics['max']['formatted_date']}</p>
                </div>
                <div class="stat-low" style="margin: 9px; padding: 13px; border-radius: 4px; min-width: 200px;">
                    <h3 style="color: #5dd0f5; margin: 0;">최저 환율</h3>
                    <p style="font-size: 24px; font-weight: bold; margin: 9px 0; color: #ff8c00;">{statistics['min']['price']:,.2f}원</p>
                    <p style="color: #8b949e; margin: 0;">{statistics['min']['formatted_date']}</p>
                </div>
                <div class="stat-current" style="margin: 9px; padding: 13px; border-radius: 4px; min-width: 200px;">
                    <h3 style="color: #7ee787; margin: 0;">현재 환율</h3>
                    <p style="font-size: 24px; font-weight: bold; margin: 9px 0; color: #ff8c00;">{statistics['current']['price']:,.2f}원</p>
                    <p style="color: #8b949e; margin: 0;">{statistics['current']['formatted_date']}</p>
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
        /* Bloomberg Terminal Style */
        body {{ font-family: 'Consolas', 'Monaco', 'Courier New', monospace; margin: 0; padding: 0; background-color: #0a0e14; color: #ff8c00; }}
        .container {{ max-width: 1400px; margin: 0 auto; padding: 18px; }}
        .header {{ text-align: center; padding: 36px 18px; background: #161b22; color: #ff8c00; border: 1px solid #30363d; border-radius: 4px; margin-bottom: 27px; }}
        .header h1 {{ margin: 0; font-size: 28px; font-weight: 600; }}
        .header p {{ color: #8b949e; margin: 8px 0 0 0; font-size: 13px; }}
        .chart-container {{ background-color: #161b22; padding: 18px; border: 1px solid #30363d; border-radius: 4px; margin-bottom: 27px; width: 100%; }}
        .chart-container > div {{ width: 100% !important; }}
        .footer {{ text-align: center; padding: 18px; color: #8b949e; font-size: 12px; }}
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
    
    def save_multi_currency_html(
        self,
        charts_data: Dict,
        output_path: str,
        title: str = "FX Trend Dashboard",
        default_currency: str = 'USD/KRW'
    ):
        """
        다중 통화 HTML 파일로 저장
        
        Args:
            charts_data: {currency_code: {'figure': fig, 'summary': html, 'info': info, 'statistics': stats}}
            output_path: 출력 파일 경로
            title: 페이지 제목
            default_currency: 기본 선택 통화
        """
        # 현재 시간
        generated_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # 통화 선택 옵션 생성
        currency_options = ""
        for currency_code, data in charts_data.items():
            selected = "selected" if currency_code == default_currency else ""
            currency_options += f'<option value="{currency_code}" {selected}>{data["info"]["name"]} ({currency_code})</option>\n'
        
        # 각 통화별 컨텐츠 생성
        currency_contents = ""
        for currency_code, data in charts_data.items():
            display_style = "block" if currency_code == default_currency else "none"
            
            # 그래프 HTML 생성
            graph_html = data['figure'].to_html(include_plotlyjs='cdn', full_html=False, config={'responsive': True})
            
            currency_contents += f"""
        <div id="currency-{currency_code}" class="currency-content" style="display: {display_style};">
            {data['summary']}
            
            <div class="chart-container">
                {graph_html}
            </div>
        </div>
"""
        
        # 전체 HTML 구성
        html_content = f"""
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        /* Bloomberg Terminal Style */
        body {{ font-family: 'Consolas', 'Monaco', 'Courier New', monospace; margin: 0; padding: 0; background-color: #0a0e14; color: #ff8c00; }}
        .container {{ max-width: 1400px; margin: 0 auto; padding: 18px; }}
        .header {{ text-align: center; padding: 36px 18px; background: #161b22; color: #ff8c00; border: 1px solid #30363d; border-radius: 4px; margin-bottom: 27px; }}
        .header h1 {{ margin: 0; font-size: 28px; font-weight: 600; letter-spacing: 0.02em; }}
        .header p {{ color: #8b949e; margin: 8px 0 0 0; font-size: 13px; }}
        .currency-selector {{ text-align: center; margin-bottom: 27px; padding: 18px; background-color: #161b22; border: 1px solid #30363d; border-radius: 4px; }}
        .currency-selector label {{ font-size: 14px; font-weight: bold; color: #ffb86c; margin-right: 12px; }}
        .currency-selector select {{ padding: 8px 16px; font-size: 14px; font-family: 'Consolas', 'Monaco', 'Courier New', monospace; border: 1px solid #30363d; border-radius: 4px; background-color: #0d1117; color: #ff8c00; cursor: pointer; min-width: 250px; }}
        .currency-selector select:hover {{ border-color: #ff8c00; }}
        .currency-selector select:focus {{ outline: none; border-color: #ff8c00; box-shadow: 0 0 0 1px #ff8c00; }}
        .currency-content {{ display: none; }}
        .chart-container {{ background-color: #161b22; padding: 18px; border: 1px solid #30363d; border-radius: 4px; margin-bottom: 27px; width: 100%; }}
        .chart-container > div {{ width: 100% !important; }}
        .footer {{ text-align: center; padding: 18px; color: #8b949e; font-size: 12px; }}
        .stat-high {{ background-color: #1a1210 !important; border: 1px solid #4a2c26 !important; }}
        .stat-low {{ background-color: #0d1522 !important; border: 1px solid #1e3a52 !important; }}
        .stat-current {{ background-color: #0d1610 !important; border: 1px solid #1e4020 !important; }}
    </style>
    <script>
        function changeCurrency() {{
            const selector = document.getElementById('currency-selector');
            const selectedCurrency = selector.value;
            
            // 모든 통화 컨텐츠 숨기기
            const allContents = document.querySelectorAll('.currency-content');
            allContents.forEach(content => {{
                content.style.display = 'none';
            }});
            
            // 선택된 통화만 표시
            const selectedContent = document.getElementById('currency-' + selectedCurrency);
            if (selectedContent) {{
                selectedContent.style.display = 'block';
                
                // Plotly 그래프 크기 재조정
                setTimeout(() => {{
                    const plotlyDivs = selectedContent.querySelectorAll('.plotly-graph-div');
                    plotlyDivs.forEach(div => {{
                        if (window.Plotly) {{
                            window.Plotly.Plots.resize(div);
                        }}
                    }});
                }}, 100);
            }}
        }}
    </script>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>💱 {title}</h1>
            <p>환율 트렌드 및 이동평균 분석 대시보드</p>
        </div>
        
        <div class="currency-selector">
            <label for="currency-selector">통화 선택:</label>
            <select id="currency-selector" onchange="changeCurrency()">
                {currency_options}
            </select>
        </div>
        
        {currency_contents}
        
        <div class="footer">
            <p>데이터 출처: FinanceDataReader</p>
            <p>생성 일시: {generated_time}</p>
            <p>© 2026 FX Trend Dashboard</p>
        </div>
    </div>
    <script>
        (function() {{
            function applyBloombergTheme() {{
                var plotlyDivs = document.querySelectorAll('.plotly-graph-div');
                var darkLayout = {{
                    paper_bgcolor: '#161b22',
                    plot_bgcolor: '#1c2128',
                    font: {{ color: '#e6edf3', family: 'Consolas, Monaco, Courier New, monospace', size: 12 }},
                    xaxis: {{ gridcolor: '#484f58', linecolor: '#586069', zerolinecolor: '#586069', tickfont: {{ color: '#e6edf3', size: 11 }}, title: {{ font: {{ color: '#ffb86c' }} }} }},
                    yaxis: {{ gridcolor: '#484f58', linecolor: '#586069', zerolinecolor: '#586069', tickfont: {{ color: '#e6edf3', size: 11 }}, title: {{ font: {{ color: '#ffb86c' }} }} }},
                    legend: {{ font: {{ color: '#e6edf3', size: 11 }}, bgcolor: 'rgba(22,27,34,0.9)', borderwidth: 1, bordercolor: '#484f58' }}
                }};
                plotlyDivs.forEach(function(div) {{
                    if (window.Plotly && div.id) Plotly.relayout(div.id, darkLayout);
                }});
            }}
            if (document.readyState === 'complete') setTimeout(applyBloombergTheme, 50);
            else window.addEventListener('load', function() {{ setTimeout(applyBloombergTheme, 50); }});
        }})();
    </script>
</body>
</html>
"""
        
        # 파일로 저장
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"다중 통화 HTML 파일이 생성되었습니다: {output_path}")
