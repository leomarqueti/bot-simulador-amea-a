import pyautogui
import time
import subprocess
import webbrowser
import random
import os

# Importa os módulos do Selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, WebDriverException, TimeoutException

# --- Configurações Iniciais ---
pyautogui.PAUSE = 0.3 # Pausa geral base entre cada ação do pyautogui

DURACAO_MAXIMA_SIMULACAO = 2400 # 40 minutos (para um teste mais longo)

# Lista de URLs "normais"
URLS_NORMAIS = [
    'https://www.google.com',
    'https://www.wikipedia.org/wiki/Ciberseguran%C3%A7a',
    'https://www.reddit.com/r/cybersecurity/',
    'https://www.bbc.com/news/technology',
    'https://br.linkedin.com/feed',
    'https://github.com/trending',
    'https://www.infosecurity-magazine.com/'
]

# URLs do YouTube
URLS_YOUTUBE = [
    'https://www.youtube.com/watch?v=dQw4w9WgXcQ', # Rick Astley de verdade (ou um vídeo aleatório)
    'https://www.youtube.com/watch?v=gT5sH2H5G3o',
    'https://www.youtube.com/watch?v=F_Sc064mIuY'
]

# --- Configurações para Cenários com Selenium ---
# URL de um site de phishing SIMULADO (para o bot tentar logar)
# CRIE OU ENCONTRE UMA PÁGINA DE LOGIN DE TESTE SEGURA QUE VOCÊ CONTROLA PARA ISSO.
# NUNCA USE UM SITE REAL DE PHISHING!
URL_PHISHING_LOGIN = 'http://test.fakeloginsite.com/login' # Mude para seu site de teste!

# Seus "dados" de login falsos para o phishing
PHISHING_USERNAME = 'estagiario.teste@empresa.com.br'
PHISHING_PASSWORD = 'SenhaFraca123!'

# Outra URL "suspeita" para acesso direto (sem login)
URL_SUSPEITA_DIRETA = 'http://site-de-malware-simulado-para-teste.com/download'

# Caminho do ChromeDriver (se estiver na mesma pasta do script, use apenas o nome)
# Se estiver em outro lugar, coloque o caminho completo: r'C:\caminho\para\chromedriver.exe'
CHROMEDRIVER_PATH = 'chromedriver.exe'

# --- Funções de Ação Comuns e de Realismo (as mesmas do script anterior) ---

def pausa_humana(min_seg=0.5, max_seg=2.0):
    tempo_pausa = random.uniform(min_seg, max_seg)
    # print(f"Pausando por {tempo_pausa:.2f} segundos para 'pensar'...")
    time.sleep(tempo_pausa)

def mover_mouse_organicamente(x, y, duration_min=0.5, duration_max=1.5):
    # print(f"Movendo o mouse para ({x},{y})...")
    pyautogui.moveTo(x, y, duration=random.uniform(duration_min, duration_max), tween=pyautogui.easeOutQuad)
    pausa_humana(0.1, 0.5)

def clicar_organicamente(x, y):
    mover_mouse_organicamente(x + random.randint(-5, 5), y + random.randint(-5, 5))
    pyautogui.click()
    pausa_humana(0.5, 1.0)

def digitar_com_erros(texto, interval_min=0.03, interval_max=0.1):
    for char in texto:
        pyautogui.write(char, interval=random.uniform(interval_min, interval_max))
        if random.random() < 0.04:
            pyautogui.write(random.choice(['a', 's', 'd', 'f', 'g', 'h', 'j']), interval=random.uniform(0.01, 0.05))
            pausa_humana(0.05, 0.15)
            pyautogui.press('backspace', presses=1, interval=random.uniform(0.05, 0.15))
            pausa_humana(0.05, 0.15)
    pausa_humana(0.5, 1.5)

def abrir_aplicativo(app_name, wait_time_min=3, wait_time_max=5):
    print(f"Abrindo aplicativo: {app_name}...")
    try:
        subprocess.Popen([app_name], shell=True)
        pausa_humana(wait_time_min, wait_time_max)
    except FileNotFoundError:
        print(f"Erro: '{app_name}' não encontrado. Verifique se está instalado e no PATH.")
    except Exception as e:
        print(f"Ocorreu um erro ao tentar abrir '{app_name}': {e}")

def fechar_janela_ativa():
    print("Fechando janela ativa...")
    pyautogui.hotkey('alt', 'f4')
    pausa_humana(1, 2)

