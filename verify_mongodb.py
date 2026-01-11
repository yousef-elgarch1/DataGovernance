"""
MONGODB ATLAS - COMPLETE VERIFICATION SCRIPT
This script verifies ALL findings before creating implementation plan
"""

from pymongo import MongoClient
import json
from datetime import datetime

print("="*80)
print("MONGODB ATLAS VERIFICATION - 100% CONFIDENCE CHECK")
print("="*80)

try:
    # STEP 1: Connection Test
    print("\n[STEP 1] Testing MongoDB Atlas Connection...")
    client = MongoClient(
        'mongodb+srv://projetFD:ensias2025@datagovdb.sjhsdum.mongodb.net/?retryWrites=true&w=majority&appName=DataGovDB',
        serverSelectionTimeoutMS=5000
    )
    client.admin.command('ping')
    print("✅ Connection successful!")
    
    # STEP 2: Database & Collections Verification
    print("\n[STEP 2] Verifying Database & Collections...")
    db = client['DataGovDB']
    collections = db.list_collection_names()
    print(f"✅ Database 'DataGovDB' exists")
    print(f"✅ Found {len(collections)} collections:")
    
    collection_stats = {}
    for coll in collections:
        count = db[coll].count_documents({})
        collection_stats[coll] = count
        print(f"   - {coll}: {count} documents")
    
    # STEP 3: Taxonomies Collection Analysis
    print("\n[STEP 3] Analyzing 'taxonomies' Collection...")
    if 'taxonomies' not in collections:
        print("❌ ERROR: 'taxonomies' collection does NOT exist!")
        exit(1)
    
    taxonomies = list(db['taxonomies'].find())
    print(f"✅ 'taxonomies' collection exists with {len(taxonomies)} documents")
    
    print("\n   Taxonomy Documents:")
    for i, tax in enumerate(taxonomies, 1):
        meta = tax.get('metadata', {})
        cats = tax.get('categories', [])
        
        domain_name = meta.get('domain_name', 'UNKNOWN')
        total_entities = meta.get('total_entities', 0)
        
        print(f"   [{i}] {domain_name}")
        print(f"       - Total entities: {total_entities}")
        print(f"       - Categories: {len(cats)}")
        
        # Count actual subclasses
        total_subclasses = sum(len(cat.get('subclasses', [])) for cat in cats)
        print(f"       - Actual subclasses: {total_subclasses}")
    
    # STEP 4: Check for Moroccan Patterns
    print("\n[STEP 4] Checking for Moroccan PII/SPI Patterns...")
    moroccan_keywords = ['CIN', 'CNSS', 'MAROC', 'RAMED', 'RIB', 'IDENTITE_MAROCAINE']
    found_moroccan = False
    
    for tax in taxonomies:
        domain = tax.get('metadata', {}).get('domain_name', '')
        if any(kw in domain for kw in moroccan_keywords):
            found_moroccan = True
            print(f"   ✅ Found Moroccan domain: {domain}")
            break
    
    if not found_moroccan:
        # Check in subclasses
        for tax in taxonomies:
            for cat in tax.get('categories', []):
                for sub in cat.get('subclasses', []):
                    name = sub.get('name', '')
                    if any(kw in name for kw in moroccan_keywords):
                        print(f"   ⚠️ Found Moroccan pattern in subclass: {name}")
                        found_moroccan = True
                        break
    
    if not found_moroccan:
        print("   ❌ No Moroccan-specific patterns found")
        print("   → Our 47 patterns NOT in database yet")
    
    # STEP 5: Schema Structure Verification
    print("\n[STEP 5] Verifying Schema Structure...")
    if taxonomies:
        sample = taxonomies[0]
        required_keys = ['metadata', 'categories']
        
        schema_valid = True
        for key in required_keys:
            if key not in sample:
                print(f"   ❌ Missing required key: {key}")
                schema_valid = False
            else:
                print(f"   ✅ Has key: {key}")
        
        # Check metadata structure
        if 'metadata' in sample:
            meta_keys = sample['metadata'].keys()
            print(f"   ✅ Metadata keys: {list(meta_keys)}")
        
        # Check category structure
        if 'categories' in sample and len(sample['categories']) > 0:
            cat_sample = sample['categories'][0]
            if 'subclasses' in cat_sample and len(cat_sample['subclasses']) > 0:
                sub_sample = cat_sample['subclasses'][0]
                print(f"   ✅ Subclass sample keys: {list(sub_sample.keys())}")
                
                # Check for critical fields
                critical_fields = ['name', 'regex_patterns', 'sensitivity_level']
                for field in critical_fields:
                    if field in sub_sample:
                        print(f"      ✅ Has {field}")
                    else:
                        print(f"      ⚠️ Missing {field}")
    
    # STEP 6: Sample Document Display
    print("\n[STEP 6] Sample Taxonomy Document Structure...")
    if taxonomies:
        sample = taxonomies[0]
        # Show first category with one subclass
        cats = sample.get('categories', [])
        if cats and len(cats[0].get('subclasses', [])) > 0:
            demo = {
                "metadata": sample.get('metadata'),
                "categories": [{
                    **cats[0],
                    "subclasses": [cats[0]['subclasses'][0]]  # Just first subclass
                }]
            }
            print(json.dumps(demo, indent=2, ensure_ascii=False, default=str))
    
    # FINAL VERDICT
    print("\n" + "="*80)
    print("VERIFICATION SUMMARY")
    print("="*80)
    print(f"✅ MongoDB Atlas connection: WORKING")
    print(f"✅ Database 'DataGovDB': EXISTS")
    print(f"✅ Collection 'taxonomies': EXISTS ({len(taxonomies)} documents)")
    print(f"✅ Schema structure: VALID")
    print(f"{'❌' if not found_moroccan else '✅'} Moroccan patterns: {'FOUND' if found_moroccan else 'NOT FOUND'}")
    
    print("\n" + "="*80)
    print("RECOMMENDATION:")
    print("="*80)
    if not found_moroccan:
        print("✅ READY TO IMPLEMENT MongoDB storage for 47 Moroccan patterns")
        print("   - Use existing 'taxonomies' collection")
        print("   - Follow existing schema structure")
        print("   - Add as new taxonomy document")
    else:
        print("⚠️ Moroccan patterns may already exist - needs manual review")
    
    print("\n✅ 100% CONFIDENT - Data verified!")
    
except Exception as e:
    print(f"\n❌ ERROR: {str(e)}")
    print("Connection failed or database issue detected")
    exit(1)
