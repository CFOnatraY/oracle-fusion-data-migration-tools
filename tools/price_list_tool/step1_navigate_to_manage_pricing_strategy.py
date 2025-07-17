from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
import time

FUSION_URL = "https://fa-exum-saasfaprod1.fa.ocs.oraclecloud.com/fscmUI/faces/FuseWelcome"
EXCEL_PATH = "pricing_strategies.xlsx"
LOG_CSV = "results_update_pricing.csv"

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
    time.sleep(1)  # Dar tiempo a que se despliegue el menú

    print("🔎 Buscando 'Manage Pricing Strategies'...")
    wait.until(EC.presence_of_element_located((By.ID, "pt1:_FOr1:1:_FONSr2:0:_FOTRaT:0:RAtl12")))
    mps_link = wait.until(EC.element_to_be_clickable((By.ID, "pt1:_FOr1:1:_FONSr2:0:_FOTRaT:0:RAtl12")))

    # Asegurar visibilidad con scroll
    driver.execute_script("arguments[0].scrollIntoView(true);", mps_link)
    mps_link.click()

    print("✅ ¡Éxito! Llegaste a Manage Pricing Strategies.")

except Exception as e:
    print(f"❌ Error durante la navegación: {e}")

finally:
    time.sleep(3)
    driver.quit()
