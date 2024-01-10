# -*- coding: utf-8 -*-
"""
Created on Mon Dec  4 17:00:50 2023

@author: SU57
"""

import database
import textPreProcessing
import rocchioVSM
import vsm
import QueryExpansion


query = "SELECT * FROM songs"
data = database.getData(query)

# Pra-pemrosesan text: punctuation removal, lowercase operation,
# stopwords removal, dan operasi stemming
corpus = textPreProcessing.textprocessing(data)


documents = []


for (index, artist, song, link, text, preprocessed_text) in corpus:
    
    
    documents.append({'artist': artist,'song' : song, 'preprocessed_text': preprocessed_text})
    
   # print(preprocessed_text)

# Program utama
if __name__ == "__main__":
    # Pengguna menginputkan query
    query = input("Masukkan query: ")
    
    # Query Expansion
    query = QueryExpansion.expand_query(query)
    print()
    
    print(f"Query baru hasil expansion: {query}")


    # Menampilkan hasil awal Vector Space Model (VSM)
    top_documents = vsm.calculate_vsm(query, corpus)

    
    print("\n7 Peringkat Dokumen Teratas:")        
    for index, array_value in top_documents:
        value = array_value[0]
        print()
        print(f" Index: {index},\n Value: {value},\n Artist : {documents[index]['artist']}, Judul : {documents[index]['song']},\nLirik : {documents[index]['preprocessed_text']} ")
        print()
        

    # Pengguna menginputkan dokumen hasil pencarian relevan dan tidak relevan
    try:
        relevant_indices = [int(idx) - 1 for idx in input("Masukkan nomor index dokumen relevan (pisahkan dengan spasi): ").split()]

    except ValueError:
        print("Input tidak valid. Masukkan nomor dokumen yang valid.")
        exit()

    try:
        non_relevant_indices = [int(idx) - 1 for idx in input("Masukkan nomor index dokumen tidak relevan (pisahkan dengan spasi):").split()]

    except ValueError:
        print("Input tidak valid. Masukkan nomor dokumen yang valid.")
        exit()

    # Menghitung bobot dokumen dan query
    document_vectors, query_vector, vocabulary = rocchioVSM.calculate_document_weights(query, [document['preprocessed_text'] for document in documents])

    # Melakukan relevance feedback dengan algoritma Rocchio
    updated_query_vector = rocchioVSM.rocchio_feedback(query_vector, document_vectors[relevant_indices],document_vectors[non_relevant_indices])

    # Menggunakan vektor query yang telah di-update untuk mencari dokumen terkait
    updated_top_documents = rocchioVSM.retrieve_documents(updated_query_vector, document_vectors, 7)

    # Menampilkan hasil
    print("\nDokumen hasil relevance feedback:\n")
    for i, doc in updated_top_documents:
        print(f"No. index {i}: Score {doc}.\n Artist : {documents[i]['artist']},\n Judul : {documents[i]['song']},\nLirik : {documents[i]['preprocessed_text']}")
        print()