# -*- coding: utf-8 -*-
"""
Pipeline OBI:
1) Baixa PDFs (Iniciação) para os anos configurados
2) Converte PDFs -> .md usando LlamaParse (com regras por ano)
3) Extrai questões dos .md no formato: ano,fase,nivel,titulo,enunciado,numero_questao,questao,alternativas
4) Apende as novas linhas ao final do Excel existente (SEM coluna id). Se não existir, cria.
"""

import os
import re
import time
from pathlib import Path
import pandas as pd

# ---- Web / Download
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from urllib.parse import urljoin
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager

# ---- LlamaParse para PDF -> MD
from llama_parse import LlamaParse

# ---- Logger
from Logger import configurar_logger
logger = configurar_logger()

# ==============================
# LlamaParse: API KEY
# ==============================
# Opção recomendada: defina LLAMA_CLOUD_API_KEY no ambiente do sistema
api_key = "llx-mzOE5hyJwlDzzbXTTJvo0DJZNSxi4tailp8QZRu9l6MyiBVK"  # opcional: coloque sua chave aqui se preferir
parser = LlamaParse(api_key=api_key, result_type="markdown")

# ==============================
# CONFIGURAÇÕES
# ==============================
ANOS = ["OBI2022"]                              # anos-alvo
BASE_DOWNLOAD_DIR = r"C:\MESTRADO\Downloads_OBI"   # onde salvar os PDFs baixados
DIR_MD_SAIDA = r"C:\MESTRADO\Downloads_OBI\md"     # onde salvar os .md convertidos
ARQUIVO_XLSX = r"C:\MESTRADO\Downloads_OBI\Questoes_OBI_Compilado.xlsx"  # planilha destino

# Colunas padrão para criar o Excel do zero (sem id)
DEFAULT_COLS = [
    'ano', 'fase', 'nivel', 'titulo', 'enunciado',
    'numero_questao', 'questao', 'alternativas'
]

# ==============================
# FUNÇÕES WEB (DOWNLOAD)
# ==============================
def configurar_webdriver_firefox():
    logger.info("Configurando WebDriver Firefox (headless).")
    options = Options()
    options.headless = True
    service = Service(GeckoDriverManager().install())
    return webdriver.Firefox(service=service, options=options)

def baixar_pdf(url, caminho_arquivo):
    try:
        resposta = requests.get(url, timeout=60)
        resposta.raise_for_status()
        Path(caminho_arquivo).parent.mkdir(parents=True, exist_ok=True)
        with open(caminho_arquivo, "wb") as f:
            f.write(resposta.content)
        logger.info(f"Baixado: {os.path.basename(caminho_arquivo)}")
    except Exception as e:
        logger.error(f"Erro ao baixar {url}: {e}")

def baixar_todos_links(driver, download_dir):
    links = driver.find_elements(By.CSS_SELECTOR, "a[href$='.pdf']")
    arquivos = [
        urljoin(driver.current_url, link.get_attribute("href"))
        for link in links if link.text.strip().startswith("Caderno de tarefas da prova")
    ]
    logger.info(f"--> Encontrados {len(arquivos)} arquivos em {driver.current_url}")
    for url in arquivos:
        nome_arquivo = os.path.basename(url)
        caminho_arquivo = os.path.join(download_dir, nome_arquivo)
        baixar_pdf(url, caminho_arquivo)

