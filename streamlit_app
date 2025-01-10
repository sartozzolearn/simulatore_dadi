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
    
    # Dizionario di rappresentazioni ASCII per altri tipi di dadi
    polygon_dice = {
        4: "▲",   # tetraedro
        8: "◊",   # ottaedro
        10: "⬟",  # decaedro
        12: "⬡",  # dodecaedro
        20: "△"   # icosaedro
    }
    
    if dice_type == 6:
        return unicode_d6.get(number, "?")
    else:
        return f"{polygon_dice.get(dice_type, '?')}{number}"

def generate_dice_face(number, max_faces):
    """Genera una rappresentazione ASCII del dado"""
    if max_faces == 6:
        dice = {
            1: ["┌─────────┐",
                "│         │",
                "│    ●    │",
                "│         │",
                "└─────────┘"],
            2: ["┌─────────┐",
                "│  ●      │",
                "│         │",
                "│      ●  │",
                "└─────────┘"],
            3: ["┌─────────┐",
                "│  ●      │",
                "│    ●    │",
                "│      ●  │",
                "└─────────┘"],
            4: ["┌─────────┐",
                "│  ●   ●  │",
                "│         │",
                "│  ●   ●  │",
                "└─────────┘"],
            5: ["┌─────────┐",
                "│  ●   ●  │",
                "│    ●    │",
                "│  ●   ●  │",
                "└─────────┘"],
            6: ["┌─────────┐",
                "│  ●   ●  │",
                "│  ●   ●  │",
                "│  ●   ●  │",
                "└─────────┘"]
        }
        return dice.get(number, [])
    else:
        # Per dadi non a 6 facce, mostra solo il numero
        return [
            "┌─────────┐",
            "│         │",
            f"│    {number:<3}   │",
            "│         │",
            "└─────────┘"
        ]

# Configurazione della pagina
st.set_page_config(page_title="Simulatore Dadi", page_icon="🎲")
st.title("🎲 Simulatore Lancio Dadi 🎲")

# Configurazione dei dadi
st.sidebar.header("Configurazione Dadi")
dice_types = [4, 6, 8, 10, 12, 20]
num_faces = st.sidebar.selectbox("Numero di facce per dado", dice_types)
num_dice = st.sidebar.slider("Numero di dadi", min_value=1, max_value=10, value=2)

# Selezione dello stile di visualizzazione
display_style = st.sidebar.radio(
    "Stile di visualizzazione",
    ["Unicode", "ASCII"],
    index=0
)

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
if display_style == "Unicode":
    st.markdown("### Risultato del lancio")
    dice_display = " ".join([generate_unicode_dice(value, num_faces) for value in st.session_state.dice_values])
    st.markdown(f"<h1 style='text-align: center; font-size: 4em;'>{dice_display}</h1>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
else:
    cols = st.columns(min(5, num_dice))  # Massimo 5 dadi per riga
    for i, value in enumerate(st.session_state.dice_values):
        col_idx = i % len(cols)
        with cols[col_idx]:
            st.markdown(f"**Dado {i+1}:**")
            dice_face = generate_dice_face(value, num_faces)
            st.text('\n'.join(dice_face))
            st.markdown(f"**(D{num_faces}: {value})**")

# Visualizzazione del totale
st.markdown(f"### Totale: {st.session_state.total}")

# Statistiche
if len(st.session_state.rolls) > 0:
    st.markdown("### Statistiche")
    st.write(f"Numero di lanci: {len(st.session_state.rolls)}")
    avg_total = sum(roll['total'] for roll in st.session_state.rolls) / len(st.session_state.rolls)
    st.write(f"Media dei totali: {avg_total:.2f}")
    
    # Range teorico
    min_possible = num_dice  # Ogni dado fa 1
    max_possible = num_dice * num_faces  # Ogni dado fa il massimo
    st.write(f"Range possibile: {min_possible} - {max_possible}")
    
    # Visualizzazione dello storico dei lanci
    if st.checkbox("Mostra storico dei lanci"):
        for i, roll in enumerate(st.session_state.rolls[::-1], 1):
            st.write(f"Lancio #{len(st.session_state.rolls)-i+1}: "
                    f"Dadi: {roll['values']} = {roll['total']}")
