
import time
import csv
import urllib.robotparser
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException

CHROMEDRIVER_PATH = "chromedriver" 
LINK = "file:///<CAMINHO_PARA_HTML_LOCAL_OU_URL_AUTORIZADA>"  

def pode_scrapear(base_url, path="/"):
    rp = urllib.robotparser.RobotFileParser()
    rp.set_url(base_url.rstrip("/") + "/robots.txt")
    try:
        rp.read()
        return rp.can_fetch("*", path)
    except Exception:
        return False

def main():
    if not LINK.startswith("file://"):
        base = "/".join(LINK.split("/")[:3])  
        if not pode_scrapear(base):
            print("robots.txt proíbe scraping ou não pôde ser lido. Abortando por precaução.")
            return

    options = Options()
    # Remova headless do exemplo se quiser ver o navegador localmente
    options.add_argument("--headless=new")  
    driver = webdriver.Chrome(CHROMEDRIVER_PATH, options=options)

    try:
        driver.get(LINK)
        time.sleep(1.5) 

        blocos = driver.find_elements(By.CSS_SELECTOR, ".exemplo-bloco") 
        results = []

        for bloco in blocos:
            try:
                nome = bloco.find_element(By.CSS_SELECTOR, ".nome").text
            except NoSuchElementException:
                nome = "[NOME_REMOVIDO]"

            try:
                crm = bloco.find_element(By.CSS_SELECTOR, ".crm").text
            except NoSuchElementException:
                crm = "[CRM_REMOVIDO]"

            try:
                especialidades = bloco.find_element(By.CSS_SELECTOR, ".especialidades").text
            except NoSuchElementException:
                especialidades = "[ESPECIALIDADES_REMOVIDAS]"

            endereco = "[ENDERECO_REMOVIDO]"

            results.append({
                "nome": nome,
                "crm": crm,
                "especialidades": especialidades,
                "endereco": endereco
            })

            time.sleep(1.0)  

        with open("sample_results.csv", "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["nome", "crm", "especialidades", "endereco"], delimiter=";")
            writer.writeheader()
            for r in results:
                writer.writerow(r)

        print("Execução concluída. Resultado salvo em sample_results.csv (dados fictícios).")

    finally:
        driver.quit()

if __name__ == "__main__":
    main()
