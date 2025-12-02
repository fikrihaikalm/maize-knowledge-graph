"""
Graph Embedding dengan Node2Vec
Convert Knowledge Graph ke vector representations
"""

import rdflib
from rdflib import Graph, Namespace
import networkx as nx
from node2vec import Node2Vec
import numpy as np
import pandas as pd
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
import pickle

def load_kg(ttl_file):
    """Load Knowledge Graph from TTL file"""
    print(f"📂 Loading KG from: {ttl_file}")
    g = Graph()
    g.parse(ttl_file, format='turtle')
    print(f"✅ Loaded {len(g)} triples")
    return g

def rdf_to_networkx(rdf_graph):
    """Convert RDF graph to NetworkX graph"""
    print("\n🔄 Converting RDF to NetworkX...")
    G = nx.Graph()
    
    # Track different edge types
    edge_types = {}
    
    for subj, pred, obj in rdf_graph:
        # Extract local names (remove namespaces)
        s = str(subj).split('#')[-1].split('/')[-1]
        p = str(pred).split('#')[-1].split('/')[-1]
        o = str(obj).split('#')[-1].split('/')[-1]
        
        # Skip some metadata properties
        if p in ['type', 'label', 'comment']:
            continue
        
        # Add nodes
        G.add_node(s)
        G.add_node(o)
        
        # Add edge with relation type
        G.add_edge(s, o, relation=p)
        
        # Track edge types
        edge_types[p] = edge_types.get(p, 0) + 1
    
    print(f"✅ NetworkX Graph created:")
    print(f"   - Nodes: {G.number_of_nodes()}")
    print(f"   - Edges: {G.number_of_edges()}")
    print(f"   - Edge types: {len(edge_types)}")
    
    # Print top edge types
    print(f"\n📊 Top 5 Edge Types:")
    for edge_type, count in sorted(edge_types.items(), key=lambda x: x[1], reverse=True)[:5]:
        print(f"   - {edge_type}: {count}")
    
    return G

def train_node2vec(nx_graph, dimensions=64, walk_length=30, num_walks=200, p=1, q=1):
    """Train Node2Vec on the graph"""
    print("\n" + "="*60)
    print("🚀 Training Node2Vec...")
    print("="*60)
    print(f"   Dimensions: {dimensions}")
    print(f"   Walk length: {walk_length}")
    print(f"   Num walks per node: {num_walks}")
    print(f"   p (return param): {p}")
    print(f"   q (in-out param): {q}")
    
    # Initialize Node2Vec
    node2vec = Node2Vec(
        nx_graph,
        dimensions=dimensions,
        walk_length=walk_length,
        num_walks=num_walks,
        workers=4,
        p=p,
        q=q,
        seed=42
    )
    
    # Train model
    print("\n⏳ Training (this may take a few minutes)...")oke sekarang hapus file file yang tidak diperlukan. misal md yg tidak diperlukan, cp satu readme gitu
    model = node2vec.fit(window=10, min_count=1, batch_words=4, epochs=10)
    
    print("✅ Node2Vec training complete!")
    return model

def get_embeddings(model, nodes):
    """Get embedding vectors for all nodes"""
    print("\n📊 Extracting embeddings...")
    embeddings = {}
    missing = 0
    
    for node in nodes:
        try:
            embeddings[node] = model.wv[node]
        except KeyError:
            missing += 1
    
    print(f"✅ Extracted {len(embeddings)} embeddings")
    if missing > 0:
        print(f"⚠️  {missing} nodes not found in model")
    
    return embeddings

def visualize_embeddings(embeddings, output_file='embeddings_plot.png', max_labels=50):
    """Visualize embeddings using t-SNE"""
    print(f"\n🎨 Creating t-SNE visualization...")
    
    nodes = list(embeddings.keys())
    vectors = np.array([embeddings[n] for n in nodes])
    
    # Apply t-SNE
    tsne = TSNE(n_components=2, random_state=42, perplexity=min(30, len(nodes)-1))
    embeddings_2d = tsne.fit_transform(vectors)
    
    # Create plot
    plt.figure(figsize=(16, 12))
    
    # Color by first letter (simple categorization)
    colors = []
    for node in nodes:
        if node.startswith(('Hama', 'Fall', 'Cucumber', 'Spotted', 'Tobacco')):
            colors.append('red')
        elif node.startswith(('Maize', 'Downy', 'Sooty', 'Foot')):
            colors.append('blue')
        elif node.startswith(('Boron', 'Iron', 'Nitrogen', 'Zinc')):
            colors.append('green')
        else:
            colors.append('gray')
    
    plt.scatter(embeddings_2d[:, 0], embeddings_2d[:, 1], c=colors, alpha=0.6, s=50)
    
    # Annotate key nodes
    for i, node in enumerate(nodes[:max_labels]):
        plt.annotate(node, (embeddings_2d[i, 0], embeddings_2d[i, 1]), 
                    fontsize=7, alpha=0.7)
    
    plt.title('Knowledge Graph Embeddings (t-SNE Visualization)', fontsize=16)
    plt.xlabel('Dimension 1', fontsize=12)
    plt.ylabel('Dimension 2', fontsize=12)
    plt.grid(True, alpha=0.3)
    
    # Add legend
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor='red', label='Hama'),
        Patch(facecolor='blue', label='Penyakit'),
        Patch(facecolor='green', label='Defisiensi'),
        Patch(facecolor='gray', label='Lainnya')
    ]
    plt.legend(handles=legend_elements, loc='best')
    
    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"✅ Visualization saved to: {output_file}")
    
    plt.close()

