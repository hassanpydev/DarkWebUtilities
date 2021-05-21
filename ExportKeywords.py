from DarkWebHelpers.db.DB_Handler import Code_Translator, SQL_Manger

db = SQL_Manger()
keywords = db.ReadWhere(Code_Translator().Done)
load_keywords = [keyword for keyword in keywords]
print(','.join(key[1] for key in load_keywords))
# for [key_id, key_name, owner, status, _, _, _] in keywords:
    