def alternar_janelas():
    print("Alternando janelas (Alt+Tab)...")
    pyautogui.hotkey('alt', 'tab')
    pausa_humana(0.5, 1)
    pyautogui.hotkey('alt', 'tab')
    pausa_humana(0.5, 1.5)

def mostrar_desktop_e_voltar():
    print("Mostrando/escondendo área de trabalho (Win+D)...")
    pyautogui.hotkey('win', 'd')
    pausa_humana(1, 2)
    pyautogui.hotkey('win', 'd')
    pausa_humana(1, 2)

def abrir_menu_iniciar():
    print("Abrindo e fechando menu Iniciar...")
    pyautogui.press('win')
    pausa_humana(0.5, 1.5)
    pyautogui.press('esc')
    pausa_humana(0.5, 1.0)

# --- Funções de Navegação e Interação Web com Selenium ---

# Variável global para o driver do Selenium
driver = None

def inicializar_driver_chrome():
    """Inicializa o driver do Chrome."""
    global driver
    if driver is None:
        print("Inicializando Chrome WebDriver...")
        try:
            # Configurações para não fechar o navegador imediatamente e para modo headless (opcional)
            chrome_options = Options()
            # chrome_options.add_argument("--headless") # Descomente para rodar sem interface gráfica (não recomendado para simulação visual)
            # chrome_options.add_experimental_option("detach", True) # Mantém o navegador aberto após o script terminar

            service = Service(executable_path=CHROMEDRIVER_PATH)
            driver = webdriver.Chrome(service=service, options=chrome_options)
            driver.maximize_window() # Maximiza a janela do navegador
            pausa_humana(2, 4)
            print("Chrome WebDriver inicializado com sucesso.")
        except WebDriverException as e:
            print(f"ERRO: Não foi possível inicializar o ChromeDriver. Verifique se 'chromedriver.exe' está na pasta correta e se a versão corresponde ao seu Chrome. Erro: {e}")
            driver = None # Garante que a variável driver seja None em caso de falha
            # Se der erro aqui, o bot pode tentar usar webbrowser.open como fallback, ou parar as ações web
            
def fechar_driver_chrome():
    """Fecha o navegador e o driver do Selenium."""
    global driver
    if driver:
        print("Fechando Chrome WebDriver...")
        driver.quit()
        driver = None
        pausa_humana(1, 2)

def navegar_e_tentar_phishing_login():
    """Cleitinho navega para um site de phishing simulado e tenta fazer login."""
    global driver
    if driver is None:
        inicializar_driver_chrome()
        if driver is None: # Se ainda não inicializou, fallback para webbrowser
            print("Selenium falhou. Usando webbrowser para URL de phishing.")
            webbrowser.open(URL_PHISHING_LOGIN)
            pausa_humana(5, 10)
            return

    print(f"*** AÇÃO SUSPEITA: Cleitinho tentando login em site de phishing: {URL_PHISHING_LOGIN} ***")
    try:
        driver.get(URL_PHISHING_LOGIN)
        pausa_humana(3, 7) # Tempo para a página carregar

        mover_mouse_organicamente(random.randint(400, 600), random.randint(300, 400)) # Mouse sobre a área do formulário

        # Tenta encontrar campos de usuário e senha (você pode precisar ajustar os IDs/Nomes)
        # Inspecione a página de login simulada para encontrar os corretores 'name' ou 'id'
        try:
            username_field = driver.find_element(By.NAME, "username") # ou By.ID, By.CSS_SELECTOR
            password_field = driver.find_element(By.NAME, "password") # ou By.ID, By.CSS_SELECTOR
            login_button = driver.find_element(By.TAG_NAME, "button") # ou By.ID, By.CLASS_NAME, By.CSS_SELECTOR

            print("Preenchendo credenciais falsas...")
            digitar_com_erros(PHISHING_USERNAME, interval_min=0.05, interval_max=0.2)
            username_field.send_keys(PHISHING_USERNAME) # Selenium digita direto, não usa pyautogui

            pausa_humana(1, 2)

            digitar_com_erros(PHISHING_PASSWORD, interval_min=0.05, interval_max=0.2)
            password_field.send_keys(PHISHING_PASSWORD) # Selenium digita direto

            pausa_humana(1, 3)
            mover_mouse_organicamente(login_button.location['x'] + random.randint(5,20), login_button.location['y'] + random.randint(5,10))
            pausa_humana(0.5, 1)

            print("Clicando no botão de login...")
            login_button.click()
            pausa_humana(5, 10) # Tempo para a submissão do formulário

        except NoSuchElementException:
            print("AVISO: Campos de login não encontrados na página de phishing. Verifique os seletores.")
            # Se não encontrar os campos, talvez o bot só navegue e feche
            pausa_humana(3, 5)

    except TimeoutException:
        print("Erro de timeout ao carregar a página de phishing.")
    except Exception as e:
        print(f"Erro inesperado durante a tentativa de phishing: {e}")
    finally:
        # Após a ação, o Cleitinho fecha a aba/navegador para disfarçar
        # Podemos fechar só a aba ou o navegador todo, dependendo do que já estiver aberto
        # driver.close() # Fecha a aba atual
        fechar_driver_chrome() # Fecha o navegador todo


