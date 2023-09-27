from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import schedule
import time


# Função para extrair e imprimir dados
def extrair_e_imprimir_dados():
    try:
        servico = Service(ChromeDriverManager().install())
        navegador = webdriver.Chrome(service=servico)
        navegador.get("https://www.flashscore.com.br/")
        time.sleep(2)

        # Espera até que a tabela ao vivo esteja carregada
        for _ in range(10):  # Tente por até 10 segundos
            try:
                aovivo = navegador.find_element('xpath', '//*[@id="live-table"]/div[1]/div[1]/div[2]').click()
                break  # Sai do loop se encontrar o elemento
            except Exception as e:
                time.sleep(1)  # Aguarde 1 segundo antes de tentar novamente

        div_mae = navegador.find_element('xpath', '//*[@id="live-table"]/section/div/div')
        html_content = div_mae.get_attribute('outerHTML')
        soup = BeautifulSoup(html_content, 'html.parser')
        ligas = soup.find_all('div', class_='event__titleBox')
        time_casa = soup.find_all('div', class_='event__participant--home')
        time_fora = soup.find_all('div', class_='event__participant--away')
        placar_casa = soup.find_all('div', class_='event__score--home')
        placar_fora = soup.find_all('div', class_='event__score--away')

        # Certifique-se de que todas as listas tenham o mesmo tamanho
        tamanho_lista = len(time_casa)
        indice = 0

        for indice in range(tamanho_lista):
            print('JOGOS AO VIVO!!')
            if indice < len(time_casa) and indice < len(placar_casa) and indice < len(placar_fora) and indice < len(
                    time_fora):
                print(time_casa[indice].get_text(), " ", placar_casa[indice].get_text(), " X ",
                      placar_fora[indice].get_text(), " ", time_fora[indice].get_text())
        print("Executando a extração de dados...")

    except Exception as e:
        print("Ocorreu um erro:", str(e))

# função para chamar imediatamente
extrair_e_imprimir_dados()

# Agendamento para executar a função a cada 3 minutos
schedule.every(3).minutes.do(extrair_e_imprimir_dados)

# Loop para manter o script em execução
while True:
    schedule.run_pending()
    time.sleep(1)  # Aguarde 1 segundo antes de verificar novamente o agendamento
