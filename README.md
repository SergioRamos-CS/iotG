# 🐣 IoT - Monitoramento de Incubação

Este projeto é um sistema para monitoramento e controle automatizado de incubadoras avícolas. Ele utiliza Python e Flask para criar um dashboard em tempo real que gerencia temperatura e umidade, simulando o comportamento físico real de um ambiente de granja.

## 🚀 Funcionalidades

- **Monitoramento em Tempo Real**: Visualização instantânea de temperatura e umidade com atualização a cada 5 segundos.
- **Controle de Malha Fechada (Setpoints)**: Interface para definir faixas ideais de operação. O sistema decide automaticamente quando ligar/desligar o aquecedor e o umidificador.
- **Simulação de Física Real**: Algoritmo de simulação que emula a perda térmica ambiental e dissipação de umidade baseada no clima de Santos/SP.
- **Gráficos Dinâmicos**: Histórico visual utilizando Chart.js com efeito de oscilação "dente de serra".
- **Exportação de Dados**: Geração de relatórios estratégicos em formato CSV com filtros por data e hora.
- **Design Responsivo**: Dashboard adaptável para computadores, tablets e smartphones.

## 🛠️ Tecnologias Utilizadas

- **Backend**: Python 3.14 + Flask
- **Banco de Dados**: SQLite (via SQLAlchemy)
- **Frontend**: HTML5, CSS3 (Grid & Flexbox), JavaScript (Vanilla)
- **Gráficos**: Chart.js
- **Simulação**: Requests & Random (Simulação de hardware ESP32)

## 📋 Pré-requisitos

- Python 3.10 ou superior
- Pip (Gerenciador de pacotes do Python)

## 🔧 Instalação e Execução

1. **Clone o repositório**:
   ```bash
   git clone [https://github.com/SergioRamos-CS/iotG.git](https://github.com/SergioRamos-CS/iotG.git)
   cd iotG

2. **Crie um ambiente virtual**:

Bash
python -m venv venv
source venv/bin/scripts/activate  # Windows: venv\Scripts\activate

3. **Instale as dependências**:

Bash
pip install -r requirements.txt

4. **Inicie o Servidor Flask**:

Bash
python app.py

5. **Inicie o Simulador de Ambiente**:

Abra um novo terminal e execute:
Bash
python simulator.py

6. **Acesse no navegador**:
http://127.0.0.1:5000