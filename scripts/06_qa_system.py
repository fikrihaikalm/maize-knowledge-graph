"""
QA System untuk Knowledge Graph Jagung
Streamlit Web App dengan Graph Embedding
"""

import streamlit as st
import pandas as pd
import numpy as np
from rdflib import Graph
import pickle
from scipy.spatial.distance import cosine

# Page config
st.set_page_config(
    page_title="🌽 KG Jagung QA System",
    page_icon="🌽",
    layout="wide"
def find_similar_by_embedding(entity, embeddings, top_k=5):
    """Find similar entities using cosine similarity"""
    if entity not in embeddings:
        return []
    
    entity_vec = embeddings[entity]
    similarities = []
    
    for other_entity, other_vec in embeddings.items():
        if other_entity != entity:
            sim = 1 - cosine(entity_vec, other_vec)
            similarities.append((other_entity, sim))
    
    similarities.sort(key=lambda x: x[1], reverse=True)
    return similarities[:top_k]

def query_kg(g, entity):
    """Query KG for entity information"""
    query = f"""
    PREFIX : <http://example.org/maize-kg#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    
    SELECT ?label ?comment ?gejala ?bagian ?pengendalian ?patogen WHERE {{
        ?entity rdfs:label "{entity}"@id .
        OPTIONAL {{ ?entity rdfs:label ?label }}
        OPTIONAL {{ ?entity rdfs:comment ?comment }}
        OPTIONAL {{ ?entity :memilikiGejala ?g . ?g rdfs:label ?gejala }}
        OPTIONAL {{ ?entity :menyerangBagian ?b . ?b rdfs:label ?bagian }}
        OPTIONAL {{ ?entity :dikendalikanDengan ?p . ?p rdfs:label ?pengendalian }}
        OPTIONAL {{ ?entity :disebabkanOleh ?pat . ?pat rdfs:label ?patogen }}
    }}
    """
    
    results = g.query(query)
    return results

def answer_question(question, g, embeddings, model):
    """Answer user question"""
    question_lower = question.lower()
    
    # Extract potential entities from question
    entities = []
    for entity in embeddings.keys():
        entity_clean = entity.replace('_', ' ').lower()
        if entity_clean in question_lower:
            entities.append(entity)
    
    if not entities:
        return "Maaf, saya tidak menemukan entitas yang relevan dalam pertanyaan Anda.", None, None
    
    # Use first entity found
    main_entity = entities[0]
    
    # Query KG
    results = query_kg(g, main_entity)
    
    # Find similar entities
    similar = find_similar_by_embedding(main_entity, embeddings, top_k=5)
    
    # Build answer
    answer_parts = []
    answer_parts.append(f"**Informasi tentang {main_entity.replace('_', ' ')}:**\n")
    
    # Extract info from SPARQL results
    gejala_set = set()
    bagian_set = set()
    pengendalian_set = set()
    patogen_set = set()
    comment = None
    
    for row in results:
        if row.comment:
            comment = str(row.comment)
        if row.gejala:
            gejala_set.add(str(row.gejala))
        if row.bagian:
            bagian_set.add(str(row.bagian))
        if row.pengendalian:
            pengendalian_set.add(str(row.pengendalian))
        if row.patogen:
            patogen_set.add(str(row.patogen))
    
    if comment:
        answer_parts.append(f"\n📖 **Definisi:** {comment}")
    
    if patogen_set:
        answer_parts.append(f"\n🦠 **Disebabkan oleh:** {', '.join(patogen_set)}")
    
    if gejala_set:
        answer_parts.append(f"\n🔴 **Gejala:** {', '.join(list(gejala_set)[:5])}")
    
    if bagian_set:
        answer_parts.append(f"\n🌿 **Menyerang bagian:** {', '.join(bagian_set)}")
    
    if pengendalian_set:
        answer_parts.append(f"\n💊 **Pengendalian:** {', '.join(list(pengendalian_set)[:5])}")
    
    answer = '\n'.join(answer_parts)
    
    return answer, main_entity, similar

# ========================================
# STREAMLIT UI
# ========================================

st.title("🌽 Sistem Tanya Jawab Knowledge Graph Jagung")
st.markdown("---")

# Sidebar
with st.sidebar:
    st.header("ℹ️ Informasi")
    st.markdown("""
    **Knowledge Graph QA System**
    
    Sistem ini menggunakan:
    - 🧠 OWL Reasoning
    - 🔢 Graph Embedding (Node2Vec)
    - 🔍 SPARQL Query
    - 📊 Similarity Search
    
    **Cara Menggunakan:**
    1. Ketik pertanyaan Anda
    2. Sistem akan mencari entitas relevan
    3. Jawaban ditampilkan dari KG
    4. Entitas similar juga ditampilkan
    """)
    
    st.markdown("---")
    st.markdown("**Contoh Pertanyaan:**")
    st.markdown("""
    - Apa gejala Fall Armyworm?
    - Bagaimana mengendalikan ulat grayak?
    - Apa penyebab maize smut?
    - Gejala defisiensi nitrogen?
    """)

# Load data
with st.spinner("Loading Knowledge Graph..."):
    g = load_kg()
    embeddings = load_embeddings()
    model = load_model()

st.success(f"✅ Loaded {len(embeddings)} entities from Knowledge Graph")

# Main interface
st.header("💬 Tanya Sesuatu!")

# Question input
question = st.text_input(
    "Ketik pertanyaan Anda:",
    placeholder="Contoh: Apa gejala fall armyworm?"
)

if question:
    with st.spinner("🔍 Mencari jawaban..."):
        answer, main_entity, similar = answer_question(question, g, embeddings, model)
    
    # Display answer
    st.markdown("### 📝 Jawaban:")
    st.markdown(answer)
    
    # Display similar entities
    if similar:
        st.markdown("---")
        st.markdown("### 🔗 Entitas yang Mirip:")
        
        cols = st.columns(5)
        for i, (entity, score) in enumerate(similar):
            with cols[i % 5]:
                st.metric(
                    label=entity.replace('_', ' '),
                    value=f"{score:.2f}",
                    help="Similarity score"
                )

# Expander untuk exploratory search
with st.expander("🔍 Pencarian Langsung (Search by Entity)"):
    st.markdown("Cari informasi langsung berdasarkan nama entitas:")
    
    # Get all entities
    all_entities = sorted(list(embeddings.keys()))
    
    selected_entity = st.selectbox(
        "Pilih entitas:",
        options=all_entities,
        format_func=lambda x: x.replace('_', ' ')
    )
    
    if st.button("Cari Informasi"):
        with st.spinner("Searching..."):
            # Query KG
            results = query_kg(g, selected_entity)
            
            # Find similar
            similar = find_similar_by_embedding(selected_entity, embeddings, top_k=10)
            
            # Display
            st.markdown(f"### 📊 Informasi: {selected_entity.replace('_', ' ')}")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Dari Knowledge Graph:**")
                for row in results:
                    if row.comment:
                        st.info(f"**Definisi:** {row.comment}")
                    if row.gejala:
                        st.write(f"🔴 Gejala: {row.gejala}")
                    if row.bagian:
                        st.write(f"🌿 Bagian: {row.bagian}")
                    if row.pengendalian:
                        st.write(f"💊 Pengendalian: {row.pengendalian}")
            
            with col2:
                st.markdown("**Entitas Serupa (Embedding):**")
                for entity, score in similar[:5]:
                    st.write(f"• {entity.replace('_', ' ')} ({score:.3f})")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center'>
    <p>🌽 Knowledge Graph Jagung | Powered by OWL + Node2Vec + SPARQL</p>
</div>
""", unsafe_allow_html=True)
