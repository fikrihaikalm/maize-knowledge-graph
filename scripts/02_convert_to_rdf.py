"""
Convert plantix_manual_30.json to RDF/Turtle
FIXED VERSION - Semua masalah diperbaiki!
"""

import json
from datetime import datetime

def safe_id(text):
    """Convert text to safe RDF ID"""
    return text.replace(' ', '_').replace('(', '').replace(')', '').replace('.', '').replace(',', '').replace('#', '').replace('/', '_')

def generate_rdf():
    """Generate RDF/Turtle from plantix_manual_30.json"""
    
    # Load data
    with open('plantix_manual_30.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Start TTL
    ttl = """@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix : <http://example.org/maize-kg#> .

# ========================================
# Knowledge Graph Hama & Penyakit Jagung
# Generated: """ + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + """
# FIXED: Class names Indonesia, Patogen filled, Domain/Range set
# ========================================

<http://example.org/maize-kg> a owl:Ontology ;
    rdfs:label "Knowledge Graph Hama & Penyakit Jagung"@id ;
    rdfs:comment "Ontologi untuk hama, penyakit, dan defisiensi pada tanaman jagung"@id .

# ========================================
# SECTION 1: TOP CLASSES (BAHASA INDONESIA!)
# ========================================

:Hama a owl:Class ;
    rdfs:label "Hama"@id ;
    rdfs:comment "Organisme yang merusak tanaman jagung"@id .

:Penyakit a owl:Class ;
    rdfs:label "Penyakit"@id ;
    rdfs:comment "Penyakit yang disebabkan oleh patogen"@id .

:DefisiensiUnsur a owl:Class ;
    rdfs:label "Defisiensi Unsur"@id ;
    rdfs:comment "Kekurangan unsur hara esensial"@id .

:Gejala a owl:Class ;
    rdfs:label "Gejala"@id ;
    rdfs:comment "Tanda atau manifestasi dari hama/penyakit"@id .

:BagianTanaman a owl:Class ;
    rdfs:label "Bagian Tanaman"@id ;
    rdfs:comment "Organ tanaman jagung"@id .

:Patogen a owl:Class ;
    rdfs:label "Patogen"@id ;
    rdfs:comment "Jenis patogen penyebab penyakit"@id .

:Vektor a owl:Class ;
    rdfs:label "Vektor"@id ;
    rdfs:comment "Organisme penyebar penyakit"@id .

:FaktorLingkungan a owl:Class ;
    rdfs:label "Faktor Lingkungan"@id ;
    rdfs:comment "Kondisi lingkungan yang mempengaruhi"@id .

:Pencegahan a owl:Class ;
    rdfs:label "Pencegahan"@id ;
    rdfs:comment "Metode pencegahan"@id .

:Pengendalian a owl:Class ;
    rdfs:label "Pengendalian"@id ;
    rdfs:comment "Metode pengendalian hama/penyakit"@id .

# Subclasses of Pengendalian
:PengendalianBiologis a owl:Class ;
    rdfs:subClassOf :Pengendalian ;
    rdfs:label "Pengendalian Biologis"@id ;
    rdfs:comment "Pengendalian menggunakan agen biologis"@id .

:PengendalianKimia a owl:Class ;
    rdfs:subClassOf :Pengendalian ;
    rdfs:label "Pengendalian Kimia"@id ;
    rdfs:comment "Pengendalian menggunakan pestisida/fungisida"@id .

:PengendalianMekanis a owl:Class ;
    rdfs:subClassOf :Pengendalian ;
    rdfs:label "Pengendalian Mekanis"@id ;
    rdfs:comment "Pengendalian secara fisik/manual"@id .

:Tanaman a owl:Class ;
    rdfs:label "Tanaman"@id .

# ========================================
# SECTION 2: OBJECT PROPERTIES (dengan Domain & Range UNION!)
# ========================================

:memilikiGejala a owl:ObjectProperty ;
    rdfs:label "memiliki gejala"@id ;
    rdfs:comment "Relasi hama/penyakit/defisiensi dengan gejala yang ditimbulkan"@id ;
    rdfs:domain [
        a owl:Class ;
        owl:unionOf ( :Hama :Penyakit :DefisiensiUnsur )
    ] ;
    rdfs:range :Gejala .

:menyerangBagian a owl:ObjectProperty ;
    rdfs:label "menyerang bagian"@id ;
    rdfs:comment "Relasi dengan bagian tanaman yang diserang"@id ;
    rdfs:domain [
        a owl:Class ;
        owl:unionOf ( :Hama :Penyakit :DefisiensiUnsur )
    ] ;
    rdfs:range :BagianTanaman .

:disebarkanOleh a owl:ObjectProperty ;
    rdfs:label "disebarkan oleh"@id ;
    rdfs:comment "Relasi dengan vektor penyebar"@id ;
    rdfs:domain :Penyakit ;  # Hanya Penyakit yang punya vektor
    rdfs:range :Vektor .

:dipengaruhiOleh a owl:ObjectProperty ;
    rdfs:label "dipengaruhi oleh"@id ;
    rdfs:comment "Relasi dengan faktor lingkungan"@id ;
    rdfs:domain [
        a owl:Class ;
        owl:unionOf ( :Hama :Penyakit :DefisiensiUnsur )
    ] ;
    rdfs:range :FaktorLingkungan .

:dicegahDengan a owl:ObjectProperty ;
    rdfs:label "dicegah dengan"@id ;
    rdfs:comment "Relasi dengan metode pencegahan"@id ;
    rdfs:domain [
        a owl:Class ;
        owl:unionOf ( :Hama :Penyakit :DefisiensiUnsur )
    ] ;
    rdfs:range :Pencegahan .

:dikendalikanDengan a owl:ObjectProperty ;
    rdfs:label "dikendalikan dengan"@id ;
    rdfs:comment "Relasi dengan metode pengendalian"@id ;
    rdfs:domain [
        a owl:Class ;
        owl:unionOf ( :Hama :Penyakit :DefisiensiUnsur )
    ] ;
    rdfs:range :Pengendalian .

:menyerangTanaman a owl:ObjectProperty ;
    rdfs:label "menyerang tanaman"@id ;
    rdfs:domain [
        a owl:Class ;
        owl:unionOf ( :Hama :Penyakit :DefisiensiUnsur )
    ] ;
    rdfs:range :Tanaman .

:disebabkanOleh a owl:ObjectProperty ;
    rdfs:label "disebabkan oleh"@id ;
    rdfs:comment "Relasi penyakit/hama dengan jenis patogen"@id ;
    rdfs:domain [
        a owl:Class ;
        owl:unionOf ( :Hama :Penyakit :DefisiensiUnsur )
    ] ;
    rdfs:range :Patogen .

# ========================================
# SECTION 3: DATA PROPERTIES (dengan Domain UNION!)
# ========================================

:namaIlmiah a owl:DatatypeProperty ;
    rdfs:label "nama ilmiah"@id ;
    rdfs:domain [
        a owl:Class ;
        owl:unionOf ( :Hama :Penyakit :DefisiensiUnsur :Tanaman )
    ] ;
    rdfs:range xsd:string .

:penyebabUtama a owl:DatatypeProperty ;
    rdfs:label "penyebab utama"@id ;
    rdfs:domain [
        a owl:Class ;
        owl:unionOf ( :Hama :Penyakit :DefisiensiUnsur )
    ] ;
    rdfs:range xsd:string .

# ========================================
# SECTION 4: TANAMAN INDIVIDUAL
# ========================================

:Jagung a :Tanaman ;
    rdfs:label "Jagung"@id ;
    :namaIlmiah "Zea mays" .

# ========================================
# SECTION 5: PATOGEN INDIVIDUALS (FILLED!)
# ========================================

:virus a :Patogen ;
    rdfs:label "Virus"@id ;
    rdfs:comment "Patogen mikroskopis yang bereplikasi di dalam sel"@id .

:jamur a :Patogen ;
    rdfs:label "Jamur"@id ;
    rdfs:comment "Patogen fungi yang menyebabkan penyakit"@id .

:bakteri a :Patogen ;
    rdfs:label "Bakteri"@id ;
    rdfs:comment "Patogen bakteri"@id .

:serangga a :Patogen ;
    rdfs:label "Serangga"@id ;
    rdfs:comment "Hama serangga"@id .

:defisiensi a :Patogen ;
    rdfs:label "Defisiensi"@id ;
    rdfs:comment "Kekurangan unsur hara"@id .

# ========================================
# SECTION 6: GEJALA INDIVIDUALS
# ========================================

"""
    
    # Collect unique entities
    gejala_set = set()
    bagian_set = set()
    vektor_set = set()
    faktor_set = set()
    pencegahan_set = set()
    pengendalian_biologis_set = set()
    pengendalian_kimia_set = set()
    pengendalian_mekanis_set = set()
    
    for item in data:
        gejala_set.update(item.get('gejala', []))
        bagian_set.update(item.get('bagianTanaman', []))
        vektor_set.update(item.get('vektor', []))
        faktor_set.update(item.get('faktorLingkungan', []))
        pencegahan_set.update(item.get('pencegahan', []))
        pengendalian_biologis_set.update(item.get('pengendalianBiologis', []))
        pengendalian_kimia_set.update(item.get('pengendalianKimia', []))
        pengendalian_mekanis_set.update(item.get('pengendalianMekanis', []))
    
    # Add Gejala
    for gejala in sorted(gejala_set):
        label = gejala.replace('_', ' ').title()
        ttl += f"""
:{gejala} a :Gejala ;
    rdfs:label "{label}"@id .\n"""
    
    # Bagian Tanaman
    ttl += "\n# ========================================\n"
    ttl += "# SECTION 7: BAGIAN TANAMAN INDIVIDUALS\n"
    ttl += "# ========================================\n\n"
    
    for bagian in sorted(bagian_set):
        label = bagian.replace('_', ' ').title()
        ttl += f"""
:{bagian} a :BagianTanaman ;
    rdfs:label "{label}"@id .\n"""
    
    # Vektor
    ttl += "\n# ========================================\n"
    ttl += "# SECTION 8: VEKTOR INDIVIDUALS\n"
    ttl += "# ========================================\n\n"
    
    for vektor in sorted(vektor_set):
        if vektor:
            label = vektor.replace('_', ' ').title()
            ttl += f"""
:{vektor} a :Vektor ;
    rdfs:label "{label}"@id .\n"""
    
    # Faktor Lingkungan
    ttl += "\n# ========================================\n"
    ttl += "# SECTION 9: FAKTOR LINGKUNGAN INDIVIDUALS\n"
    ttl += "# ========================================\n\n"
    
    for faktor in sorted(faktor_set):
        if faktor:
            label = faktor.replace('_', ' ').title()
            ttl += f"""
:{faktor} a :FaktorLingkungan ;
    rdfs:label "{label}"@id .\n"""
    
    # Pencegahan
    ttl += "\n# ========================================\n"
    ttl += "# SECTION 10: PENCEGAHAN INDIVIDUALS\n"
    ttl += "# ========================================\n\n"
    
    for p in sorted(pencegahan_set):
        if p:
            label = p.replace('_', ' ').title()
            ttl += f"""
:{p} a :Pencegahan ;
    rdfs:label "{label}"@id .\n"""
    
    # Pengendalian Biologis
    ttl += "\n# ========================================\n"
    ttl += "# SECTION 11: PENGENDALIAN BIOLOGIS INDIVIDUALS\n"
    ttl += "# ========================================\n\n"
    
    for p in sorted(pengendalian_biologis_set):
        if p:
            label = p.replace('_', ' ').title()
            ttl += f"""
:{p} a :PengendalianBiologis ;
    rdfs:label "{label}"@id .\n"""
    
    # Pengendalian Kimia
    ttl += "\n# ========================================\n"
    ttl += "# SECTION 12: PENGENDALIAN KIMIA INDIVIDUALS\n"
    ttl += "# ========================================\n\n"
    
    for p in sorted(pengendalian_kimia_set):
        if p:
            label = p.replace('_', ' ').title()
            ttl += f"""
:{p} a :PengendalianKimia ;
    rdfs:label "{label}"@id .\n"""
    
    # Pengendalian Mekanis
    ttl += "\n# ========================================\n"
    ttl += "# SECTION 13: PENGENDALIAN MEKANIS INDIVIDUALS\n"
    ttl += "# ========================================\n\n"
    
    for p in sorted(pengendalian_mekanis_set):
        if p:
            label = p.replace('_', ' ').title()
            ttl += f"""
:{p} a :PengendalianMekanis ;
    rdfs:label "{label}"@id .\n"""
    
    # HAMA, PENYAKIT, DEFISIENSI INDIVIDUALS
    ttl += "\n# ========================================\n"
    ttl += "# SECTION 14: HAMA INDIVIDUALS\n"
    ttl += "# ========================================\n\n"
    
    hama_count = 0
    for item in data:
        if item['jenis'] == 'Hama':
            hama_count += 1
            item_id = safe_id(f"{item['nama']}")
            
            ttl += f"\n:{item_id} a :Hama ;\n"
            ttl += f'    rdfs:label "{item["nama"]}"@id ;\n'
            ttl += f'    :namaIlmiah "{item["namaIlmiah"]}" ;\n'
            ttl += f'    :penyebabUtama "{item["penyebabUtama"]}" ;\n'
            ttl += f'    :disebabkanOleh :serangga ;\n'  # Hama = serangga
            ttl += f'    :menyerangTanaman :Jagung ;\n'
            
            if item.get('gejala'):
                gejala_list = ', '.join([f':{g}' for g in item['gejala']])
                ttl += f"    :memilikiGejala {gejala_list} ;\n"
            
            if item.get('bagianTanaman'):
                bagian_list = ', '.join([f':{b}' for b in item['bagianTanaman']])
                ttl += f"    :menyerangBagian {bagian_list} ;\n"
            
            if item.get('vektor'):
                vektor_list = ', '.join([f':{v}' for v in item['vektor']])
                ttl += f"    :disebarkanOleh {vektor_list} ;\n"
            
            if item.get('faktorLingkungan'):
                faktor_list = ', '.join([f':{f}' for f in item['faktorLingkungan']])
                ttl += f"    :dipengaruhiOleh {faktor_list} ;\n"
            
            if item.get('pencegahan'):
                pencegahan_list = ', '.join([f':{p}' for p in item['pencegahan']])
                ttl += f"    :dicegahDengan {pencegahan_list} ;\n"
            
            # Pengendalian dengan subclass yang tepat
            all_control = []
            all_control.extend([f':{p}' for p in item.get('pengendalianBiologis', [])])
            all_control.extend([f':{p}' for p in item.get('pengendalianKimia', [])])
            all_control.extend([f':{p}' for p in item.get('pengendalianMekanis', [])])
            if all_control:
                control_list = ', '.join(all_control)
                ttl += f"    :dikendalikanDengan {control_list} ;\n"
            
            ttl = ttl.rstrip(';\n') + ' .\n'
    
    # PENYAKIT
    ttl += "\n# ========================================\n"
    ttl += "# SECTION 15: PENYAKIT INDIVIDUALS\n"
    ttl += "# ========================================\n\n"
    
    penyakit_count = 0
    for item in data:
        if item['jenis'] == 'Penyakit':
            penyakit_count += 1
            item_id = safe_id(f"{item['nama']}")
            
            # Determine patogen type
            patogen_type = ':jamur'
            if item['jenisPatogen'] == 'virus':
                patogen_type = ':virus'
            elif item['jenisPatogen'] == 'bakteri':
                patogen_type = ':bakteri'
            elif item['jenisPatogen'] == 'jamur':
                patogen_type = ':jamur'
            
            ttl += f"\n:{item_id} a :Penyakit ;\n"
            ttl += f'    rdfs:label "{item["nama"]}"@id ;\n'
            ttl += f'    :namaIlmiah "{item["namaIlmiah"]}" ;\n'
            ttl += f'    :penyebabUtama "{item["penyebabUtama"]}" ;\n'
            ttl += f'    :disebabkanOleh {patogen_type} ;\n'
            ttl += f'    :menyerangTanaman :Jagung ;\n'
            
            if item.get('gejala'):
                gejala_list = ', '.join([f':{g}' for g in item['gejala']])
                ttl += f"    :memilikiGejala {gejala_list} ;\n"
            
            if item.get('bagianTanaman'):
                bagian_list = ', '.join([f':{b}' for b in item['bagianTanaman']])
                ttl += f"    :menyerangBagian {bagian_list} ;\n"
            
            if item.get('vektor'):
                vektor_list = ', '.join([f':{v}' for v in item['vektor']])
                ttl += f"    :disebarkanOleh {vektor_list} ;\n"
            
            if item.get('faktorLingkungan'):
                faktor_list = ', '.join([f':{f}' for f in item['faktorLingkungan']])
                ttl += f"    :dipengaruhiOleh {faktor_list} ;\n"
            
            if item.get('pencegahan'):
                pencegahan_list = ', '.join([f':{p}' for p in item['pencegahan']])
                ttl += f"    :dicegahDengan {pencegahan_list} ;\n"
            
            all_control = []
            all_control.extend([f':{p}' for p in item.get('pengendalianBiologis', [])])
            all_control.extend([f':{p}' for p in item.get('pengendalianKimia', [])])
            all_control.extend([f':{p}' for p in item.get('pengendalianMekanis', [])])
            if all_control:
                control_list = ', '.join(all_control)
                ttl += f"    :dikendalikanDengan {control_list} ;\n"
            
            ttl = ttl.rstrip(';\n') + ' .\n'
    
    # DEFISIENSI
    ttl += "\n# ========================================\n"
    ttl += "# SECTION 16: DEFISIENSI UNSUR INDIVIDUALS\n"
    ttl += "# ========================================\n\n"
    
    defisiensi_count = 0
    for item in data:
        if item['jenis'] == 'DefisiensiUnsur':
            defisiensi_count += 1
            item_id = safe_id(f"{item['nama']}")
            
            ttl += f"\n:{item_id} a :DefisiensiUnsur ;\n"
            ttl += f'    rdfs:label "{item["nama"]}"@id ;\n'
            ttl += f'    :namaIlmiah "{item["namaIlmiah"]}" ;\n'
            ttl += f'    :penyebabUtama "{item["penyebabUtama"]}" ;\n'
            ttl += f'    :disebabkanOleh :defisiensi ;\n'
            ttl += f'    :menyerangTanaman :Jagung ;\n'
            
            if item.get('gejala'):
                gejala_list = ', '.join([f':{g}' for g in item['gejala']])
                ttl += f"    :memilikiGejala {gejala_list} ;\n"
            
            if item.get('bagianTanaman'):
                bagian_list = ', '.join([f':{b}' for b in item['bagianTanaman']])
                ttl += f"    :menyerangBagian {bagian_list} ;\n"
            
            if item.get('faktorLingkungan'):
                faktor_list = ', '.join([f':{f}' for f in item['faktorLingkungan']])
                ttl += f"    :dipengaruhiOleh {faktor_list} ;\n"
            
            if item.get('pencegahan'):
                pencegahan_list = ', '.join([f':{p}' for p in item['pencegahan']])
                ttl += f"    :dicegahDengan {pencegahan_list} ;\n"
            
            all_control = []
            all_control.extend([f':{p}' for p in item.get('pengendalianBiologis', [])])
            all_control.extend([f':{p}' for p in item.get('pengendalianKimia', [])])
            if all_control:
                control_list = ', '.join(all_control)
                ttl += f"    :dikendalikanDengan {control_list} ;\n"
            
            ttl = ttl.rstrip(';\n') + ' .\n'
    
    # Save
    with open('maize_kg.ttl', 'w', encoding='utf-8') as f:
        f.write(ttl)
    
    print("✅ Created maize_kg.ttl (FIXED VERSION!)")
    print(f"\n📊 Statistics:")
    print(f"   - Classes: 14 (termasuk subclass Pengendalian)")
    print(f"   - Hama: {hama_count}")
    print(f"   - Penyakit: {penyakit_count}")
    print(f"   - DefisiensiUnsur: {defisiensi_count}")
    print(f"   - Patogen: 5 (virus, jamur, bakteri, serangga, defisiensi)")
    print(f"   - Gejala: {len(gejala_set)}")
    print(f"   - Bagian Tanaman: {len(bagian_set)}")
    print(f"\n✅ FIXED:")
    print(f"   ✓ Class names: BAHASA INDONESIA")
    print(f"   ✓ Pengendalian: Subclass (Biologis, Kimia, Mekanis)")
    print(f"   ✓ Patogen: FILLED (5 individuals)")
    print(f"   ✓ Object properties: Domain & Range SET")
    print(f"   ✓ Data properties: Domain & Range SET")

if __name__ == "__main__":
    generate_rdf()
