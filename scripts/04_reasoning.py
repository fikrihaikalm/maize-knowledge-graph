"""
OWL Reasoning Script untuk Knowledge Graph Jagung
Menggunakan rdflib dengan SPARQL-based inference
"""

from rdflib import Graph, Namespace, RDF, RDFS, OWL
from rdflib.namespace import SKOS
import os

def run_reasoning(input_file='corn_kg.ttl', output_file='corn_kg_reasoned.ttl'):
    """
    Run simple RDFS/OWL reasoning pada knowledge graph
    
    Args:
        input_file: Input TTL file
        output_file: Output TTL file dengan hasil reasoning
    """
    
    print("="*60)
    print("🧠 RDFS/OWL REASONING - Knowledge Graph Jagung")
    print("="*60)
    
    # 1. Load ontology
    print(f"\n📂 Loading ontology from: {input_file}")
    try:
        g = Graph()
        g.parse(input_file, format='turtle')
        print(f"✅ Loaded {len(g)} triples")
    except Exception as e:
        print(f"❌ Error loading ontology: {e}")
        return
    
    # Define namespaces
    EX = Namespace("http://example.org/maize-kg#")
    
    # 2. Print statistics BEFORE reasoning
    print("\n📊 BEFORE Reasoning:")
    
    # Count classes
    classes = set(g.subjects(RDF.type, OWL.Class))
    print(f"   - Classes: {len(classes)}")
    
    # Count individuals
    individuals = set()
    for s, p, o in g:
        if (s, RDF.type, OWL.Class) not in g:
            if isinstance(s, rdflib.term.URIRef) and '#' in str(s):
                individuals.add(s)
    print(f"   - Individuals: {len(individuals)}")
    
    # Count properties
    obj_props = set(g.subjects(RDF.type, OWL.ObjectProperty))
    data_props = set(g.subjects(RDF.type, OWL.DatatypeProperty))
    print(f"   - Object Properties: {len(obj_props)}")
    print(f"   - Data Properties: {len(data_props)}")
    
    # 3. Apply simple inference rules
    print("\n⚙️  Applying inference rules...")
    
    inferred_count = 0
    
    # Rule 1: SubClass inference (RDFS)
    # If X subClassOf Y and A type X, then A type Y
    print("   → Applying subClassOf inference...")
    subclass_query = """
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    
    SELECT ?instance ?superclass WHERE {
        ?instance rdf:type ?subclass .
        ?subclass rdfs:subClassOf ?superclass .
        FILTER NOT EXISTS { ?instance rdf:type ?superclass }
    }
    """
    
    for row in g.query(subclass_query):
        g.add((row.instance, RDF.type, row.superclass))
        inferred_count += 1
    
    print(f"   ✅ Inferred {inferred_count} new type assertions")
    
    # Rule 2: Domain inference
    # If property P has domain D and (a, P, b), then a type D
    print("   → Applying domain inference...")
    domain_inferred = 0
    domain_query = """
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    
    SELECT ?subject ?domain WHERE {
        ?property rdfs:domain ?domain .
        ?subject ?property ?object .
        FILTER NOT EXISTS { ?subject rdf:type ?domain }
    }
    """
    
    for row in g.query(domain_query):
        # Skip literal domains
        if not isinstance(row.domain, rdflib.term.Literal):
            g.add((row.subject, RDF.type, row.domain))
            domain_inferred += 1
    
    print(f"   ✅ Inferred {domain_inferred} new type assertions from domains")
    
    # Rule 3: Range inference
    # If property P has range R and (a, P, b), then b type R
    print("   → Applying range inference...")
    range_inferred = 0
    range_query = """
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    
    SELECT ?object ?range WHERE {
        ?property rdfs:range ?range .
        ?subject ?property ?object .
        FILTER NOT EXISTS { ?object rdf:type ?range }
        FILTER (!isLiteral(?object))
    }
    """
    
    for row in g.query(range_query):
        g.add((row.object, RDF.type, row.range))
        range_inferred += 1
    
    print(f"   ✅ Inferred {range_inferred} new type assertions from ranges")
    
    total_inferred = inferred_count + domain_inferred + range_inferred
    
    # 4. Print statistics AFTER reasoning
    print("\n📊 AFTER Reasoning:")
    print(f"   - Total triples: {len(g)}")
    print(f"   - New inferred triples: {total_inferred}")
    
    # 5. Check for potential inconsistencies
    print("\n🔍 Checking for potential issues...")
    
    # Check if any instance has contradictory types (Hama AND Penyakit)
    inconsistency_query = """
    PREFIX : <http://example.org/maize-kg#>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    
    SELECT ?instance WHERE {
        ?instance rdf:type :Hama .
        ?instance rdf:type :Penyakit .
    }
    """
    
    inconsistent = list(g.query(inconsistency_query))
    if inconsistent:
        print(f"⚠️  Found {len(inconsistent)} potential inconsistencies")
        for row in inconsistent[:5]:
            print(f"   • {row.instance}")
    else:
        print("✅ No obvious inconsistencies found!")
    
    # 6. Show some inferred knowledge
    print("\n🔍 Sample Inferred Knowledge:")
    
    # Find instances that were classified
    sample_query = """
    PREFIX : <http://example.org/maize-kg#>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    
    SELECT ?instance ?type WHERE {
        ?instance rdf:type ?type .
        FILTER (
            ?type = :Pengendalian ||
            ?type = :BagianTanaman ||
            ?type = :Gejala
        )
    }
    LIMIT 10
    """
    
    count = 0
    for row in g.query(sample_query):
        instance_name = str(row.instance).split('#')[-1]
        type_name = str(row.type).split('#')[-1]
        print(f"   • {instance_name} → type: {type_name}")
        count += 1
    
    if count == 0:
        print("   (Limited inference in this simple reasoner)")
    
    # 7. Save reasoned ontology
    print(f"\n💾 Saving reasoned ontology to: {output_file}")
    try:
        g.serialize(destination=output_file, format='turtle')
        print("✅ Saved!")
        
    except Exception as e:
        print(f"❌ Error saving: {e}")
    
    print("\n" + "="*60)
    print("✅ REASONING COMPLETE!")
    print("="*60)
    print("\n💡 Note: This is a simple RDFS reasoner.")
    print("   For full OWL reasoning, use Protégé with HermiT/Pellet.")
    
    return g


