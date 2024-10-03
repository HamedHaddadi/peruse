from langchain_community.document_loaders import PyPDFLoader, pdf
from langchain_core.documents.base import Document  
from typing import Dict, List, Union  

# ################################ #
# utilities to work with documents #
# ################################ #
def format_doc_object(doc: List, replacements: Dict[str, str]) -> List:
	"""
	takes a doc object from PyPDFLoader and replace a str with another
	Returns: formatted doc
	"""
	for page in doc:
		for find,replace in replacements.items():
			page.page_content = page.page_content.replace(find, replace)
	return doc 

# pdf loading
def page_content_not_empty(docs: List[Document]) -> bool:
	if len(docs) == 0:
		return False 
	len_page_contnet = sum([len(doc.page_content) for doc in docs])
	if len_page_contnet == len(docs):
		return False 
	elif len_page_contnet > len(docs):
		return True 

def load_and_split_pdf(pdf_file: str, split = True) -> Union[List, None]:
	loader = PyPDFLoader(pdf_file)
	if split:
		docs = loader.load_and_split()
	else:
		docs = loader.load()
	if page_content_not_empty(docs):
		return docs 
	else:
		try:
			loader = pdf.PyMuPDFLoader(pdf_file, extract_images = True)
			docs = loader.load_and_split()
			if page_content_not_empty(docs):
				return docs 
			else:
				return None 
		except:
			return None 