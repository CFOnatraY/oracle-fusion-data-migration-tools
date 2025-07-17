from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time
from datetime import datetime

# Constantes
FUSION_URL = "https://fa-exum-saasfaprod1.fa.ocs.oraclecloud.com/fscmUI/faces/FuseWelcome"
EXCEL_PATH = "pricing_strategies.xlsx"
LOG_CSV = "results_update_pricing.csv"

# Leer Excel
df = pd.read_excel(EXCEL_PATH)
df = df[['Pricing Strategy', 'Price List']].dropna()
strategy_map = df.groupby('Pricing Strategy')['Price List'].apply(list).to_dict()

# Inicializar navegador
print("🟡 Inicializando navegador con webdriver-manager...")
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
wait = WebDriverWait(driver, 25)

try:
    print("🌐 Abriendo Oracle Fusion...")
    driver.get(FUSION_URL)
    driver.maximize_window()
    input("🔐 Haz login manualmente y presiona Enter cuando estés en el Home...")

    # Navegación
    print("🔎 Navegando a 'Manage Pricing Strategies'...")
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="groupNode_order_management"]'))).click()
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="itemNode_pricing_administration_pricing_administration"]'))).click()
    tasks_icon = wait.until(EC.element_to_be_clickable((By.XPATH, '//a[contains(@id,"_FOTsdi_Default_item_node::disAcr")]')))
    tasks_icon.click()
    time.sleep(1)

    mps_link = wait.until(EC.element_to_be_clickable((By.XPATH, '//a[text()="Manage Pricing Strategies"]')))
    driver.execute_script("arguments[0].scrollIntoView(true);", mps_link)
    mps_link.click()

    # Iterar estrategias
    for pricing_strategy, price_lists in strategy_map.items():
        print(f"\n🔍 Buscando estrategia: {pricing_strategy}")
        input_field = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="pt1:_FOr1:1:_FONSr2:0:MAt2:0:AP1:qryId2:value00::content"]')))
        input_field.clear()
        input_field.send_keys(pricing_strategy)

        search_btn = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[contains(@id, "qryId2::search")]')))
        driver.execute_script("arguments[0].click();", search_btn)

        result_link = wait.until(EC.element_to_be_clickable((By.XPATH, f'//a[text()="{pricing_strategy}"]')))
        result_link.click()
        time.sleep(1)

        for idx, pl in enumerate(price_lists, start=0):
            print(f"➕ Agregando Price List: {pl}")

            # Abrir modal
            icon_xpath = '//a[contains(@id,"AT4:_ATp:cil30")]'
            select_add_icon = wait.until(EC.element_to_be_clickable((By.XPATH, icon_xpath)))
            driver.execute_script("arguments[0].click();", select_add_icon)

            # Ingresar nombre y buscar
            pl_input = wait.until(EC.presence_of_element_located((By.XPATH, '//label[contains(text(), "Name")]/following::input[contains(@id,"qryId2:value00")][1]')))
            pl_input.clear()
            pl_input.send_keys(pl)

            pl_search_btn = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[contains(@id,"qryId2::search")]')))
            driver.execute_script("arguments[0].click();", pl_search_btn)
            time.sleep(1)

            # Simular selección con teclas
            actions = ActionChains(driver)
            actions.send_keys(Keys.TAB).pause(0.1).send_keys(Keys.TAB).pause(0.1).send_keys(Keys.TAB).pause(0.1)
            actions.send_keys(Keys.ARROW_DOWN).pause(0.1).send_keys(Keys.ARROW_RIGHT).pause(0.1).perform()
            time.sleep(1)

            # Clic en OK
            ok_btn = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[contains(@id,"segmentOkButton")]')))
            driver.execute_script("arguments[0].click();", ok_btn)

            # Esperar que se cierre el modal y aparezca el registro
            wait.until(EC.presence_of_element_located((By.XPATH, f'//span[contains(text(),"{pl}")]')))
            print(f"✅ {pl} agregado correctamente.")

            # Ingresar Start Date (fecha actual)
            today = datetime.today().strftime("%d/%m/%Y %I:%M %p")
            print(f"📅 Ingresando Start Date: {today}")
            try:
                date_input_xpath = f'//*[@id="pt1:_FOr1:1:_FONSr2:0:MAt3:0:AP1:r2:0:AT4:_ATp:ATt4:{idx}:id1::content"]'
                date_input = wait.until(EC.presence_of_element_located((By.XPATH, date_input_xpath)))
                driver.execute_script("arguments[0].scrollIntoView(true);", date_input)
                time.sleep(0.2)  # Pequeña pausa para permitir que se renderice correctamente
                date_input.clear()
                date_input.send_keys(today)
                print("✅ Fecha ingresada correctamente.")
            except Exception as e:
                print(f"⚠️ No se pudo ingresar la fecha en idx {idx}: {e}")

        # Aquí podrías dar clic en Save si quieres persistirlo
        # save_btn_xpath = '//button[contains(@id,"pt1:_FOr1:0:_FONSr2:0:MAt10:0:AP1:save")]'
        # save_btn = wait.until(EC.element_to_be_clickable((By.XPATH, save_btn_xpath)))
        # driver.execute_script("arguments[0].click();", save_btn)

        print(f"✅ Todas las Price List agregadas para: {pricing_strategy}")
        break  # ⚠️ Solo para el primer Name en prueba

except Exception as e:
    print(f"❌ Error durante la ejecución: {e}")

finally:
    time.sleep(5)
    driver.quit()