def find_similar_entities(model, entity, top_k=10):
    """Find most similar entities"""
    try:
        similar = model.wv.most_similar(entity, topn=top_k)
        return similar
    except KeyError:
        return []

def save_embeddings(embeddings, output_file='entity_embeddings.csv'):
    """Save embeddings to CSV"""
    print(f"\n💾 Saving embeddings to: {output_file}")
    df = pd.DataFrame.from_dict(embeddings, orient='index')
    df.to_csv(output_file)
    print("✅ Embeddings saved!")

def save_model(model, output_file='node2vec_model.pkl'):
    """Save trained model"""
    print(f"\n💾 Saving model to: {output_file}")
"""
Graph Embedding dengan Node2Vec
Convert Knowledge Graph ke vector representations
"""

import rdflib
from rdflib import Graph, Namespace
import networkx as nx
from node2vec import Node2Vec
import numpy as np
import pandas as pd
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
import pickle

def load_kg(ttl_file):
    """Load Knowledge Graph from TTL file"""
    print(f"📂 Loading KG from: {ttl_file}")
    g = Graph()
    g.parse(ttl_file, format='turtle')
    print(f"✅ Loaded {len(g)} triples")
    return g

def rdf_to_networkx(rdf_graph):
    """Convert RDF graph to NetworkX graph"""
    print("\n🔄 Converting RDF to NetworkX...")
    G = nx.Graph()
    
    # Track different edge types
    edge_types = {}
    
    for subj, pred, obj in rdf_graph:
        # Extract local names (remove namespaces)
        s = str(subj).split('#')[-1].split('/')[-1]
        p = str(pred).split('#')[-1].split('/')[-1]
        o = str(obj).split('#')[-1].split('/')[-1]
        
        # Skip some metadata properties
        if p in ['type', 'label', 'comment']:
            continue
        
        # Add nodes
        G.add_node(s)
        G.add_node(o)
        
        # Add edge with relation type
        G.add_edge(s, o, relation=p)
        
        # Track edge types
        edge_types[p] = edge_types.get(p, 0) + 1
    
    print(f"✅ NetworkX Graph created:")
    print(f"   - Nodes: {G.number_of_nodes()}")
    print(f"   - Edges: {G.number_of_edges()}")
    print(f"   - Edge types: {len(edge_types)}")
    
    # Print top edge types
    print(f"\n📊 Top 5 Edge Types:")
    for edge_type, count in sorted(edge_types.items(), key=lambda x: x[1], reverse=True)[:5]:
        print(f"   - {edge_type}: {count}")
    
    return G

def train_node2vec(nx_graph, dimensions=64, walk_length=30, num_walks=200, p=1, q=1):
    """Train Node2Vec on the graph"""
    print("\n" + "="*60)
    print("🚀 Training Node2Vec...")
    print("="*60)
    print(f"   Dimensions: {dimensions}")
    print(f"   Walk length: {walk_length}")
    print(f"   Num walks per node: {num_walks}")
    print(f"   p (return param): {p}")
    print(f"   q (in-out param): {q}")
    
    # Initialize Node2Vec
    node2vec = Node2Vec(
        nx_graph,
        dimensions=dimensions,
        walk_length=walk_length,
        num_walks=num_walks,
        workers=4,
        p=p,
        q=q,
        seed=42
    )
    
    # Train model
    print("\n⏳ Training (this may take a few minutes)...")oke sekarang hapus file file yang tidak diperlukan. misal md yg tidak diperlukan, cp satu readme gitu
    model = node2vec.fit(window=10, min_count=1, batch_words=4, epochs=10)
    
    print("✅ Node2Vec training complete!")
    return model

def get_embeddings(model, nodes):
    """Get embedding vectors for all nodes"""
    print("\n📊 Extracting embeddings...")
    embeddings = {}
    missing = 0
    
    for node in nodes:
        try:
            embeddings[node] = model.wv[node]
        except KeyError:
            missing += 1
    
    print(f"✅ Extracted {len(embeddings)} embeddings")
    if missing > 0:
        print(f"⚠️  {missing} nodes not found in model")
    
    return embeddings

