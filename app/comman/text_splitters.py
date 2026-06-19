from langchain_text_splitters import CharacterTextSplitter
from langchain_community.vectorstores.utils import filter_complex_metadata

def text_splitter(content):
    print("#"*20)
    print("DOCLING_LOADER")
    print("#"*20)
    print("/n/n")

    splitter = CharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=0
    )
    print("DOCUMENT SPLITTING IN PROGRESS....")
    print("/n/n")
    documents = splitter.split_documents(content)
    print("DOCUMENT SPLITTING COMPLETED!")
    print("/n/n")

    return filter_complex_metadata(documents)