import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# 1. Page Configuration & SEO Best Practices
st.set_page_config(
    page_title="OLED Deposition Process Analytics Dashboard",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Premium Design Aesthetics: Custom HSL Dark & Glassmorphism Theme CSS
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

/* Main App Styles */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background-color: #0d1117;
    color: #c9d1d9;
}

/* Sidebar Styling Overrides */
[data-testid="stSidebar"] {
    background-color: #161b22 !important;
    border-right: 1px solid rgba(240, 246, 252, 0.1);
}

[data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2 {
    color: #58a6ff !important;
}

/* Header & Accent styles */
h1, h2, h3, h4, h5, h6 {
    font-family: 'Inter', sans-serif;
    font-weight: 700 !important;
    color: #f0f6fc !important;
    letter-spacing: -0.02em;
}

/* Premium KPI Card System */
.kpi-container {
    display: flex;
    flex-wrap: wrap;
    gap: 16px;
    margin-bottom: 24px;
    width: 100%;
}

.kpi-card {
    background: rgba(22, 27, 34, 0.7);
    border: 1px solid rgba(240, 246, 252, 0.1);
    border-radius: 14px;
    padding: 22px 18px;
    flex: 1;
    min-width: 220px;
    text-align: center;
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.25);
    transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1);
    position: relative;
    overflow: hidden;
}

.kpi-card:hover {
    transform: translateY(-4px);
    border-color: rgba(88, 166, 255, 0.45);
    box-shadow: 0 12px 30px rgba(88, 166, 255, 0.15);
}

.kpi-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 4px;
    background: linear-gradient(90deg, #58a6ff, #1f6feb);
}

