
from haystack.document_store.elasticsearch import ElasticsearchDocumentStore
import pandas as pd 

Username="weweztms"
Password="?/xij7n#bk4HeS?"
Port=9200

# Create an instance of ElasticsearchDocumentStore
# 'host' is set to localhost, 'username' and 'password' are defined
document = ElasticsearchDocumentStore(host="localhost", username=Username, password=Password, index="document")

# Read the source data file into a DataFrame
df = pd.read_csv('out.csv')

# Convert the DataFrame into a list of dictionaries
dict = df.to_dict('records')

# Initialize an empty list to hold the restructured dictionaries
new_dict = []

# Iterate over each dictionary in the list
for each in dict:
    # Initialize a new dictionary
    data = {}
    
    data['text'] = each.pop('body_text')
    data['meta'] = each
    
    new_dict.append(data)

# Write the new list of dictionaries into the Elasticsearch document store
document.write_documents(new_dict)