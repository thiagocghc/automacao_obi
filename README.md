🧠 Automação OBI – Download e Extração de Questões (Iniciação)

Script em Python que automatiza o download, conversão e extração de questões dos “Cadernos de Tarefas das Provas” da modalidade Iniciação da Olimpíada Brasileira de Informática (OBI).

A aplicação navega automaticamente pelas páginas da OBI, faz o download dos arquivos PDF das provas, converte-os para Markdown e extrai as questões para uma planilha Excel final, padronizando o processo de coleta de dados.

🚀 Funcionalidades

Acessa automaticamente as URLs da OBI (por ano e fase) na modalidade Iniciação.

Identifica e baixa apenas os PDFs cujo link começa com “Caderno de tarefas da prova”.

Faz o download direto via requests (sem abrir PDF no navegador).

Converte PDFs para .md usando LlamaParse, preservando a hierarquia de subpastas.

Extrai questões de todos os arquivos .md e anexa no Excel (criando se não existir).

Suporte a fases e subfases (fase1, fase2, fase3, fase1A, fase1B, etc).

Geração automática de logs e estrutura de diretórios organizada.

🛠️ Tecnologias e Bibliotecas

Python 3.13.2

Selenium
 (execução headless via Firefox + geckodriver)

webdriver_manager

requests

LlamaParse API

pandas

openpyxl

📦 Instalação
1️⃣ (Opcional) Criar e ativar ambiente virtual no Windows
python -m venv AmbienteVirtual
cd AmbienteVirtual\Scripts
activate
cd ../..
code .


2️⃣ Instalar dependências
pip install -r requeriments.txt

⚙️ Configuração

Edite no arquivo main.py:
anos = ["OBI2018", "OBI2019", "OBI2020", "OBI2021", "OBI2022", "OBI2023", "OBI2024"]
base_download_dir = r"C:\Users\seu.usuario\Downloads\Downloads_OBI"
Ajuste os anos conforme a necessidade.

Troque base_download_dir para o diretório de destino no seu sistema.

O script busca automaticamente fases normais e subfases (fase1, fase1A, etc).

🔑 Configurar chave da LlamaParse
setx LLAMA_CLOUD_API_KEY "sua_chave_aqui"

▶️ Execução
python3 main.py

Exemplo de saída

=== Baixando arquivos de OBI2018 - Iniciação ===
→ Encontrados 3 arquivos em https://olimpiada.ic.unicamp.br/passadas/OBI2018/fase1/iniciacao/
   ✅ Baixado: ProvaOBI2018_f1ij.pdf
   ✅ Baixado: ProvaOBI2018_f1ix.pdf
...

🔍 Funcionamento Técnico

Selenium (modo headless) abre cada URL de Iniciação.

Coleta todos os <a href$='.pdf'> e filtra apenas os que começam com “Caderno de tarefas da prova”.

Cada PDF é baixado diretamente via requests.get() para a pasta correta.

LlamaParse converte PDFs em .md, preservando subpastas por ano/fase.

O script percorre os .md, identifica blocos “Questão N”, separa enunciado, pergunta e alternativas (A–E), e salva no Excel (criando se não existir).

📂 Estrutura do Projeto
<pre lang="markdown">``` Automacao_OBI/ ├── main.py ├── Logger.py ├── requeriments.txt ├── README.md ├── AmbienteVirtual/ → (opcional) Ambiente virtual ├── Downloads_OBI/ → PDFs, arquivos .md e planilha Excel final │ ├── md/ │ └── resultados.xlsx └── logs/ ```</pre>

✅ Boas Práticas

Respeite o robots.txt e os termos de uso do site da OBI.

Evite execuções paralelas desnecessárias (um ano/fase por vez é suficiente).

Mantenha logs claros e identifique erros por ano/fase/arquivo.

Não redistribua os PDFs sem permissão dos autores originais.

💬 Contato

Autor: Thiago Almeida
GitHub: @thiagocghc

WhatsApp: 67 98402-6511