.kpi-card.yield::before {
    background: linear-gradient(90deg, #3fb950, #2ea043);
}

.kpi-card.score::before {
    background: linear-gradient(90deg, #db6d28, #f0883e);
}

.kpi-card.defect::before {
    background: linear-gradient(90deg, #ff7b72, #f85149);
}

.kpi-title {
    font-size: 0.8rem;
    font-weight: 600;
    color: #8b949e;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-bottom: 8px;
}

.kpi-value {
    font-size: 2.1rem;
    font-weight: 800;
    line-height: 1.2;
    background: linear-gradient(135deg, #ffffff 30%, #c9d1d9 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.kpi-card.yield .kpi-value {
    background: linear-gradient(135deg, #56d364 30%, #3fb950 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.kpi-card.score .kpi-value {
    background: linear-gradient(135deg, #ff9e64 30%, #db6d28 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.kpi-card.defect .kpi-value {
    background: linear-gradient(135deg, #ffa198 30%, #ff7b72 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

/* Glassmorphism Wrapper for Plotly Cards */
.chart-card {
    background: rgba(22, 27, 34, 0.45);
    border: 1px solid rgba(240, 246, 252, 0.08);
    border-radius: 16px;
    padding: 20px;
    margin-bottom: 20px;
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
    transition: border-color 0.3s ease;
}

.chart-card:hover {
    border-color: rgba(240, 246, 252, 0.15);
}

.chart-header {
    font-size: 1.1rem;
    font-weight: 600;
    color: #f0f6fc;
    margin-bottom: 15px;
    border-left: 4px solid #58a6ff;
    padding-left: 10px;
    line-height: 1.2;
}

/* Adjust streamlit padding */
.block-container {
    padding-top: 2rem !important;
    padding-bottom: 2rem !important;
}
</style>
""", unsafe_allow_html=True)


# 3. Interactive Sidebar - File Upload & Cached Data Loading Engine
st.sidebar.image("https://img.icons8.com/nolan/64/physics.png", width=64)
st.sidebar.markdown("<h2 style='margin-top: 0px;'>Data Source</h2>", unsafe_allow_html=True)

uploaded_file = st.sidebar.file_uploader(
    "Upload Process CSV Data", 
    type=["csv"], 
    help="Upload an alternative OLED process CSV file to analyze. If empty, the default local file is analyzed."
)
st.sidebar.markdown("---")

@st.cache_data
def load_data(file_obj=None):
    if file_obj is not None:
        df = pd.read_csv(file_obj)
    else:
        df = pd.read_csv("oled_deposition_xymap.csv")
    return df

# Robust Column Standardization & Verification Engine
def standardize_columns(df):
    col_mapping = {
        'chamber_id': 'chamber',
        'thickness': 'thickness_nm',
        'x_position': 'x_index',
        'y_position': 'y_index',
        'x_mm': 'x_index',
        'y_mm': 'y_index'
    }
    for old_col, new_col in col_mapping.items():
        if old_col in df.columns and new_col not in df.columns:
            df[new_col] = df[old_col]
            
    # Essential Columns Integrity Verification
    required_cols = ['chamber', 'lot_id', 'panel_id', 'x_index', 'y_index', 'thickness_nm', 'yield_score', 'pass_fail', 'defect_type']
    missing_cols = [col for col in required_cols if col not in df.columns]
    if missing_cols:
        raise ValueError(f"Missing required columns in dataset: {', '.join(missing_cols)}")
    return df

try:
    if uploaded_file is not None:
        df_raw = standardize_columns(load_data(uploaded_file))
        st.sidebar.success("📊 Custom file loaded & verified!")
    else:
        df_raw = standardize_columns(load_data(None))
except Exception as e:
    st.sidebar.error(f"⚠️ Validation Failure: {e}")
    st.error(f"❌ The loaded dataset does not match the dashboard requirements: {e}")
    st.stop()


# 4. Interactive Sidebar Filtration Panel
st.sidebar.markdown("<h2>Process Control</h2>", unsafe_allow_html=True)

# Filter 1: Chamber ID Selection (using standardized 'chamber' column)
all_chambers = sorted(df_raw['chamber'].unique())
selected_chambers = st.sidebar.multiselect(
    "Select Chamber",
    options=all_chambers,
    default=all_chambers,
    help="Filter data by manufacturing deposition chamber."
)

# Filter 2: Lot ID Selection
all_lots = sorted(df_raw['lot_id'].unique())
selected_lots = st.sidebar.multiselect(
    "Select Lot ID",
    options=all_lots,
    default=all_lots,
    help="Filter data by manufacturing material batch/lot."
)

# Filtering implementation
filtered_df = df_raw[
    (df_raw['chamber'].isin(selected_chambers)) &
    (df_raw['lot_id'].isin(selected_lots))
]


# 5. Header Section
st.markdown("<h1 style='text-align: left; margin-bottom: 5px; background: linear-gradient(to right, #58a6ff, #56d364); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>OLED Deposition Process Insights</h1>", unsafe_allow_html=True)
st.markdown("<p style='color: #8b949e; font-size: 0.95rem; margin-top: 0px; margin-bottom: 25px;'>Real-time deposition engineering monitoring and spatial anomaly mapping system.</p>", unsafe_allow_html=True)

# Safety check for empty filtered dataframe
if len(filtered_df) == 0:
    st.warning("⚠️ No data matches the selected filters. Please expand your selections in the sidebar.")
    st.stop()


# 6. Dynamic KPI Metrics Calculations
# 수율 정의 (pass_fail이 'pass'인 비율 * 100) -> yield_score 평균을 절대 수율로 쓰지 않음!
total_datapoints = len(filtered_df)
pass_points = len(filtered_df[filtered_df['pass_fail'] == 'pass'])
fail_points = len(filtered_df[filtered_df['pass_fail'] == 'fail'])
yield_percentage = (pass_points / total_datapoints) * 100 if total_datapoints > 0 else 0
average_yield_score = filtered_df['yield_score'].mean()

# Render KPI UI
kpi_html = f"""
<div class="kpi-container">
    <div class="kpi-card">
        <div class="kpi-title">Total Datapoints</div>
        <div class="kpi-value">{total_datapoints:,}</div>
    </div>
    <div class="kpi-card yield">
        <div class="kpi-title">Total Yield (%)</div>
        <div class="kpi-value">{yield_percentage:.2f}%</div>
    </div>
    <div class="kpi-card score">
        <div class="kpi-title">Avg Quality Score</div>
        <div class="kpi-value">{average_yield_score:.2f}</div>
    </div>
    <div class="kpi-card defect">
        <div class="kpi-title">Defect Count</div>
        <div class="kpi-value">{fail_points:,}</div>
    </div>
</div>
"""
st.markdown(kpi_html, unsafe_allow_html=True)


# 7. Chart Layout Configurations & Templates
plotly_layout_defaults = dict(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font=dict(family="Inter, sans-serif", color="#c9d1d9"),
    margin=dict(t=30, b=40, l=40, r=30),
    hoverlabel=dict(
        bgcolor="#161b22",
        bordercolor="rgba(240,246,252,0.1)",
        font_size=12,
        font_family="Inter, sans-serif"
    )
)

plotly_grid_styling = dict(
    showgrid=True,
    gridwidth=1,
    gridcolor="rgba(240,246,252,0.06)",
    zeroline=False
)


# ==========================================
# ROW 1: Yield by Chamber & Thickness Boxplot
# ==========================================
col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.markdown('<div class="chart-header">Chamber-specific Yield Performance (pass_fail ratio)</div>', unsafe_allow_html=True)
    
    # Calculate yield per chamber dynamically
    chamber_stats = filtered_df.groupby('chamber').agg(
        total=('pass_fail', 'count'),
        passed=('pass_fail', lambda x: (x == 'pass').sum())
    ).reset_index()
    chamber_stats['yield_pct'] = (chamber_stats['passed'] / chamber_stats['total']) * 100
    
    fig_yield = go.Figure()
    
    # Elegant custom green gradient bars
    fig_yield.add_trace(go.Bar(
        x=chamber_stats['chamber'],
        y=chamber_stats['yield_pct'],
        text=chamber_stats['yield_pct'].round(2).astype(str) + '%',
        textposition='outside',
        marker=dict(
            color=chamber_stats['yield_pct'],
            colorscale=[[0, '#2ea043'], [1, '#56d364']],
            line=dict(width=1.5, color='#3fb950')
        ),
        hovertemplate="<b>Chamber: %{x}</b><br>Yield: %{y:.2f}%<br>Total Points: %{customdata[0]:,}<br>Passed Points: %{customdata[1]:,}<extra></extra>",
        customdata=np.stack((chamber_stats['total'], chamber_stats['passed']), axis=-1)
    ))
    
    # Update layout to scale Y-axis strictly 70% to 100%
    fig_yield.update_layout(
        template="plotly_dark",
        height=350,
        yaxis=dict(range=[70, 100], **plotly_grid_styling, ticksuffix="%"),
        xaxis=dict(showgrid=False),
        **plotly_layout_defaults
    )
    
    st.plotly_chart(fig_yield, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.markdown('<div class="chart-header">Chamber-specific Thickness Distribution (nm)</div>', unsafe_allow_html=True)
    
    # Box plot showing thickness_nm distribution across chambers
    # Using specific premium color maps
    chamber_colors = {'C1': '#58a6ff', 'C2': '#ff7b72', 'C3': '#ff9e64', 'C4': '#d8b4fe'}
    
    fig_box = go.Figure()
    for ch in sorted(filtered_df['chamber'].unique()):
        ch_df = filtered_df[filtered_df['chamber'] == ch]
        fig_box.add_trace(go.Box(
            y=ch_df['thickness_nm'],
            name=ch,
            marker_color=chamber_colors.get(ch, '#58a6ff'),
            boxpoints='outliers',
            jitter=0.2,
            whiskerwidth=0.8,
            line=dict(width=1.8),
            fillcolor='rgba(22, 27, 34, 0.45)'
        ))
        
    fig_box.update_layout(
        template="plotly_dark",
        height=350,
        yaxis=dict(**plotly_grid_styling, title="Thickness (nm)"),
        xaxis=dict(showgrid=False),
        showlegend=False,
        **plotly_layout_defaults
    )
    
    st.plotly_chart(fig_box, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)


# ==========================================
# ROW 2: Spatial Defect Map & Defect Pareto
# ==========================================
col3, col4 = st.columns(2)

with col3:
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.markdown('<div class="chart-header">X-Y Spatial Defect Analysis Map</div>', unsafe_allow_html=True)
    
    fig_map = go.Figure()
    
    # 1. Plot passed coordinates as a background (faint style)
    pass_df = filtered_df[filtered_df['pass_fail'] == 'pass']
    if len(pass_df) > 0:
        fig_map.add_trace(go.Scatter(
            x=pass_df['x_index'],
            y=pass_df['y_index'],
            mode='markers',
            name='Pass',
            marker=dict(
                size=3.5,
                color='rgba(88, 166, 255, 0.12)', # Faint, translucent slate blue
                line=dict(width=0)
            ),
            customdata=np.stack((
                pass_df['panel_id'],
                pass_df['lot_id'],
                pass_df['thickness_nm'],
                pass_df['yield_score']
            ), axis=-1),
            hovertemplate=(
                "<b>🟢 Pass Point</b><br>" +
                "X-Y Index: (%{x}, %{y})<br>" +
                "Panel ID: %{customdata[0]}<br>" +
                "Lot ID: %{customdata[1]}<br>" +
                "Thickness: %{customdata[2]:.2f} nm<br>" +
                "Quality Score: %{customdata[3]:.2f}<extra></extra>"
            )
        ))
        
    # 2. Plot failed coordinates overlayed in vibrant, bold red
    fail_df = filtered_df[filtered_df['pass_fail'] == 'fail']
    if len(fail_df) > 0:
        fig_map.add_trace(go.Scatter(
            x=fail_df['x_index'],
            y=fail_df['y_index'],
            mode='markers',
            name='Fail',
            marker=dict(
                size=7,
                color='#ff7b72', # Vibrant neon rose/red
                opacity=0.95,
                line=dict(width=1.2, color='#f85149')
            ),
            customdata=np.stack((
                fail_df['panel_id'],
                fail_df['lot_id'],
                fail_df['defect_type'],
                fail_df['thickness_nm'],
                fail_df['yield_score']
            ), axis=-1),
            hovertemplate=(
                "<b>🚨 Defect Detected</b><br>" +
                "X-Y Index: (%{x}, %{y})<br>" +
                "Panel ID: %{customdata[0]}<br>" +
                "Lot ID: %{customdata[1]}<br>" +
                "Defect: <span style='color:#ff7b72'><b>%{customdata[2]}</b></span><br>" +
                "Thickness: %{customdata[3]:.2f} nm<br>" +
                "Quality Score: %{customdata[4]:.2f}<extra></extra>"
            )
        ))
        
    fig_map.update_layout(
        template="plotly_dark",
        height=380,
        xaxis=dict(**plotly_grid_styling, title="X Index (0 ~ 95)"),
        yaxis=dict(**plotly_grid_styling, title="Y Index (0 ~ 63)"),
        showlegend=True,
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01,
            bgcolor="rgba(13, 17, 23, 0.7)",
            bordercolor="rgba(240, 246, 252, 0.1)",
            borderwidth=1
        ),
        **plotly_layout_defaults
    )
    
    st.plotly_chart(fig_map, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col4:
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.markdown('<div class="chart-header">Defect Type Pareto Chart (Excludes "None")</div>', unsafe_allow_html=True)
    
    # Process data to compile authentic defect statistics
    defects_only = filtered_df[filtered_df['defect_type'] != 'none']
    
    if len(defects_only) == 0:
        # Graceful handling if no defects are present in filtered subset
        fig_pareto = go.Figure()
        fig_pareto.add_annotation(
            text="🎉 No defects found in the selected range!",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=15, color="#8b949e")
        )
        fig_pareto.update_layout(
            template="plotly_dark",
            height=380,
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            **plotly_layout_defaults
        )
    else:
        defect_counts = defects_only['defect_type'].value_counts().reset_index()
        defect_counts.columns = ['defect_type', 'count']
        defect_counts = defect_counts.sort_values(by='count', ascending=False)
        total_defects = defect_counts['count'].sum()
        defect_counts['cumulative_pct'] = (defect_counts['count'].cumsum() / total_defects) * 100
        
        # Dual axis subplot for Pareto Chart
        fig_pareto = make_subplots(specs=[[{"secondary_y": True}]])
        
        # Left Y-Axis: Bar Chart for Counts
        fig_pareto.add_trace(
            go.Bar(
                x=defect_counts['defect_type'],
                y=defect_counts['count'],
                name="Defect Count",
                marker=dict(
                    color='rgba(255, 123, 114, 0.8)',
                    line=dict(color='#ff7b72', width=1.5)
                ),
                hovertemplate="Defect: %{x}<br>Count: %{y}<extra></extra>"
            ),
            secondary_y=False
        )
        
        # Right Y-Axis: Line Chart for Cumulative %
        fig_pareto.add_trace(
            go.Scatter(
                x=defect_counts['defect_type'],
                y=defect_counts['cumulative_pct'],
                name="Cumulative %",
                mode="lines+markers",
                marker=dict(size=6, color="#f0883e"),
                line=dict(width=2, color="#db6d28", dash="solid"),
                hovertemplate="Cumulative: %{y:.2f}%<extra></extra>"
            ),
            secondary_y=True
        )
        
        # 80% Threshold Guide Line
        fig_pareto.add_shape(
            type="line",
            x0=-0.5,
            x1=len(defect_counts) - 0.5,
            y0=80,
            y1=80,
            line=dict(color="rgba(240, 246, 252, 0.3)", width=1.5, dash="dash"),
            secondary_y=True
        )
        
        # Add annotation for 80% Pareto line
        fig_pareto.add_annotation(
            x=len(defect_counts) - 1.2,
            y=81,
            text="80% Pareto Cut-off",
            showarrow=False,
            font=dict(color="rgba(240, 246, 252, 0.5)", size=9),
            secondary_y=True
        )
        
        fig_pareto.update_layout(
            template="plotly_dark",
            height=380,
            showlegend=False,
            xaxis=dict(showgrid=False),
            yaxis=dict(title="Defect Count", **plotly_grid_styling),
            yaxis2=dict(
                title="Cumulative Percentage",
                range=[0, 105],
                showgrid=False,
                ticksuffix="%"
            ),
            **plotly_layout_defaults
        )
        
    st.plotly_chart(fig_pareto, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)


# ==========================================
# ROW 3: Yield Score Distribution (Quality)
# ==========================================
st.markdown('<div class="chart-card">', unsafe_allow_html=True)
st.markdown('<div class="chart-header">Quality Index (yield_score) Distribution & Process Control Threshold</div>', unsafe_allow_html=True)

fig_hist = go.Figure()

# Plot beautiful quality score histogram
fig_hist.add_trace(go.Histogram(
    x=filtered_df['yield_score'],
    name="Quality Score",
    nbinsx=100,
    marker=dict(
        color='#58a6ff',
        line=dict(width=0.5, color='#0d1117')
    ),
    hovertemplate="Score Range: %{x}<br>Count: %{y}<extra></extra>"
))

# Draw the 91.5 Control Threshold line
fig_hist.add_vline(
    x=91.5,
    line_width=2.5,
    line_dash="dash",
    line_color="#ff7b72"
)

# Text Label next to the control line
fig_hist.add_annotation(
    x=91.5,
    y=0.93,
    yref="paper",
    text="Quality Limit (91.5)",
    showarrow=True,
    arrowhead=1,
    ax=80,
    ay=0,
    font=dict(color="#ff7b72", size=11, family="Inter, sans-serif"),
    bgcolor="#161b22",
    bordercolor="#ff7b72",
    borderwidth=1,
    borderpad=4
)

fig_hist.update_layout(
    template="plotly_dark",
    height=320,
    xaxis=dict(title="yield_score (Quality Index)", **plotly_grid_styling),
    yaxis=dict(title="Measurement Points Count", **plotly_grid_styling),
    **plotly_layout_defaults
)

st.plotly_chart(fig_hist, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)
