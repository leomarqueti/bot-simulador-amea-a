import pyautogui
import time
import subprocess
import webbrowser
import random
import os

# --- Configurações Iniciais ---
# Pausa geral entre cada ação do pyautogui. Aumente para um comportamento mais "lento" e humano.
pyautogui.PAUSE = 1.0

# Tempo máximo que o script vai rodar em segundos (aprox.)
DURACAO_MAXIMA_SIMULACAO = 900 # 15 minutos (60 * 15) para um ciclo de trabalho mais longo

# Lista de URLs "normais" para navegar
URLS_NORMAIS = [
    'https://www.google.com',
    'https://www.wikipedia.org',
    'https://www.reddit.com/r/cybersecurity/',
    'https://www.bbc.com/news',
    'https://br.linkedin.com',
    'https://github.com/public-repos' # Um estagiário pode navegar no GitHub
]

# URL "suspeita" que você quer que seu SIEM detecte
URL_SUSPEITA = 'http://site-de-phishing-simulado-para-teste.com' # Altere para um domínio que seu SIEM possa identificar como malicioso ou blacklistado

# Caminho de um compartilhamento de rede que DEVERIA ser restrito para o Cleitinho
# Altere para um caminho real na sua rede de testes que o usuário da VM não tenha acesso
COMPARTILHAMENTO_RESTRITO = '\\\\192.168.1.100\\DadosConfidenciais' # Exemplo: IP ou nome de host da máquina de teste + nome do compartilhamento

# --- Funções de Ação ---

def pausar_aleatoriamente(min_seg=1, max_seg=3):
    """Adiciona uma pausa aleatória para simular tempo de pensamento humano."""
    tempo_pausa = random.uniform(min_seg, max_seg)
    print(f"Pausando por {tempo_pausa:.2f} segundos...")
    time.sleep(tempo_pausa)

def abrir_navegador(url=None):
    """Abre o navegador padrão e, opcionalmente, uma URL."""
    print("Abrindo navegador...")
    # No Windows 10, 'start chrome' ou 'start msedge' geralmente funcionam
    try:
        if random.choice([True, False]): # Aleatoriamente Chrome ou Edge
            subprocess.Popen(['start', 'chrome'], shell=True)
        else:
            subprocess.Popen(['start', 'msedge'], shell=True)
    except FileNotFoundError:
        webbrowser.open('about:blank') # Último recurso se não encontrar Chrome/Edge
        print("Nenhum navegador comum encontrado para abrir. Abrindo página em branco.")
    pausar_aleatoriamente(2, 5)

def navegar_aleatoriamente():
    """Navega para uma URL normal aleatória."""
    url = random.choice(URLS_NORMAIS)
    print(f"Navegando para: {url}")
    webbrowser.open(url)
    pausar_aleatoriamente(3, 8) # Tempo maior para carregar a página

    # Simular rolagem de página
    if random.random() < 0.6: # 60% de chance de rolar
        print("Rolando a página...")
        pyautogui.scroll(random.randint(-1000, -300)) # Rola para baixo
        pausar_aleatoriamente(1, 2)
        pyautogui.scroll(random.randint(100, 500))   # Rola um pouco para cima
        pausar_aleatoriamente(1, 2)

def simular_trabalho_documento():
    """Abre o Bloco de Notas, digita um texto e simula salvamento/fechamento."""
    print("Simulando trabalho em um documento (Bloco de Notas)...")
    try:
        subprocess.Popen(['notepad.exe']) # Abre o Bloco de Notas
        pausar_aleatoriamente(2, 4)

        conteudo_documento = [
            "Relatório de status do projeto X. Concluídas as tarefas de análise de requisitos.",
            "Notas da reunião de hoje: discutir a implementação da nova política de segurança.",
            "Rascunho de e-mail para o gerente: solicitando acesso a recursos adicionais para o projeto.",
            "Pesquisa sobre 'melhores práticas de hardening de servidores Windows'.",
            "Lista de tarefas para amanhã: revisar logs do firewall, atualizar documentação."
        ]
        texto_para_digitar = random.choice(conteudo_documento) + "\n\n" + \
                             "Data: " + time.strftime("%Y-%m-%d %H:%M:%S") + "\n" + \
                             "Conteúdo gerado por simulador de usuário 'Cleitinho'."

        print(f"Digitando: '{texto_para_digitar.splitlines()[0]}...'")
        pyautogui.write(texto_para_digitar, interval=random.uniform(0.03, 0.1)) # Digita com atraso para parecer humano
        pausar_aleatoriamente(1, 3)

        # Simula o salvamento (mas não salva de fato para não encher a VM de arquivos)
        # Se quiser salvar, descomente e ajuste o caminho:
        # pyautogui.hotkey('ctrl', 's')
        # pausar_aleatoriamente(0.5, 1)
        # pyautogui.write(f'C:\\Users\\Public\\Documentos\\relatorio_cleitinho_{int(time.time())}.txt')
        # pyautogui.press('enter')
        # pausar_aleatoriamente(1, 2)

        print("Fechando o documento...")
        pyautogui.hotkey('alt', 'f4') # Fecha a janela do editor
        pausar_aleatoriamente(1, 2)

    except FileNotFoundError:
        print("Erro: Bloco de Notas (notepad.exe) não encontrado.")
    except Exception as e:
        print(f"Ocorreu um erro ao simular trabalho no documento: {e}")

