"""
Generate plantix_manual_30.json dengan STRUKTUR BENAR
Mengikuti entity structure yang diminta user
"""

import json

# Load original data
with open('plantix.json', 'r', encoding='utf-8') as f:
    plantix_data = json.load(f)

# Manual extraction untuk 30 items pertama dengan STRUKTUR BENAR
manual_30 = []

# Item 1: Flower Chafer (HAMA)
manual_30.append({
    "id": 1,
    "nama": "Flower Chafer",
    "namaIlmiah": "Oxycetonia versicolor",
    "jenis": "Hama",  # ← JENIS UTAMA
    "jenisPatogen": "serangga",  # Sub-type
    "bagianTanaman": ["bunga", "pucuk"],
    "gejala": ["kerusakan", "penurunan_hasil"],
    "penyebabUtama": "kumbang_flower_chafer",
    "vektor": [],
    "faktorLingkungan": [],
    "pencegahan": ["monitoring_rutin", "rotasi_tanaman"],
    "pengendalianBiologis": [],
    "pengendalianKimia": [],
    "pengendalianMekanis": []
})

# Item 2: Boron Deficiency (DEFISIENSI)
manual_30.append({
    "id": 2,
    "nama": "Boron Deficiency",
    "namaIlmiah": "Boron Deficiency",
    "jenis": "DefisiensiUnsur",
    "jenisPatogen": "defisiensi",
    "bagianTanaman": ["daun", "batang", "akar", "pucuk"],
    "gejala": ["klorosis", "nekrosis", "daun_rapuh", "batang_rapuh", "daun_mengkerut"],
    "penyebabUtama": "defisiensi_boron",
    "vektor": [],
    "faktorLingkungan": ["pH_tinggi", "tanah_berpasir", "bahan_organik_rendah"],
    "pencegahan": ["tes_tanah_rutin", "hindari_pH_tinggi"],
    "pengendalianBiologis": ["pupuk_kandang"],
    "pengendalianKimia": ["boron_foliar"],
    "pengendalianMekanis": []
})

# Item 3: MCMV (PENYAKIT - Virus)
manual_30.append({
    "id": 3,
    "nama": "Maize Chlorotic Mottle Virus",
    "namaIlmiah": "MCMV",
    "jenis": "Penyakit",
    "jenisPatogen": "virus",
    "bagianTanaman": ["daun", "bunga_jantan", "tongkol"],
    "gejala": ["bercak", "klorosis", "nekrosis", "tanaman_kerdil", "deformasi"],
    "penyebabUtama": "virus_mcmv",
    "vektor": ["wereng", "kumbang", "tungau", "thrips"],
    "faktorLingkungan": ["suhu_tinggi", "kelembaban_tinggi"],
    "pencegahan": ["varietas_tahan", "monitoring_rutin", "eradikasi_tanaman_sakit", "rotasi_tanaman"],
    "pengendalianBiologis": [],
    "pengendalianKimia": ["insektisida_vektor"],
    "pengendalianMekanis": ["cabut_tanaman_terinfeksi"]
})

