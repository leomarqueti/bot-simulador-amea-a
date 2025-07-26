import pyautogui
import time
import subprocess
import webbrowser
import random
import os

# --- Configurações Iniciais ---
# Pausa geral entre cada ação do pyautogui. Pequenas pausas para parecer mais humano.
pyautogui.PAUSE = 0.5

# Tempo máximo que o script vai rodar em segundos (aprox.)
DURACAO_MAXIMA_SIMULACAO = 1200 # 20 minutos (60 * 20) para um dia de trabalho estendido

# Lista de URLs "normais" para navegar
URLS_NORMAIS = [
    'https://www.google.com',
    'https://www.wikipedia.org/wiki/Ciberseguran%C3%A7a',
    'https://www.reddit.com/r/cybersecurity/',
    'https://www.bbc.com/news/technology',
    'https://br.linkedin.com/feed',
    'https://github.com/trending' # Um estagiário pode navegar no GitHub
]

# URLs do YouTube (para simular acesso a vídeos)
URLS_YOUTUBE = [
    'https://www.youtube.com/results?search_query=curso+python',
    'https://www.youtube.com/watch?v=dQw4w9WgXcQ', # Rick Astley (enganação de URL, pode ser divertido para logs)
    'https://www.youtube.com/results?search_query=ultimas+noticias+tecnologia'
]

# URL "suspeita" 
URL_SUSPEITA = 'http://site-de-phishing-simulado-para-teste.com' # ALtere para um domínio que seu SIEM possa identificar como malicioso ou blacklistado

# Caminho de um compartilhamento de rede que DEVERIA ser restrito para o Cleitinho
# Altere para um caminho real na sua rede de testes que o usuário da VM não tenha acesso
COMPARTILHAMENTO_RESTRITO = '\\\\192.168.1.100\\DadosConfidenciais' # Exemplo: IP ou nome de host da máquina de teste + nome do compartilhamento

# --- Funções de Ação ---

def pausa_humana(min_seg=0.5, max_seg=2.0):
    """Adiciona uma pausa aleatória para simular tempo de pensamento humano."""
    tempo_pausa = random.uniform(min_seg, max_seg)
    print(f"Pausando por {tempo_pausa:.2f} segundos para 'pensar'...")
    time.sleep(tempo_pausa)

def mover_mouse_sutilmente():
    """Move o mouse um pouco de forma aleatória para simular um humano ajustando a mão."""
    print("Movendo o mouse sutilmente...")
    x, y = pyautogui.position()
    pyautogui.moveTo(x + random.randint(-10, 10), y + random.randint(-10, 10), duration=random.uniform(0.1, 0.3))
    pausa_humana(0.1, 0.5)

def digitar_com_erros(texto):
    """Digita um texto com chances de erro e correção, para parecer mais humano."""
    print(f"Digitando com toques humanos: '{texto[:30]}...'")
    for char in texto:
        pyautogui.write(char, interval=random.uniform(0.02, 0.1)) # Atraso entre cada letra
        if random.random() < 0.05: # 5% de chance de erro de digitação
            pyautogui.write(random.choice(['a', 's', 'd', 'f', 'g']), interval=random.uniform(0.01, 0.03)) # Digita uma letra errada
            pausa_humana(0.05, 0.15)
            pyautogui.press('backspace', presses=1, interval=random.uniform(0.05, 0.15)) # Apaga a letra errada
            pausa_humana(0.05, 0.15)
    pausa_humana(0.5, 1.5)

def abrir_aplicativo(app_name, wait_time=3):
    """Abre um aplicativo usando subprocess, com tratamento para Windows."""
    print(f"Abrindo aplicativo: {app_name}...")
    try:
        if os.name == 'nt': # Windows
            subprocess.Popen([app_name], shell=True) # Use shell=True para 'start' ou apenas o nome do executável
        else: # Linux/macOS (não usado neste cenário, mas boa prática)
            subprocess.Popen([app_name])
        pausa_humana(wait_time, wait_time + 2) # Espera um pouco para o app abrir
    except FileNotFoundError:
        print(f"Erro: '{app_name}' não encontrado. Verifique se está instalado e no PATH.")
    except Exception as e:
        print(f"Ocorreu um erro ao tentar abrir '{app_name}': {e}")

def fechar_janela_ativa():
    """Fecha a janela que está ativa (simula clicar no X ou Alt+F4)."""
    print("Fechando janela ativa...")
    pyautogui.hotkey('alt', 'f4')
    pausa_humana(1, 2)

def alternar_janelas():
    """Simula Alt+Tab para alternar entre janelas abertas."""
    print("Alternando janelas (Alt+Tab)...")
    pyautogui.hotkey('alt', 'tab')
    pausa_humana(0.5, 1) # Pequena pausa para a janela mudar
    # Soltar o Alt+Tab
    pyautogui.hotkey('alt', 'tab') # Pressiona e solta novamente para selecionar a próxima janela
    pausa_humana(0.5, 1.5)

