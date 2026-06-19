from langchain_docling.loader import DoclingLoader


def docling_loader(files):
    print("#"*20)
    print("DOCLING_LOADER")
    print("#"*20)
    print("/n/n")

    loader = DoclingLoader(file_path=files)
    return loader.load()


