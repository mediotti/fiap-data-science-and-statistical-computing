from pathlib import Path
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import plotly.express as px
import plotly.graph_objects as go
from streamlit_extras.app_logo import add_logo

# Function to load data
@st.cache_data
def load_data():
    try:
        df = pd.read_csv('license_plates_with_hamming_distance.csv')
        # Ensure the Hamming distance is numeric
        df['hammingDistance'] = pd.to_numeric(df['hammingDistance'], errors='coerce')
        return df
    except FileNotFoundError:
        st.error("Dataset file not found. Please upload the license_plates_with_hamming_distance.csv file.")
        return None

# Function to allow user to upload data
def upload_data():
    uploaded_file = st.file_uploader("Upload your license plate dataset", type=['csv'])
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        
        # Check if hammingDistance column exists
        if 'hammingDistance' not in df.columns:
            # If not, we need to calculate it
            if 'licensePlateDetected' in df.columns and 'irregularLicensePlate' in df.columns:
                # Calculate Hamming distance
                df['hammingDistance'] = df.apply(
                    lambda row: sum(c1 != c2 for c1, c2 in zip(
                        str(row['licensePlateDetected']), 
                        str(row['irregularLicensePlate'])
                    )) if len(str(row['licensePlateDetected'])) == len(str(row['irregularLicensePlate'])) 
                    else max(len(str(row['licensePlateDetected'])), len(str(row['irregularLicensePlate']))),
                    axis=1
                )
                st.success("Hamming distance calculated successfully!")
            else:
                st.error("The uploaded file doesn't contain required columns: licensePlateDetected and irregularLicensePlate")
                return None
        else:
            # If column exists, ensure it's numeric
            df['hammingDistance'] = pd.to_numeric(df['hammingDistance'], errors='coerce')
        
        return df
    return None

# Load or upload data
data = load_data()
if data is None:
    data = upload_data()
    if data is None:
        st.warning("Por favor, carregue o arquivo de dados para continuar.")
    else:
        st.success("Dados carregados com sucesso!")

if data is not None:
    tab1, tab2, tab3 = st.tabs([
        "1. Distribuição Binomial", 
        "2. Distribuição de Poisson", 
        "3. Distribuição Normal"
    ])
    
    # Tab 1: Data Presentation
    with tab1:
        st.header("3. Aplicação de Distribuições Probabilísticas")
        
        # 1. Binomial Distribution
        st.subheader("Distribuição Binomial para Erros de Detecção")
        
        st.markdown("""
        ### Distribuição Binomial
        
        **Justificativa da Escolha:**
        
        A distribuição binomial é adequada para modelar o número de "sucessos" em um número fixo de tentativas 
        independentes, onde cada tentativa tem a mesma probabilidade de sucesso. No nosso contexto, podemos 
        considerar um "sucesso" como a ocorrência de um erro de detecção (distância de Hamming > 0).
        
        Esta distribuição nos ajuda a modelar a probabilidade de ocorrer um certo número de erros de detecção 
        em um conjunto de placas analisadas.
        """)
        
        # Calculate proportion of errors (Hamming distance > 0)
        error_prob = (data['hammingDistance'] > 0).mean()
        
        # Number of trials for binomial simulation
        n_trials = st.slider("Número de detecções a simular", 10, 100, 50)
        
        # Calculate binomial probabilities
        k_values = np.arange(0, n_trials + 1)
        binomial_probs = stats.binom.pmf(k_values, n_trials, error_prob)
        
        # Create binomial distribution plot
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.bar(k_values, binomial_probs, alpha=0.7)
        ax.set_xlabel('Número de Erros de Detecção')
        ax.set_ylabel('Probabilidade')
        ax.set_title(f'Distribuição Binomial: Probabilidade de Erros em {n_trials} Detecções\n(p = {error_prob:.2f})')
        ax.grid(alpha=0.3)
        
        st.pyplot(fig)
    
    with tab2:
        # 2. Poisson Distribution
        st.subheader("Distribuição de Poisson para Taxa de Erros por Câmera")
        
        st.markdown("""
        ### Distribuição de Poisson
        
        **Justificativa da Escolha:**
        
        A distribuição de Poisson é adequada para modelar o número de eventos que ocorrem em um intervalo fixo 
        de tempo ou espaço. No nosso contexto, utilizamos esta distribuição para modelar o número de erros de detecção 
        por câmera, assumindo que cada câmera tem uma taxa média de erros.
        """)
        
        # Group errors by MAC address
        errors_by_camera = data[data['hammingDistance'] > 1].groupby('macAddress').size().reset_index()
        errors_by_camera.columns = ['macAddress', 'error_count']
        
        # Calculate the average error rate per camera
        avg_error_rate = errors_by_camera['error_count'].mean()
        
        # Create Poisson distribution plot
        k_values_poisson = np.arange(0, max(20, int(avg_error_rate * 3)))
        poisson_probs = stats.poisson.pmf(k_values_poisson, avg_error_rate)
        
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.bar(k_values_poisson, poisson_probs, alpha=0.7)
        ax.set_xlabel('Número de Erros por Câmera')
        ax.set_ylabel('Probabilidade')
        ax.set_title(f'Distribuição de Poisson: Probabilidade de Erros por Câmera\n(λ = {avg_error_rate:.2f})')
        ax.grid(alpha=0.3)
        
        st.pyplot(fig)
    
    with tab3:
        # 3. Normal Distribution
        st.subheader("Distribuição Normal para Variação da Distância de Hamming")
        
        st.markdown("""
        ### Distribuição Normal
        
        **Justificativa da Escolha:**
        
        A distribuição normal é adequada para modelar variáveis contínuas influenciadas por muitos fatores independentes.
        Em nosso caso, a variação da distância de Hamming pode resultar de múltiplos fatores como qualidade da imagem, 
        condições de iluminação, posicionamento da câmera, entre outros.
        """)
        
        # Calculate the mean and standard deviation of Hamming distance
        hamming_mean = data['hammingDistance'].mean()
        hamming_std = data['hammingDistance'].std()
        
        # Create a range for the x-axis
        x = np.linspace(max(0, hamming_mean - 4*hamming_std), hamming_mean + 4*hamming_std, 1000)
        
        # Calculate the pdf values
        pdf = stats.norm.pdf(x, hamming_mean, hamming_std)
        
        # Create the plot
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(x, pdf, 'b-', lw=2, label='Normal PDF')
        
        # Plot histograma normal
        hist_data = data['hammingDistance']
        ax.hist(hist_data, bins=20, density=True, alpha=0.5, color='skyblue', label='Dados Observados')
        
        ax.set_xlabel('Distância de Hamming')
        ax.set_ylabel('Densidade de Probabilidade')
        ax.set_title(f'Distribuição Normal: Distância de Hamming\n(μ = {hamming_mean:.2f}, σ = {hamming_std:.2f})')
        ax.grid(alpha=0.3)
        ax.legend()
        
        st.pyplot(fig)
