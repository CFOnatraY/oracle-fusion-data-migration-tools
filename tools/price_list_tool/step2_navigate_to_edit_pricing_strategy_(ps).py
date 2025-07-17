from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

# Constantes
FUSION_URL = "https://fa-exum-saasfaprod1.fa.ocs.oraclecloud.com/fscmUI/faces/FuseWelcome"
EXCEL_PATH = "pricing_strategies.xlsx"
LOG_CSV = "results_update_pricing.csv"

# Leer Excel
df = pd.read_excel(EXCEL_PATH)
names = df['Name'].dropna().unique()  # Solo valores únicos no nulos

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

    print("⏳ Navegando a Order Management...")
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="groupNode_order_management"]'))).click()

    print("⏳ Navegando a Pricing Administration...")
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="itemNode_pricing_administration_pricing_administration"]'))).click()

    print("⏳ Abriendo menú lateral 'Tasks'...")
    tasks_icon = wait.until(EC.element_to_be_clickable((By.XPATH, '//a[contains(@id,"_FOTsdi_Default_item_node::disAcr")]')))
    tasks_icon.click()
    time.sleep(1)

    print("🔎 Buscando 'Manage Pricing Strategies'...")
    mps_link_xpath = '//a[text()="Manage Pricing Strategies"]'
    mps_link = wait.until(EC.element_to_be_clickable((By.XPATH, mps_link_xpath)))
    driver.execute_script("arguments[0].scrollIntoView(true);", mps_link)
    mps_link.click()
    print("✅ ¡Éxito! Llegaste a Manage Pricing Strategies.")


    # Ahora: iterar por cada estrategia (solo hacemos la primera como prueba)
    for name in names[:1]:  # Cambiar [:1] por [:N] si quieres más
        print(f"🔍 Buscando estrategia: {name}")

        input_field = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="pt1:_FOr1:1:_FONSr2:0:MAt2:0:AP1:qryId2:value00::content"]')))
        input_field.clear()
        input_field.send_keys(name)

        # # Botón Search
        # Esperar y asegurarse de que el botón Search esté visible e interactuable
        search_button_xpath = '//button[contains(@id, "qryId2::search")]'
        search_button = wait.until(EC.presence_of_element_located((By.XPATH, search_button_xpath)))
        driver.execute_script("arguments[0].scrollIntoView(true);", search_button)
        time.sleep(1)  # Dar tiempo al scroll

        # Intentar clic normal, si no funciona usamos JS
        try:
            wait.until(EC.element_to_be_clickable((By.XPATH, search_button_xpath))).click()
        except:
            print("⚠️ Clic tradicional falló, intentando con JavaScript...")
            driver.execute_script("arguments[0].click();", search_button)


        # Esperar que el resultado esté presente y dar clic en el enlace correcto
        result_link_xpath = f'//a[text()="{name}"]'
        result_link = wait.until(EC.element_to_be_clickable((By.XPATH, result_link_xpath)))
        result_link.click()

        print(f"✅ Estrategia '{name}' seleccionada correctamente.")
        break  # Por ahora solo el primero

except Exception as e:
    print(f"❌ Error durante la navegación o búsqueda: {e}")

finally:
    time.sleep(5)
    driver.quit()