def baixar_iniciacao(ano: str):
    fases = ["fase1", "fase2", "fase3"]
    subfases = ["A", "B"]
    for fase in fases:
        try:
            # Caso especial OBI2020 fase 1 (turnos)
            if ano == "OBI2020" and fase == "fase1":
                links_fase1_2020 = {
                    "Turno A": "https://olimpiada.ic.unicamp.br/passadas/OBI2020/fase1/iniciacao-a/",
                    "Turno B": "https://olimpiada.ic.unicamp.br/passadas/OBI2020/fase1/iniciacao-b/"
                }
                for turno, link in links_fase1_2020.items():
                    pasta_turno = os.path.join(BASE_DOWNLOAD_DIR, ano, fase, turno)
                    Path(pasta_turno).mkdir(parents=True, exist_ok=True)
                    logger.info(f"Acessando {link} ({turno})")
                    driver = configurar_webdriver_firefox()
                    driver.get(link); time.sleep(2)
                    if "Not Found" not in driver.page_source:
                        logger.info(f"Página encontrada para {fase} {turno} de {ano}.")
                        baixar_todos_links(driver, pasta_turno)
                    else:
                        logger.warning(f"Página não encontrada para {fase} {turno} de {ano}.")
                    driver.quit()
                continue

            # Caso especial OBI2024 (rota cadernos/)
            if ano == "OBI2024":
                url_fase = f"https://olimpiada.ic.unicamp.br/passadas/{ano}/{fase}/iniciacao/cadernos/"
                pasta_fase = os.path.join(BASE_DOWNLOAD_DIR, ano, fase)
                Path(pasta_fase).mkdir(parents=True, exist_ok=True)
                logger.info(f"Acessando URL especial para OBI2024: {url_fase}")
                driver = configurar_webdriver_firefox()
                driver.get(url_fase); time.sleep(2)
                if "Not Found" not in driver.page_source:
                    logger.info(f"Página encontrada para {fase} de {ano}.")
                    baixar_todos_links(driver, pasta_fase)
                else:
                    logger.warning(f"Página não encontrada para {fase} de {ano}.")
                driver.quit()
                continue

            # Padrão geral
            url_fase = f"https://olimpiada.ic.unicamp.br/passadas/{ano}/{fase}/iniciacao/"
            pasta_fase = os.path.join(BASE_DOWNLOAD_DIR, ano, fase)
            Path(pasta_fase).mkdir(parents=True, exist_ok=True)
            logger.info(f"Acessando {url_fase}")
            driver = configurar_webdriver_firefox()
            driver.get(url_fase); time.sleep(2)
            if "Not Found" not in driver.page_source:
                logger.info(f"Página encontrada para {fase} de {ano}.")
                baixar_todos_links(driver, pasta_fase)
                driver.quit()
                continue

            logger.warning(f"Página não encontrada para {fase} de {ano}. Tentando subfases...")
            driver.quit()
            for sub in subfases:
                try:
                    url_sub = f"https://olimpiada.ic.unicamp.br/passadas/{ano}/{fase}{sub}/iniciacao/"
                    pasta_sub = os.path.join(BASE_DOWNLOAD_DIR, ano, f"{fase}{sub}")
                    Path(pasta_sub).mkdir(parents=True, exist_ok=True)
                    logger.info(f"Acessando subfase {fase}{sub}: {url_sub}")
                    driver_sub = configurar_webdriver_firefox()
                    driver_sub.get(url_sub); time.sleep(2)
                    if "Not Found" not in driver_sub.page_source:
                        logger.info(f"Página encontrada para subfase {fase}{sub} de {ano}.")
                        baixar_todos_links(driver_sub, pasta_sub)
                    else:
                        logger.warning(f"Subfase {fase}{sub} não encontrada para {ano}.")
                    driver_sub.quit()
                except Exception as e:
                    logger.error(f"Erro na subfase {fase}{sub} do ano {ano}: {e}")
        except Exception as e:
            logger.error(f"Erro na fase {fase} do ano {ano}: {e}")

# ==============================
# CONVERSÃO PDF -> MD (LlamaParse, recursivo)
# ==============================
def convert_pdfs_to_md_llama(input_dir: str | Path, output_dir: str | Path):
    """
    Converte TODOS os PDFs (recursivo) de input_dir para arquivos .md em output_dir
    usando LlamaParse, aplicando regras de páginas específicas por ano.
    Mantém a estrutura relativa de subpastas.
    """
    input_dir = Path(input_dir)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    year_pattern = re.compile(r'OBI(\d{4})', re.IGNORECASE)

    count = 0
    for raiz, _, arquivos in os.walk(input_dir):
        raiz = Path(raiz)
        for file_name in arquivos:
            if not file_name.lower().endswith(".pdf"):
                continue

            pdf_path = raiz / file_name
            try:
                # extrair ano do nome do arquivo
                m = year_pattern.search(file_name)
                year = int(m.group(1)) if m else None

                # processar com LlamaParse
                document = parser.load_data(str(pdf_path))

                # regras de páginas
                if year and year < 2009:
                    start_page, last_page = 1, None          # ignora a 1ª
                elif year and year == 2009:
                    start_page, last_page = 0, len(document) - 1  # ignora a última
                else:
                    start_page, last_page = 2, None          # ignora as 2 primeiras

                # montar markdown
                if len(document) > start_page:
                    extracted_text = "".join(doc.text for doc in document[start_page:last_page])
                else:
                    extracted_text = "".join(doc.text for doc in document)

                # preservar subpasta relativa
                rel = pdf_path.relative_to(input_dir).with_suffix(".md")
                md_file_path = output_dir / rel
                md_file_path.parent.mkdir(parents=True, exist_ok=True)
                md_file_path.write_text(extracted_text, encoding="utf-8")

                logger.info(f"Convertido PDF→MD: {pdf_path} -> {md_file_path}")
                count += 1

            except Exception as e:
                logger.error(f"Erro ao processar {pdf_path}: {e}")

    logger.info(f"Conversão concluída: {count} arquivo(s) PDF convertidos para .md")

