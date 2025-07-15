from bs4 import BeautifulSoup
import re

# XML completo (usé el fragmento que enviaste, pero para el ejemplo cortado en la parte principal)
xml_response = '''<?xml version="1.0" ?>
<?Adf-Rich-Response-Type ?>
<content action="/fscmUI/faces/FndOverview?_adf.ctrl-state=b9kufglj0_847&amp;pageParams=fndGlobalItemNodeId%3DitemNode_receivables_billing&amp;fndGlobalItemNodeId=itemNode_receivables_billing">
  <fragment><![CDATA[
    <div>
      <label for="_FOpt1:_FOr1:0:_FONSr2:0:MAnt2:1:cupt1:CManF:1:cupanel1:sitedet:0:pt_r1:0:dynam1:0:s2:i1:4:inputComboboxListOfValues2::content">Ciudad</label>
      <select id="_FOpt1:_FOr1:0:_FONSr2:0:MAnt2:1:cupt1:CManF:1:cupanel1:sitedet:0:pt_r1:0:dynam1:0:s2:i1:4:inputComboboxListOfValues2::content" name="some_name" style="width:14em" class="xpj" maxlength="240" type="text" value="PALMIRA" role="combobox" aria-describedby="desc" aria-expanded="false" aria-live="off">
        <option value="0">Bogotá</option>
        <option value="1">Medellín</option>
        <option value="2">Cali</option>
        <option value="3" selected>Palmira</option>
        <option value="4">Barranquilla</option>
      </select>
    </div>
  ]]></fragment>
</content>
'''

# 1. Extraer contenido CDATA del XML
cdata_pattern = re.compile(r'<!\[CDATA\[(.*?)\]\]>', re.DOTALL)
cdata_matches = cdata_pattern.findall(xml_response)

ciudades = []

for cdata in cdata_matches:
    # 2. Parsear el HTML contenido en CDATA
    soup = BeautifulSoup(cdata, 'html.parser')

    # 3. Buscar el label que contiene "Ciudad"
    label = soup.find('label', string=lambda s: s and 'Ciudad' in s)
    if label:
        select_id = label.get('for')
        if select_id:
            # 4. Buscar el select con el id indicado en el label "for"
            select = soup.find('select', id=select_id)
            if select:
                # 5. Extraer texto de todas las opciones dentro del select
                for option in select.find_all('option'):
                    text = option.get_text(strip=True)
                    if text:
                        ciudades.append(text)

if ciudades:
    print("Ciudades encontradas:")
    for ciudad in ciudades:
        print(ciudad)
else:
    print("No se encontraron ciudades en el XML.")
