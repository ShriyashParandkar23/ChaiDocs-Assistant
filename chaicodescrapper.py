import requests
from bs4 import BeautifulSoup
import os
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_qdrant import Qdrant
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
from urllib.parse import urljoin
from openai import OpenAI

load_dotenv()


def get_html_content(url, title='firstPage'):
    folder_path = f'./{title}'
    os.makedirs(folder_path, exist_ok=True)  # Ensure folder exists

    response = requests.get(url)
    with open(os.path.join(folder_path, 'output.html'), 'w', encoding='utf-8') as f:
        f.write(response.text)
    return response.text

def parse_html(html, base_url):
    soup = BeautifulSoup(html, 'html.parser')

    # Extract title
    page_title = soup.title.string if soup.title else 'No Title'
    # print(page_title)

    # Extract main content text
    page_content = soup.get_text(separator='\n', strip=True)


    # Extract all links with visible text
    links = []
    for a in soup.find_all('a', href=True):
        text = a.get_text(strip=True)
        href = a['href']
        full_url = urljoin(base_url, href)  # ✔ safely resolves full URL
        if full_url.startswith("http"):
            links.append({
                'text': text,
                'url': full_url
            })
                
    return {
        'page_title': page_title,
        'page_content': page_content,
        'urls': links
    }

# # ! USER INPUT
# url = "https://chaidocs.vercel.app/youtube/getting-started/" 


# html = get_html_content(url)
# website_data = parse_html(html, base_url=url)

# newDoc = html
# count = 0 
# for i in website_data['urls']:
#     count += 1
#     url = i['url']

#     html = get_html_content(url)
#     website_data = parse_html(html,url)
#     newDoc += website_data['page_content']
#     # print(f'\n\n{count} fetching {url}\n\n')


# splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)
# chunks = splitter.split_text(newDoc)
# # print(chunks[0])
embedding_model = OpenAIEmbeddings(model="text-embedding-3-small")
# embeddings = embedding_model.embed_documents(chunks)


# 3. Connect to Qdrant client (running locally)
qdrant = QdrantClient(
    url="http://localhost:6333",
)

# # 4. Create a collection (if not already created)
collection_name = "WebSite Crawling"
# qdrant.recreate_collection(
#     collection_name=collection_name,
#     vectors_config=VectorParams(size=1536, distance=Distance.COSINE),  # 1536 for text-embedding-3-small
# )

# 5. Store embeddings using LangChain Qdrant wrapper
qdrant_langchain = Qdrant(
    client=qdrant,
    collection_name=collection_name,
    embeddings=embedding_model,
)


# 6. Add documents (LangChain auto-generates IDs)
# qdrant_langchain.add_texts(chunks)

# print(f"✅ Stored {len(chunks)} chunks in Qdrant!")


# easy2 = 'What is HTML?'
# easy3 = '''HTML Tags for Text Content
# <p> – Paragraph
# <span> – Inline container for text
# <div> – Generic container (block-level element)
# <a> – Anchor (hyperlink)
# '''

# results = qdrant_langchain.similarity_search('what is django', k=3)
# print('\n\nFinal Chunks From Qdrant\n\n', results)


client = OpenAI()

system_prompt = '''You are helpful AI Assistant who can understand the user query. 
And find the referance in given context. Context is qdrant document
if there is nothing related to context it provided you then You can simply answer Qdrant operation failed to user. 
else You would understand the context and provide the exact sentences from context as well as qdrant document details. 

return answer in below format 

{
"user_query: here it will come only user query without context ,
"ai_response": here will be your answer to user query by using context,
"reference_doc_content": exact lines from document in points ,
"document_id":
}
''' 


while True:
        
    user_query = input('\n\n 😎 >>  ')
    print('\n\n')
    if not user_query:
        break 

#   get the related documents from qdrant 
    print('\n\n---- 🧠 searching in QdrantDB ----\n\n')
    response = qdrant_langchain.similarity_search(user_query, k=3)

    
    modified_user_prompt = f'''orignial_user_query:{user_query}\n context: {response} \n'''
    messages = [
        {'role':'system', 'content':system_prompt},
        {'role':'user', 'content':modified_user_prompt},
    ]
    response = client.chat.completions.create(
        # model='gpt-3.5-turbo'
        model='gpt-4',
        messages=messages
    )

    final_response = response.choices[0].message.content

    print(f'🤖: {final_response}')