# ==============================
# EXTRATOR .MD → REGISTROS (QUESTÕES) — robusto
# ==============================
class OBIQuestionExtractor:
    def __init__(self, input_dir: str, output_file: str):
        self.input_dir = Path(input_dir)
        self.output_file = Path(output_file)
        self.data = []

        # colunas padrão quando criar o xlsx do zero
        self.DEFAULT_COLS = [
            'ano', 'fase', 'nivel', 'titulo', 'enunciado',
            'numero_questao', 'questao', 'alternativas'
        ]
        
    def clean_text(self, text: str) -> str:
        """Limpa o texto removendo espaços extras e caracteres indesejados."""
        if not text:
            return ""
        text = re.sub(r'\r', ' ', text)
        text = re.sub(r'\n\s*\n', '\n', text)
        text = re.sub(r'[ \t]+', ' ', text)
        text = text.replace('|', ' ').replace('---', ' ')
        return text.strip()
    
    # ---------- META: ano/fase/nivel ----------
    def extract_file_info_from_path(self, file_path: Path) -> dict:
        """Extrai ano/fase/nível do NOME e, se preciso, do CAMINHO (pastas OBIYYYY/faseX)."""
        info = {'ano': 'desconhecido', 'fase': 'desconhecido', 'nivel': 'desconhecido'}
        name = file_path.name
        path_str = str(file_path).lower().replace('\\', '/')

        m = re.search(r'obi(\d{4})', name, re.IGNORECASE)
        if not m:
            m = re.search(r'obi(\d{4})', path_str, re.IGNORECASE)
        if m:
            info['ano'] = m.group(1)

        m = re.search(r'f(\d)i([12j])', name.lower())
        if m:
            fase, nivel_code = m.groups()
            info['fase'] = '1' if fase == '0' else fase
            info['nivel'] = {'0': '2', 'j': '0'}.get(nivel_code, nivel_code)

        if info['fase'] == 'desconhecido':
            m = re.search(r'/fase\s*([123])(?:[ab])?/', path_str)
            if m:
                info['fase'] = m.group(1)

        return info

    # ---------- PARSER “heading” (compatível com sua versão) ----------
    def _parse_with_headings(self, content: str) -> list:
        """Versão compatível com sua lógica por '#', com fallback de título."""
        sections = re.split(r'#\s+', content)
        problems = []
        current_problem = None
        
        for section in sections[1:]:
            lines = section.strip().split('\n')
            if not lines:
                continue
                
            section_title = lines[0].strip()
            section_content = '\n'.join(lines[1:]).strip()
            
            # ignora headers de caderno
            if 'obi' in section_title.lower() and any(x in section_title.lower() for x in ['fase', 'nível', 'nivel']):
                continue
            
            question_match = re.match(r'(?:quest[aã]o|QUEST[ÃA]O)\s*\.?\s*(\d+)\.?', section_title, re.IGNORECASE)
            
            if not question_match:
                current_problem = {
                    'titulo': self.clean_text(section_title).lower(),
                    'enunciado': self.clean_text(section_content).lower(),
                    'questoes': []
                }
                problems.append(current_problem)
            else:
                if current_problem:
                    numero = question_match.group(1)
                    # separa parte antes de (A)
                    question_parts = re.split(r'\(\s*A\s*\)', section_content, 1, flags=re.IGNORECASE)
                    questao_text = section_title[question_match.end():].strip()
                    
                    if len(question_parts) > 1:
                        if question_parts[0].strip():
                            extra = self.clean_text(question_parts[0])
                            questao_text = extra if not questao_text else (questao_text + " " + extra)
                        alternativas_text = "(A) " + question_parts[1]
                    else:
                        alternativas_text = section_content
                        
                    alternativas = self.extract_alternatives(alternativas_text)
                    alternativas_formatadas = '\n'.join([f"({k}) {v.lower()}" for k, v in sorted(alternativas.items())]).replace('\n', ' ')
                    
                    # fallback de título quando a seção anterior não tiver “título”
                    titulo_final = current_problem.get('titulo') or f"Questão {numero}"

                    current_problem['questoes'].append({
                        'numero': numero,
                        'questao': self.clean_text(questao_text).lower(),
                        'alternativas': alternativas_formatadas,
                        'titulo_fallback': titulo_final  # guardado para uso na montagem das linhas
                    })
        return problems

    # ---------- PARSER “flat” (não depende de '#') ----------
    def _split_questoes_blocks_flat(self, full_text: str):
        """Divide o texto em blocos por 'Questão N' (com ou sem heading)."""
        pat = re.compile(
            r'(?s)(?:^|\n+)\s*(?:#{1,6}\s*)?(?:Quest(?:[aã]o)|QUEST(?:[ÃA]O))\s*\.?\s*(\d+)[\s:\-–.]*\n?(.*?)(?=(?:^|\n+)\s*(?:#{1,6}\s*)?(?:Quest(?:[aã]o)|QUEST(?:[ÃA]O))\s*\.?\s*\d+[\s:\-–.]*|\Z)',
            re.IGNORECASE
        )
        return list(pat.finditer(full_text or ""))

    def _separate_enunciado_e_questao(self, pre_alt_text: str):
        """Última sentença com '?' vira 'questão'; resto vira 'enunciado'."""
        def _c(s: str):
            s = re.sub(r'\r', ' ', s or '')
            s = re.sub(r'\n\s*\n', '\n', s)
            s = re.sub(r'[ \t]+', ' ', s)
            return s.strip()
        txt = _c(pre_alt_text)
        qmatch = list(re.finditer(r'[^?]*\?', txt))
        if qmatch:
            last = qmatch[-1]
            enun = _c(txt[:last.start()])
            perg = _c(txt[last.start():last.end()])
            return enun, perg
        return txt, ""

    def _parse_flat(self, content: str) -> list:
        """Cada 'Questão N' vira um problema com título padrão."""
        problems = []
        blocks = self._split_questoes_blocks_flat(content)
        for m in blocks:
            numero = m.group(1)
            bloco = m.group(2) or ""

            partes = re.split(r'\(\s*A\s*\)', bloco, maxsplit=1, flags=re.IGNORECASE)
            if len(partes) == 2:
                pre_alt = partes[0]
                alternativas_texto = "(A) " + partes[1]
            else:
                pre_alt = bloco
                alternativas_texto = bloco

            alternativas = self.extract_alternatives(alternativas_texto)
            alternativas_formatadas = '\n'.join([f"({k}) {v.lower()}" for k, v in sorted(alternativas.items())]).replace('\n', ' ')

            enun, perg = self._separate_enunciado_e_questao(pre_alt)
            enun = self.clean_text(enun).lower()
            perg = self.clean_text(perg).lower()
            if not enun and pre_alt.strip():
                enun = self.clean_text(pre_alt).lower()

            problems.append({
                'titulo': f"Questão {numero}",  # título garantido
                'enunciado': enun,
                'questoes': [{
                    'numero': numero,
                    'questao': perg,
                    'alternativas': alternativas_formatadas,
                    'titulo_fallback': f"Questão {numero}"
                }]
            })
        return problems

    # ---------- Alternativas ----------
    def extract_alternatives(self, text: str) -> dict:
        """Extrai as alternativas do texto da questão."""
        alternatives = {}
        alt_pattern = re.compile(r'\(\s*([A-E])\s*\)\s*(.*?)(?=\(\s*[A-E]\s*\)|\Z)', re.DOTALL | re.IGNORECASE)
        for match in alt_pattern.finditer(text or ""):
            letter, content = match.groups()
            alternatives[letter.upper()] = self.clean_text(content).replace('\n', ' ')
        return alternatives
    
    def process_file(self, file_path: Path):
        try:
            content = file_path.read_text(encoding='utf-8')

            # 1) tenta parser por headings
            problems = self._parse_with_headings(content)

            # Se não encontrou nenhuma questão via headings, usa o parser flat
            total_q_headings = sum(len(p.get('questoes', [])) for p in problems)
            if total_q_headings == 0:
                problems = self._parse_flat(content)

            file_info = self.extract_file_info_from_path(file_path)

            for problem in problems:
                titulo_base = problem.get('titulo') or "Questão"
                for question in problem.get('questoes', []):
                    # título final: preferir o 'titulo' do problema, senão fallback
                    titulo_final = titulo_base or question.get('titulo_fallback') or f"Questão {question.get('numero','')}"
                    self.data.append({
                        'ano': file_info['ano'],
                        'fase': file_info['fase'],
                        'nivel': file_info['nivel'],
                        'titulo': titulo_final,
                        'enunciado': problem.get('enunciado', ''),
                        'numero_questao': question.get('numero', ''),
                        'questao': question.get('questao', ''),
                        'alternativas': question.get('alternativas', '')
                    })
        except Exception as e:
            print(f"⚠️ Erro ao processar {file_path.name}: {str(e)}")
    
    # ---------- XLSX (append ou cria) ----------
    def save_to_xlsx(self):
        if not self.data:
            print("⚠️ Nenhuma questão foi extraída.")
            return
        
        df_new = pd.DataFrame(self.data)

        # fallback final para título
        if 'titulo' in df_new.columns:
            mask = df_new['titulo'].isna() | (df_new['titulo'].astype(str).str.strip() == "")
            if 'numero_questao' in df_new.columns:
                df_new.loc[mask, 'titulo'] = "Questão " + df_new.loc[mask, 'numero_questao'].astype(str)

        out = self.output_file
        out = out if isinstance(out, Path) else Path(out)
        out.parent.mkdir(parents=True, exist_ok=True)

        if out.exists():
            try:
                df_old = pd.read_excel(out, engine='openpyxl')
            except Exception:
                df_old = pd.DataFrame(columns=self.DEFAULT_COLS)

            existing_cols = list(df_old.columns)
            # completa df_new com colunas existentes; remove extras
            for col in existing_cols:
                if col not in df_new.columns:
                    df_new[col] = pd.NA
            df_new = df_new[existing_cols]

            df_all = pd.concat([df_old, df_new], ignore_index=True)
            save_cols = existing_cols
        else:
            # cria do zero com colunas padrão
            for col in self.DEFAULT_COLS:
                if col not in df_new.columns:
                    df_new[col] = pd.NA
            df_all = df_new[self.DEFAULT_COLS]
            save_cols = self.DEFAULT_COLS

        df_all.to_excel(out, index=False, engine='openpyxl', columns=save_cols)
        print(f"✅ {len(df_new)} questões salvas/apendadas em {out}")
    
    def extract(self):
        if not self.input_dir.exists():
            raise FileNotFoundError(f"Diretório não encontrado: {self.input_dir}")
        
        # Busca RECURSIVA
        files = list(self.input_dir.rglob("*.md"))
        if not files:
            raise FileNotFoundError(f"Nenhum arquivo .md encontrado (recursivo) em {self.input_dir}")
        
        for file_path in files:
            self.process_file(file_path)
        
        self.save_to_xlsx()