def acao_suspeita_download_malware_simulado():
    """Cleitinho navega para uma URL suspeita e tenta um download."""
    global driver
    if driver is None:
        inicializar_driver_chrome()
        if driver is None:
            print("Selenium falhou. Usando webbrowser para URL de download.")
            webbrowser.open(URL_SUSPEITA_DIRETA)
            pausa_humana(5, 10)
            return

    print(f"*** AÇÃO SUSPEITA: Cleitinho tentando download de malware simulado: {URL_SUSPEITA_DIRETA} ***")
    try:
        driver.get(URL_SUSPEITA_DIRETA)
        pausa_humana(5, 10) # Tempo para a página carregar e o download iniciar

        # Aqui, Selenium não vai "clicar" no download, mas a tentativa de acesso à URL já gera logs.
        # Para um download real, precisaríamos de uma página com um botão de download clicável
        # e identificar esse botão com driver.find_element().click()

    except TimeoutException:
        print("Erro de timeout ao carregar a página de download de malware.")
    except Exception as e:
        print(f"Erro inesperado durante a tentativa de download: {e}")
    finally:
        fechar_driver_chrome()

# --- Funções de Ação Normal do Cleitinho (utilizando Selenium ocasionalmente) ---

def acao_normal_navegacao():
    """Cleitinho navega para sites normais ou YouTube."""
    global driver
    if random.random() < 0.2: # 20% de chance de usar Selenium para navegação normal
        if driver is None:
            inicializar_driver_chrome()
            if driver is None: # Fallback se Selenium falhar
                print("Selenium falhou para navegação normal. Usando webbrowser.")
                url = random.choice(URLS_NORMAIS + URLS_YOUTUBE)
                webbrowser.open(url)
                pausa_humana(5, 10)
                return

        url = random.choice(URLS_NORMAIS + URLS_YOUTUBE)
        print(f"Navegação normal (Selenium): {url}")
        try:
            driver.get(url)
            pausa_humana(3, 8)
            mover_mouse_organicamente(random.randint(200, 800), random.randint(200, 600), duration_min=0.5, duration_max=1.0)
            # Simula rolagem dentro do navegador via Selenium
            driver.execute_script("window.scrollBy(0, document.body.scrollHeight/2);")
            pausa_humana(1, 3)
            driver.execute_script("window.scrollBy(0, -document.body.scrollHeight/4);")
            pausa_humana(1, 3)
        except WebDriverException as e:
            print(f"Erro de Selenium durante navegação normal: {e}. Fechando driver e usando webbrowser.")
            fechar_driver_chrome()
            webbrowser.open(url) # Fallback
            pausa_humana(5, 10)
        finally:
            if random.random() < 0.5: # 50% de chance de fechar o navegador após a navegação normal
                fechar_driver_chrome()
            else:
                pass # Deixa o navegador aberto para a próxima ação Selenium
    else: # 80% de chance de usar webbrowser para navegação normal (mais leve)
        url = random.choice(URLS_NORMAIS + URLS_YOUTUBE)
        print(f"Navegação normal (webbrowser): {url}")
        webbrowser.open(url)
        pausa_humana(3, 8)
        # Aqui, o pyautogui faz a rolagem (fora do controle do Selenium)
        pyautogui.scroll(random.randint(-1500, -300))
        pausa_humana(1, 3)
        pyautogui.scroll(random.randint(100, 500))
        pausa_humana(1, 3)
        fechar_janela_ativa() # Fecha a aba/janela do navegador (pyautogui)

# Funções restantes (trabalho_documento, explorador_arquivos, comandos_cmd) permanecem as mesmas do script anterior,
# pois não dependem de interação web inteligente.

