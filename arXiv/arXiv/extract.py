import asyncio
import aiohttp
import csv
import fitz
import sys

# Increase the field size limit
csv.field_size_limit(sys.maxsize)

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

async def extract_pdf_text(csv_filename):
    data_for_csv = []

    with open(csv_filename, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        pdf_links = [row['PDF Link'] for row in reader if 'PDF Link' in row]

    async with aiohttp.ClientSession() as session:
        tasks = [fetch_pdf_content(session, pdf_url) for pdf_url in pdf_links]
        pdf_texts = await asyncio.gather(*tasks)

        for pdf_text in pdf_texts:
            data_for_csv.append([pdf_text])

    with open('pdf_text_data.csv', 'w', newline='', encoding='utf-8') as output_csv:
        writer = csv.writer(output_csv)
        writer.writerow(['PDF Text'])
        for entry_data in data_for_csv:
            writer.writerow(entry_data)

    print("PDF text extraction completed. Results saved to 'pdf_text_data.csv'.")

# Run the PDF text extraction process
asyncio.run(extract_pdf_text(r'C:\Users\ASUS\Desktop\arxiv_data (15).csv'))