def simular_acao_suspeita_acesso_rede():
    """Cleitinho tenta acessar um compartilhamento de rede restrito."""
    print(f"*** AÇÃO SUSPEITA: Cleitinho tentando acessar compartilhamento restrito: {COMPARTILHAMENTO_RESTRITO} ***")
    try:
        # Abre o Explorador de Arquivos e tenta navegar para o caminho
        subprocess.Popen(['explorer.exe', COMPARTILHAMENTO_RESTRITO])
        pausar_aleatoriamente(3, 7)
        # O Windows vai mostrar uma mensagem de "Acesso Negado" ou pedir credenciais.
        # Cleitinho "desiste" e fecha a janela.
        print("Fechando janela de acesso de rede...")
        pyautogui.hotkey('alt', 'f4')
        pausar_aleatoriamente(1, 2)
    except FileNotFoundError:
        print("Erro: explorer.exe não encontrado.")
    except Exception as e:
        print(f"Ocorreu um erro ao simular acesso de rede: {e}")

def simular_acao_suspeita_busca_arquivos():
    """Cleitinho busca por termos sensíveis no Explorador de Arquivos."""
    print("*** AÇÃO SUSPEITA: Cleitinho buscando por arquivos sensíveis... ***")
    try:
        # Abre o Explorador de Arquivos
        subprocess.Popen(['explorer.exe'])
        pausar_aleatoriamente(2, 4)

        # Clica na barra de pesquisa do Explorador (geralmente no canto superior direito)
        # As coordenadas podem variar. Uma alternativa é usar Ctrl+F para focar na busca.
        pyautogui.hotkey('ctrl', 'f') # Tenta focar na busca
        pausar_aleatoriamente(1, 2)

        termos_sensivel = random.choice(['senhas', 'confidencial', 'dados_financeiros', 'clientes_lista', 'rh_privado'])
        print(f"Buscando por: '{termos_sensivel}'")
        pyautogui.write(termos_sensivel)
        pyautogui.press('enter')
        pausar_aleatoriamente(5, 10) # Tempo para a busca acontecer

        print("Fechando o Explorador de Arquivos...")
        pyautogui.hotkey('alt', 'f4')
        pausar_aleatoriamente(1, 2)
    except Exception as e:
        print(f"Ocorreu um erro ao simular busca de arquivos: {e}")

def simular_acao_suspeita_url():
    """Cleitinho tenta acessar uma URL "maliciosa" (para ser detectada pelo SIEM)."""
    print(f"*** AÇÃO SUSPEITA: Cleitinho tentando acessar URL maliciosa: {URL_SUSPEITA} ***")
    webbrowser.open(URL_SUSPEITA)
    pausar_aleatoriamente(3, 7)
    # Tenta fechar o navegador após a tentativa de acesso suspeito
    pyautogui.hotkey('alt', 'f4')
    pausar_aleatoriamente(1, 2)

# --- Loop Principal da Simulação do Cleitinho ---
if __name__ == "__main__":
    print("Iniciando simulação do 'Cleitinho' na VM (Windows 10)...")
    start_time = time.time()
    
    # Cleitinho começa abrindo o navegador como se fosse um dia normal
    abrir_navegador()

    while (time.time() - start_time) < DURACAO_MAXIMA_SIMULACAO:
        print(f"\n--- Tempo de simulação decorrido: {int(time.time() - start_time)}s ---")

        # Decide aleatoriamente qual ação fazer (normal ou suspeita)
        # Cleitinho é 80% "normal", 20% "malicioso"
        if random.random() < 0.80: # 80% de chance de fazer uma ação normal
            acao_normal = random.choice(['navegar', 'digitar', 'pausar'])
            if acao_normal == 'navegar':
                navegar_aleatoriamente()
            elif acao_normal == 'digitar':
                simular_trabalho_documento()
            elif acao_normal == 'pausar':
                print("Cleitinho está em uma pausa curta, pensando na vida (e na vingança)...")
                pausar_aleatoriamente(5, 15) # Uma pausa mais longa
        else: # 20% de chance de fazer uma ação suspeita
            acao_suspeita = random.choice(['acesso_rede', 'busca_arquivos', 'url_maliciosa'])
            if acao_suspeita == 'acesso_rede':
                simular_acao_suspeita_acesso_rede()
            elif acao_suspeita == 'busca_arquivos':
                simular_acao_suspeita_busca_arquivos()
            elif acao_suspeita == 'url_maliciosa':
                simular_acao_suspeita_url()
            
            # Após uma ação suspeita, Cleitinho pode dar uma pausa maior para não levantar suspeitas
            pausar_aleatoriamente(10, 25)

        # Pausa entre os ciclos principais de atividade
        pausar_aleatoriamente(5, 15)
        
    print("\nSimulação do 'Cleitinho' finalizada por tempo.")
    print("Fechando possíveis janelas abertas (tentativa)...")
    # Tenta fechar qualquer janela ativa no final
    for _ in range(3): # Tenta fechar algumas vezes
        pyautogui.hotkey('alt', 'f4')
        time.sleep(1)

    print("Desligando a VM (se configurado para isso no seu ambiente de automação)...")
    # Se você quiser que a VM desligue automaticamente após o teste, você precisaria de:
    # 1. Ferramentas do hypervisor (VirtualBox Guest Additions, VMware Tools) instaladas.
    # 2. Um comando como: subprocess.Popen(['shutdown', '/s', '/t', '0'], shell=True)
    # CUIDADO ao usar comandos de desligamento automático!