def acao_normal_trabalho_documento():
    print("Simulando trabalho em um documento (Bloco de Notas)...")
    abrir_aplicativo('notepad.exe', wait_time_min=1.5, wait_time_max=3)
    conteudo_documento = [
        "Relatório de status do projeto X. Concluídas as tarefas de análise de requisitos.",
        "Notas da reunião de hoje: discutir a implementação da nova política de segurança da informação.",
        "Rascunho de e-mail para o gerente: solicitando acesso a recursos adicionais para o projeto Y.",
        "Pesquisando sobre 'melhores práticas de hardening de servidores Windows' para a equipe de Blue Team.",
        "Lista de tarefas para amanhã: revisar logs do firewall, atualizar documentação da rede interna.",
        "Teste de documentação interna para a equipe. Verificando o acesso aos compartilhamentos.",
        "Planejamento de rotina diária de verificação de emails e calendários."
    ]
    texto_para_digitar = random.choice(conteudo_documento) + "\n\n" + \
                         "Data: " + time.strftime("%Y-%m-%d %H:%M:%S") + "\n" + \
                         "Conteúdo gerado por simulador de usuário 'Cleitinho', o estagiário dedicado."
    digitar_com_erros(texto_para_digitar)
    pausa_humana(3, 7)
    mover_mouse_organicamente(random.randint(100, 500), random.randint(100, 300))
    if random.random() < 0.6:
        pyautogui.hotkey('ctrl', 's')
        pausa_humana(0.5, 1.0)
        if random.random() < 0.5:
            pyautogui.press('n')
            print("Cleitinho não salvou o documento.")
        else:
            pyautogui.press('escape')
            print("Cleitinho cancelou o salvamento do documento.")
        pausa_humana(0.5, 1.0)
    fechar_janela_ativa()

def acao_normal_explorador_arquivos():
    print("Cleitinho navegando no Explorador de Arquivos...")
    abrir_aplicativo('explorer.exe', wait_time_min=2, wait_time_max=4)
    mover_mouse_organicamente(random.randint(100, 300), random.randint(50, 150))
    pyautogui.write('C:\\')
    pyautogui.press('enter')
    pausa_humana(1, 2)
    pastas_comuns = ['Users', 'Program Files', 'Windows', 'ProgramData']
    if random.random() < 0.7:
        pyautogui.write(f'C:\\{random.choice(pastas_comuns)}')
        pyautogui.press('enter')
        pausa_humana(2, 4)
        pyautogui.press('backspace', presses=random.randint(1,2))
        pausa_humana(1, 2)
    fechar_janela_ativa()

def acao_normal_outros_apps():
    apps_comuns = ['calc.exe', 'mspaint.exe']
    app_escolhido = random.choice(apps_comuns)
    print(f"Cleitinho abrindo aplicativo comum: {app_escolhido}")
    abrir_aplicativo(app_escolhido, wait_time_min=2, wait_time_max=5)
    fechar_janela_ativa()

def acao_suspeita_acesso_rede():
    print(f"*** AÇÃO SUSPEITA: Cleitinho tentando acessar compartilhamento restrito: {COMPARTILHAMENTO_RESTRITO} ***")
    abrir_aplicativo(f'explorer.exe "{COMPARTILHAMENTO_RESTRITO}"', wait_time_min=4, wait_time_max=7)
    mover_mouse_organicamente(random.randint(400, 600), random.randint(300, 400))
    pausa_humana(2, 5)
    fechar_janela_ativa()

def acao_suspeita_busca_arquivos():
    print("*** AÇÃO SUSPEITA: Cleitinho buscando por arquivos sensíveis... ***")
    abrir_aplicativo('explorer.exe', wait_time_min=2, wait_time_max=4)
    mover_mouse_organicamente(random.randint(800, 1200), random.randint(20, 50))
    clicar_organicamente(random.randint(800, 1200), random.randint(20, 50))
    pyautogui.hotkey('ctrl', 'e')
    pausa_humana(0.5, 1)
    termos_sensivel = random.choice(['senhas', 'confidencial', 'dados_financeiros', 'clientes_lista', 'rh_privado', 'sql_dump', 'credenciais', 'acesso_vpn', 'documentos_legais'])
    digitar_com_erros(termos_sensivel)
    pyautogui.press('enter')
    pausa_humana(7, 15)
    fechar_janela_ativa()

