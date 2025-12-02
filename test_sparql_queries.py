"""
SPARQL Query Testing untuk Knowledge Graph Jagung
10 queries untuk testing berbagai aspek KG
"""

from rdflib import Graph
import pandas as pd

def load_kg():
    """Load Knowledge Graph"""
    g = Graph()
    g.parse('ontology/corn_kg.ttl', format='turtle')
    print(f"Loaded {len(g)} triples from corn_kg.ttl\n")
    return g

def print_results(title, results, limit=None):
    """Print query results dengan format yang rapi"""
    print("="*80)
    print(f"QUERY: {title}")
    print("="*80)
    
    result_list = list(results)
    
    if not result_list:
        print("No results found.\n")
        return
    
    # Convert to DataFrame for better display
    data = []
    for row in result_list[:limit] if limit else result_list:
        data.append({str(var): str(row[var]) for var in row.labels})
    
    if data:
        df = pd.DataFrame(data)
        print(df.to_string(index=False))
        print(f"\nTotal results: {len(result_list)}")
        if limit and len(result_list) > limit:
            print(f"(Showing first {limit} of {len(result_list)} results)")
    
    print("\n")

# ============================================================================
# LOAD KNOWLEDGE GRAPH
# ============================================================================

g = load_kg()

# ============================================================================
# QUERY 1: Menampilkan semua Hama beserta nama ilmiah dan penyebab utama
# ============================================================================

query1 = """
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

results1 = g.query(query1)
print_results("1. Semua Hama dengan Nama Ilmiah dan Penyebab Utama", results1)

# ============================================================================
# QUERY 2: Hama/Penyakit yang menyerang DAUN beserta gejalanya
# ============================================================================

query2 = """
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

results2 = g.query(query2)
print_results("2. Entitas yang Menyerang Daun dan Gejalanya", results2)

# ============================================================================
# QUERY 3: Metode Pengendalian untuk Fall Armyworm
# ============================================================================

query3 = """
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

results3 = g.query(query3)
print_results("3. Metode Pengendalian untuk Fall Armyworm", results3)

# ============================================================================
# QUERY 4: Penyakit yang disebabkan oleh VIRUS
# ============================================================================

query4 = """
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

results4 = g.query(query4)
print_results("4. Penyakit yang Disebabkan oleh Virus", results4)

# ============================================================================
# QUERY 5: Hitung jumlah Hama, Penyakit, dan Defisiensi
# ============================================================================

query5 = """
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

results5 = g.query(query5)
print_results("5. Statistik: Jumlah Hama, Penyakit, dan Defisiensi", results5)

# ============================================================================
# QUERY 6: Gejala yang paling sering muncul (TOP 5)
# ============================================================================

query6 = """
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

results6 = g.query(query6)
print_results("6. Top 5 Gejala Paling Sering Muncul", results6)

# ============================================================================
# QUERY 7: Entitas yang bisa dicegah dengan ROTASI TANAMAN
# ============================================================================

query7 = """
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

results7 = g.query(query7)
print_results("7. Entitas yang Dicegah dengan Rotasi Tanaman", results7)

# ============================================================================
# QUERY 8: Defisiensi Unsur dengan gejala KLOROSIS
# ============================================================================

query8 = """
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

results8 = g.query(query8)
print_results("8. Defisiensi Unsur dengan Gejala Klorosis", results8)

# ============================================================================
# QUERY 9: Entitas lengkap dengan semua informasinya (contoh: Fall Armyworm)
# ============================================================================

query9 = """
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

results9 = g.query(query9)
print_results("9. Informasi Lengkap Fall Armyworm", results9, limit=20)

# ============================================================================
# QUERY 10: Pengendalian Biologis yang paling banyak digunakan
# ============================================================================

query10 = """
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

results10 = g.query(query10)
print_results("10. Top 5 Pengendalian Biologis Paling Banyak Digunakan", results10)

# ============================================================================
# SUMMARY
# ============================================================================

print("="*80)
print("TESTING SELESAI!")
print("="*80)
print("\nAnda telah menjalankan 10 SPARQL queries yang mencakup:")
print("1. SELECT sederhana dengan filtering")
print("2. JOIN antar entitas (bagian tanaman + gejala)")
print("3. Query spesifik untuk satu entitas")
print("4. Filtering berdasarkan tipe patogen")
print("5. Aggregation (COUNT, GROUP BY)")
print("6. Ordering dan LIMIT")
print("7. Query dengan OPTIONAL")
print("8. Multiple conditions")
print("9. Explore semua properties dari satu entitas")
print("10. Ranking dengan aggregation")
print("\nSemua query berhasil dijalankan!")
