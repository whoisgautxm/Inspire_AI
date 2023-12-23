import aiohttp
import asyncio
from bs4 import BeautifulSoup
import csv
from django.http import HttpResponse
import fitz

def replace_newlines_with_spaces(text):
    return ' '.join(text.splitlines())



async def fetch_pdf_content(session, pdf_url):
    try:
        async with session.get(pdf_url) as response:
            if response.status == 200:
                pdf_content = await response.read()
                pdf_document = fitz.open(stream=pdf_content, filetype="pdf")
                extracted_text = ''

                for page_num in range(pdf_document.page_count):
                    page = pdf_document.load_page(page_num)
                    extracted_text += page.get_text()

                return extracted_text
            else:
                return ''
    except Exception as e:
        print(f"Error converting PDF from {pdf_url}: {str(e)}")
        return ''

async def scrape_arxiv_api(request):
    base_url = "http://export.arxiv.org/api/query"

    params = {
        'search_query': 'all:cybersecurity',
        'start': 0,
        'max_results': 100,
    }

    async with aiohttp.ClientSession() as session:
        response = await session.get(base_url, params=params)
        if response.status == 200:
            soup = BeautifulSoup(await response.text(), 'xml')
            entries = soup.find_all('entry')
            data_for_csv = []

            tasks = []
            for entry in entries:
                title = entry.find('title').text
                summary_tag = entry.find('summary')
                summary = replace_newlines_with_spaces(summary_tag.get_text(strip=True)) if summary_tag else ''

                authors = ', '.join([author.find('name').text for author in entry.find_all('author')])
                pdf_link = entry.find('link', {'title': 'pdf'})

                if pdf_link:
                    pdf_url = pdf_link['href']
                    task = asyncio.create_task(fetch_pdf_content(session, pdf_url))
                    tasks.append((title, authors, summary, pdf_url, task))

            for title, authors, summary, pdf_url, task in tasks:
                pdf_text = await task
                data_for_csv.append([title, authors, summary, pdf_url, pdf_text])

            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="arxiv_data.csv"'

            writer = csv.writer(response)
            writer.writerow(['Title', 'Authors', 'Summary', 'PDF Link', 'PDF Text'])

            for entry_data in data_for_csv:
                writer.writerow(entry_data)

            return response
        else:
            return HttpResponse(f"Error: {response.status}", status=response.status)