# 🤖 Automação OBI – Download e Extração de Questões (Iniciação)

Script em **Python** que automatiza o download, conversão e extração das questões dos **“Cadernos de Tarefas das Provas”** da modalidade **Iniciação** da Olimpíada Brasileira de Informática (OBI).

A aplicação realiza todo o processo de forma automática: navega pelo site da OBI, identifica e baixa os PDFs corretos, converte-os em Markdown com o **LlamaParse** e extrai as questões para uma planilha Excel consolidada.  
O objetivo é otimizar a coleta de dados para análises, treinamentos e experimentos de classificação de questões.

---

## 🚀 Funcionalidades

- Acessa automaticamente as páginas da OBI por **ano e fase** (fase1/2/3 e subfases 1A/1B/2A/2B).  
- Baixa apenas os PDFs cujo link começa com **“Caderno de tarefas da prova”**.  
- Faz o download direto via `requests` (sem abrir PDF no navegador).  
- Converte todos os PDFs para `.md` usando **LlamaParse**, preservando a estrutura de subpastas.  
- Varre recursivamente os `.md`, extrai as **questões**, e apenda os dados no arquivo Excel (cria se não existir).  
- Cria automaticamente pastas de **downloads**, **markdowns** e **logs**.  
- Evita timeouts e falhas comuns no uso do navegador via Selenium.  

---

## 🛠️ Tecnologias e Bibliotecas

- [Python 3.13.2](https://www.python.org/)  
- [Selenium](https://selenium.dev/)  
- [webdriver_manager](https://github.com/SergeyPirogov/webdriver_manager)  
- [Requests](https://docs.python-requests.org/)  
- [LlamaParse API](https://docs.llamaindex.ai/)  
- [Pandas](https://pandas.pydata.org/)  
- [OpenPyXL](https://openpyxl.readthedocs.io/en/stable/)  

---

## ⚙️ Instalação e Configuração

### 1️⃣ (Opcional) Criar e ativar ambiente virtual (Windows)
```bash
python -m venv AmbienteVirtual
cd AmbienteVirtual\Scripts
activate
cd ../..
code .

2️⃣ Instalar dependências
pip install -r requeriments.txt

3️⃣ Configurar variáveis principais

No arquivo main.py, edite:
anos = ["OBI2018", "OBI2019", "OBI2020", "OBI2021", "OBI2022", "OBI2023", "OBI2024"]
base_download_dir = r"C:\Users\seu.usuario\Downloads\Downloads_OBI"

Ajuste os anos conforme necessidade.

Altere o caminho base_download_dir para o diretório de destino dos downloads.

O script detecta automaticamente fases normais e subfases (fase1, fase1A etc).

4️⃣ Configurar a chave da LlamaParse
setx LLAMA_CLOUD_API_KEY "sua_chave_aqui"

▶️ Execução
automacao_obi> python3 main.py

Exemplo de saída:
=== Baixando arquivos de OBI2018 - Iniciação ===
→ Encontrados 3 arquivos em https://olimpiada.ic.unicamp.br/passadas/OBI2018/fase1/iniciacao/
   ✅ Baixado: ProvaOBI2018_f1ij.pdf
   ✅ Baixado: ProvaOBI2018_f1ix.pdf
...

---

## 🧩 Como Funciona (Resumo Técnico)

- Selenium (headless) abre cada URL de Iniciação (por ano e fase).

- Coleta todos os links <a href$='.pdf'> cujo texto começa com “Caderno de tarefas da prova”.

- Faz download direto via requests.get() para a pasta de destino.

- LlamaParse converte todos os PDFs em .md, preservando a hierarquia por ano/fase.

- Um extrator percorre os arquivos Markdown:

- Identifica blocos “Questão N”;

- Separa enunciado, pergunta e alternativas (A–E);

- Exporta os dados para o Excel (cria caso não exista).

---

## 📂 Estrutura do Projeto
Automacao_OBI/
├── main.py                 → Script principal
├── Logger.py               → Classe de logging e mensagens
├── requeriments.txt        → Dependências do projeto
├── README.md               → Documentação do projeto
│
├── AmbienteVirtual/        → (opcional) Ambiente virtual Python
│
├── Downloads_OBI/          → PDFs, arquivos .md e planilha final
│   ├── md/                 → Arquivos convertidos em Markdown
│   └── resultados.xlsx     → Planilha consolidada
│
└── logs/                   → Arquivos de log da execução

---

🧠 Boas Práticas

- Respeite o robots.txt e os termos de uso do site da OBI.

- Evite execuções paralelas desnecessárias.

- Mantenha logs e verifique erros por ano/fase/arquivo.

- Não redistribua PDFs sem autorização dos autores originais.

---

## 📞 Contato

- Autor: Thiago Almeida
- GitHub: @thiagocghc

- WhatsApp: 67 98402-6511