def generate_reasoning_report(g):
    """Generate detailed reasoning report"""
    
    report = []
    report.append("="*60)
    report.append("REASONING REPORT (RDFS-based)")
    report.append("="*60)
    report.append("")
    
    # 1. Statistics
    report.append("1. STATISTICS:")
    report.append("-" * 40)
    report.append(f"   Total triples: {len(g)}")
    
    # Count by type
    classes = len(set(g.subjects(RDF.type, OWL.Class)))
    obj_props = len(set(g.subjects(RDF.type, OWL.ObjectProperty)))
    data_props = len(set(g.subjects(RDF.type, OWL.DatatypeProperty)))
    
    report.append(f"   Classes: {classes}")
    report.append(f"   Object Properties: {obj_props}")
    report.append(f"   Data Properties: {data_props}")
    report.append("")
    
    # 2. Sample triples
    report.append("2. SAMPLE INFERRED TRIPLES:")
    report.append("-" * 40)
    
    sample_query = """
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    SELECT ?s ?p ?o WHERE {
        ?s ?p ?o .
    }
    LIMIT 20
    """
    
    for row in g.query(sample_query):
        s = str(row.s).split('#')[-1][:30]
        p = str(row.p).split('#')[-1][:20]
        o = str(row.o).split('#')[-1][:30] if not isinstance(row.o, rdflib.term.Literal) else str(row.o)[:30]
        report.append(f"   {s} → {p} → {o}")
    
    report.append("")
    report.append("="*60)
    
    return "\n".join(report)

    
    # 3. Apply simple inference rules
    print("\n⚙️  Applying inference rules...")
    
    inferred_count = 0
    
    # Rule 1: SubClass inference (RDFS)
    # If X subClassOf Y and A type X, then A type Y
    print("   → Applying subClassOf inference...")
    subclass_query = """
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    
    SELECT ?instance ?superclass WHERE {
        ?instance rdf:type ?subclass .
        ?subclass rdfs:subClassOf ?superclass .
        FILTER NOT EXISTS { ?instance rdf:type ?superclass }
    }
    """
    
    for row in g.query(subclass_query):
        g.add((row.instance, RDF.type, row.superclass))
        inferred_count += 1
    
    print(f"   ✅ Inferred {inferred_count} new type assertions")
    
    # Rule 2: Domain inference
    # If property P has domain D and (a, P, b), then a type D
    print("   → Applying domain inference...")
    domain_inferred = 0
    domain_query = """
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    
    SELECT ?subject ?domain WHERE {
        ?property rdfs:domain ?domain .
        ?subject ?property ?object .
        FILTER NOT EXISTS { ?subject rdf:type ?domain }
    }
    """
    
    for row in g.query(domain_query):
        # Skip literal domains
        if not isinstance(row.domain, rdflib.term.Literal):
            g.add((row.subject, RDF.type, row.domain))
            domain_inferred += 1
    
    print(f"   ✅ Inferred {domain_inferred} new type assertions from domains")
    
    # Rule 3: Range inference
    # If property P has range R and (a, P, b), then b type R
    print("   → Applying range inference...")
    range_inferred = 0
    range_query = """
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    
    SELECT ?object ?range WHERE {
        ?property rdfs:range ?range .
        ?subject ?property ?object .
        FILTER NOT EXISTS { ?object rdf:type ?range }
        FILTER (!isLiteral(?object))
    }
    """
    
    for row in g.query(range_query):
        g.add((row.object, RDF.type, row.range))
        range_inferred += 1
    
    print(f"   ✅ Inferred {range_inferred} new type assertions from ranges")
    
    total_inferred = inferred_count + domain_inferred + range_inferred
    
    # 4. Print statistics AFTER reasoning
    print("\n📊 AFTER Reasoning:")
    print(f"   - Total triples: {len(g)}")
    print(f"   - New inferred triples: {total_inferred}")
    
    # 5. Check for potential inconsistencies
    print("\n🔍 Checking for potential issues...")
    
    # Check if any instance has contradictory types (Hama AND Penyakit)
    inconsistency_query = """
    PREFIX : <http://example.org/maize-kg#>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    
    SELECT ?instance WHERE {
        ?instance rdf:type :Hama .
        ?instance rdf:type :Penyakit .
    }
    """
    
    inconsistent = list(g.query(inconsistency_query))
    if inconsistent:
        print(f"⚠️  Found {len(inconsistent)} potential inconsistencies")
        for row in inconsistent[:5]:
            print(f"   • {row.instance}")
    else:
        print("✅ No obvious inconsistencies found!")
    
    # 6. Show some inferred knowledge
    print("\n🔍 Sample Inferred Knowledge:")
    
    # Find instances that were classified
    sample_query = """
    PREFIX : <http://example.org/maize-kg#>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    
    SELECT ?instance ?type WHERE {
        ?instance rdf:type ?type .
        FILTER (
            ?type = :Pengendalian ||
            ?type = :BagianTanaman ||
            ?type = :Gejala
        )
    }
    LIMIT 10
    """
    
    count = 0
    for row in g.query(sample_query):
        instance_name = str(row.instance).split('#')[-1]
        type_name = str(row.type).split('#')[-1]
        print(f"   • {instance_name} → type: {type_name}")
        count += 1
    
    if count == 0:
        print("   (Limited inference in this simple reasoner)")
    
    # 7. Save reasoned ontology
    print(f"\n💾 Saving reasoned ontology to: {output_file}")
    try:
        g.serialize(destination=output_file, format='turtle')
        print("✅ Saved!")
        
    except Exception as e:
        print(f"❌ Error saving: {e}")
    
    print("\n" + "="*60)
    print("✅ REASONING COMPLETE!")
    print("="*60)
    print("\n💡 Note: This is a simple RDFS reasoner.")
    print("   For full OWL reasoning, use Protégé with HermiT/Pellet.")
    
    return g


