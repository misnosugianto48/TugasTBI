import random
import string
from django.shortcuts import render

import requests
from bs4 import BeautifulSoup

from myapp.models import Jurnal
import myapp.modeltbi.QueryExpansion as QueryExpansionModule
import myapp.modeltbi.textPreProcessing as textPreProcessingModule
import myapp.modeltbi.vsm as vsmModel

all_jurnals = Jurnal.objects.all()

documents = []
text_preprocessor = textPreProcessingModule.TextPreProcessing()
vsmmodel = vsmModel.vsm()

# Create your views here.
def send_to_model(query):
    # Query Expansion
    query_expander = QueryExpansionModule.QueryExpansion()

    query = query_expander.expand_query(query)
    print()
    
    print(f"Query baru hasil expansion: {query}\n")

    return textPreProcessing(query, all_jurnals)

def textPreProcessing(query, data):
    corpus =     text_preprocessor.textprocessing(data)
    for (index, linkjurnal, abstrak,  preprocessed_text) in corpus:
        print()
        print(f" Index : {index},\n Judul : {preprocessed_text}")
        print()
        documents.append({'id': index, 'link': linkjurnal, 'abstrak': abstrak, 'preprocessed_text': preprocessed_text})

    result_top_document = []
    top_documents = vsmmodel.calculate_vsm(query, corpus)
    print("\n7 Peringkat Dokumen Teratas:")        
    for index, array_value in top_documents:
        value = array_value[0]
        if value == 0.0:
            pass
        else:
            print(f"Judul : {documents[index]['preprocessed_text']} \nRANK : {value}\n Abstrak: {documents[index]['abstrak']}\n Link Jurnal: {documents[index]['link']} \n\n")
            print()
            result_top_document.append({'id': index, 'rank': value, 'judul': documents[index]['preprocessed_text'], 'link': documents[index]['link'], 'abstrak': documents[index]['abstrak']})
    return result_top_document

# def get_search_results(query):
# # pass

def home(request):
    return render(request, "home.html")

def results(request):
    query = request.GET.get('q', '')
    results = send_to_model(query)
    return render(request, 'results.html', {'query': query, 'results': results})

def generate_random_string():
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(8))

def check_duplicate_titles(title_to_check):
    # Check if there are duplicates for the given title
    is_duplicate = Jurnal.objects.filter(title=title_to_check).exists()

    return is_duplicate

