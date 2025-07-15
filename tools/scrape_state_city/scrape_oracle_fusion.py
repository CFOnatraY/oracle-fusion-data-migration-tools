import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# URL de la página de Oracle Fusion que deseas raspar
URL = os.getenv("URL")

# Configura las opciones de Chrome para Selenium
options = Options()
options.add_argument("--headless")  # Ejecutar en modo sin cabeza (sin UI)
options.add_argument("--disable-gpu")  # Desactivar GPU (ayuda a evitar problemas en algunos sistemas)

# Configura el controlador de Chrome (esto descargará el controlador adecuado)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Navega a la página de Oracle Fusion
driver.get(URL)

# Espera explícita para cargar la página
driver.implicitly_wait(10)  # Espera hasta 10 segundos para que los elementos estén disponibles

# Extrae el listado de departamentos del campo 'DEPARTMENT'
department_dropdown = driver.find_element(By.ID, "FOpt1:_FOr1:0:_FONSr2:0:MAnt2:1:cupt1:CManF:1:cupanel1:sitedet:0:pt_r1:0:dynam1:0:s2:i1:3:inputComboboxListOfValues1")  # Asegúrate de que el ID sea correcto
departments = [option.text for option in department_dropdown.find_elements(By.TAG_NAME, "option")]

# Diccionario para almacenar las ciudades por cada departamento
cities_by_department = {}

# Para cada departamento seleccionado, se extraen las ciudades relacionadas
for department in departments:
    # Seleccionamos el departamento (el proceso puede variar según cómo esté configurado el dropdown)
    department_dropdown.send_keys(department)
    time.sleep(2)  # Espera para permitir que las ciudades se carguen

    # Encontrar el dropdown de la ciudad y extraer las opciones
    city_dropdown = driver.find_element(By.ID, "FOpt1:_FOr1:0:_FONSr2:0:MAnt2:1:cupt1:CManF:1:cupanel1:sitedet:0:pt_r1:0:dynam1:0:s2:i1:4:inputComboboxListOfValues2")  # Asegúrate de que el ID sea correcto
    cities = [option.text for option in city_dropdown.find_elements(By.TAG_NAME, "option")]

    # Guardamos las ciudades en el diccionario bajo su departamento correspondiente
    cities_by_department[department] = cities

# Imprime el diccionario con los departamentos y sus ciudades
print("Departamentos y sus ciudades:")
for department, cities in cities_by_department.items():
    print(f"{department}: {', '.join(cities)}")

# Cierra el navegador
driver.quit()