def generate_reasoning_report(g):
    """Generate detailed reasoning report"""
    
    report = []
    report.append("="*60)
    report.append("REASONING REPORT (RDFS-based)")
    report.append("="*60)
    report.append("")
    
    # 1. Statistics
    report.append("1. STATISTICS:")
    report.append("-" * 40)
    report.append(f"   Total triples: {len(g)}")
    
    # Count by type
    classes = len(set(g.subjects(RDF.type, OWL.Class)))
    obj_props = len(set(g.subjects(RDF.type, OWL.ObjectProperty)))
    data_props = len(set(g.subjects(RDF.type, OWL.DatatypeProperty)))
    
    report.append(f"   Classes: {classes}")
    report.append(f"   Object Properties: {obj_props}")
    report.append(f"   Data Properties: {data_props}")
    report.append("")
    
    # 2. Sample triples
    report.append("2. SAMPLE INFERRED TRIPLES:")
    report.append("-" * 40)
    
    sample_query = """
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    SELECT ?s ?p ?o WHERE {
        ?s ?p ?o .
    }
    LIMIT 20
    """
    
    for row in g.query(sample_query):
        s = str(row.s).split('#')[-1][:30]
        p = str(row.p).split('#')[-1][:20]
        o = str(row.o).split('#')[-1][:30] if not isinstance(row.o, rdflib.term.Literal) else str(row.o)[:30]
        report.append(f"   {s} → {p} → {o}")
    
    report.append("")
    report.append("="*60)
    
    return "\n".join(report)


if __name__ == "__main__":
    import rdflib
    
    # Run reasoning
    g = run_reasoning('../ontology/corn_kg.ttl', '../ontology/corn_kg_reasoned.ttl')
    
    if g:
        # Generate report
        print("\n📄 Generating detailed report...")
        report = generate_reasoning_report(g)
        
        # Save report
        with open('../assets/reasoning_report.txt', 'w', encoding='utf-8') as f:
            f.write(report)
        print("✅ Report saved to: ../assets/reasoning_report.txt")
