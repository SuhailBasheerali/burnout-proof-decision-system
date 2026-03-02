import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from typing import List, Dict
import json

# ═══════════════════════════════════════════════════════════════════════════════
# CONFIG & SETUP
# ═══════════════════════════════════════════════════════════════════════════════

st.set_page_config(
    page_title="Decision Companion",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern styling
st.markdown("""
<style>
    * {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
    }
    
    .title-section {
        text-align: center;
        color: white;
        margin-bottom: 3rem;
    }
    
    .card-container {
        background: white;
        border-radius: 12px;
        padding: 2rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        margin-bottom: 1.5rem;
    }
    
    .metric-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        text-align: center;
    }
    
    .zone-execute {
        background: #10b981;
        color: white;
    }
    
    .zone-caution {
        background: #f59e0b;
        color: white;
    }
    
    .zone-avoid {
        background: #ef4444;
        color: white;
    }
    
    h1 {
        color: white;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
    }
    
    .stSlider > div > div > div {
        color: #667eea;
    }
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# BACKEND CONFIG
# ═══════════════════════════════════════════════════════════════════════════════

BACKEND_URL = "http://localhost:8000"

# ═══════════════════════════════════════════════════════════════════════════════
# SESSION STATE INITIALIZATION
# ═══════════════════════════════════════════════════════════════════════════════

if "current_phase" not in st.session_state:
    st.session_state.current_phase = 1  # 1: Entry, 2: Input, 3: Analysis, 4-5: Results

if "decision_topic" not in st.session_state:
    st.session_state.decision_topic = ""

if "num_options" not in st.session_state:
    st.session_state.num_options = 2

if "options_data" not in st.session_state:
    st.session_state.options_data = {}

if "analysis_results" not in st.session_state:
    st.session_state.analysis_results = None

if "ai_reflection" not in st.session_state:
    st.session_state.ai_reflection = None

# ═══════════════════════════════════════════════════════════════════════════════
# HELPER FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════

def get_zone_color(zone: str) -> str:
    """Return color based on zone classification"""
    zone_colors = {
        "EXECUTE_FULLY": "green",
        "TIME_BOX": "orange",
        "LIGHT_RECOVERY": "blue",
        "STEADY_EXECUTION": "blue",
        "AVOID": "red"
    }
    return zone_colors.get(zone, "gray")

def get_risk_color(risk: str) -> str:
    """Return color based on risk level"""
    risk_colors = {
        "LOW": "green",
        "MODERATE": "orange",
        "HIGH": "red",
        "SEVERE_BURNOUT_RISK": "darkred"
    }
    return risk_colors.get(risk, "gray")

def create_gauge_chart(value: float, max_value: float, title: str, color: str = "lightblue") -> go.Figure:
    """Create a gauge chart for score visualization"""
    fig = go.Figure(data=[go.Indicator(
        mode="gauge+number",
        value=value,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': title},
        gauge={
            'axis': {'range': [0, max_value]},
            'bar': {'color': color},
            'steps': [
                {'range': [0, max_value * 0.33], 'color': "#fee"},
                {'range': [max_value * 0.33, max_value * 0.66], 'color': "#ffc"},
                {'range': [max_value * 0.66, max_value], 'color': "#cfc"}
            ]
        }
    )])
    fig.update_layout(height=300, font={'size': 12}, margin=dict(l=20, r=20, t=60, b=20))
    return fig

def generate_decision_clarification(growth: float, sustainability: float, zone: str, risk_level: str) -> str:
    """Generate a brief explanatory statement about what the scores mean for decision-making"""
    
    if zone == "EXECUTE_FULLY":
        return (
            "✅ **STRONG CHOICE** - This option offers solid growth opportunities with manageable sustainability. "
            "It balances advancement with realistic workload and long-term feasibility. "
            "Recommended if you want meaningful progress without excessive burnout risk."
        )
    elif zone == "TIME_BOX":
        return (
            "⏰ **LIMITED-TIME OPPORTUNITY** - High growth potential but requires careful time management. "
            "Best suited for short-term intensive work that you can sustain for a defined period. "
            "Plan recovery time afterward and ensure other commitments are flexible."
        )
    elif zone == "LIGHT_RECOVERY":
        return (
            "😌 **RECOVERY OPTION** - Lower growth but high sustainability. Choose this if you need breathing room "
            "to recharge from intense periods, or to maintain balance while pursuing other goals. "
            "Good for consolidating skills rather than rapid advancement."
        )
    elif zone == "STEADY_EXECUTION":
        return (
            "🔄 **STEADY-STATE OPTION** - Moderate growth with strong sustainability. "
            "This is a reliable choice for consistent progress without overcommitment. "
            "Ideal if you prefer stable advancement over high-risk opportunities."
        )
    else:  # AVOID
        return (
            "🛑 **LOW VALUE** - This option underperforms across both growth and sustainability dimensions. "
            "Limited academic benefit and manageable difficulty. Reconsider fundamentally or deprioritize "
            "compared to other options."
        )

def call_backend(options: List[Dict]) -> Dict:
    """Call the backend API with options data"""
    try:
        payload = {
            "options": options
        }
        
        response = requests.post(
            f"{BACKEND_URL}/decision/compare",
            json=payload,
            timeout=10
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.ConnectionError:
        st.error("❌ Cannot connect to backend. Make sure the backend is running on http://localhost:8000")
        return None
    except requests.exceptions.RequestException as e:
        st.error(f"❌ Backend error: {str(e)}")
        return None

def call_reflection(options: List[Dict], comparison_result: Dict) -> Dict:
    """Call the AI reflection API to get Absolem's wisdom"""
    try:
        payload = {
            "options": options,
            "comparison_result": comparison_result
        }
        
        response = requests.post(
            f"{BACKEND_URL}/decision/reflect",
            json=payload,
            timeout=15
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.ConnectionError:
        st.error("❌ Cannot connect to AI reflection layer. Backend may be offline.")
        return None
    except requests.exceptions.HTTPError as e:
        # Log full error response for debugging
        try:
            error_detail = e.response.json() if e.response.text else str(e)
            st.warning(f"⚠️ AI reflection error: {error_detail}. Using default wisdom.")
        except:
            st.warning(f"⚠️ AI reflection unavailable ({e.response.status_code}). Using default wisdom.")
        return None
    except requests.exceptions.RequestException as e:
        st.warning(f"⚠️ AI reflection unavailable: {str(e)}. Using default wisdom.")
        return None

def format_option_for_api(title: str, productivity: float, impact: int, 
                          importance: float, feasibility: int) -> Dict:
    """Format option data for API"""
    return {
        "title": title,
        "growth_criteria": [
            {
                "weight": productivity,
                "impact": impact
            }
        ],
        "sustainability_criteria": [
            {
                "weight": importance,
                "impact": feasibility
            }
        ]
    }

# ═══════════════════════════════════════════════════════════════════════════════
# PHASE 1: DECISION ENTRY
# ═══════════════════════════════════════════════════════════════════════════════

def render_phase_1():
    """Render decision entry phase"""
    st.markdown("""
    <div class="title-section">
        <h1>ABSOLEM</h1>
        <p style="font-size: 1.2em; margin-top: 1rem;">Optimizing Academic Growth with Mental Bandwidth</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1], gap="large")
    
    with col1:
        st.markdown("### 🎯 Target Goal")
        topic = st.text_input(
            "Enter your decision topic",
            placeholder="e.g., Course Selection for Next Semester",
            help="What academic decision are you trying to make?"
        )
        st.session_state.decision_topic = topic
    
    with col2:
        st.markdown("### 🔢 Number of Paths?")
        num_opts = st.selectbox(
            "Select number of options",
            options=list(range(1, 6)),
            index=1,
            help="Compare 1-5 options (recommended: 2-3 for best analysis)"
        )
        st.session_state.num_options = num_opts
        
        # Guidance based on selection
        if num_opts == 2:
            st.info("ℹ️ Perfect! 2 options provide clear, focused comparison.")
        elif num_opts == 3:
            st.info("ℹ️ Excellent! 3 options give flexibility with manageable analysis.")
        elif num_opts >= 4:
            st.warning(f"⚠️ {num_opts} options will take longer to analyze. Consider narrowing to top 3 if possible.")
    
    st.divider()
    
    # Display what will happen next
    st.markdown("""
    ### How We Solve It
    
    1️⃣ **Identify Traits** - For each option, rate 4 metrics (5 seconds per option)
    2️⃣ **Balance Audit** - Our system analyzes growth vs. sustainability
    3️⃣ **Get Clarity** - Get ranked recommendations with detailed insights
    """)
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("🚀 Start Comparing Options", width='stretch', type="primary"):
            if not st.session_state.decision_topic.strip():
                st.error("⚠️ Please enter a decision topic first!")
            else:
                st.session_state.current_phase = 2
                st.rerun()

# ═══════════════════════════════════════════════════════════════════════════════
# PHASE 2: OPTION INPUT
# ═══════════════════════════════════════════════════════════════════════════════

def render_phase_2():
    """Render option input phase"""
    st.markdown(f"""
    <div class="title-section">
        <h1>📋 Comparing {st.session_state.num_options} Options</h1>
        <p style="font-size: 1.1em; margin-top: 0.5rem;">Decision: {st.session_state.decision_topic}</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### Options to Compare")
    
    # First, get all option titles
    option_titles = []
    title_cols = st.columns(st.session_state.num_options)
    
    for i in range(st.session_state.num_options):
        with title_cols[i]:
            title = st.text_input(
                "Option title",
                key=f"title_{i}",
                placeholder=f"Option {i+1}",
                help=f"Name for option {i+1}"
            )
            option_titles.append(title)
    
    st.divider()
    
    # Then, get metrics for each option
    for opt_idx in range(st.session_state.num_options):
        st.markdown(f"### Option {opt_idx + 1}: {option_titles[opt_idx] or f'Option {opt_idx+1}'}")
        
        col1, col2 = st.columns(2, gap="large")
        
        # Growth Criteria
        with col1:
            st.markdown("#### 🚀 GROWTH CRITERIA")
            st.markdown("*How much academic advancement & skill gain?*")
            
            productivity = st.slider(
                "📊 Task Volume (How much work is needed?)",
                min_value=1.0,
                max_value=10.0,
                value=5.0,
                step=0.5,
                key=f"productivity_{opt_idx}",
                help="1 = Minimal effort, 10 = Extreme time commitment"
            )
            
            impact = st.slider(
                "⚡ Impact (How much academic/career gain?)",
                min_value=1,
                max_value=10,
                value=5,
                step=1,
                key=f"impact_{opt_idx}",
                help="1 = Minimal benefit, 10 = Exceptional game-changer"
            )
        
        # Sustainability Criteria
        with col2:
            st.markdown("#### 😌 SUSTAINABILITY CRITERIA")
            st.markdown("*Can you realistically manage this long-term?*")
            
            importance = st.slider(
                "💪 Importance (How important for your goals?)",
                min_value=1.0,
                max_value=10.0,
                value=5.0,
                step=0.5,
                key=f"importance_{opt_idx}",
                help="1 = Not very important, 10 = Critical for career"
            )
            
            feasibility = st.slider(
                "✅ Feasibility (Can you realistically do it?)",
                min_value=1,
                max_value=10,
                value=5,
                step=1,
                key=f"feasibility_{opt_idx}",
                help="1 = Challenging, 10 = Very feasible"
            )
        
        # Store in session state
        st.session_state.options_data[opt_idx] = {
            "title": option_titles[opt_idx],
            "productivity": productivity,
            "impact": impact,
            "importance": importance,
            "feasibility": feasibility
        }
        
        # Calculate quick stats (but don't show yet)
        growth_score = (productivity * impact) / 10
        sust_score = (importance * feasibility) / 10
        balance = abs(growth_score - sust_score)
        
        # View stats button
        if st.button("📊 View Stats", key=f"view_stats_{opt_idx}", width='stretch'):
            if f"show_stats_{opt_idx}" not in st.session_state:
                st.session_state[f"show_stats_{opt_idx}"] = False
            st.session_state[f"show_stats_{opt_idx}"] = not st.session_state[f"show_stats_{opt_idx}"]
        
        # Show stats only if button is clicked
        if st.session_state.get(f"show_stats_{opt_idx}", False):
            stats_col1, stats_col2, stats_col3 = st.columns(3)
            with stats_col1:
                st.metric("Growth Score", f"{growth_score:.1f}/10")
            with stats_col2:
                st.metric("Sustainability Score", f"{sust_score:.1f}/10")
            with stats_col3:
                st.metric("Balance Gap", f"{balance:.1f}")
        
        st.divider()
    
    # Navigation buttons
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        if st.button("← Back", width='stretch'):
            st.session_state.current_phase = 1
            st.rerun()
    
    with col3:
        if st.button("Analyze & Compare →", width='stretch', type="primary"):
            # Validate all options have titles
            if any(not title.strip() for title in option_titles):
                st.error("⚠️ Please enter titles for all options!")
            # Validate no metric is 0
            elif any(
                st.session_state.options_data[i]["productivity"] == 0 or
                st.session_state.options_data[i]["impact"] == 0 or
                st.session_state.options_data[i]["importance"] == 0 or
                st.session_state.options_data[i]["feasibility"] == 0
                for i in range(st.session_state.num_options)
            ):
                st.error("⚠️ All metrics must be at least 1 (cannot be 0). Please adjust your ratings!")
            else:
                # Prepare API payload
                options = [
                    format_option_for_api(
                        st.session_state.options_data[i]["title"],
                        st.session_state.options_data[i]["productivity"],
                        st.session_state.options_data[i]["impact"],
                        st.session_state.options_data[i]["importance"],
                        st.session_state.options_data[i]["feasibility"]
                    )
                    for i in range(st.session_state.num_options)
                ]
                
                # Call backend
                with st.spinner("🔄 Analyzing your decision..."):
                    results = call_backend(options)
                
                if results:
                    st.session_state.analysis_results = results
                    st.session_state.current_phase = 3
                    st.rerun()

# ═══════════════════════════════════════════════════════════════════════════════
# PHASE 3: ANALYSIS RESULTS
# ═══════════════════════════════════════════════════════════════════════════════

def render_phase_3():
    """Render analysis results dashboard"""
    if not st.session_state.analysis_results:
        st.error("No analysis results available")
        return
    
    results = st.session_state.analysis_results
    evaluations = results["evaluations"]
    recommended = results["recommended_option"]
    decision_status = results["decision_status"]
    
    st.markdown("""
    <div class="title-section">
        <h1> Decision Analysis </h1>
    </div>
    """, unsafe_allow_html=True)

    
    # ═══════════════════════════════════════════════════════════════════════════
    # RECOMMENDATION CARD - HANDLES ALL SCENARIOS
    # ═══════════════════════════════════════════════════════════════════════════
    
    if decision_status == "CLOSE_COMPETITION":
        # Scenario 1: Competitive Options - Show top 2 equally
        st.markdown("### 🏆 COMPETITIVE OPTIONS - NO CLEAR WINNER")
        st.info("⏳ **Top options have comparable scores.** Both are strong choices - consider non-numerical factors.")
        
        top_two = evaluations[:2]
        col1, col2 = st.columns(2)
        
        with col1:
            eval1 = top_two[0]
            st.markdown(f"""
            #### 📌 Option 1: {eval1['title']}
            - **Composite Score:** {eval1['composite_score']}/100
            - **Stability:** {eval1['stability_level']}
            - **Zone:** {eval1['zone']}
            - **Risk:** {eval1['risk_level']}
            """)
        
        with col2:
            eval2 = top_two[1]
            st.markdown(f"""
            #### 📌 Option 2: {eval2['title']}
            - **Composite Score:** {eval2['composite_score']}/100
            - **Stability:** {eval2['stability_level']}
            - **Zone:** {eval2['zone']}
            - **Risk:** {eval2['risk_level']}
            """)
        
        st.warning("💡 **Decision Guidance:**\n- Choose based on personal preference, time availability, or team fit\n- Both options are academically sound\n- Review detailed breakdowns below to help decide")
    
    elif decision_status == "ALL_OPTIONS_POOR_FIT":
        # Scenario 2: No Viable Option - All below threshold
        st.markdown("### ❌ NO VIABLE OPTIONS")
        st.error(
            "**All options score below the viability threshold (40/100).**\n\n"
            "None of these options are structurally sound as-is. This suggests your problem needs redesign, not just better execution.\n\n"
            "**Consider:**\n"
            "- Are your criteria too strict? (Unrealistic expectations)\n"
            "- Do better options exist outside this set?\n"
            "- Should you reframe the decision entirely?\n"
            "- Do your weights align with your actual priorities?"
        )
    
    else:
        # Scenario 3: Clear Winner or Single Option
        recommended_eval = next((e for e in evaluations if e["title"] == recommended), None)
        
        if recommended_eval:
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown(f"""
                ### 🥇 RECOMMENDED: {recommended}
                
                **Composite Score:** {recommended_eval['composite_score']}/100  
                **Decision Status:** {decision_status.replace('_', ' ')}  
                **Risk Level:** {recommended_eval['risk_level']}
                """)
            
            with col2:
                # Color-coded zone badge
                zone = recommended_eval['zone']
                color_map = {
                    "EXECUTE_FULLY": "🟢",
                    "TIME_BOX": "🟡",
                    "LIGHT_RECOVERY": "🔵",
                    "STEADY_EXECUTION": "🔵",
                    "AVOID": "🔴"
                }
                zone_emoji = color_map.get(zone, "⚪")
                st.markdown(f"<div style='text-align: center; font-size: 3em;'>{zone_emoji}</div>", unsafe_allow_html=True)
                st.markdown(f"<div style='text-align: center; font-weight: bold;'>{zone}</div>", unsafe_allow_html=True)
            
            # Scenario 4: Highlight if top option is fragile
            if recommended_eval['stability_level'] == "FRAGILE":
                st.warning("⚠️ **FRAGILE DECISION:** High sensitivity detected. Scores may vary with slight changes.\nConsider reviewing alternatives or validating your ratings.")
    
    st.divider()
    
    # ═══════════════════════════════════════════════════════════════════════════
    # RANKING TABLE
    # ═══════════════════════════════════════════════════════════════════════════
    
    st.markdown("### 📊 Ranking (Best to Worst)")
    
    ranking_data = []
    for idx, eval in enumerate(evaluations, 1):
        ranking_data.append({
            "Rank": f"{'🥇' if idx == 1 else '🥈' if idx == 2 else '🥉' if idx == 3 else f'{idx}️⃣'}",
            "Option": eval["title"],
            "Growth": f"{eval['growth_score']:.0f}/100",
            "Sustainability": f"{eval['sustainability_score']:.0f}/100",
            "Balance": "✅" if eval["tension_index"] <= 15 else "⚠️" if eval["tension_index"] <= 30 else "🔴",
            "Risk": eval["risk_level"],
            "Score": f"{eval['composite_score']:.1f}"
        })
    
    df_ranking = pd.DataFrame(ranking_data)
    st.dataframe(df_ranking, width='stretch', hide_index=True)
    
    st.divider()
    
    # ═══════════════════════════════════════════════════════════════════════════
    # DETAILED METRICS FOR EACH OPTION
    # ═══════════════════════════════════════════════════════════════════════════
    
    st.markdown("### 📈 Detailed Breakdown")
    
    tabs = st.tabs([eval["title"] for eval in evaluations])
    
    for tab_idx, (tab, eval) in enumerate(zip(tabs, evaluations)):
        with tab:
            # Decision Clarification
            clarification = generate_decision_clarification(
                eval["growth_score"],
                eval["sustainability_score"],
                eval["zone"],
                eval["risk_level"]
            )
            st.markdown(f"### 💡 What This Means For Your Decision\n{clarification}")
            st.divider()
            
            col1, col2, col3 = st.columns(3)
            
            # Growth Score
            with col1:
                fig_growth = create_gauge_chart(
                    eval["growth_score"],
                    100,
                    "Growth Score",
                    color="#667eea"
                )
                st.plotly_chart(fig_growth, width='stretch', key=f"growth_{tab_idx}")
            
            # Sustainability Score
            with col2:
                fig_sust = create_gauge_chart(
                    eval["sustainability_score"],
                    100,
                    "Sustainability",
                    color="#10b981"
                )
                st.plotly_chart(fig_sust, width='stretch', key=f"sust_{tab_idx}")
            
            # Tension Index
            with col3:
                fig_tension = create_gauge_chart(
                    eval["tension_index"],
                    100,
                    "Tension Index",
                    color="#f59e0b"
                )
                st.plotly_chart(fig_tension, width='stretch', key=f"tension_{tab_idx}")
            
            st.divider()
            
            # Detailed info
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### 🎯 Classification")
                st.write(f"**Zone:** {eval['zone']}")
                st.write(f"**Zone Reason:** {eval['zone_reason']}")
                st.write(f"**Tension Severity:** {eval['tension_severity']}")
                st.write(f"**Risk Level:** {eval['risk_level']}")
            
            with col2:
                st.markdown("#### 🔒 Stability & Reliability")
                st.write(f"**Sensitivity Range:** {eval['sensitivity_range']} pts")
                st.write(f"**Stability Level:** {eval['stability_level']}")
                st.metric("Composite Score", f"{eval['composite_score']:.1f}/100")
            
            st.divider()
            
            # Detailed Sensitivity Breakdown
            if eval['stability_level'] == "FRAGILE":
                st.warning(f"📊 **Sensitivity Breakdown:**\n{eval.get('sensitivity_breakdown', 'High uncertainty in estimates')}")
            elif eval['stability_level'] == "MODERATELY_STABLE":
                st.info(f"📊 **Sensitivity Breakdown:**\n{eval.get('sensitivity_breakdown', 'Moderate sensitivity detected')}")
            else:
                st.success(f"📊 **Sensitivity Breakdown:**\n{eval.get('sensitivity_breakdown', 'Robust decision')}")
            
            st.divider()
            
            st.markdown("#### 💡 Triggered Insights")
            for msg in eval["triggered_messages"]:
                st.info(f"• {msg}")
    
    st.divider()
    
    # ═══════════════════════════════════════════════════════════════════════════
    # VISUAL COMPARISON CHART
    # ═══════════════════════════════════════════════════════════════════════════
    
    st.markdown("### 📊 Visual Comparison")
    
    col1, col2 = st.columns(2)
    
    # Radar chart
    with col1:
        fig_radar = go.Figure()
        
        for eval in evaluations:
            fig_radar.add_trace(go.Scatterpolar(
                r=[
                    eval["growth_score"],
                    eval["sustainability_score"],
                    100 - eval["tension_index"],
                    100 - (float(eval["risk_level"].split("/")[0]) * 25 if "/" in eval["risk_level"] else 0)
                ],
                theta=["Growth", "Sustainability", "Balance", "Safety"],
                fill="toself",
                name=eval["title"][:20]
            ))
        
        fig_radar.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
            height=400,
            title="Multi-Dimensional Comparison"
        )
        st.plotly_chart(fig_radar, width='stretch', key="radar_comparison")
    
    # Bar chart
    with col2:
        comparison_data = {
            "Option": [e["title"][:15] for e in evaluations],
            "Growth": [e["growth_score"] for e in evaluations],
            "Sustainability": [e["sustainability_score"] for e in evaluations],
            "Composite": [e["composite_score"] for e in evaluations]
        }
        
        fig_bar = go.Figure(data=[
            go.Bar(name="Growth", x=comparison_data["Option"], y=comparison_data["Growth"]),
            go.Bar(name="Sustainability", x=comparison_data["Option"], y=comparison_data["Sustainability"]),
            go.Bar(name="Composite", x=comparison_data["Option"], y=comparison_data["Composite"])
        ])
        
        fig_bar.update_layout(barmode="group", height=400, title="Score Comparison")
        st.plotly_chart(fig_bar, width='stretch', key="bar_comparison")
    
    st.divider()
    
    # ═══════════════════════════════════════════════════════════════════════════
    # ABSOLEM'S REFLECTIVE WISDOM LAYER
    # ═══════════════════════════════════════════════════════════════════════════
    
    st.markdown("### Ask Absolem")
    st.markdown("*Get philosophical guidance on burnout prevention*")
    
    # Check if we already have a reflection cached
    if not st.session_state.ai_reflection:
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button(
                "✨ Get Absolem's Wisdom",
                width='stretch',
                type="primary",
                help="Receive cryptic yet insightful advice on which option prevents burnout best"
            ):
                with st.spinner("🔮 Absolem is contemplating..."):
                    # Prepare options list (convert dict to list) and results for reflection API
                    options_list = [
                        format_option_for_api(
                            opt_data["title"],
                            opt_data["productivity"],
                            opt_data["impact"],
                            opt_data["importance"],
                            opt_data["feasibility"]
                        )
                        for idx in sorted(st.session_state.options_data.keys(), key=lambda x: int(x))
                        for opt_data in [st.session_state.options_data[idx]]
                    ]
                    reflection_result = call_reflection(
                        options_list,
                        st.session_state.analysis_results
                    )
                    if reflection_result:
                        st.session_state.ai_reflection = reflection_result
                        st.rerun()
    else:
        # Display the wisdom
        reflection = st.session_state.ai_reflection
        
        # ABSOLEM'S PHILOSOPHICAL ADVICE
        with st.container(border=True):
            st.markdown("#### 💭 Absolem's Guidance")
            st.write(reflection.get('philosophical_advice', 'Choose what sustains your spirit.'))
        
        # ACTION PLAN
        with st.container(border=True):
            st.markdown("#### 🛤️ Your Action Plan")
            for action in reflection.get('action_plan', []):
                st.markdown(f"• {action}")
        
        st.divider()
        
        col1, col2 = st.columns([3, 1])
        with col2:
            if st.button("🔄 Get New Advice", width='stretch'):
                st.session_state.ai_reflection = None
                st.rerun()
        
        with col1:
            st.caption(f"*Source: {reflection.get('source', 'Unknown')}*")
    
    st.divider()
    
    # ═══════════════════════════════════════════════════════════════════════════
    # NAVIGATION
    # ═══════════════════════════════════════════════════════════════════════════
    
    with col1:
        if st.button("← Back", width='stretch'):
            st.session_state.current_phase = 2
            st.rerun()
    
    with col3:
        if st.button("Start New Decision 🔄", width='stretch', type="primary"):
            st.session_state.current_phase = 1
            st.session_state.decision_topic = ""
            st.session_state.num_options = 2
            st.session_state.options_data = {}
            st.session_state.analysis_results = None
            st.session_state.ai_reflection = None
            st.rerun()

# ═══════════════════════════════════════════════════════════════════════════════
# MAIN APP LOGIC
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    """Main app logic"""
    
    # Sidebar with info
    with st.sidebar:
        st.markdown("### 📚 Academic Burnout-Proof Decision Analyzer")
        st.markdown("---")
        st.markdown("""
        #### How it works:
        
        1. **Enter Decision** - What are you deciding?
        2. **Rate Options** - 4 quick metrics per option
        3. **Get Analysis** - Growth vs. Sustainability
        4. **See Results** - Ranked recommendations
        """)
        
        st.markdown("---")
        st.markdown("""
        #### 📊 The Metrics:
        
        **Growth Criteria:**
        - 📊 Task Volume: Time needed
        - ⚡ Impact: Academic/career benefit
        
        **Sustainability:**
        - 💪 Importance: Matters for goals?
        - ✅ Feasibility: Can you do it?
        """)
        
        st.markdown("---")
        
        # Status indicator
        try:
            response = requests.get(f"{BACKEND_URL}/", timeout=2)
            st.success("✅ Backend Connected")
        except:
            st.error("❌ Backend Offline")
            st.markdown("""
            To start the backend, run:
            ```bash
            python -m uvicorn app.main:app --reload
            ```
            """)
    
    # Main content based on current phase
    if st.session_state.current_phase == 1:
        render_phase_1()
    elif st.session_state.current_phase == 2:
        render_phase_2()
    elif st.session_state.current_phase == 3:
        render_phase_3()

if __name__ == "__main__":
    main()
