import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

# Configuração da página
st.set_page_config(
    page_title="Economia Russa — Dashboard 1999–2025",
    page_icon="🇷🇺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilo CSS customizado para manter a identidade visual do original
st.markdown("""
    <style>
    .main {
        background-color: #0d0f14;
        color: #e8e6df;
    }
    [data-testid="stHeader"] {
        background-color: #141720;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 30px;
        background-color: #141720;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #141720;
        border-radius: 4px 4px 0px 0px;
        gap: 1px;
        padding-top: 10px;
        padding-bottom: 10px;
    }
    .stMetric {
        background-color: #141720;
        padding: 15px;
        border-radius: 8px;
        border-top: 2px solid #e8401c;
    }
    </style>
    """, unsafe_allow_html=True)

# Função para carregar dados
@st.cache_data
def load_data():
    data_path = './data'
    pib = pd.read_csv(os.path.join(data_path, 'pib.csv'))
    emprego = pd.read_csv(os.path.join(data_path, 'emprego.csv'))
    desemprego = pd.read_csv(os.path.join(data_path, 'desemprego.csv'))
    dolar_anual = pd.read_csv(os.path.join(data_path, 'dolar_anual.csv'))
    euro_anual = pd.read_csv(os.path.join(data_path, 'euro_anual.csv'))
    dolar_mensal = pd.read_csv(os.path.join(data_path, 'dolar_mensal.csv'))
    euro_mensal = pd.read_csv(os.path.join(data_path, 'euro_mensal.csv'))
    receitas = pd.read_csv(os.path.join(data_path, 'receitas.csv'))
    return pib, emprego, desemprego, dolar_anual, euro_anual, dolar_mensal, euro_mensal, receitas

pib, emprego, desemprego, dolar_anual, euro_anual, dolar_mensal, euro_mensal, receitas = load_data()

# Sidebar - Filtros
st.sidebar.title("🇷🇺 Economia Russa")
st.sidebar.markdown("DADOS MACRO ECONÔMICOS · 1999–2025")

min_year = int(pib['ANO'].min())
max_year = int(pib['ANO'].max())

year_range = st.sidebar.slider(
    "Selecione o Período",
    min_value=min_year,
    max_value=max_year + 1, # Para incluir 2025 se houver
    value=(min_year, max_year)
)

# Filtragem de dados
def filter_by_year(df, year_col='ANO'):
    return df[(df[year_col] >= year_range[0]) & (df[year_col] <= year_range[1])]

pib_f = filter_by_year(pib)
emp_f = filter_by_year(emprego)
des_f = filter_by_year(desemprego)
dol_a_f = filter_by_year(dolar_anual)
eur_a_f = filter_by_year(euro_anual)
rec_f = filter_by_year(receitas)

# Para dados mensais
dol_m_f = dolar_mensal[(dolar_mensal['ano'] >= year_range[0]) & (dolar_mensal['ano'] <= year_range[1])]
eur_m_f = euro_mensal[(euro_mensal['ano'] >= year_range[0]) & (euro_mensal['ano'] <= year_range[1])]

# Tabs principais
tab_visao, tab_pib, tab_emprego, tab_cambio, tab_receitas = st.tabs([
    "Visão Geral", "PIB", "Emprego", "Câmbio", "Receitas"
])

# --- TAB VISÃO GERAL ---
with tab_visao:
    # KPIs
    col1, col2, col3, col4, col5 = st.columns(5)
    
    def get_delta(df, col):
        if len(df) >= 2:
            last = df[col].iloc[-1]
            prev = df[col].iloc[-2]
            return f"{((last - prev) / prev * 100):.1f}%"
        return None

    with col1:
        last_pib = pib_f['Total'].iloc[-1] if not pib_f.empty else 0
        st.metric("PIB Total (bi ₽)", f"{last_pib:,.0f}".replace(",", "."), delta=get_delta(pib_f, 'Total'))
    
    with col2:
        last_emp = emp_f['Empregados'].iloc[-1] if not emp_f.empty else 0
        st.metric("Empregados (mi)", f"{last_emp:,.1f}".replace(",", "."), delta=get_delta(emp_f, 'Empregados'))
        
    with col3:
        last_des = des_f['Desempregados'].iloc[-1] if not des_f.empty else 0
        st.metric("Desempregados (mi)", f"{last_des:,.1f}".replace(",", "."), delta=get_delta(des_f, 'Desempregados'), delta_color="inverse")
        
    with col4:
        last_dol = dol_a_f['Valor'].iloc[-1] if not dol_a_f.empty else 0
        st.metric("Dólar/Rublo (Dez)", f"₽ {last_dol:,.2f}".replace(",", "."), delta=get_delta(dol_a_f, 'Valor'), delta_color="inverse")
        
    with col5:
        last_rec = rec_f['Consolidado'].iloc[-1] if not rec_f.empty else 0
        st.metric("Receita Consolidada", f"{last_rec:,.0f} bi".replace(",", "."), delta=get_delta(rec_f, 'Consolidado'))

    # Gráficos Visão Geral
    c1, c2 = st.columns(2)
    with c1:
        fig_pib = px.bar(pib_f, x='ANO', y='Total', title="PIB Total (bi rublos)", color_discrete_sequence=['#e8401c'])
        fig_pib.update_layout(template="plotly_dark", plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_pib, use_container_width=True)
        
        fig_dol = px.line(dol_a_f, x='ANO', y='Valor', title="Câmbio Dólar/Rublo (anual, Dez)", color_discrete_sequence=['#4ea8de'])
        fig_dol.update_layout(template="plotly_dark", plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_dol, use_container_width=True)

    with c2:
        # Emprego vs Desemprego
        fig_emp_des = go.Figure()
        fig_emp_des.add_trace(go.Scatter(x=emp_f['ANO'], y=emp_f['Empregados'], name='Empregados', fill='tozeroy', line_color='#3ecf8e'))
        fig_emp_des.add_trace(go.Scatter(x=des_f['ANO'], y=des_f['Desempregados'], name='Desempregados', line_color='#e8401c'))
        fig_emp_des.update_layout(title="Emprego vs Desemprego (mi pessoas)", template="plotly_dark", plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_emp_des, use_container_width=True)
        
        # Receitas
        fig_rec = px.bar(rec_f, x='ANO', y=['Consolidado', 'Federal'], barmode='group', title="Receitas Orçamentárias (bi rublos)", color_discrete_map={'Consolidado': '#4ea8de', 'Federal': '#e8401c'})
        fig_rec.update_layout(template="plotly_dark", plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_rec, use_container_width=True)

# --- TAB PIB ---
with tab_pib:
    st.subheader("PIB Anual por Trimestre (bi rublos)")
    pib_mode = st.radio("Modo de Visualização", ["Barras Empilhadas", "Linhas"], horizontal=True)
    
    quarters = ['T1', 'T2', 'T3', 'T4']
    if pib_mode == "Barras Empilhadas":
        fig_pib_det = px.bar(pib_f, x='ANO', y=quarters, title="PIB Trimestral", color_discrete_sequence=['#4ea8de','#3ecf8e','#f5c518','#e8401c'])
    else:
        fig_pib_det = px.line(pib_f, x='ANO', y=quarters, title="PIB Trimestral", color_discrete_sequence=['#4ea8de','#3ecf8e','#f5c518','#e8401c'])
    
    fig_pib_det.update_layout(template="plotly_dark", plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_pib_det, use_container_width=True)
    
    st.markdown("### Tabela de PIB por Trimestre")
    st.dataframe(pib_f[['ANO', 'T1', 'T2', 'T3', 'T4', 'Total']].sort_values('ANO', ascending=False), use_container_width=True)
    st.info("Dados de 1999–2010 não revisados. A partir de 2022, excluem regiões de Donetsk, Luhansk, Zaporizhzhia e Kherson.")

# --- TAB EMPREGO ---
with tab_emprego:
    c1, c2 = st.columns(2)
    with c1:
        fig_emp = px.line(emp_f, x='ANO', y='Empregados', title="Empregados (mi pessoas)", color_discrete_sequence=['#3ecf8e'])
        fig_emp.update_layout(template="plotly_dark", plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_emp, use_container_width=True)
    with c2:
        fig_des = px.line(des_f, x='ANO', y='Desempregados', title="Desempregados (mi pessoas)", color_discrete_sequence=['#e8401c'])
        fig_des.update_layout(template="plotly_dark", plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_des, use_container_width=True)
    
    st.markdown("### Tabela Emprego e Desemprego")
    # Calcular taxa de desemprego
    emp_des_merged = pd.merge(emp_f, des_f, on='ANO')
    emp_des_merged['% Desemprego'] = (emp_des_merged['Desempregados'] / (emp_des_merged['Empregados'] + emp_des_merged['Desempregados']) * 100).round(1)
    st.dataframe(emp_des_merged[['ANO', 'Empregados', 'Desempregados', '% Desemprego']].sort_values('ANO', ascending=False), use_container_width=True)
    st.info("1999–2016: população de 15–72 anos. A partir de 2017: 15 anos ou mais.")

# --- TAB CÂMBIO ---
with tab_cambio:
    st.subheader("Câmbio Mensal — Rublo/Moeda")
    cambio_mode = st.multiselect("Selecione as Moedas", ["Dólar", "Euro"], default=["Dólar"])
    
    fig_cambio_m = go.Figure()
    if "Dólar" in cambio_mode:
        fig_cambio_m.add_trace(go.Scatter(x=dol_m_f['label'], y=dol_m_f['valor'], name='USD', line_color='#4ea8de'))
    if "Euro" in cambio_mode:
        fig_cambio_m.add_trace(go.Scatter(x=eur_m_f['label'], y=eur_m_f['valor'], name='EUR', line_color='#f5c518'))
    
    fig_cambio_m.update_layout(template="plotly_dark", plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_cambio_m, use_container_width=True)
    
    c1, c2 = st.columns(2)
    with c1:
        fig_dol_a = px.bar(dol_a_f, x='ANO', y='Valor', title="Dólar Anual (Dez) — Rublo/USD", color_discrete_sequence=['#4ea8de'])
        fig_dol_a.update_layout(template="plotly_dark", plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_dol_a, use_container_width=True)
    with c2:
        fig_eur_a = px.bar(eur_a_f, x='ANO', y='Valor', title="Euro Anual (Dez) — Rublo/EUR", color_discrete_sequence=['#f5c518'])
        fig_eur_a.update_layout(template="plotly_dark", plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_eur_a, use_container_width=True)

# --- TAB RECEITAS ---
with tab_receitas:
    st.subheader("Receitas Orçamentárias (bi rublos)")
    fig_rec_det = px.bar(rec_f, x='ANO', y=['Consolidado', 'Federal'], barmode='group', title="Orçamento Consolidado vs Federal", color_discrete_map={'Consolidado': '#4ea8de', 'Federal': '#e8401c'})
    fig_rec_det.update_layout(template="plotly_dark", plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_rec_det, use_container_width=True)
    
    st.markdown("### Tabela de Receitas")
    rec_f['% Federal'] = (rec_f['Federal'] / rec_f['Consolidado'] * 100).round(1)
    st.dataframe(rec_f[['ANO', 'Consolidado', 'Federal', '% Federal']].sort_values('ANO', ascending=False), use_container_width=True)
    st.info("Orçamento consolidado agrega todos os entes da federação. Orçamento federal: somente União.")