# ==============================
# MAIN
# ==============================
if __name__ == "__main__":
    logger.info(">>> Pipeline OBI: Download PDFs → MD (LlamaParse) → Extração (.md) → Append XLSX")

    # 1) DOWNLOAD DOS PDFs
    for ano in ANOS:
        logger.info(f"[DOWNLOAD] {ano} - Iniciação")
        try:
            baixar_iniciacao(ano)
        except Exception as e:
            logger.error(f"Erro geral no ano {ano}: {e}")

    # 2) CONVERTER TODOS OS PDFs BAIXADOS PARA .MD (via LlamaParse)
    try:
        convert_pdfs_to_md_llama(BASE_DOWNLOAD_DIR, DIR_MD_SAIDA)
    except Exception as e:
        logger.error(f"Falha na conversão PDF→MD: {e}")

    # 3) EXTRAIR DAS .MD (recursivo, parser robusto)
    extractor = OBIQuestionExtractor(DIR_MD_SAIDA, ARQUIVO_XLSX)
    novas_linhas = extractor.extract()

    # 4) ADICIONAR A QUESTÃO NA PLANILHA EXISTENTE
    if not novas_linhas:
        logger.warning("Nenhuma nova questão extraída das .md. Nada a apendar no Excel.")
    else:
        try:
            extractor.save_to_xlsx(novas_linhas, ARQUIVO_XLSX)
        except Exception as e:
            logger.error(f"Falha ao salvar no Excel: {e}")

    logger.info(">>> Fim do pipeline OBI.")