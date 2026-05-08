# 📊 Dashboard de Economia Russa — Streamlit

Dashboard interativo com dados macroeconômicos da Rússia (1999–2025),
incluindo PIB, emprego, câmbio e receitas orçamentárias.


## ✅ Pré-requisitos

- Python 3.10 ou superior
- pip instalado

## 🔧 Instalação

### 1. Instalar o pip (se ainda não tiver)

```bash
sudo apt update
sudo apt install python3-pip
```

### 2. Clonar ou baixar o projeto

```bash
# Se tiver git:
git clone https://github.com/CristianoSantan/dash_petroleo.git
cd dash_petroleo
```

### 3. (Recomendado) Criar um ambiente virtual

```bash
python3 -m venv venv
source venv/bin/activate
```

> Você vai ver `(venv)` no início do terminal — isso significa que o ambiente está ativo.

### 4. Instalar as dependências

```bash
pip install streamlit pandas plotly openpyxl
```

> Se aparecer o erro `externally-managed-environment`, adicione a flag:
> ```bash
> pip install streamlit pandas plotly openpyxl --break-system-packages
> ```

## ▶️ Rodando a aplicação

```bash
streamlit run app.py
```

O terminal vai exibir algo como:

```
  Local URL: http://localhost:8501
  Network URL: http://192.168.x.x:8501
```

Abra o endereço `http://localhost:8501` no navegador. O dashboard carrega automaticamente.

---

## 🔄 Parando a aplicação

No terminal, pressione:

```
Ctrl + C
```