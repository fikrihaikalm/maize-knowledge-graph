# Knowledge Graph untuk Hama dan Penyakit Tanaman Jagung

Repository untuk sistem Knowledge Graph lengkap mencakup ontology, reasoning, graph embedding, dan question answering system untuk identifikasi hama dan penyakit pada tanaman jagung.

---

## Struktur Direktori

```
KG/
├── data/                           # Data mentah dan hasil ekstraksi
│   ├── plantix.json               # Data original (50 entries)
│   ├── plantix.csv                # Format CSV
│   ├── plantix_manual_30.json     # Manual extraction (30 items)
│   ├── plantix_manual_30.csv      # Format CSV
│   ├── vocabulary_definitions.json # Definisi vocabulary terms
│   └── disease_definitions.json    # Definisi penyakit/hama
│
├── ontology/                       # Knowledge Graph (TTL/RDF)
│   ├── corn_kg.ttl                # Main KG (dengan definisi)
│   └── maize_kg.ttl               # Base KG (tanpa definisi)
│
├── embeddings/                     # Graph embeddings output
│   ├── entity_embeddings.csv      # Vector representations (64-dim)
│   └── node2vec_model.pkl         # Trained Node2Vec model
│
├── assets/                         # Visualisasi dan output
│   └── embeddings_plot.png        # t-SNE visualization
│
├── scripts/                        # Python scripts
│   ├── 01_create_manual_extraction.py   # Generate manual extraction
│   ├── 02_convert_to_rdf.py             # Convert CSV to TTL
│   ├── 03_generate_kg_with_definitions.py # Generate corn_kg.ttl
│   ├── 04_reasoning.py                  # OWL reasoning
│   ├── 05_graph_embedding.py            # Node2Vec embedding
│   └── 06_qa_system.py                  # Streamlit QA system
│
└── README.md                       # Dokumentasi (file ini)
```

---

## Tahapan Project

### 1. Data Collection
- **Input**: plantix.json (330KB, 50 entries)
- **Output**: Dataset hama dan penyakit jagung

### 2. Manual Extraction
- **Script**: `01_create_manual_extraction.py`
- **Metode**: Manual extraction dengan strict vocabulary
- **Output**: plantix_manual_30.json (30 items)

### 3. RDF Generation
- **Script**: `03_generate_kg_with_definitions.py`
- **Format**: Turtle (TTL)
- **Output**: corn_kg.ttl (Knowledge Graph dengan definisi)

### 4. Reasoning (Optional)
- **Script**: `04_reasoning.py`
- **Method**: RDFS-based inference
- **Output**: corn_kg_reasoned.ttl

### 5. Graph Embedding
- **Script**: `05_graph_embedding.py`
- **Algorithm**: Node2Vec
- **Parameters**: 64-dim, walk_length=30, num_walks=200
- **Output**: entity_embeddings.csv, node2vec_model.pkl

### 6. Question Answering System
- **Script**: `06_qa_system.py`
- **Framework**: Streamlit
- **Features**: SPARQL query, similarity search, entity exploration

---

## Quick Start

### Instalasi Dependencies

```bash
pip install rdflib networkx node2vec scikit-learn matplotlib pandas scipy streamlit
```

### Generate Knowledge Graph

```bash
# Step 1: Generate manual extraction (sudah ada hasilnya)
python scripts/01_create_manual_extraction.py

# Step 2: Generate Knowledge Graph dengan definisi
python scripts/03_generate_kg_with_definitions.py
```

### Generate Graph Embeddings

```bash
python scripts/05_graph_embedding.py
```

Output:
- embeddings/entity_embeddings.csv
- embeddings/node2vec_model.pkl
- assets/embeddings_plot.png

### Jalankan QA System

```bash
streamlit run scripts/06_qa_system.py
```

Browser akan otomatis membuka di http://localhost:8501

---

## Ontology Structure

### Classes

**Main Classes:**
- Hama (Pest)
- Penyakit (Disease)  
- DefisiensiUnsur (Nutrient Deficiency)

**Supporting Classes:**
- Gejala (Symptom)
- BagianTanaman (Plant Part)
- Patogen (Pathogen): virus, jamur, bakteri, serangga, defisiensi
- Vektor (Vector)
- FaktorLingkungan (Environmental Factor)
- Pencegahan (Prevention)
- Pengendalian (Control)
  - PengendalianBiologis (Biological Control)
  - PengendalianKimia (Chemical Control)
  - PengendalianMekanis (Mechanical Control)

### Object Properties

- memilikiGejala: has symptom
- menyerangBagian: attacks part
- menyerangTanaman: attacks plant
- disebarkanOleh: spread by
- dipengaruhiOleh: influenced by
- dicegahDengan: prevented by
- dikendalikanDengan: controlled by
- disebabkanOleh: caused by

