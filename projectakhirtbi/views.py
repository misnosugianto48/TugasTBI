from django.shortcuts import render

import requests
from bs4 import BeautifulSoup

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
            link = row.select_one('td a[href^="https://jurnal.fikom.umi.ac.id/index.php/ILKOM/issue/view/"]')
            title = row.select_one('td[width="30%"]')
            

            if link and title:
                link_url = link['href']
                title_text = title.text.strip()

                results.append({'title': title_text, 'link': link_url})

                # Output the result
                print("Title:", title_text)
                print("Link:", link_url)
                print()

        

        # Move to the next page
        page_number += 1

        return results

# Scraping data for each keyword
# for keyword in keywords:
#     print(f"Scraping data for keyword: {keyword}")
#     scrape_data(keyword)
#     print("\n---\n")

# def get_search_results(query):
#     url = f'https://jurnal.fikom.umi.ac.id/index.php/ILKOM/search/search?query={query}'
#     response = requests.get(url)
    
#     if response.status_code == 200:
#         soup = BeautifulSoup(response.text, 'html.parser')
#         results = []

#         # Extract relevant information from the website
#         for article in soup.find_all('h3', class_='title'):
#             title = article.text.strip()
#             link = article.a['href']
#             results.append({'title': title, 'link': link})

#         return results

#     return None
    
def search(request):
    return render(request, 'projectakhirtbi/search.html')

def search_results(request):
    # Your search results logic here
    return render(request, 'projectakhirtbi/search_results.html')