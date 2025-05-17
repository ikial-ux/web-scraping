from pymongo import MongoClient

# Conexión a MongoDB Atlas
mongo_uri = "mongodb+srv://kialilyas:PLnlhyirHzcdXYJK@cluster0.mdpwawe.mongodb.net/amazon_scraper?retryWrites=true&w=majority"
client = MongoClient(mongo_uri)
col = client['amazon_scraper']['productos']

# Mostrar cuántos documentos hay y cuántos tienen el precio como string
total_docs = col.count_documents({})
str_docs = col.count_documents({ "price": { "$type": "string" } })
print(f"Total documentos: {total_docs}, Con price como string: {str_docs}")

# Migrar los valores
migrated = 0
for doc in col.find():
    price_field = doc.get('price')
    if not isinstance(price_field, str):
        continue

    # Limpiar el texto y convertir a float
    cleaned = price_field.replace(" €", "").replace(".", "").replace(",", ".")
    try:
        price_val = float(cleaned)
        col.update_one({'_id': doc['_id']}, {'$set': {'price': price_val}})
        migrated += 1
        print(f"Actualizado {doc['_id']} → {price_val}")
    except ValueError:
        print(f"No se pudo convertir: {price_field}")

print(f"Migración completada. Documentos convertidos: {migrated}")