def acao_suspeita_comandos_cmd():
    print("*** AÇÃO SUSPEITA: Cleitinho abrindo CMD e executando comandos... ***")
    abrir_aplicativo('cmd.exe', wait_time_min=1.5, wait_time_max=3)
    comandos_suspeitos = [
        'whoami /all', 'ipconfig /all', 'net user', 'net localgroup administrators',
        'dir /s C:\\windows\\system32\\config\\*.reg', 'tasklist', 'netstat -ano',
        'net share', 'net view', 'systeminfo', 'route print', 'sc query state= all'
    ]
    comando_escolhido = random.choice(comandos_suspeitos)
    print(f"Digitando comando no CMD: {comando_escolhido}")
    digitar_com_erros(comando_escolhido)
    pyautogui.press('enter')
    pausa_humana(3, 7)
    if random.random() < 0.4:
        comando_secundario = random.choice(['echo %username%', 'date /t', 'time /t'])
        digitar_com_erros(comando_secundario)
        pyautogui.press('enter')
        pausa_humana(1, 3)
    pyautogui.write('exit')
    pyautogui.press('enter')
    pausa_humana(0.5, 1.5)


# --- Loop Principal da Simulação do Cleitinho ---
if __name__ == "__main__":
    print("Iniciando simulação do 'Cleitinho com Consciência Web' na VM (Windows 10)...")
    start_time = time.time()
    
    # Inicializa o driver Chrome uma vez no início (se necessário)
    inicializar_driver_chrome() 
    
    # Cleitinho começa o dia navegando um pouco
    if driver: # Se o driver foi inicializado com sucesso
        driver.get('https://www.google.com')
        pausa_humana(3, 5)
    else: # Fallback
        webbrowser.open('https://www.google.com')
        pausa_humana(3, 5)

    while (time.time() - start_time) < DURACAO_MAXIMA_SIMULACAO:
        print(f"\n--- Tempo de simulação decorrido: {int(time.time() - start_time)}s ---")

        # Chance para ações de distração/fundo
        if random.random() < 0.2:
            acao_aleatoria = random.choice(['mouse_mover', 'menu_iniciar', 'desktop_toggle', 'alternar'])
            if acao_aleatoria == 'mouse_mover':
                mover_mouse_organicamente(random.randint(100, 1000), random.randint(100, 700))
            elif acao_aleatoria == 'menu_iniciar':
                abrir_menu_iniciar()
            elif acao_aleatoria == 'desktop_toggle':
                mostrar_desktop_e_voltar()
            elif acao_aleatoria == 'alternar':
                alternar_janelas()
            pausa_humana(1, 3)

        # Decide qual ação principal fazer (normal vs suspeita)
        # Mais chances de ação normal. Ações suspeitas são mais impactantes agora.
        if random.random() < 0.80: 
            acao_normal = random.choice(['navegar', 'trabalhar_doc', 'explorador_files', 'outros_apps'])
            
            if acao_normal == 'navegar':
                acao_normal_navegacao() # Pode usar Selenium ou webbrowser
            elif acao_normal == 'trabalhar_doc':
                acao_normal_trabalho_documento()
            elif acao_normal == 'explorador_files':
                acao_normal_explorador_arquivos()
            elif acao_normal == 'outros_apps':
                acao_normal_outros_apps() # Apps como Calc/Paint
                
        else: # 20% de chance de fazer uma ação suspeita
            acao_suspeita = random.choice([
                'phishing_login', # Nova ação suspeita com Selenium
                'download_malware_simulado', # Nova ação suspeita com Selenium
                'acesso_rede', 
                'busca_arquivos', 
                'comandos_cmd'
            ])
            
            if acao_suspeita == 'phishing_login':
                navegar_e_tentar_phishing_login()
            elif acao_suspeita == 'download_malware_simulado':
                acao_suspeita_download_malware_simulado()
            elif acao_suspeita == 'acesso_rede':
                acao_suspeita_acesso_rede()
            elif acao_suspeita == 'busca_arquivos':
                acao_suspeita_busca_arquivos()
            elif acao_suspeita == 'comandos_cmd':
                acao_suspeita_comandos_cmd()
            
            pausa_humana(15, 40) # Aumentei a pausa após ação suspeita para simular disfarce

        pausa_humana(10, 25) # Pausa entre os ciclos principais de atividade
        
    print("\nSimulação do 'Cleitinho com Consciência Web' finalizada por tempo.")
    print("Fechando todos os navegadores e janelas abertas (tentativa exaustiva)...")
    fechar_driver_chrome() # Garante que o Selenium feche o navegador
    for _ in range(7):
        fechar_janela_ativa()
        time.sleep(0.5)

    print("Processo finalizado. Monitore seu SIEM para as pegadas do Cleitinho!")
