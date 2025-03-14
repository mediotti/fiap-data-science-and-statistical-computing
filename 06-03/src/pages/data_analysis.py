import streamlit as st
import pandas as pd
import plotly.express as px


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

st.title("Análise de Dados - Detecção de Placas de Veículos")
    
# Load or upload data
data = load_data()
if data is None:
    data = upload_data()
    if data is None:
        st.warning("Por favor, carregue o arquivo de dados para continuar.")
    else:
        st.success("Dados carregados com sucesso!")

# Create tabs for different analysis sections

    st.header("1. Apresentação dos Dados e Tipos de Variáveis")
    
    # Introduction to the dataset
    st.markdown("""
    ### Conjunto de Dados: Sistema de Detecção de Placas de Veículos
    
    Este conjunto de dados contém informações coletadas por uma rede de câmeras de vigilância que detectam e registram placas de veículos em ambiente urbano. 
    O principal objetivo da análise é avaliar a precisão do sistema de detecção e identificar padrões de irregularidades nas placas detectadas.
    
    #### Contexto do Problema:
    
    Os sistemas de reconhecimento automático de placas veiculares (ALPR - Automatic License Plate Recognition) são fundamentais para a segurança urbana, 
    controle de tráfego, e identificação de veículos irregulares. No entanto, esses sistemas podem apresentar falhas de reconhecimento devido a diversos fatores, 
    como condições ambientais, qualidade da imagem, ou placas adulteradas.
    
    Esta análise visa identificar padrões nessas falhas para melhorar a eficiência do sistema.
    """)
    
    # Show the first few rows of data
    st.subheader("Amostra dos Dados")
    st.dataframe(data.head(10))
    
    # Display dataset information
    st.subheader("Informações do Dataset")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Número de Registros", data.shape[0])
        st.metric("Número de Colunas", data.shape[1])
    
    with col2:
        missing_values = data.isnull().sum().sum()
        st.metric("Valores Ausentes", missing_values)
        duplicated_rows = data.duplicated().sum()
        st.metric("Linhas Duplicadas", duplicated_rows)
    
    # Data types and description
    st.subheader("Tipos de Variáveis")
    
    variable_types = pd.DataFrame({
        'Variável': data.columns,
        'Tipo de Dado': data.dtypes.astype(str),
        'Tipo de Variável': [
            'Categorical (ID)', 
            'Categorical', 
            'Categorical', 
            'Numerical (Continuous)', 
            'Numerical (Continuous)', 
            'Categorical',
            'Numerical (Discrete)'
        ],
        'Descrição': [
            'Identificador único do registro',
            'Placa de veículo detectada pelo sistema',
            'Placa irregular ou com possíveis adulterações',
            'Coordenada geográfica - latitude',
            'Coordenada geográfica - longitude',
            'Endereço MAC da câmera que realizou a detecção',
            'Distância de Hamming entre a placa detectada e a placa irregular'
        ]
    })
    
    st.table(variable_types)
    
    # Main analysis questions
    st.subheader("Perguntas Principais para Análise")
    
    st.markdown("""
    1. **Qual é a distribuição da distância de Hamming entre placas detectadas e placas irregulares?**
        - Isso nos ajudará a entender o padrão de diferenças/erros na detecção.
    
    2. **Existem regiões específicas (coordenadas geográficas) onde ocorrem mais erros de detecção?**
        - Identificação de possíveis pontos problemáticos na rede de câmeras.
    
    3. **Qual é a probabilidade de ocorrer um erro de detecção com distância de Hamming maior que 1?**
        - Aplicação de distribuições probabilísticas para modelar ocorrências de erros.
    
    4. **Existe correlação entre a localização geográfica e a frequência/tipo de irregularidades?**
        - Análise de padrões geoespaciais nas detecções incorretas.
    
    5. **Quais câmeras (MAC addresses) apresentam mais falhas de detecção?**
        - Identificação de equipamentos que podem precisar de manutenção ou substituição.
    """)

    st.header("2. Medidas Centrais, Análise Inicial, Dispersão e Correlação")
    
    # Central tendency measures for Hamming Distance
    st.subheader("Medidas de Tendência Central da Distância de Hamming")
    
    hamming_mean = data['hammingDistance'].mean()
    hamming_median = data['hammingDistance'].median()
    hamming_mode = data['hammingDistance'].mode()[0]
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Média", f"{hamming_mean:.2f}")
    
    with col2:
        st.metric("Mediana", f"{hamming_median:.2f}")
    
    with col3:
        st.metric("Moda", f"{hamming_mode:.0f}")
    
    # Histogram of Hamming Distance
    st.subheader("Distribuição da Distância de Hamming")
    
    fig = px.histogram(
        data, 
        x='hammingDistance',
        nbins=10,
        title='Distribuição da Distância de Hamming',
        color_discrete_sequence=['#3b82f6']
    )
    fig.update_layout(bargap=0.1)
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("""
    **Análise da Distribuição:**
    
    A distância de Hamming mede a diferença entre a placa detectada e a placa irregular. 
    Observando o histograma, podemos identificar que a maioria das detecções tem uma distância de Hamming 
    entre 0-3, o que sugere que muitas detecções estão próximas da placa real ou têm poucas diferenças.
    """)
    
    # Dispersion metrics
    st.subheader("Medidas de Dispersão")
    
    hamming_std = data['hammingDistance'].std()
    hamming_var = data['hammingDistance'].var()
    hamming_range = data['hammingDistance'].max() - data['hammingDistance'].min()
    hamming_iqr = data['hammingDistance'].quantile(0.75) - data['hammingDistance'].quantile(0.25)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Desvio Padrão", f"{hamming_std:.2f}")
        st.metric("Amplitude", f"{hamming_range:.0f}")
    
    with col2:
        st.metric("Variância", f"{hamming_var:.2f}")
        st.metric("Amplitude Interquartil (IQR)", f"{hamming_iqr:.2f}")
    
    # Box plot for Hamming Distance
    st.subheader("Box Plot da Distância de Hamming")
    
    fig = px.box(
        data, 
        y='hammingDistance',
        title='Box Plot da Distância de Hamming',
        color_discrete_sequence=['#3b82f6']
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Geographical analysis
    st.subheader("Análise Geográfica de Erros de Detecção")
    
    # Create a geospatial visualization
    st.markdown("Mapa de calor das distâncias de Hamming por localização:")
    
    fig = px.scatter_mapbox(
        data, 
        lat='latitude', 
        lon='longitude', 
        color='hammingDistance',
        size='hammingDistance',
        color_continuous_scale=px.colors.sequential.Viridis,
        mapbox_style="carto-positron",
        zoom=10,
        title='Distribuição Geográfica das Distâncias de Hamming'
    )
    st.plotly_chart(fig, use_container_width=True)