import streamlit as st
import random
from time import sleep
import plotly.graph_objects as go
from collections import Counter

def generate_unicode_dice(number, dice_type):
    """Genera una rappresentazione Unicode del dado"""
    # Dizionario dei dadi Unicode per D6
    unicode_d6 = {
        1: "⚀",
        2: "⚁",
        3: "⚂",
        4: "⚃",
        5: "⚄",
        6: "⚅"
    }
    
    # Dizionario dei numeri cerchiati Unicode
    circled_numbers = {
        1: "①", 2: "②", 3: "③", 4: "④", 5: "⑤",
        6: "⑥", 7: "⑦", 8: "⑧", 9: "⑨", 10: "⑩",
        11: "⑪", 12: "⑫", 13: "⑬", 14: "⑭", 15: "⑮",
        16: "⑯", 17: "⑰", 18: "⑱", 19: "⑲", 20: "⑳"
    }
    
    if dice_type == 6:
        return unicode_d6.get(number, "?")
    else:
        return circled_numbers.get(number, str(number))

def create_distribution_plot(rolls_history, num_dice, num_faces):
    """Crea un grafico della distribuzione dei risultati"""
    totals = [roll['total'] for roll in rolls_history]
    counts = Counter(totals)
    
    # Calcola il range possibile di risultati
    min_possible = num_dice
    max_possible = num_dice * num_faces
    
    # Crea una lista completa di tutti i possibili risultati
    all_possible = list(range(min_possible, max_possible + 1))
    values = [counts.get(x, 0) for x in all_possible]
    
    # Crea il grafico
    fig = go.Figure()
    
    # Aggiungi l'istogramma
    fig.add_trace(go.Bar(
        x=all_possible,
        y=values,
        name='Frequenza',
        marker_color='rgb(30, 136, 229)',
    ))
    
    # Personalizza il layout
    fig.update_layout(
        title=f'Distribuzione dei Risultati ({len(totals)} lanci)',
        xaxis_title='Somma dei Dadi',
        yaxis_title='Frequenza',
        bargap=0.1,
        height=400,
    )
    
    return fig

def create_timeline_plot(rolls_history):
    """Crea un grafico dell'andamento temporale dei risultati"""
    if not rolls_history:
        return None
        
    totals = [roll['total'] for roll in rolls_history]
    roll_numbers = list(range(1, len(totals) + 1))
    
    # Calcola la media mobile
    window = min(5, len(totals))  # Usa una finestra di 5 o meno se ci sono meno lanci
    moving_avg = []
    for i in range(len(totals)):
        start = max(0, i - window + 1)
        avg = sum(totals[start:i+1]) / (i - start + 1)
        moving_avg.append(avg)
    
    fig = go.Figure()
    
    # Aggiungi la linea dei risultati
    fig.add_trace(go.Scatter(
        x=roll_numbers,
        y=totals,
        mode='lines+markers',
        name='Risultati',
        line=dict(color='rgb(30, 136, 229)'),
    ))
    
    # Aggiungi la media mobile
    fig.add_trace(go.Scatter(
        x=roll_numbers,
        y=moving_avg,
        mode='lines',
        name='Media Mobile',
        line=dict(color='rgb(255, 87, 34)', dash='dash'),
    ))
    
    # Personalizza il layout
    fig.update_layout(
        title='Andamento dei Risultati nel Tempo',
        xaxis_title='Numero del Lancio',
        yaxis_title='Risultato',
        height=400,
    )
    
    return fig

# Configurazione della pagina
st.set_page_config(page_title="Simulatore Dadi", page_icon="🎲", layout="wide")
st.title("🎲 Simulatore Lancio Dadi 🎲")

# Configurazione dei dadi
st.sidebar.header("Configurazione Dadi")
dice_types = [4, 6, 8, 10, 12, 20]
num_faces = st.sidebar.selectbox("Numero di facce per dado", dice_types)
num_dice = st.sidebar.slider("Numero di dadi", min_value=1, max_value=10, value=2)

# Inizializzazione delle variabili di stato
if 'dice_values' not in st.session_state:
    st.session_state.dice_values = [1] * num_dice
if 'total' not in st.session_state:
    st.session_state.total = num_dice
if 'rolls' not in st.session_state:
    st.session_state.rolls = []
if 'last_config' not in st.session_state:
    st.session_state.last_config = (num_dice, num_faces)

# Se la configurazione è cambiata, resetta i valori
if st.session_state.last_config != (num_dice, num_faces):
    st.session_state.dice_values = [1] * num_dice
    st.session_state.total = num_dice
    st.session_state.rolls = []
    st.session_state.last_config = (num_dice, num_faces)

# Layout principale in due colonne
col_left, col_right = st.columns([2, 1])

with col_left:
    # Pulsante per lanciare i dadi
    if st.button(f"Lancia {num_dice} {'dado' if num_dice == 1 else 'dadi'} D{num_faces}"):
        # Animazione del lancio
        with st.spinner("Lancio in corso..."):
            sleep(0.5)
            
            # Generazione numeri casuali
            st.session_state.dice_values = [random.randint(1, num_faces) for _ in range(num_dice)]
            st.session_state.total = sum(st.session_state.dice_values)
            
            # Aggiunta del risultato allo storico
            st.session_state.rolls.append({
                'values': st.session_state.dice_values.copy(),
                'total': st.session_state.total
            })

    # Visualizzazione dei dadi
    st.markdown("### Risultato del lancio")
    dice_display = " ".join([generate_unicode_dice(value, num_faces) for value in st.session_state.dice_values])
    st.markdown(f"<h1 style='text-align: center; font-size: 4em;'>{dice_display}</h1>", unsafe_allow_html=True)
    
    # Visualizzazione dei valori numerici
    values_display = ", ".join(str(value) for value in st.session_state.dice_values)
    st.markdown(f"**Valori**: {values_display}")
    
    # Visualizzazione del totale con stile
    st.markdown(f"<h3 style='text-align: center; color: #1e88e5;'>Totale: {st.session_state.total}</h3>", unsafe_allow_html=True)

with col_right:
    # Statistiche base
    if len(st.session_state.rolls) > 0:
        st.markdown("### Statistiche")
        st.write(f"Numero di lanci: {len(st.session_state.rolls)}")
        avg_total = sum(roll['total'] for roll in st.session_state.rolls) / len(st.session_state.rolls)
        st.write(f"Media dei totali: {avg_total:.2f}")
        min_possible = num_dice
        max_possible = num_dice * num_faces
        st.write(f"Range possibile: {min_possible} - {max_possible}")

# Grafici (sotto le colonne principali)
if len(st.session_state.rolls) > 0:
    st.markdown("### Analisi dei Risultati")
    
    # Tabs per i diversi grafici
    tab1, tab2 = st.tabs(["📊 Distribuzione", "📈 Andamento Temporale"])
    
    with tab1:
        # Grafico della distribuzione
        dist_fig = create_distribution_plot(st.session_state.rolls, num_dice, num_faces)
        st.plotly_chart(dist_fig, use_container_width=True)
        
    with tab2:
        # Grafico dell'andamento temporale
        time_fig = create_timeline_plot(st.session_state.rolls)
        st.plotly_chart(time_fig, use_container_width=True)

# Storico dei lanci (in fondo alla pagina)
if len(st.session_state.rolls) > 0 and st.checkbox("Mostra storico dei lanci"):
    st.markdown("#### Ultimi lanci")
    for i, roll in enumerate(st.session_state.rolls[::-1], 1):
        st.write(f"Lancio #{len(st.session_state.rolls)-i+1}: "
                f"Dadi: {roll['values']} = {roll['total']}")