# Items 4-30 continuation
items_data = [
    # Item 4: Bagrada Bug (HAMA)
    {
        "id": 4, "nama": "Bagrada Bug", "namaIlmiah": "Bagrada hilaris", "jenis": "Hama", "jenisPatogen": "serangga",
        "bagianTanaman": ["daun", "batang", "bunga", "pucuk"],
        "gejala": ["bercak", "klorosis", "layu", "nekrosis"],
        "penyebabUtama": "bagrada_bug", "vektor": [],
        "faktorLingkungan": ["suhu_tinggi", "kelembaban_rendah"],
        "pencegahan": ["monitoring_rutin", "sanitasi_lahan"],
        "pengendalianBiologis": ["parasitoid_telur"],
        "pengendalianKimia": ["imidacloprid", "pyrethroid"],
        "pengendalianMekanis": []
    },
    # Item 5: Spotted Stemborer (HAMA)
    {
        "id": 5, "nama": "Spotted Stemborer", "namaIlmiah": "Chilo partellus", "jenis": "Hama", "jenisPatogen": "serangga",
        "bagianTanaman": ["daun", "batang"],
        "gejala": ["kerusakan", "nekrosis", "tanaman_kerdil", "busuk"],
        "penyebabUtama": "chilo_partellus", "vektor": [],
        "faktorLingkungan": ["suhu_tinggi", "kelembaban_tinggi"],
        "pencegahan": ["varietas_tahan", "monitoring_rutin", "rotasi_tanaman"],
        "pengendalianBiologis": ["bacillus_thuringiensis", "tawon_parasitoid"],
        "pengendalianKimia": ["deltamethrin"],
        "pengendalianMekanis": ["cabut_tanaman_terinfeksi"]
    },
    # Item 6: Cucumber Beetle (HAMA)
    {
        "id": 6, "nama": "Cucumber Beetle", "namaIlmiah": "Diabrotica spp.", "jenis": "Hama", "jenisPatogen": "serangga",
        "bagianTanaman": ["daun", "bunga", "akar", "batang"],
        "gejala": ["kerusakan", "layu", "busuk"],
        "penyebabUtama": "diabrotica", "vektor": ["diabrotica"],
        "faktorLingkungan": ["suhu_tinggi", "kelembaban_tinggi"],
        "pencegahan": ["rotasi_tanaman"],
        "pengendalianBiologis": ["nematoda", "jamur_beauveria"],
        "pengendalianKimia": ["acetamiprid", "pyrethroid"],
        "pengendalianMekanis": ["perangkap"]
    },
    # Item 7: Iron Deficiency (DEFISIENSI)
    {
        "id": 7, "nama": "Iron Deficiency", "namaIlmiah": "Iron Deficiency", "jenis": "DefisiensiUnsur", "jenisPatogen": "defisiensi",
        "bagianTanaman": ["daun"],
        "gejala": ["klorosis", "nekrosis", "tanaman_kerdil"],
        "penyebabUtama": "defisiensi_zat_besi", "vektor": [],
        "faktorLingkungan": ["pH_tinggi", "drainase_buruk", "suhu_rendah"],
        "pencegahan": ["hindari_pH_tinggi", "drainase_baik"],
        "pengendalianBiologis": ["pupuk_kandang", "kompos"],
        "pengendalianKimia": ["ferrous_sulphate"],
        "pengendalianMekanis": []
    },
    # Item 8: Downy Mildew (PENYAKIT - Jamur)
    {
        "id": 8, "nama": "Downy Mildew of Maize", "namaIlmiah": "Peronosclerospora sorghi", "jenis": "Penyakit", "jenisPatogen": "jamur",
        "bagianTanaman": ["daun", "batang", "bunga_jantan"],
        "gejala": ["busuk", "tanaman_kerdil", "deformasi"],
        "penyebabUtama": "peronosclerospora_sorghi", "vektor": [],
        "faktorLingkungan": [],
        "pencegahan": ["varietas_tahan", "sanitasi_lahan", "rotasi_tanaman"],
        "pengendalianBiologis": [],
        "pengendalianKimia": ["metalaxyl", "mancozeb"],
        "pengendalianMekanis": ["cabut_tanaman_terinfeksi"]
    },
    # Item 9: Maize Bushy Stunt (PENYAKIT - Bakteri)
    {
        "id": 9, "nama": "Maize Bushy Stunt Phytoplasma", "namaIlmiah": "Phytoplasma asteris", "jenis": "Penyakit", "jenisPatogen": "bakteri",
        "bagianTanaman": ["daun", "batang", "bunga_jantan", "tongkol"],
        "gejala": ["klorosis", "tanaman_kerdil", "deformasi"],
        "penyebabUtama": "phytoplasma_asteris", "vektor": ["wereng"],
        "faktorLingkungan": ["suhu_tinggi"],
        "pencegahan": ["varietas_tahan", "monitoring_rutin", "eradikasi_tanaman_sakit"],
        "pengendalianBiologis": ["jamur_metarhizium", "jamur_beauveria"],
        "pengendalianKimia": ["insektisida_vektor"],
        "pengendalianMekanis": ["cabut_tanaman_terinfeksi"]
    },
    # Item 10: Tobacco Caterpillar (HAMA)
    {
        "id": 10, "nama": "Tobacco Caterpillar", "namaIlmiah": "Spodoptera litura", "jenis": "Hama", "jenisPatogen": "serangga",
        "bagianTanaman": ["daun", "bunga", "akar"],
        "gejala": ["kerusakan", "gugur_daun"],
        "penyebabUtama": "spodoptera_litura", "vektor": [],
        "faktorLingkungan": ["suhu_tinggi"],
        "pencegahan": ["varietas_tahan", "monitoring_rutin"],
        "pengendalianBiologis": ["bacillus_thuringiensis", "npv", "neem_oil"],
        "pengendalianKimia": ["chlorpyrifos"],
        "pengendalianMekanis": ["pengumpulan_manual", "perangkap"]
    },
    # Item 11: Sooty Mold (PENYAKIT - Jamur)
    {
        "id": 11, "nama": "Sooty Mold", "namaIlmiah": "Pezizomycotina", "jenis": "Penyakit", "jenisPatogen": "jamur",
        "bagianTanaman": ["daun"],
        "gejala": ["busuk", "gugur_daun"],
        "penyebabUtama": "pezizomycotina", "vektor": ["kutu_daun", "wereng"],
        "faktorLingkungan": ["kelembaban_tinggi"],
        "pencegahan": ["jarak_tanam_optimal"],
        "pengendalianBiologis": [],
        "pengendalianKimia": ["neem_oil", "insektisida_organophosphate"],
        "pengendalianMekanis": []
    },
    # Item 12: Fruit Molds (PENYAKIT - Jamur)
    {
        "id": 12, "nama": "Fruit Molds", "namaIlmiah": "Aspergillus spp.", "jenis": "Penyakit", "jenisPatogen": "jamur",
        "bagianTanaman": ["tongkol", "biji"],
        "gejala": ["busuk", "bercak"],
        "penyebabUtama": "aspergillus", "vektor": [],
        "faktorLingkungan": ["suhu_tinggi", "kelembaban_tinggi"],
        "pencegahan": ["penyiraman_tepat"],
        "pengendalianBiologis": [],
        "pengendalianKimia": ["chlorothalonil", "fungisida_copper"],
        "pengendalianMekanis": []
    },
    # Item 13: Nitrogen Deficiency (DEFISIENSI)
    {
        "id": 13, "nama": "Nitrogen Deficiency", "namaIlmiah": "Nitrogen Deficiency", "jenis": "DefisiensiUnsur", "jenisPatogen": "defisiensi",
        "bagianTanaman": ["daun"],
        "gejala": ["klorosis", "layu", "tanaman_kerdil"],
        "penyebabUtama": "defisiensi_nitrogen", "vektor": [],
        "faktorLingkungan": ["tanah_berpasir", "kelembaban_tinggi"],
        "pencegahan": ["tes_tanah_rutin", "drainase_baik"],
        "pengendalianBiologis": ["pupuk_kandang", "kompos"],
        "pengendalianKimia": ["urea", "ammonium_nitrate"],
        "pengendalianMekanis": []
    },
    # Item 14: Maize Smut (PENYAKIT - Jamur)
    {
        "id": 14, "nama": "Maize Smut", "namaIlmiah": "Ustilago maydis", "jenis": "Penyakit", "jenisPatogen": "jamur",
        "bagianTanaman": ["daun", "batang", "tongkol"],
        "gejala": ["busuk", "tanaman_kerdil", "deformasi"],
        "penyebabUtama": "ustilago_maydis", "vektor": [],
        "faktorLingkungan": ["kelembaban_tinggi"],
        "pencegahan": ["varietas_tahan", "monitoring_rutin", "sanitasi_lahan"],
        "pengendalianBiologis": [],
        "pengendalianKimia": [],
        "pengendalianMekanis": ["cabut_tanaman_terinfeksi"]
    },
    # Item 15: Fall Armyworm (HAMA)
    {
        "id": 15, "nama": "Fall Armyworm", "namaIlmiah": "Spodoptera frugiperda", "jenis": "Hama", "jenisPatogen": "serangga",
        "bagianTanaman": ["daun", "pucuk", "tongkol", "biji"],
        "gejala": ["kerusakan", "gugur_daun"],
        "penyebabUtama": "spodoptera_frugiperda", "vektor": [],
        "faktorLingkungan": ["suhu_tinggi", "kelembaban_tinggi"],
        "pencegahan": ["varietas_tahan", "monitoring_rutin"],
        "pengendalianBiologis": ["bacillus_thuringiensis", "neem_oil", "tawon_parasitoid"],
        "pengendalianKimia": ["chlorpyrifos"],
        "pengendalianMekanis": ["perangkap", "pengumpulan_manual"]
    },
    # Items 16-30 (continue pattern)
    # Item 16: Stunt of Maize (PENYAKIT - Bakteri)
    {
        "id": 16, "nama": "Stunt of Maize", "namaIlmiah": "Spiroplasma kunkelii", "jenis": "Penyakit", "jenisPatogen": "bakteri",
        "bagianTanaman": ["daun", "batang", "tongkol"],
        "gejala": ["layu", "klorosis", "bercak", "tanaman_kerdil", "deformasi"],
        "penyebabUtama": "spiroplasma_kunkelii", "vektor": ["wereng"],
        "faktorLingkungan": ["suhu_tinggi"],
        "pencegahan": ["varietas_tahan", "monitoring_rutin", "rotasi_tanaman"],
        "pengendalianBiologis": ["jamur_metarhizium", "jamur_beauveria"],
        "pengendalianKimia": [],
        "pengendalianMekanis": []
    },
    # Item 17: Termites (HAMA)
    {
        "id": 17, "nama": "Termites", "namaIlmiah": "Termitidae", "jenis": "Hama", "jenisPatogen": "serangga",
        "bagianTanaman": ["akar", "batang"],
        "gejala": ["layu", "kerusakan", "busuk"],
        "penyebabUtama": "termites", "vektor": [],
        "faktorLingkungan": [],
        "pencegahan": ["monitoring_rutin", "sanitasi_lahan"],
        "pengendalianBiologis": ["nematoda", "jamur_beauveria", "neem_oil"],
        "pengendalianKimia": ["chlorpyrifos", "deltamethrin", "imidacloprid"],
        "pengendalianMekanis": []
    },
    # Item 18: Brown Stink Bug (HAMA)
    {
        "id": 18, "nama": "Brown Stink Bug", "namaIlmiah": "Euschistus servus", "jenis": "Hama", "jenisPatogen": "serangga",
        "bagianTanaman": ["tongkol", "biji"],
        "gejala": ["kerusakan", "bercak", "busuk"],
        "penyebabUtama": "euschistus_servus", "vektor": [],
        "faktorLingkungan": ["suhu_tinggi"],
        "pencegahan": ["monitoring_rutin"],
        "pengendalianBiologis": ["tawon_parasitoid"],
        "pengendalianKimia": ["pyrethroid"],
        "pengendalianMekanis": []
    },
    # Item 19: Sugarcane Pyrilla (HAMA)
    {
        "id": 19, "nama": "Sugarcane Pyrilla", "namaIlmiah": "Pyrilla perpusilla", "jenis": "Hama", "jenisPatogen": "serangga",
        "bagianTanaman": ["daun"],
        "gejala": ["klorosis", "nekrosis", "tanaman_kerdil", "penurunan_hasil"],
        "penyebabUtama": "pyrilla_perpusilla", "vektor": [],
        "faktorLingkungan": ["kelembaban_tinggi"],
        "pencegahan": ["monitoring_rutin", "sanitasi_lahan"],
        "pengendalianBiologis": ["parasitoid_telur"],
        "pengendalianKimia": ["chlorpyrifos"],
        "pengendalianMekanis": []
    },
    # Item 20: Shoot Flies (HAMA)
    {
        "id": 20, "nama": "Shoot Flies", "namaIlmiah": "Atherigona sp.", "jenis": "Hama", "jenisPatogen": "serangga",
        "bagianTanaman": ["daun", "pucuk", "batang"],
        "gejala": ["kerusakan", "klorosis", "layu", "tanaman_kerdil", "nekrosis"],
        "penyebabUtama": "atherigona", "vektor": [],
        "faktorLingkungan": [],
        "pencegahan": ["varietas_tahan", "sanitasi_lahan", "rotasi_tanaman"],
        "pengendalianBiologis": [],
        "pengendalianKimia": ["pyrethroid"],
        "pengendalianMekanis": []
    },
    # Item 21: Foot and Collar Rot (PENYAKIT - Jamur)
    {
        "id": 21, "nama": "Foot and Collar Rot", "namaIlmiah": "Athelia rolfsii", "jenis": "Penyakit", "jenisPatogen": "jamur",
        "bagianTanaman": ["batang", "akar", "daun"],
        "gejala": ["busuk", "layu", "klorosis", "nekrosis"],
        "penyebabUtama": "athelia_rolfsii", "vektor": [],
        "faktorLingkungan": ["pH_rendah", "suhu_tinggi", "kelembaban_tinggi"],
        "pencegahan": ["varietas_tahan", "drainase_baik", "sanitasi_lahan"],
        "pengendalianBiologis": ["trichoderma", "bacillus_subtilis"],
        "pengendalianKimia": ["metam_sodium"],
        "pengendalianMekanis": ["cabut_tanaman_terinfeksi"]
    },
    # Item 22: MLND (PENYAKIT - Virus)
    {
        "id": 22, "nama": "Maize Lethal Necrosis Disease", "namaIlmiah": "MLND", "jenis": "Penyakit", "jenisPatogen": "virus",
        "bagianTanaman": ["daun", "batang", "tongkol"],
        "gejala": ["klorosis", "nekrosis", "tanaman_kerdil", "deformasi", "busuk"],
        "penyebabUtama": "virus_mlnd", "vektor": ["thrips", "kumbang"],
        "faktorLingkungan": [],
        "pencegahan": ["varietas_tahan", "monitoring_rutin", "eradikasi_tanaman_sakit", "rotasi_tanaman"],
        "pengendalianBiologis": [],
        "pengendalianKimia": ["insektisida_vektor"],
        "pengendalianMekanis": ["cabut_tanaman_terinfeksi"]
    },
    # Item 23: Leaf Spot (PENYAKIT - Jamur)
    {
        "id": 23, "nama": "Leaf Spot of Maize", "namaIlmiah": "Cochliobolus lunatus", "jenis": "Penyakit", "jenisPatogen": "jamur",
        "bagianTanaman": ["daun", "biji"],
        "gejala": ["bercak", "klorosis", "nekrosis", "busuk"],
        "penyebabUtama": "cochliobolus_lunatus", "vektor": [],
        "faktorLingkungan": ["suhu_tinggi", "kelembaban_tinggi"],
        "pencegahan": ["varietas_tahan", "sanitasi_lahan"],
        "pengendalianBiologis": [],
        "pengendalianKimia": ["mancozeb", "chlorothalonil"],
        "pengendalianMekanis": []
    },
    # Item 24: Spotted Maize Beetle (HAMA)
    {
        "id": 24, "nama": "Spotted Maize Beetle", "namaIlmiah": "Astylus atromaculatus", "jenis": "Hama", "jenisPatogen": "serangga",
        "bagianTanaman": ["bunga", "biji"],
        "gejala": ["kerusakan"],
        "penyebabUtama": "astylus_atromaculatus", "vektor": [],
        "faktorLingkungan": ["suhu_tinggi"],
        "pencegahan": ["rotasi_tanaman"],
        "pengendalianBiologis": [],
        "pengendalianKimia": [],
        "pengendalianMekanis": ["perangkap"]
    },
    # Item 25: Stalk Rot (PENYAKIT - Jamur)
    {
        "id": 25, "nama": "Stalk Rot of Maize", "namaIlmiah": "Gibberella fujikuroi", "jenis": "Penyakit", "jenisPatogen": "jamur",
        "bagianTanaman": ["batang", "daun", "biji", "tongkol"],
        "gejala": ["busuk", "tanaman_kerdil", "klorosis", "nekrosis", "bercak"],
        "penyebabUtama": "gibberella_fujikuroi", "vektor": [],
        "faktorLingkungan": ["suhu_tinggi", "kelembaban_tinggi"],
        "pencegahan": ["varietas_tahan", "rotasi_tanaman"],
        "pengendalianBiologis": ["trichoderma", "pseudomonas", "neem_oil"],
        "pengendalianKimia": ["mancozeb", "carbendazim"],
        "pengendalianMekanis": ["cabut_tanaman_terinfeksi"]
    },
    # Item 26: Northern Leaf Spot (PENYAKIT - Jamur)
    {
        "id": 26, "nama": "Northern Leaf Spot of Maize", "namaIlmiah": "Cochliobolus carbonum", "jenis": "Penyakit", "jenisPatogen": "jamur",
        "bagianTanaman": ["daun", "tongkol"],
        "gejala": ["bercak", "busuk"],
        "penyebabUtama": "cochliobolus_carbonum", "vektor": [],
        "faktorLingkungan": ["kelembaban_tinggi"],
        "pencegahan": ["varietas_tahan", "rotasi_tanaman"],
        "pengendalianBiologis": [],
        "pengendalianKimia": ["mancozeb"],
        "pengendalianMekanis": []
    },
    # Item 27: Zinc Deficiency (DEFISIENSI)
    {
        "id": 27, "nama": "Zinc Deficiency", "namaIlmiah": "Zinc Deficiency", "jenis": "DefisiensiUnsur", "jenisPatogen": "defisiensi",
        "bagianTanaman": ["daun"],
        "gejala": ["klorosis", "nekrosis", "tanaman_kerdil", "deformasi"],
        "penyebabUtama": "defisiensi_zinc", "vektor": [],
        "faktorLingkungan": ["pH_tinggi", "tanah_berpasir"],
        "pencegahan": ["tes_tanah_rutin", "hindari_pH_tinggi"],
        "pengendalianBiologis": ["pupuk_kandang"],
        "pengendalianKimia": ["zinc_sulfate"],
        "pengendalianMekanis": []
    },
    # Item 28: Damping-Off (PENYAKIT - Jamur)
    {
        "id": 28, "nama": "Damping-Off of Seedlings", "namaIlmiah": "Pythium spp.", "jenis": "Penyakit", "jenisPatogen": "jamur",
        "bagianTanaman": ["batang", "akar", "biji"],
        "gejala": ["busuk", "layu", "klorosis", "nekrosis"],
        "penyebabUtama": "pythium", "vektor": [],
        "faktorLingkungan": ["kelembaban_tinggi", "suhu_tinggi"],
        "pencegahan": ["varietas_tahan", "drainase_baik"],
        "pengendalianBiologis": ["trichoderma", "bacillus_subtilis", "pseudomonas"],
        "pengendalianKimia": ["metalaxyl", "fungisida_copper"],
        "pengendalianMekanis": []
    },
    # Item 29: Lesser Stalk Borer (HAMA)
    {
        "id": 29, "nama": "Lesser Stalk Borer of Maize", "namaIlmiah": "Elasmopalpus lignosellus", "jenis": "Hama", "jenisPatogen": "serangga",
        "bagianTanaman": ["batang", "daun"],
        "gejala": ["kerusakan", "layu", "tanaman_kerdil", "nekrosis"],
        "penyebabUtama": "elasmopalpus_lignosellus", "vektor": [],
        "faktorLingkungan": ["suhu_tinggi"],
        "pencegahan": ["monitoring_rutin"],
        "pengendalianBiologis": ["tawon_parasitoid", "bacillus_thuringiensis", "jamur_beauveria"],
        "pengendalianKimia": ["chlorpyrifos"],
        "pengendalianMekanis": ["perangkap"]
    },
    # Item 30: Helicoverpa Caterpillar (HAMA)
    {
        "id": 30, "nama": "Helicoverpa Caterpillar", "namaIlmiah": "Helicoverpa armigera", "jenis": "Hama", "jenisPatogen": "serangga",
        "bagianTanaman": ["daun", "bunga", "tongkol", "pucuk"],
        "gejala": ["kerusakan", "busuk"],
        "penyebabUtama": "helicoverpa_armigera", "vektor": [],
        "faktorLingkungan": [],
        "pencegahan": ["varietas_tahan", "monitoring_rutin"],
        "pengendalianBiologis": ["tawon_parasitoid", "bacillus_thuringiensis", "neem_oil"],
        "pengendalianKimia": ["chlorpyrifos"],
        "pengendalianMekanis": ["pengumpulan_manual", "perangkap"]
    }
]

manual_30.extend(items_data)

# Save
with open('plantix_manual_30.json', 'w', encoding='utf-8') as f:
    json.dump(manual_30, f, indent=2, ensure_ascii=False)

print("✅ Created plantix_manual_30.json with CORRECT structure!")
print(f"\n📊 Statistics:")

# Count by jenis
jenis_count = {}
for item in manual_30:
    jenis = item['jenis']
    jenis_count[jenis] = jenis_count.get(jenis, 0) + 1

for jenis, count in jenis_count.items():
    print(f"   - {jenis}: {count} items")

print(f"\nTotal: {len(manual_30)} items")
print(f"\n✅ Struktur BENAR:")
print(f"   - Hama (Insect) → Fall Armyworm, Flower Chafer, dll")
print(f"   - Penyakit (Virus/Jamur/Bakteri) → MCMV, Downy Mildew, dll")
print(f"   - DefisiensiUnsur → Boron, Nitrogen, Zinc, Iron")
