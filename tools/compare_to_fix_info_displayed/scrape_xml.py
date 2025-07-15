import xml.etree.ElementTree as ET
import pandas as pd

# Ruta del archivo XML
xml_path = "xml_reference_report.xml"  # Cambia a tu ruta real si es distinta

# Parsear el archivo XML
tree = ET.parse(xml_path)
root = tree.getroot()

# Recorrer todos los nodos <G_1>
data = []
for g1 in root.findall("G_1"):
    row = {child.tag: child.text for child in g1}
    data.append(row)

# Convertir a DataFrame
df = pd.DataFrame(data)

# Exportar a Excel
output_path = "reporte_convertido.xlsx"
df.to_excel(output_path, index=False)

print(f"✅ Archivo exportado exitosamente a: {output_path}")
