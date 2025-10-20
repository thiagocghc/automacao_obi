Automação OBI – Download dos “Cadernos de tarefas das provas” (Iniciação)

Script em Python que: navega pelo portal da OBI e baixa apenas os PDFs cujo link começa com “Caderno de tarefas da prova” na modalidade Iniciação (anos com fases normais fase1/2/3 e anos com subfases fase1A/1B/2A/2B);

  --> converte esses PDFs para Markdown (.md) usando LlamaParse (com regras de páginas por ano);
  --> extrai as questões dos .md e append no arquivo Excel final (cria se não existir).

 - O que o script faz?

  --> Acessa automaticamente as URLs de Iniciação para cada ano configurado.
  --> Identifica os links de PDF cujo texto do link começa com “Caderno de tarefas da prova”.
  --> Faz download direto via requests (não abre PDF no navegador).
  --> Converte todos os PDFs (busca recursiva) para .md, preservando a hierarquia de subpastas.
  --> Varre recursivamente os .md, extrai as questões e apenda no Excel sem coluna id.
  --> Se a planilha não existir, cria com as colunas padrão.

 - Pré-requisitos

--> Python 3.9+ (Nesse código estou utilizando o Python Mais Atual "Python 3.13.2")
--> pip (Para baixar as Bibliotecas necessárias dentro do arquivo "requeriments.txt")
--> Firefox (o script usa Selenium + geckodriver; o webdriver_manager baixa o driver automaticamente)
--> Sistema testado em Windows (ajuste caminhos no base_download_dir se necessário).

 - Instalação
# 1) (opcional) criar e ativar venv no Windows
python -m venv AmbienteVirtual (Cria o Ambiente Virtual)
cd AmbienteVirtual (Entra na pasta do Ambiente Virtual)
cd Scripts (Entra na pasta de Scripts)
activate (Ativa o Ambiente Virtual para uso)
cd .. (Volta uma pasta)
cd .. (Volta uma pasta)
code . (Inicia o VsCode)

# 2) instalar dependências
pip install -r requeriments.txt

 - Configuração

Edite no arquivo principal:

anos = ["OBI2018", "OBI2019", "OBI2020", "OBI2021", "OBI2022", "OBI2023", "OBI2024"]
base_download_dir = r"C:\Users\seu.usuario\Downloads\Downloads_OBI"

- Ajuste anos conforme a necessidade.
- Troque base_download_dir para a sua pasta de destino.
- O script procura automaticamente por fase1, fase2, fase3 e, se não encontrar, tenta fase1A, fase1B (e o mesmo para fase2, fase3).

# 3) LlamaParse – configuração da chave
setx LLAMA_CLOUD_API_KEY "sua_chave_aqui"

▶ Execução:
python main.py

Exemplo de saída:

=== Baixando arquivos de OBI2018 - Iniciação ===
→ Encontrados 3 arquivos em https://olimpiada.ic.unicamp.br/passadas/OBI2018/fase1/iniciacao/
   ✅ Baixado: ProvaOBI2018_f1ij.pdf
   ✅ Baixado: ProvaOBI2018_f1ix.pdf
...

 - Como funciona (resumo técnico):
Selenium (headless) abre cada URL de Iniciação por ano/fase.

  --> Coleta todos os <a href$='.pdf'> e filtra os cujo .text começa com “Caderno de tarefas da prova”.
  --> Para cada PDF, faz download direto via requests.get() para a pasta adequada.
  --> LlamaParse converte todos os PDFs (recursivo) em .md, preservando a estrutura de subpastas.
  --> O extrator percorre os .md (recursivo), detecta blocos “Questão N”, separa enunciado/pergunta por heurística (última frase com ?), lê alternativas (A)…(E) e salva/apenda no Excel.

Esse desenho evita:
  --> timeouts do geckodriver ao abrir PDFs no navegador;
  --> problemas de salvamento aleatório (o download é por código);
  --> falhas quando o Excel ainda não existe (ele é criado automaticamente).

📂 Estrutura do projeto
Automacao_OBI/
  main.py
  Logger.py
  README.md
  requeriments.txt
  AmbienteVirtual/          # (opcional) venv
  Downloads_OBI/            # PDFs + md + planilha final
    md/
  logs/

- Boas práticas

- Respeite o robots.txt e os termos do site.
- Evite cargas excessivas: não rode com paralelismo alto sem necessidade.
- Faça logs claros (o script já imprime ano/fase/URL/arquivo).