"""
Generate corn_kg.ttl from plantix_manual_30.json
Includes Indonesian definitions and correct classification.
"""

import json
import os
from datetime import datetime

def safe_id(text):
    """Convert text to safe RDF ID"""
    if not text: return ""
    return text.replace(' ', '_').replace('(', '').replace(')', '').replace('.', '').replace(',', '').replace('#', '').replace('/', '_').replace("'", "")

def generate_kg():
    # Paths
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    json_path = os.path.join(base_dir, 'data', 'plantix_manual_30.json')
    vocab_path = os.path.join(base_dir, 'data', 'vocabulary_definitions.json')
    disease_defs_path = os.path.join(base_dir, 'data', 'disease_definitions.json')
    output_path = os.path.join(base_dir, 'ontology', 'corn_kg.ttl')

    print(f"Loading data from {json_path}...")
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Load definitions if available, otherwise use fallbacks/manual
    # For this script, we will embed the manual definitions to ensure they are used as requested
    
    # Header
    ttl = """@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix : <http://example.org/maize-kg#> .

<http://example.org/maize-kg> a owl:Ontology ;
    rdfs:label "Knowledge Graph Hama & Penyakit Jagung"@id ;
    rdfs:comment "Ontologi hama dan penyakit jagung dengan definisi Bahasa Indonesia"@id .

# CLASSES
:Hama a owl:Class ; rdfs:label "Hama"@id .
:Penyakit a owl:Class ; rdfs:label "Penyakit"@id .
:DefisiensiUnsur a owl:Class ; rdfs:label "Defisiensi Unsur"@id .
:Gejala a owl:Class ; rdfs:label "Gejala"@id .
:BagianTanaman a owl:Class ; rdfs:label "Bagian Tanaman"@id .
:Patogen a owl:Class ; rdfs:label "Patogen"@id .
:Vektor a owl:Class ; rdfs:label "Vektor"@id .
:FaktorLingkungan a owl:Class ; rdfs:label "Faktor Lingkungan"@id .
:Pencegahan a owl:Class ; rdfs:label "Pencegahan"@id .
:Pengendalian a owl:Class ; rdfs:label "Pengendalian"@id .
:PengendalianBiologis a owl:Class ; rdfs:subClassOf :Pengendalian ; rdfs:label "Pengendalian Biologis"@id .
:PengendalianKimia a owl:Class ; rdfs:subClassOf :Pengendalian ; rdfs:label "Pengendalian Kimia"@id .
:PengendalianMekanis a owl:Class ; rdfs:subClassOf :Pengendalian ; rdfs:label "Pengendalian Mekanis"@id .
:Tanaman a owl:Class ; rdfs:label "Tanaman"@id .

# PROPERTIES
:memilikiGejala a owl:ObjectProperty ; rdfs:domain [ a owl:Class ; owl:unionOf (:Hama :Penyakit :DefisiensiUnsur) ] ; rdfs:range :Gejala .
:menyerangBagian a owl:ObjectProperty ; rdfs:domain [ a owl:Class ; owl:unionOf (:Hama :Penyakit :DefisiensiUnsur) ] ; rdfs:range :BagianTanaman .
:disebarkanOleh a owl:ObjectProperty ; rdfs:domain :Penyakit ; rdfs:range :Vektor .
:dipengaruhiOleh a owl:ObjectProperty ; rdfs:domain [ a owl:Class ; owl:unionOf (:Hama :Penyakit :DefisiensiUnsur) ] ; rdfs:range :FaktorLingkungan .
:dicegahDengan a owl:ObjectProperty ; rdfs:domain [ a owl:Class ; owl:unionOf (:Hama :Penyakit :DefisiensiUnsur) ] ; rdfs:range :Pencegahan .
:dikendalikanDengan a owl:ObjectProperty ; rdfs:domain [ a owl:Class ; owl:unionOf (:Hama :Penyakit :DefisiensiUnsur) ] ; rdfs:range :Pengendalian .
:menyerangTanaman a owl:ObjectProperty ; rdfs:domain [ a owl:Class ; owl:unionOf (:Hama :Penyakit :DefisiensiUnsur) ] ; rdfs:range :Tanaman .
:disebabkanOleh a owl:ObjectProperty ; rdfs:domain [ a owl:Class ; owl:unionOf (:Hama :Penyakit :DefisiensiUnsur) ] ; rdfs:range :Patogen .
:namaIlmiah a owl:DatatypeProperty ; rdfs:range xsd:string .
:penyebabUtama a owl:DatatypeProperty ; rdfs:range xsd:string .

# INDIVIDUALS (Static)
:Jagung a :Tanaman ; rdfs:label "Jagung"@id ; :namaIlmiah "Zea mays" .
:virus a :Patogen ; rdfs:label "Virus"@id .
:jamur a :Patogen ; rdfs:label "Jamur"@id .
:bakteri a :Patogen ; rdfs:label "Bakteri"@id .
:serangga a :Patogen ; rdfs:label "Serangga"@id .
:defisiensi a :Patogen ; rdfs:label "Defisiensi"@id .

"""

    # Manual Definitions Map (Indonesian)
    definitions = {
        # Hama
        'Fall_Armyworm': 'Hama ulat yang sangat destruktif, menyerang daun dan tongkol jagung.',
        'Cucumber_Beetle': 'Kumbang yang menyerang akar dan daun, dapat menyebarkan penyakit layu.',
        'Spotted_Stemborer': 'Penggerek batang yang merusak jaringan dalam batang.',
        'Tobacco_Caterpillar': 'Ulat grayak yang menyerang daun secara berkelompok.',
        'Flower_Chafer': 'Kumbang yang menyerang bunga dan pollen.',
        'Helicoverpa_Caterpillar': 'Ulat penggerek buah dan tongkol yang polifag.',
        'Termites': 'Rayap yang menyerang akar dan batang bawah.',
        'Brown_Stink_Bug': 'Kepik pengisap cairan biji yang menyebabkan biji keriput.',
        'Sugarcane_Pyrilla': 'Wereng tebu yang menghisap cairan tanaman.',
        'Shoot_Flies': 'Lalat pucuk yang menyerang pucuk muda.',
        'Spotted_Maize_Beetle': 'Kumbang berbintik yang menyerang kepala bunga.',
        'Bagrada_Bug': 'Kepik penghisap yang menyerang tanaman muda.',
        'Black_Cutworm': 'Ulat tanah yang memotong batang tanaman muda.',
        
        # Penyakit
        'Maize_Chlorotic_Mottle_Virus': 'Penyakit virus penyebab bercak klorosis pada daun.',
        'Downy_Mildew_of_Maize': 'Penyakit embun bulu yang menyebabkan pertumbuhan putih.',
        'Maize_Bushy_Stunt_Phytoplasma': 'Penyakit phytoplasma menyebabkan tanaman kerdil.',
        'Stunt_of_Maize': 'Penyakit kerdil yang disebabkan Spiroplasma.',
        'Maize_Smut': 'Penyakit jamur membentuk benjolan hitam pada tongkol.',
        'Sooty_Mold': 'Jamur jelaga yang tumbuh pada embun madu.',
        'Fruit_Molds': 'Jamur buah penyebab pembusukan.',
        'Foot_and_Collar_Rot': 'Busuk pangkal batang menyebabkan tanaman layu.',
        'Maize_Lethal_Necrosis_Disease': 'Penyakit nekrosis mematikan akibat kombinasi virus.',
        'Leaf_Spot_of_Maize': 'Bercak daun menyebabkan klorosis dan nekrosis.',
        'Stalk_Rot_of_Maize': 'Busuk batang yang menyebabkan batang rapuh.',
        'Northern_Leaf_Spot_of_Maize': 'Bercak daun utara dengan lesi memanjang.',
        'Damping-Off_of_Seedlings': 'Penyakit rebah semai pada bibit muda.',
        
        # Defisiensi
        'Boron_Deficiency': 'Kekurangan unsur Boron menghambat pertumbuhan.',
        'Iron_Deficiency': 'Kekurangan zat besi menyebabkan klorosis interveinal.',
        'Nitrogen_Deficiency': 'Kekurangan nitrogen menyebabkan daun menguning.',
        'Zinc_Deficiency': 'Kekurangan seng menyebabkan daun memutih.',
    }

    # Sets to collect unique vocabulary items
    vocabs = {
        'Gejala': set(),
        'BagianTanaman': set(),
        'Vektor': set(),
        'FaktorLingkungan': set(),
        'Pencegahan': set(),
        'PengendalianBiologis': set(),
        'PengendalianKimia': set(),
        'PengendalianMekanis': set()
    }

    print("Processing items...")
    for item in data:
        # Determine class
        cls = item['jenis']
        if cls not in [':Hama', ':Penyakit', ':DefisiensiUnsur']:
            # Fallback mapping if needed, though data seems clean
            if item['jenis'] == 'Hama': cls = ':Hama'
            elif item['jenis'] == 'Penyakit': cls = ':Penyakit'
            elif item['jenis'] == 'DefisiensiUnsur': cls = ':DefisiensiUnsur'
            else: cls = ':Hama' # Default

        safe_name = safe_id(item['nama'])
        ttl += f"\n:{safe_name} a {cls} ;\n"
        ttl += f'    rdfs:label "{item["nama"]}"@id ;\n'
        
        # Definition
        if safe_name in definitions:
            ttl += f'    rdfs:comment "{definitions[safe_name]}"@id ;\n'
        
        ttl += f'    :namaIlmiah "{item["namaIlmiah"]}" ;\n'
        ttl += f'    :penyebabUtama "{item["penyebabUtama"]}" ;\n'
        ttl += f'    :menyerangTanaman :Jagung ;\n'

        # Pathogen type
        if item.get('jenisPatogen'):
            pat_map = {
                'virus': ':virus', 'jamur': ':jamur', 'bakteri': ':bakteri', 
                'serangga': ':serangga', 'defisiensi': ':defisiensi'
            }
            pat = pat_map.get(item['jenisPatogen'], ':serangga')
            ttl += f'    :disebabkanOleh {pat} ;\n'

        # Lists processing
        def add_list_prop(prop, values, vocab_key):
            res = ""
            if values:
                safe_vals = [f":{safe_id(v)}" for v in values]
                res += f'    {prop} {", ".join(safe_vals)} ;\n'
                vocabs[vocab_key].update(values)
            return res

        ttl += add_list_prop(':memilikiGejala', item.get('gejala', []), 'Gejala')
        ttl += add_list_prop(':menyerangBagian', item.get('bagianTanaman', []), 'BagianTanaman')
        ttl += add_list_prop(':disebarkanOleh', item.get('vektor', []), 'Vektor')
        ttl += add_list_prop(':dipengaruhiOleh', item.get('faktorLingkungan', []), 'FaktorLingkungan')
        ttl += add_list_prop(':dicegahDengan', item.get('pencegahan', []), 'Pencegahan')
        
        # Controls
        controls = []
        
        bio = item.get('pengendalianBiologis', [])
        if bio:
            safe_bio = [f":{safe_id(x)}" for x in bio]
            controls.extend(safe_bio)
            vocabs['PengendalianBiologis'].update(bio)
            
        kim = item.get('pengendalianKimia', [])
        if kim:
            safe_kim = [f":{safe_id(x)}" for x in kim]
            controls.extend(safe_kim)
            vocabs['PengendalianKimia'].update(kim)
            
        mek = item.get('pengendalianMekanis', [])
        if mek:
            safe_mek = [f":{safe_id(x)}" for x in mek]
            controls.extend(safe_mek)
            vocabs['PengendalianMekanis'].update(mek)
            
        if controls:
            ttl += f'    :dikendalikanDengan {", ".join(controls)} ;\n'

        ttl = ttl.rstrip(' ;\n') + " .\n"

    # Add Vocabulary Individuals
    print("Adding vocabulary individuals...")
    
    for vocab_type, items in vocabs.items():
        ttl += f"\n# {vocab_type}\n"
        for item in sorted(items):
            safe_item = safe_id(item)
            label = item.replace('_', ' ').title()
            ttl += f":{safe_item} a :{vocab_type} ; rdfs:label \"{label}\"@id .\n"

    # Write output
    print(f"Writing to {output_path}...")
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(ttl)
    print("Done!")

if __name__ == "__main__":
    generate_kg()