def abrir_navegador_e_navegar(url=None):
    """Abre o navegador e navega para uma URL, com mais realismo."""
    print("Abrindo navegador e navegando...")
    if url:
        webbrowser.open(url)
    else:
        # Tenta abrir um navegador comum ou uma página em branco
        if random.choice([True, False]):
            abrir_aplicativo('chrome') # Tenta abrir Chrome
        else:
            abrir_aplicativo('msedge') # Tenta abrir Edge
    
    pausa_humana(3, 7) # Tempo para carregar a página
    mover_mouse_sutilmente()
    pyautogui.scroll(random.randint(-800, -200)) # Rola um pouco para baixo
    pausa_humana(1, 3) # Pausa depois de rolar
    pyautogui.scroll(random.randint(100, 400)) # Rola um pouco para cima
    pausa_humana(1, 3)

# --- Funções de Ação Normal do Cleitinho ---

def acao_normal_navegacao():
    """Cleitinho navega para sites normais ou YouTube."""
    if random.random() < 0.7: # 70% de chance de ir para site normal
        url = random.choice(URLS_NORMAIS)
        print(f"Navegação normal: {url}")
        abrir_navegador_e_navegar(url)
    else: # 30% de chance de ir para o YouTube
        url = random.choice(URLS_YOUTUBE)
        print(f"Navegação YouTube: {url}")
        abrir_navegador_e_navegar(url)
    
    # Cleitinho passa um tempo navegando
    pausa_humana(5, 15)
    fechar_janela_ativa() # Fecha a aba/janela do navegador

def acao_normal_trabalho_documento():
    """Cleitinho trabalha no Bloco de Notas."""
    print("Simulando trabalho em um documento (Bloco de Notas)...")
    abrir_aplicativo('notepad.exe', wait_time=2) # Espera menos tempo para app leve
    
    conteudo_documento = [
        "Relatório de status do projeto X. Concluídas as tarefas de análise de requisitos.",
        "Notas da reunião de hoje: discutir a implementação da nova política de segurança da informação.",
        "Rascunho de e-mail para o gerente: solicitando acesso a recursos adicionais para o projeto Y.",
        "Pesquisando sobre 'melhores práticas de hardening de servidores Windows' para a equipe de Blue Team.",
        "Lista de tarefas para amanhã: revisar logs do firewall, atualizar documentação da rede interna."
    ]
    texto_para_digitar = random.choice(conteudo_documento) + "\n\n" + \
                         "Data: " + time.strftime("%Y-%m-%d %H:%M:%S") + "\n" + \
                         "Conteúdo gerado por simulador de usuário 'Cleitinho', o estagiário dedicado."

    digitar_com_erros(texto_para_digitar)
    
    # Simula o salvamento (mas não salva de fato) ou fecha direto
    if random.random() < 0.5: # 50% de chance de tentar salvar antes de fechar
        print("Cleitinho simulando salvamento do documento (sem salvar de fato)...")
        pyautogui.hotkey('ctrl', 's')
        pausa_humana(0.5, 1)
        pyautogui.press('escape') # Cancela o salvamento para não abrir a caixa
        pausa_humana(0.5, 1)

    fechar_janela_ativa() # Fecha a janela do editor

def acao_normal_outros_apps():
    """Cleitinho abre outros aplicativos comuns."""
    apps_comuns = ['calc.exe', 'mspaint.exe', 'explorer.exe'] # Calculadora, Paint, Explorador
    app_escolhido = random.choice(apps_comuns)
    print(f"Cleitinho abrindo aplicativo comum: {app_escolhido}")
    abrir_aplicativo(app_escolhido, wait_time=random.uniform(2, 5))
    
    if app_escolhido == 'explorer.exe':
        # Simula uma pequena navegação no explorador
        pyautogui.write('C:\\')
        pyautogui.press('enter')
        pausa_humana(1, 2)
        pyautogui.press('backspace') # Volta para "Este PC"
        pausa_humana(1, 2)
    
    fechar_janela_ativa()

# --- Funções de Ação Suspeita do Cleitinho ---

def acao_suspeita_acesso_rede():
    """Cleitinho tenta acessar um compartilhamento de rede restrito."""
    print(f"*** AÇÃO SUSPEITA: Cleitinho tentando acessar compartilhamento restrito: {COMPARTILHAMENTO_RESTRITO} ***")
    abrir_aplicativo(f'explorer.exe "{COMPARTILHAMENTO_RESTRITO}"', wait_time=4) # Abre explorador e tenta ir direto
    
    # O Windows vai mostrar uma mensagem de "Acesso Negado" ou pedir credenciais.
    # Cleitinho "desiste" e fecha a janela.
    mover_mouse_sutilmente()
    fechar_janela_ativa()

