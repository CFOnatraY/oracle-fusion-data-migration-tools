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
full_df = pd.read_excel(EXCEL_PATH)
full_df = full_df[['Pricing Strategy', 'Price List', 'Discount List', 'Currency Conversion List']].dropna(subset=['Pricing Strategy'])
strategy_map = full_df.groupby('Pricing Strategy').agg({
    'Price List': lambda x: list(x.dropna()),
    'Discount List': 'first',
    'Currency Conversion List': 'first'
}).to_dict('index')

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
    for pricing_strategy, values in strategy_map.items():
        price_lists = values['Price List']
        discount_list = values['Discount List']
        currency_list = values['Currency Conversion List']

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
            time.sleep(2)

            # Simular selección con teclas
            actions = ActionChains(driver)
            actions.send_keys(Keys.TAB).pause(0.2).send_keys(Keys.TAB).pause(0.2).send_keys(Keys.TAB).pause(0.2)
            actions.send_keys(Keys.ARROW_DOWN).pause(0.2).send_keys(Keys.ARROW_RIGHT).pause(0.2).perform()
            time.sleep(2)

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
                time.sleep(0.5)  # Pequeña pausa para permitir que se renderice correctamente
                date_input.clear()
                date_input.send_keys(today)
                print("✅ Fecha ingresada correctamente.")
            except Exception as e:
                print(f"⚠️ No se pudo ingresar la fecha en idx {idx}: {e}")

        print(f"✅ Todas las Price List agregadas para: {pricing_strategy}")

        # ➕ Agregar Discount List si aplica
        if str(discount_list).strip().upper() != "NO APLICA":
            try:
                print(f"➕ Agregando Discount List: {discount_list}")

                # Clic en la pestaña Discount Lists
                discount_tab = wait.until(EC.element_to_be_clickable((By.XPATH, '//a[contains(text(),"Discount Lists")]')))
                driver.execute_script("arguments[0].click();", discount_tab)
                time.sleep(1)

                # Botón Select and Add
                dl_add_btn = wait.until(EC.element_to_be_clickable((By.XPATH, '//a[contains(@id,"AT2:_ATp:cil45")]')))
                driver.execute_script("arguments[0].click();", dl_add_btn)

                # Buscar Discount List
                dl_input = wait.until(EC.presence_of_element_located((By.XPATH, '//label[contains(text(), "Name")]/following::input[contains(@id,"qryId1:value00")][1]')))
                dl_input.clear()
                dl_input.send_keys(discount_list)

                dl_search_btn = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[contains(@id,"qryId1::search")]')))
                driver.execute_script("arguments[0].click();", dl_search_btn)
                time.sleep(1)

                # Simular navegación con teclas
                ActionChains(driver).send_keys(Keys.TAB).pause(0.1).send_keys(Keys.TAB).pause(0.1).send_keys(Keys.TAB).pause(0.1)\
                    .send_keys(Keys.ARROW_DOWN).pause(0.1).send_keys(Keys.ARROW_RIGHT).pause(0.1).perform()

                # Clic en OK
                dl_ok = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[contains(@id,"discountListOkButton")]')))
                driver.execute_script("arguments[0].click();", dl_ok)

                # ✅ Confirmación visual
                wait.until(EC.presence_of_element_located((By.XPATH, f'//span[contains(text(),"{discount_list}")]')))
                print("✅ Discount List agregado correctamente.")

                # 🔁 Esperar específicamente que se renderice el campo de fecha en Discount List (por ID exacto)
                today = datetime.today().strftime("%d/%m/%Y %I:%M %p")
                print(f"📅 Ingresando Start Date en Discount Lists: {today}")

                time.sleep(1)  # Forzamos espera visual ligera para evitar solape con el último campo activo
                dl_date_input_xpath = '//*[@id="pt1:_FOr1:1:_FONSr2:0:MAt3:0:AP1:r2:0:AT2:_ATp:t1:0:id7::content"]'
                dl_date_input = wait.until(EC.presence_of_element_located((By.XPATH, dl_date_input_xpath)))
                driver.execute_script("arguments[0].scrollIntoView(true);", dl_date_input)
                time.sleep(0.2)
                dl_date_input.clear()
                dl_date_input.send_keys(today)
                print("✅ Fecha de inicio en Discount List ingresada correctamente.")

            except Exception as e:
                print(f"⚠️ Error al agregar Discount List '{discount_list}': {e}")
        else:
            print("⏩ Discount List marcado como 'NO APLICA'. Se omite.")

        if str(currency_list).strip().upper() != "NO APLICA":
            try:
                print(f"💱 Agregando Currency Conversion List: {currency_list}")
                ccl_tab = wait.until(EC.element_to_be_clickable((By.XPATH, '//a[contains(text(),"Currency Conversion Lists")]')))
                driver.execute_script("arguments[0].click();", ccl_tab)
                time.sleep(1)

                ccl_add_btn = wait.until(EC.element_to_be_clickable((By.XPATH, '//a[contains(@id,"AT5:_ATp:cil29")]')))
                driver.execute_script("arguments[0].click();", ccl_add_btn)

                ccl_input = wait.until(EC.presence_of_element_located((By.XPATH, '//label[contains(text(), "Name")]/following::input[contains(@id,"qryId1:value00")][1]')))
                ccl_input.clear()
                ccl_input.send_keys(currency_list)

                ccl_search_btn = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[contains(@id,"qryId1::search")]')))
                driver.execute_script("arguments[0].click();", ccl_search_btn)
                time.sleep(1)

                ActionChains(driver).send_keys(Keys.TAB).pause(0.1).send_keys(Keys.TAB).pause(0.1).send_keys(Keys.TAB).pause(0.1)\
                    .send_keys(Keys.ARROW_DOWN).pause(0.1).send_keys(Keys.ARROW_RIGHT).pause(0.1).perform()

                ccl_ok = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[contains(@id,"CurrencyConvOkButton")]')))
                driver.execute_script("arguments[0].click();", ccl_ok)

                time.sleep(1)
                ActionChains(driver).send_keys(Keys.TAB).pause(0.1).send_keys(Keys.ENTER).pause(0.1).perform()
                warning_yes = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="pt1:_FOr1:0:_FONSr2:0:MAt3:0:AP1:r2:0:cb12"]')))
                driver.execute_script("arguments[0].click();", warning_yes)

                # 🔁 Forzar reactivación del campo de fecha
                print("🔁 Rehaciendo clic en pestaña Currency Conversion Lists para activar Start Date...")
                ccl_tab = wait.until(EC.element_to_be_clickable((By.XPATH, '//a[contains(text(),"Currency Conversion Lists")]')))
                driver.execute_script("arguments[0].click();", ccl_tab)
                time.sleep(2.5)

                # 🕒 Ingresar fecha actual
                today = datetime.today().strftime("%d/%m/%Y %I:%M %p")
                print(f"📅 Ingresando Start Date en Currency Conversion Lists: {today}")

                # Esperar que haya al menos un input de fecha visible y activo
                date_inputs = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//input[contains(@id,"ATt5") and contains(@id,"::content")]')))
                target_input = None
                for inp in date_inputs:
                    try:
                        if inp.is_displayed() and inp.is_enabled():
                            target_input = inp
                            break
                    except:
                        continue

                if target_input:
                    driver.execute_script("arguments[0].scrollIntoView(true);", target_input)
                    time.sleep(0.3)
                    target_input.clear()
                    target_input.send_keys(today)
                    print("✅ Currency Conversion List agregado y fecha ingresada correctamente.")
                else:
                    raise Exception("❌ No se encontró un campo de Start Date activo para Currency Conversion Lists")
                print("✅ Currency Conversion List agregado y fecha ingresada correctamente.")

            except Exception as e:
                print(f"⚠️ Error al agregar Currency Conversion List '{currency_list}': {e}")
        else:
            print("⏩ Currency Conversion List marcado como 'NO APLICA'. Se omite.")

        save_and_close_btn = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[text()="Save and Close"]')))
        driver.execute_script("arguments[0].click();", save_and_close_btn)
        print(f"💾 Estrategia '{pricing_strategy}' guardada y cerrada.")

        time.sleep(2)

except Exception as e:
    print(f"❌ Error durante la ejecución: {e}")

finally:
    time.sleep(5)
    driver.quit()