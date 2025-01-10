import streamlit as st
import random
from time import sleep

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
    
    # Dizionario di rappresentazioni 3D per altri tipi di dadi
    polygon_dice = {
        4: "🎲₄",    # dado tetraedro
        8: "🎲₈",    # dado ottaedro
        10: "🎲₁₀",  # dado decaedro
        12: "🎲₁₂",  # dado dodecaedro
        20: "🎲₂₀"   # dado icosaedro
    }
    
    # Pedici per i numeri
    subscript = {
        '0': '₀', '1': '₁', '2': '₂', '3': '₃', '4': '₄', 
        '5': '₅', '6': '₆', '7': '₇', '8': '₈', '9': '₉'
    }
    
    if dice_type == 6:
        return unicode_d6.get(number, "?")
    else:
        # Converti il numero in pedici
        number_sub = ''.join(subscript.get(d, d) for d in str(number))
        return f"🎲{number_sub}"

# Configurazione della pagina
st.set_page_config(page_title="Simulatore Dadi 3D", page_icon="🎲")
st.title("🎲 Simulatore Lancio Dadi 3D 🎲")

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

# Pulsante per lanciare i dadi
if st.button(f"Lancia {num_dice} {'dado' if num_dice == 1 else 'dadi'} D{num_faces}"):
    # Animazione del lancio
    with st.spinner("Lancio in corso..."):
        sleep(0.5)  # Breve pausa per effetto animazione
        
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

# Usa una dimensione del font più grande per i dadi non-D6
font_size = "4em" if num_faces == 6 else "6em"
dice_display = " ".join([generate_unicode_dice(value, num_faces) for value in st.session_state.dice_values])
st.markdown(f"<h1 style='text-align: center; font-size: {font_size};'>{dice_display}</h1>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

# Visualizzazione dei valori numerici
values_display = ", ".join(str(value) for value in st.session_state.dice_values)
st.markdown(f"**Valori**: {values_display}")

# Visualizzazione del totale con stile
st.markdown(f"<h3 style='text-align: center; color: #1e88e5;'>Totale: {st.session_state.total}</h3>", unsafe_allow_html=True)

# Statistiche
if len(st.session_state.rolls) > 0:
    st.markdown("### Statistiche")
    col1, col2 = st.columns(2)
    
    with col1:
        st.write(f"Numero di lanci: {len(st.session_state.rolls)}")
        avg_total = sum(roll['total'] for roll in st.session_state.rolls) / len(st.session_state.rolls)
        st.write(f"Media dei totali: {avg_total:.2f}")
    
    with col2:
        # Range teorico
        min_possible = num_dice  # Ogni dado fa 1
        max_possible = num_dice * num_faces  # Ogni dado fa il massimo
        st.write(f"Range possibile: {min_possible} - {max_possible}")
        
    # Visualizzazione dello storico dei lanci
    if st.checkbox("Mostra storico dei lanci"):
        st.markdown("#### Ultimi lanci")
        for i, roll in enumerate(st.session_state.rolls[::-1], 1):
            st.write(f"Lancio #{len(st.session_state.rolls)-i+1}: "
                    f"Dadi: {roll['values']} = {roll['total']}")
