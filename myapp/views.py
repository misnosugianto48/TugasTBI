import random
import string
from django.shortcuts import render

import requests
from bs4 import BeautifulSoup

from myapp.models import Jurnal


# Create your views here.

def get_search_results(query):
    page_number = 1
    results = []

    while True:
        search_url = f'https://jurnal.fikom.umi.ac.id/index.php/ILKOM/search/search?query={query}&searchJournal=1&authors=&title=&abstract=&galleyFullText=&suppFiles=&discipline=&subject=&type=&coverage=&indexTerms=&dateFromMonth=&dateFromDay=&dateFromYear=&dateToMonth=&dateToDay=&dateToYear=&orderBy=&orderDir=&searchPage={page_number}#results'

        print(search_url)

        print(f'{str(search_url)}\n')
        response = requests.get(search_url)
        html_content = response.content
        soup = BeautifulSoup(html_content, 'html.parser')

        issue_rows = soup.select('tr[valign="top"]')

        if "No Results" in str(html_content):
            
            break  # No more pages, exit the loop

        

        for row in issue_rows:
            i = 1
            link = row.select_one('td a[href^="https://jurnal.fikom.umi.ac.id/index.php/ILKOM/issue/view/"]')
            title = row.select_one('td[width="30%"]')
            abstract = row.select_one('td a[href^="https://jurnal.fikom.umi.ac.id/index.php/ILKOM/article/view/"]')
            

            if link and title:
                link_url = link['href']
                title_text = title.text.strip()
                abstract_url = abstract['href']

                response2 = requests.get(abstract_url)
                html_content2 = response2.content
                soup2 = BeautifulSoup(html_content2, 'html.parser')

                rows = soup2.select_one('div[id="articleAbstract"] div')

                abstract_text = rows.text.strip()

                id = generate_random_string()

                jurnal = Jurnal(
                    id = id,
                    title = title.text,
                    abstract = abstract_text,
                    link =  link_url,
                    abstracturl = abstract_url
                )

                
                jurnal.save()

                

                results.append({'title': title_text, 'link': link_url, 'abstract' : abstract_text})

                # Output the result
                print("Title:", title_text)
                print("Link:", link_url)
                print("Abstract URL", abstract_url)
                print("Abstract Content", abstract_text)
                print()
                i+=1

            

                

        

        # Move to the next page
        page_number += 1

        return results

def home(request):
    return render(request, "home.html")

def results(request):
    query = request.GET.get('q', '')
    results = get_search_results(query)
    return render(request, 'results.html', {'query': query, 'results': results})

def generate_random_string():
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(8))

def check_duplicate_titles(title_to_check):
    # Check if there are duplicates for the given title
    is_duplicate = Jurnal.objects.filter(title=title_to_check).exists()

    return is_duplicate

