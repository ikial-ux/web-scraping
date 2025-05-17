from pymongo import MongoClient

client = MongoClient("mongodb+srv://kialilyas:PLnlhyirHzcdXYJK@cluster0.mdpwawe.mongodb.net/amazon_scraper?retryWrites=true&w=majority")
col = client['amazon_scraper']['productos']

for doc in col.find().limit(5):
    val = doc.get('price')
    print(val, type(val))
