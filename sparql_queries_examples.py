"""
SPARQL Query Examples untuk Knowledge Graph Jagung
File ini berisi contoh-contoh query SPARQL yang bisa digunakan langsung
"""

# ============================================================================
# QUERY 1: Menampilkan semua Hama beserta nama ilmiah dan penyebab utama
# ============================================================================
# Use case: Melihat daftar semua hama dalam KG
# Output: nama, namaIlmiah, penyebabUtama

QUERY_1_ALL_PESTS = """
PREFIX : <http://example.org/maize-kg#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?nama ?namaIlmiah ?penyebabUtama WHERE {
    ?hama a :Hama .
    ?hama rdfs:label ?nama .
    ?hama :namaIlmiah ?namaIlmiah .
    ?hama :penyebabUtama ?penyebabUtama .
}
ORDER BY ?nama
"""

# ============================================================================
# QUERY 2: Hama/Penyakit yang menyerang DAUN beserta gejalanya
# ============================================================================
# Use case: Mencari entitas yang menyerang bagian tanaman tertentu
# Output: nama entitas, gejala

QUERY_2_ATTACKS_LEAVES = """
PREFIX : <http://example.org/maize-kg#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?entitas ?gejala WHERE {
    ?e rdfs:label ?entitas .
    ?e :menyerangBagian :daun .
    ?e :memilikiGejala ?g .
    ?g rdfs:label ?gejala .
}
ORDER BY ?entitas ?gejala
"""

# ============================================================================
# QUERY 3: Metode Pengendalian untuk entitas tertentu (contoh: Fall Armyworm)
# ============================================================================
# Use case: Mencari cara mengendalikan hama/penyakit spesifik
# Output: jenis pengendalian, metode

QUERY_3_CONTROL_METHODS = """
PREFIX : <http://example.org/maize-kg#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?jenisPengendalian ?metode WHERE {
    :Fall_Armyworm :dikendalikanDengan ?p .
    ?p rdfs:label ?metode .
    ?p a ?type .
    ?type rdfs:label ?jenisPengendalian .
    FILTER(?type IN (:PengendalianBiologis, :PengendalianKimia, :PengendalianMekanis))
}
ORDER BY ?jenisPengendalian ?metode
"""

# ============================================================================
# QUERY 4: Penyakit yang disebabkan oleh patogen tertentu (contoh: VIRUS)
# ============================================================================
# Use case: Filter penyakit berdasarkan jenis patogen
# Output: nama penyakit, nama ilmiah, penyebab

QUERY_4_DISEASES_BY_PATHOGEN = """
PREFIX : <http://example.org/maize-kg#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?penyakit ?namaIlmiah ?penyebab WHERE {
    ?p a :Penyakit .
    ?p rdfs:label ?penyakit .
    ?p :namaIlmiah ?namaIlmiah .
    ?p :disebabkanOleh :virus .
    ?p :penyebabUtama ?penyebab .
}
ORDER BY ?penyakit
"""

# Variasi: ganti :virus dengan :jamur, :bakteri, :serangga, :defisiensi

# ============================================================================
# QUERY 5: Statistik - Hitung jumlah Hama, Penyakit, dan Defisiensi
# ============================================================================
# Use case: Mendapatkan overview dataset
# Output: kategori, jumlah

QUERY_5_STATISTICS = """
PREFIX : <http://example.org/maize-kg#>

SELECT ?kategori (COUNT(?entitas) AS ?jumlah) WHERE {
    {
        ?entitas a :Hama .
        BIND("Hama" AS ?kategori)
    } UNION {
        ?entitas a :Penyakit .
        BIND("Penyakit" AS ?kategori)
    } UNION {
        ?entitas a :DefisiensiUnsur .
        BIND("Defisiensi Unsur" AS ?kategori)
    }
}
GROUP BY ?kategori
ORDER BY ?kategori
"""

# ============================================================================
# QUERY 6: Gejala yang paling sering muncul (TOP 5)
# ============================================================================
# Use case: Analisis gejala yang paling umum
# Output: gejala, frekuensi kemunculan

QUERY_6_TOP_SYMPTOMS = """
PREFIX : <http://example.org/maize-kg#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?gejala (COUNT(?entitas) AS ?frekuensi) WHERE {
    ?entitas :memilikiGejala ?g .
    ?g rdfs:label ?gejala .
}
GROUP BY ?gejala
ORDER BY DESC(?frekuensi)
LIMIT 5
"""

# ============================================================================
# QUERY 7: Entitas yang bisa dicegah dengan metode tertentu
# ============================================================================
# Use case: Mencari entitas yang cocok dengan metode pencegahan tertentu
# Output: nama entitas, jenis (Hama/Penyakit/Defisiensi)

QUERY_7_PREVENTION_METHOD = """
PREFIX : <http://example.org/maize-kg#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?entitas ?jenis WHERE {
    ?e rdfs:label ?entitas .
    ?e :dicegahDengan :rotasi_tanaman .
    ?e a ?type .
    ?type rdfs:label ?jenis .
    FILTER(?type IN (:Hama, :Penyakit, :DefisiensiUnsur))
}
ORDER BY ?jenis ?entitas
"""

