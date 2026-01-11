from pymongo import MongoClient
import json

# Connect to MongoDB Atlas
client = MongoClient('mongodb+srv://projetFD:ensias2025@datagovdb.sjhsdum.mongodb.net/?retryWrites=true&w=majority&appName=DataGovDB')
db = client['DataGovDB']

print("=" * 60)
print("MongoDB Atlas Database Analysis - DataGovDB")
print("=" * 60)

# List all collections
collections = db.list_collection_names()
print(f"\nTotal Collections: {len(collections)}")
print("\nCollection Counts:")
for coll_name in collections:
    count = db[coll_name].count_documents({})
    print(f"  - {coll_name}: {count} documents")

# Analyze taxonomies collection
print("\n" + "=" * 60)
print("TAXONOMIES COLLECTION ANALYSIS")
print("=" * 60)
taxonomies = list(db['taxonomies'].find())
print(f"\nTotal taxonomy documents: {len(taxonomies)}")

for i, tax in enumerate(taxonomies, 1):
    meta = tax.get('metadata', {})
    print(f"\n[{i}] Domain: {meta.get('domain_name', 'N/A')}")
    print(f"    - Domain ID: {meta.get('domain_id', 'N/A')}")
    print(f"    - Total Entities: {meta.get('total_entities', 0)}")
    print(f"    - Version: {meta.get('version', 'N/A')}")
    
    categories = tax.get('categories', [])
    print(f"    - Categories: {len(categories)}")
    for cat in categories:
        subclasses = cat.get('subclasses', [])
        print(f"      • {cat.get('class', 'N/A')}: {len(subclasses)} subclasses")

# Analyze domains collection
print("\n" + "=" * 60)
print("DOMAINS COLLECTION ANALYSIS")
print("=" * 60)
domains = list(db['domains'].find())
print(f"\nTotal domain documents: {len(domains)}")

# Get sample domain structure
if domains:
    sample = domains[0]
    print("\nSample domain structure keys:")
    for key in sample.keys():
        print(f"  - {key}")

# Analyze entities collection
print("\n" + "=" * 60)
print("ENTITIES COLLECTION ANALYSIS")
print("=" * 60)
entities = list(db['entities'].find().limit(5))
print(f"\nTotal entities: {db['entities'].count_documents({})}")
if entities:
    print("\nSample entity structure:")
    print(json.dumps(entities[0], indent=2, default=str))

print("\n" + "=" * 60)
print("ANALYSIS COMPLETE")
print("=" * 60)