### Data Properties

- namaIlmiah: scientific name
- penyebabUtama: main cause

---

## Graph Embedding

### Method: Node2Vec

**Parameters:**
- Dimensions: 64
- Walk Length: 30
- Number of Walks: 200 per node
- p (return parameter): 1
- q (in-out parameter): 1

**Applications:**
1. Entity Similarity - menemukan entitas serupa
2. Link Prediction - prediksi relasi yang hilang
3. Entity Clustering - grouping entitas sejenis
4. Recommendation - rekomendasi metode pengendalian

**Evaluation:**
- Visual inspection: t-SNE plot
- Similarity score: cosine similarity > 0.7 untuk entitas sejenis
- Clustering quality: separation antar kategori (hama, penyakit, defisiensi)

---

## QA System Features

### 1. Natural Language Question Answering

Sistem menjawab pertanyaan dalam bahasa natural:

```
Input: "Apa gejala fall armyworm?"
Output:
  - Definisi: Hama ulat yang sangat destruktif...
  - Gejala: lubang_daun, frass, defoliasi
  - Pengendalian: chlorpyrifos, bacillus_thuringiensis
```

### 2. Similarity-based Recommendation

Sistem menampilkan entitas serupa berdasarkan embedding:

```
Similar to Fall_Armyworm:
  - Helicoverpa_Caterpillar (0.89)
  - Tobacco_Caterpillar (0.82)
```

### 3. Entity Explorer

Browse dan eksplorasi semua entitas dalam Knowledge Graph dengan informasi lengkap dari SPARQL query.

---

## Troubleshooting

### Error: File not found

Pastikan working directory benar dan jalankan dari root project:

```bash
cd e:\Project\KG
python scripts/05_graph_embedding.py
```

### Error: entity_embeddings.csv not found

Jalankan graph embedding terlebih dahulu:

```bash
python scripts/05_graph_embedding.py
```

### Streamlit cache error

Clear cache Streamlit:

```bash
streamlit cache clear
streamlit run scripts/06_qa_system.py
```

---

## Technical Stack

**Data Processing:**
- Python 3.x
- pandas
- rdflib

**Graph Processing:**
- networkx
- node2vec

**Machine Learning:**
- scikit-learn
- scipy

**Visualization:**
- matplotlib
- Streamlit

**Ontology:**
- OWL 2
- RDF/Turtle
- SPARQL 1.1

---

## Dataset Information

**Source**: Plantix Dataset  
**Domain**: Pertanian - Tanaman Jagung  
**Total Entries**: 50 (original), 30 (curated)  
**Language**: Bahasa Indonesia  
**Format**: JSON, CSV, TTL/RDF

**Entities:**
- Hama: 13 instances
- Penyakit: 13 instances
- Defisiensi Unsur: 4 instances
- Gejala: 13 types
- Bagian Tanaman: 8 types
- Pengendalian: 35 methods (biologis, kimia, mekanis)

---

## Untuk Laporan

### File Utama yang Harus Dilampirkan:

**Data:**
1. data/plantix_manual_30.json
2. ontology/corn_kg.ttl

**Embeddings:**
3. embeddings/entity_embeddings.csv
4. assets/embeddings_plot.png

**Scripts:**
5. scripts/01_create_manual_extraction.py
6. scripts/03_generate_kg_with_definitions.py
7. scripts/05_graph_embedding.py
8. scripts/06_qa_system.py

**Documentation:**
9. README.md (file ini)

**Screenshots:**
10. Screenshot Protege (class hierarchy)
11. Screenshot QA System (pertanyaan + jawaban)
12. Screenshot t-SNE visualization

---

## Checklist Deliverables

- [x] Domain Discovery
- [x] Representasi Graf & Ontologi
- [x] Akuisisi Data
- [x] Ekstraksi Entitas & Relasi
- [x] Integrasi Data & Schema Matching
- [x] Graph Embedding (Node2Vec)
- [x] Reasoning (RDFS-based)
- [x] SPARQL Query
- [x] QA System (Streamlit)

---

## References

**Tools:**
- rdflib: https://rdflib.readthedocs.io/
- Node2Vec: https://github.com/eliorc/node2vec
- Streamlit: https://docs.streamlit.io/

**Standards:**
- OWL 2: https://www.w3.org/TR/owl2-overview/
- RDF 1.1: https://www.w3.org/TR/rdf11-concepts/
- SPARQL 1.1: https://www.w3.org/TR/sparql11-query/

---

**Project Status:** Complete  
**Last Updated:** 2025-12-02  
**Domain:** Agriculture - Maize Pests & Diseases
