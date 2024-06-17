from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
from selenium.webdriver.common.keys import Keys
import requests
from selenium.common.exceptions import TimeoutException

# Inicializa o WebDriver (por exemplo, Chrome)
driver = webdriver.Chrome()

# Abra o site
driver.get("https://www.pexels.com/pt-br/")

# Aguarde um momento para a página carregar completamente
time.sleep(3)

# Encontre o campo de busca e insira o termo de pesquisa
search_box = driver.find_element(By.XPATH, "//input[@placeholder='Buscar fotos gratuitas']")
search_box.send_keys("baby eating" + Keys.ENTER)

# Aguarde um momento para a página carregar os resultados da pesquisa
time.sleep(2)

# Aguarde até que o botão de aceitar cookies seja clicável
accept_cookies_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler"))
)
# Clique no botão de aceitar cookies
accept_cookies_button.click()

# Clique no botão "Vídeos"
video_button = driver.find_element(By.XPATH, "//a[@href='/pt-br/procurar/videos/baby%20eating/']")
video_button.click()

# Aguarde um momento para a página carregar os resultados da pesquisa
time.sleep(5)

# Espera até que os elementos de vídeo estejam presentes na página
wait = WebDriverWait(driver, 20)  # Aumente o tempo limite para 20 segundos
videos = wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, ".MediaCard_badges__GWRPE")))

# Defina um contador para o número de downloads realizados
download_count = 0

# Iterar sobre a lista de vídeos
for i, video in enumerate(videos):
    # Clicar no vídeo para abrir
    video.click()
    time.sleep(3)  # Aguardar um momento para o vídeo carregar completamente
    
    # Obter a URL do vídeo
    video_url = driver.current_url
    
    if video_url is not None:
        # Extrair as palavras finais da URL após "/video/"
        last_part_of_url = video_url.split("/video/")[-1]
        last_part_of_url_cleaned = re.sub(r'[-0-9]+', ' ', last_part_of_url)
        last_part_of_url_cleaned_ = last_part_of_url_cleaned[:-1].strip()  # Remover o espaço no início e no final
        print(f"Palavras finais da URL do vídeo {i+1} após '/video/':", last_part_of_url_cleaned_)

        #pegar o ID para download
        url_parts = video_url.split("-")
        last_part = url_parts[-1]
        match = re.search(r'\d+', last_part)

        if match:
            video_id = match.group()
            print("ID do vídeo:", video_id)
            download_url = f"https://www.pexels.com/pt-br/download/video/{video_id}/"
            print(f"URL de download do vídeo {i+1}: {download_url}")
        
        # Verificar se a última parte da URL contém as palavras-chave
        words_to_check = ['bebê comendo', 'bebê alimentando', 'bebê papinha', 'bebê frutas', 'bebê vegetais', 'bebê bagunça com comida', 'bebê engasgando', 'bebê pai', 'pai filho', 'pai filha']
        found_words = [word for word in words_to_check if word in last_part_of_url_cleaned_]
        
        if found_words:
            print("Contém as seguintes palavras na URL:", ', '.join(found_words))
            
            if download_count <= 5:
                driver.get(download_url)
                #download_url.click()
                download_count += 1
    
    # Voltar para a página anterior para selecionar o próximo vídeo
    driver.execute_script("window.history.go(-1)")

    time.sleep(3)  # Aguardar um momento para o vídeo fechar

# Fechar o navegador
driver.quit()