def acao_suspeita_busca_arquivos():
    """Cleitinho busca por termos sensíveis no Explorador de Arquivos."""
    print("*** AÇÃO SUSPEITA: Cleitinho buscando por arquivos sensíveis... ***")
    abrir_aplicativo('explorer.exe', wait_time=3)
    
    mover_mouse_sutilmente()
    pyautogui.hotkey('ctrl', 'e') # Atalho para focar na barra de pesquisa no Explorer do Win10
    pausa_humana(0.5, 1)

    termos_sensivel = random.choice(['senhas', 'confidencial', 'dados_financeiros', 'clientes_lista', 'rh_privado', 'sql_dump', 'credenciais'])
    digitar_com_erros(termos_sensivel) # Usa a digitação com erros
    pyautogui.press('enter')
    pausa_humana(5, 12) # Tempo para a busca acontecer e ele "analisar" os resultados

    fechar_janela_ativa()

def acao_suspeita_url_maliciosa():
    """Cleitinho tenta acessar uma URL "maliciosa"."""
    print(f"*** AÇÃO SUSPEITA: Cleitinho tentando acessar URL maliciosa: {URL_SUSPEITA} ***")
    abrir_navegador_e_navegar(URL_SUSPEITA)
    
    mover_mouse_sutilmente()
    # Cleitinho fica pouco tempo, talvez a página não carregue ou seja bloqueada
    pausa_humana(3, 7)
    fechar_janela_ativa()

def acao_suspeita_comandos_cmd():
    """Cleitinho abre o CMD e executa comandos suspeitos (mas não destrutivos)."""
    print("*** AÇÃO SUSPEITA: Cleitinho abrindo CMD e executando comandos... ***")
    abrir_aplicativo('cmd.exe', wait_time=2)

    comandos_suspeitos = [
        'whoami /all',
        'ipconfig /all',
        'net user',
        'net localgroup administrators',
        'dir /s C:\\windows\\system32\\config\\*.reg', # Busca por arquivos de registro
        'tasklist',
        'netstat -ano',
        'net share',
        'net view' # Tenta listar compartilhamentos de rede
    ]
    comando_escolhido = random.choice(comandos_suspeitos)
    print(f"Digitando comando no CMD: {comando_escolhido}")
    digitar_com_erros(comando_escolhido)
    pyautogui.press('enter')
    pausa_humana(3, 7) # Tempo para o comando rodar e Cleitinho ler o output

    pyautogui.write('exit') # Fecha o CMD
    pyautogui.press('enter')
    pausa_humana(0.5, 1.5)

# --- Loop Principal da Simulação do Cleitinho ---
if __name__ == "__main__":
    print("Iniciando simulação do 'Cleitinho Super-Realista' na VM (Windows 10)...")
    start_time = time.time()
    
    # Cleitinho começa abrindo o navegador como se fosse um dia normal
    abrir_navegador_e_navegar()

    while (time.time() - start_time) < DURACAO_MAXIMA_SIMULACAO:
        print(f"\n--- Tempo de simulação decorrido: {int(time.time() - start_time)}s ---")

        # Decide aleatoriamente qual ação fazer (normal ou suspeita)
        # Cleitinho é 75% "normal", 25% "malicioso" (agora mais frequente)
        if random.random() < 0.75: # 75% de chance de fazer uma ação normal
            acao_normal = random.choice(['navegar', 'trabalhar_doc', 'outros_apps', 'alternar'])
            
            if acao_normal == 'navegar':
                acao_normal_navegacao()
            elif acao_normal == 'trabalhar_doc':
                acao_normal_trabalho_documento()
            elif acao_normal == 'outros_apps':
                acao_normal_outros_apps()
            elif acao_normal == 'alternar':
                alternar_janelas()
                pausa_humana(2, 5) # Uma pausa depois de alternar

        else: # 25% de chance de fazer uma ação suspeita
            acao_suspeita = random.choice([
                'acesso_rede', 
                'busca_arquivos', 
                'url_maliciosa', 
                'comandos_cmd' # Nova ação suspeita
            ])
            
            if acao_suspeita == 'acesso_rede':
                acao_suspeita_acesso_rede()
            elif acao_suspeita == 'busca_arquivos':
                acao_suspeita_busca_arquivos()
            elif acao_suspeita == 'url_maliciosa':
                acao_suspeita_url_maliciosa()
            elif acao_suspeita == 'comandos_cmd':
                acao_suspeita_comandos_cmd()
            
            # Após uma ação suspeita, Cleitinho dá uma pausa maior para não levantar suspeitas
            pausa_humana(10, 25)
            mover_mouse_sutilmente() # Uma última sutil movimentação para não parecer parado

        # Pausa entre os ciclos principais de atividade
        pausa_humana(5, 15)
        
    print("\nSimulação do 'Cleitinho Super-Realista' finalizada por tempo.")
    print("Fechando possíveis janelas abertas (tentativa)...")
    for _ in range(5): # Tenta fechar mais vezes para garantir
        fechar_janela_ativa()
        time.sleep(1) # Pequena pausa entre cada tentativa de fechar

    print("Processo finalizado. Monitore seu SIEM!")
