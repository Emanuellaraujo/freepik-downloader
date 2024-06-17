from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pyautogui

# Inicializa o WebDriver (por exemplo, Chrome)
driver = webdriver.Chrome()

driver.get("https://br.freepik.com/search?aspect_ratio=16%3A9&format=search&last_filter=query&last_value=baby+eating&query=baby+eating&type=video")

# Aguarda um momento para a página carregar completamente
time.sleep(2)

# Aguarde até que o botão de aceitar cookies seja clicável
accept_cookies_button = driver.find_element(By.ID, "onetrust-accept-btn-handler")
accept_cookies_button.click()

# Localiza a seção de vídeos
video_section = driver.find_element(By.CSS_SELECTOR, "div._1n8py6t4")

# Localiza todos os elementos de link <a> dentro da seção
video_links = video_section.find_elements(By.TAG_NAME, "a")

# Imprime os URLs dos vídeos
print("Número de links encontrados:", len(video_links))

for link in video_links:
    video_url = link.get_attribute("href")
    print("URL do vídeo:", video_url)

    # Abrir nova janela do navegador com a URL do vídeo
    driver.execute_script("window.open('" + video_url + "', '_blank');")
    time.sleep(5)

    # Alternar para a nova aba
    driver.switch_to.window(driver.window_handles[1])

    # Realizar o scroll 20 vezes para baixo
    for _ in range(20):
        pyautogui.press('down')
    time.sleep(2)

    # Obter as coordenadas do clique
    x = 600.400
    y = 800.800

    # Mover o cursor para as coordenadas especificadas
    pyautogui.moveTo(x, y)
    time.sleep(5)

    # Simular um clique do mouse
    pyautogui.click()
    time.sleep(20)

    # Fechar a aba atual
    driver.close()

    # Mudar o foco para a aba principal
    driver.switch_to.window(driver.window_handles[0])

# Fechar o navegador ao finalizar
driver.quit()