# Variasi: ganti :rotasi_tanaman dengan metode lain seperti:
# :varietas_tahan, :sanitasi_lahan, :drainase_baik, dll

# ============================================================================
# QUERY 8: Defisiensi dengan gejala tertentu
# ============================================================================
# Use case: Diagnosis defisiensi berdasarkan gejala
# Output: nama defisiensi, unsur, bagian yang terserang

QUERY_8_DEFICIENCY_BY_SYMPTOM = """
PREFIX : <http://example.org/maize-kg#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?defisiensi ?unsur ?bagian WHERE {
    ?d a :DefisiensiUnsur .
    ?d rdfs:label ?defisiensi .
    ?d :namaIlmiah ?unsur .
    ?d :memilikiGejala :klorosis .
    OPTIONAL {
        ?d :menyerangBagian ?b .
        ?b rdfs:label ?bagian .
    }
}
ORDER BY ?defisiensi
"""

# Variasi: ganti :klorosis dengan gejala lain

# ============================================================================
# QUERY 9: Informasi lengkap untuk satu entitas
# ============================================================================
# Use case: Mendapatkan semua informasi tentang entitas tertentu
# Output: property, value

QUERY_9_ENTITY_DETAILS = """
PREFIX : <http://example.org/maize-kg#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?property ?value WHERE {
    :Fall_Armyworm ?p ?o .
    ?p rdfs:label ?property .
    
    OPTIONAL { ?o rdfs:label ?label }
    
    BIND(IF(BOUND(?label), ?label, STR(?o)) AS ?value)
}
ORDER BY ?property
"""

# Variasi: ganti :Fall_Armyworm dengan entitas lain

# ============================================================================
# QUERY 10: Ranking metode pengendalian yang paling banyak digunakan
# ============================================================================
# Use case: Mencari metode pengendalian yang paling efektif/populer
# Output: nama pengendalian, jumlah penggunaan

QUERY_10_TOP_CONTROL_METHODS = """
PREFIX : <http://example.org/maize-kg#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?pengendalian (COUNT(?entitas) AS ?digunakan_oleh) WHERE {
    ?entitas :dikendalikanDengan ?p .
    ?p a :PengendalianBiologis .
    ?p rdfs:label ?pengendalian .
}
GROUP BY ?pengendalian
ORDER BY DESC(?digunakan_oleh)
LIMIT 5
"""

# Variasi: ganti :PengendalianBiologis dengan :PengendalianKimia atau :PengendalianMekanis

# ============================================================================
# BONUS QUERIES
# ============================================================================

# BONUS 1: Entitas yang disebarkan oleh vektor tertentu
QUERY_BONUS_1 = """
PREFIX : <http://example.org/maize-kg#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?penyakit ?vektor WHERE {
    ?p a :Penyakit .
    ?p rdfs:label ?penyakit .
    ?p :disebarkanOleh ?v .
    ?v rdfs:label ?vektor .
}
ORDER BY ?vektor ?penyakit
"""

# BONUS 2: Entitas yang dipengaruhi oleh faktor lingkungan tertentu
QUERY_BONUS_2 = """
PREFIX : <http://example.org/maize-kg#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?entitas ?faktor WHERE {
    ?e rdfs:label ?entitas .
    ?e :dipengaruhiOleh ?f .
    ?f rdfs:label ?faktor .
}
ORDER BY ?faktor ?entitas
"""

# BONUS 3: Pencarian berdasarkan nama ilmiah (partial match)
QUERY_BONUS_3 = """
PREFIX : <http://example.org/maize-kg#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?nama ?namaIlmiah WHERE {
    ?e rdfs:label ?nama .
    ?e :namaIlmiah ?namaIlmiah .
    FILTER(CONTAINS(LCASE(?namaIlmiah), "spodoptera"))
}
"""

# ============================================================================
# CARA MENGGUNAKAN
# ============================================================================

"""
CARA 1: Menggunakan rdflib (Python)

from rdflib import Graph

g = Graph()
g.parse('ontology/corn_kg.ttl', format='turtle')

results = g.query(QUERY_1_ALL_PESTS)
for row in results:
    print(f"{row.nama} - {row.namaIlmiah}")

CARA 2: Menggunakan Apache Jena (Command Line)

arq --data=ontology/corn_kg.ttl --query=query1.sparql

CARA 3: Menggunakan Protege (GUI)

1. Load corn_kg.ttl di Protege
2. Buka tab "DL Query" atau plugin SPARQL
3. Paste query
4. Execute

CARA 4: Menggunakan SPARQL Endpoint (jika deploy ke server)

curl -X POST http://localhost:3030/maize/sparql \
  --data-urlencode "query=SELECT * WHERE { ?s ?p ?o } LIMIT 10"
"""
