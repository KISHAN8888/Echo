#loading libraries
import pymongo

import speech_recognition as sr
import google.generativeai as palm
import requests
from langchain.llms.google_palm import GooglePalm






# Configure API keys
palm.configure(api_key='AIzaSyAgLq3ekvXz5Z5S-gklC3B8ZmOViAAXB9I')
client = pymongo.MongoClient("mongodb+srv://userx:usery@emoai2.yxn6itg.mongodb.net/")
hf_token = "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"
embedding_url = "https://api-inference.huggingface.co/pipeline/feature-extraction/sentence-transformers/all-MiniLM-L6-v2"

db = client["tab"]
collection = db["summaries"]

llm = GooglePalm


# Speech recognition initialization
recognizer = sr.Recognizer()
microphone = sr.Microphone()

full_transcript = ""

print("Type 'start' to begin recording and 'stop' when finished.")

while True:
    input_text = input(">")
    
    if input_text.lower() == "start":
        print("Recording started. Say something.")
        
        with microphone as source:
            audio = recognizer.listen(source)
            
        try:
            transcript = recognizer.recognize_google(audio)
            full_transcript += " " + transcript
            
        except sr.UnknownValueError:
            print("Could not understand speech")
        except sr.RequestError as e:
            print("Error: ", e)
            
    elif input_text.lower() == "stop":
        break
    

    

#printing the transcript
print("Full transcript:")
print(full_transcript)
#generating summary from transcript
summary1 = palm.chat(context = " Generate a summary of this conversation without loosing the context and keywords so that in future i can query with this summary and don't make up things by your own. use this message and generate a short summary as this is a conversation. :", messages= full_transcript)
print("summary")
print(summary1)




#taking the content from llm response
message_content = next((msg['content'] for msg in summary1.messages if msg['author'] == '1'), None)
print("message content")
print(message_content)
#addressing the database name and collection
db1 = client["tab"]
collection1 = db1["summaries"]

#function for generating embedding 
def generate_embedding(text: str) -> list[float]:
    response = requests.post(
        embedding_url,
        headers={"Authorization": f"Bearer {hf_token}"},
        json={"inputs": text})

    if response.status_code != 200:
        raise ValueError(f"Request failed with status code {response.status_code}: {response.text}")

    return response.json()

#generating embedding
embedding = generate_embedding(message_content)
#adding it to database
document = {"transcript_id": 1, "summary_embedding": embedding, "summary": message_content}
collection.insert_one(document)






# Verify insertion
doc = collection.find_one({"transcript_id": 1})
print(doc["summary_embedding"])


#checking length
len(embedding)

#tak query as an input from user
query = input("Enter your query (or type 'exit' to stop): ")

while query.lower() != 'exit':
    # Generate embedding for the current query
    query_embedding = generate_embedding(query)

    results = collection.aggregate([

        {"$vectorSearch": {
        "queryVector": query_embedding,
        "path": "summary_embedding",
        "numCandidates": 384,
        "limit": 1,
        "index": "tryingtab",
        }}
    ]);





#storing the result
    result = print(f'id: {document["transcript_id"]},\nsummary_embeddings: {document["summary_embedding"]},\nsummary : {document["summary"]}\n')


    for document in results:
      result = (f'summary : {document["summary"]}\n')


    print(result)

#taking query response from llm
    query_response =  palm.chat(context = "Strictly answer based on this. Don't make up things by your own use this as a knowledge base and be real with this:  "+result  , messages= query)
    print(query_response)

#printing the content of rsponsse
    author_1_content = next((msg['content'] for msg in query_response.messages if msg['author'] == '1'), None)
    print(author_1_content)
     


     
     

    
     
    
    # Get the next query from the user
    query = input("Enter your next query (or type 'exit' to stop): ")

print("It was great talking to you. Goodbye!")