def visualize_embeddings(embeddings, output_file='embeddings_plot.png', max_labels=50):
    """Visualize embeddings using t-SNE"""
    print(f"\n🎨 Creating t-SNE visualization...")
    
    nodes = list(embeddings.keys())
    vectors = np.array([embeddings[n] for n in nodes])
    
    # Apply t-SNE
    tsne = TSNE(n_components=2, random_state=42, perplexity=min(30, len(nodes)-1))
    embeddings_2d = tsne.fit_transform(vectors)
    
    # Create plot
    plt.figure(figsize=(16, 12))
    
    # Color by first letter (simple categorization)
    colors = []
    for node in nodes:
        if node.startswith(('Hama', 'Fall', 'Cucumber', 'Spotted', 'Tobacco')):
            colors.append('red')
        elif node.startswith(('Maize', 'Downy', 'Sooty', 'Foot')):
            colors.append('blue')
        elif node.startswith(('Boron', 'Iron', 'Nitrogen', 'Zinc')):
            colors.append('green')
        else:
            colors.append('gray')
    
    plt.scatter(embeddings_2d[:, 0], embeddings_2d[:, 1], c=colors, alpha=0.6, s=50)
    
    # Annotate key nodes
    for i, node in enumerate(nodes[:max_labels]):
        plt.annotate(node, (embeddings_2d[i, 0], embeddings_2d[i, 1]), 
                    fontsize=7, alpha=0.7)
    
    plt.title('Knowledge Graph Embeddings (t-SNE Visualization)', fontsize=16)
    plt.xlabel('Dimension 1', fontsize=12)
    plt.ylabel('Dimension 2', fontsize=12)
    plt.grid(True, alpha=0.3)
    
    # Add legend
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor='red', label='Hama'),
        Patch(facecolor='blue', label='Penyakit'),
        Patch(facecolor='green', label='Defisiensi'),
        Patch(facecolor='gray', label='Lainnya')
    ]
    plt.legend(handles=legend_elements, loc='best')
    
    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"✅ Visualization saved to: {output_file}")
    
    plt.close()

def find_similar_entities(model, entity, top_k=10):
    """Find most similar entities"""
    try:
        similar = model.wv.most_similar(entity, topn=top_k)
        return similar
    except KeyError:
        return []

def save_embeddings(embeddings, output_file='entity_embeddings.csv'):
    """Save embeddings to CSV"""
    print(f"\n💾 Saving embeddings to: {output_file}")
    df = pd.DataFrame.from_dict(embeddings, orient='index')
    df.to_csv(output_file)
    print("✅ Embeddings saved!")

def save_model(model, output_file='node2vec_model.pkl'):
    """Save trained model"""
    print(f"\n💾 Saving model to: {output_file}")
    with open(output_file, 'wb') as f:
        pickle.dump(model, f)
    print("✅ Model saved!")

def main():
    print("="*60)
    print("Graph Embedding - Knowledge Graph Jagung")
    print("="*60)
    
    # 1. Load KG
    rdf_graph = load_kg('../ontology/corn_kg.ttl')
    
    # 2. Convert to NetworkX
    nx_graph = rdf_to_networkx(rdf_graph)
    
    # 3. Train Node2Vec
    model = train_node2vec(
        nx_graph, 
        dimensions=64,
        walk_length=30,
        num_walks=200,
        p=1,
        q=1
    )
    
    # 4. Get embeddings
    embeddings = get_embeddings(model, nx_graph.nodes())
    
    # 5. Save embeddings
    save_embeddings(embeddings, '../embeddings/entity_embeddings.csv')
    save_model(model, '../embeddings/node2vec_model.pkl')
    
    # 6. Visualize
    visualize_embeddings(embeddings, '../assets/embeddings_plot.png')
    
    # 7. Test similarity search
    print("\n" + "="*60)
    print("Testing Similarity Search")
    print("="*60)
    
    test_entities = ['Fall_Armyworm', 'Maize_Smut', 'Nitrogen_Deficiency']
    
    for entity in test_entities:
        print(f"\nSimilar to '{entity}':")
        similar = find_similar_entities(model, entity, top_k=5)
        if similar:
            for sim_entity, score in similar:
                print(f"   {score:.3f} - {sim_entity}")
        else:
            print(f"   Entity not found")
    
    print("\n" + "="*60)
    print("Graph Embedding Complete")
    print("="*60)
    print("\nGenerated files:")
    print("   - ../embeddings/entity_embeddings.csv")
    print("   - ../embeddings/node2vec_model.pkl")
    print("   - ../assets/embeddings_plot.png")

if __name__ == "__main__":
    main()
