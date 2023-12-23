# from django.http import HttpResponse
# import requests
# import time
# from bs4 import BeautifulSoup
# import csv

# def scrape_arxiv(request):
#     # URL to scrape
#     url = 'https://export.arxiv.org/api/query?search_query=all:electron'

#     # Set headers to mimic a browser visit
#     headers = {
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
#     }

#     # Implementing rate limiting
#     delay = 0.25  # 4 requests per second

#     # Counter for request bursts
#     burst_counter = 0

#     try:
#         # Loop through for multiple pages if needed
#         while True:
#             # Make a request to the URL with headers
#             response = requests.get(url, headers=headers)

#             if response.status_code == 200:
#                 # Parse the HTML content using Beautiful Soup
#                 soup = BeautifulSoup(response.content, 'lxml')
                
#                 # Find all article titles containing 'electron'
#                 article_titles = soup.find_all(class_='title')

#                 # Extract and save the titles of articles
#                 extracted_titles = [title.text.strip() for title in article_titles]
#                 with open('output.csv', 'a', newline='', encoding='utf-8') as csvfile:
#                     csv_writer = csv.writer(csvfile)
#                     csv_writer.writerows(zip(extracted_titles,))  # Updated line

#                 # Check for next page
#                 next_button = soup.find('a', {'rel': 'next'})
#                 if next_button:
#                     url = 'https://export.arxiv.org' + next_button['href']
#                 else:
#                     break  # Exit loop if no more pages

#                 # Implementing rate limiting
#                 burst_counter += 1
#                 if burst_counter >= 4:
#                     time.sleep(1)  # 1 second sleep per burst
#                     burst_counter = 0
#                 else:
#                     time.sleep(delay)

#             else:
#                 return HttpResponse("Failed to retrieve data from the URL.")

#     except Exception as e:
#         return HttpResponse(f"An error occurred: {str(e)}")
    
#     with open('output.csv', 'rb') as csvfile:
#         response = HttpResponse(csvfile.read(), content_type='text/csv')
#         response['Content-Disposition'] = 'attachment; filename="output.csv"'
#         return response

#     return HttpResponse("Scraping and CSV creation successful!")
# import requests
# import time
# import xml.etree.ElementTree as ET
# import csv

# base_url = "http://export.arxiv.org/api/query"

# # Define query parameters to search for 'electron' in the title
# params = {
#     'search_query': 'all:"electron"',
#     'start': 0,
#     'max_results': 10,
#     'sortBy': 'relevance',  # or 'lastUpdatedDate', 'submittedDate'
#     'sortOrder': 'descending'  # or 'ascending'
# }

# # Function to make API requests respecting rate limit
# def make_arxiv_request(url, params):
#     response = requests.get(url, params=params)
#     if response.status_code == 200:
#         return response.content
#     else:
#         return None
    

# def make_requests_with_burst_rate_limit(url, params):
#     burst_start_time = time.time()
#     requests_count = 0

#     response = make_arxiv_request(url, params)
#     if response:
#         yield response  # Yield the first response

#     while True:
#         elapsed_time = time.time() - burst_start_time

#         if elapsed_time >= 1:  # Check if 1 second has passed for the burst
#             burst_start_time = time.time()  # Reset the burst start time
#             requests_count = 0  # Reset request count for the new burst

#         if requests_count < 4:  # Check if within the burst limit
#             response = make_arxiv_request(url, params)
#             if response:
#                 yield response
#                 requests_count += 1
#             else:
#                 break
#         else:
#             time.sleep(0.1)  # Sleep if burst limit reached within 1 second   

# # Make requests respecting rate limit
# def make_requests_with_rate_limit(url, params):
#     response = make_arxiv_request(url, params)
#     if response:
#         return response
#     else:
#         return None

# # Fetch data while respecting the rate limit
# response = make_requests_with_rate_limit(base_url, params)

# # Process the response (parse XML, extract information, etc.)
# if response:
#     # Parse the XML response and extract data
#     atom_feed = ET.fromstring(response)
    
#     # List to store extracted information
#     data = []
    
#     for entry in atom_feed.findall('.//{http://www.w3.org/2005/Atom}entry'):
#         # Extract information from the Atom feed
#         title = entry.find('{http://www.w3.org/2005/Atom}title').text
#         # Extract other relevant information similarly
        
#         # Append extracted data to the list
#         data.append({
#             'Title': title,
#             # Add other extracted fields here
#         })

#     # Specify the CSV file name
#     csv_file = 'arxiv_data_with_electron.csv'

#     # Write the extracted data into a CSV file
#     with open(csv_file, 'w', newline='', encoding='utf-8') as file:
#         writer = csv.DictWriter(file, fieldnames=['Title'])  # Add other fieldnames here
#         writer.writeheader()
#         writer.writerows(data)

#     print(f"Data extracted and saved to '{csv_file}'")
# else:
#     print("Failed to fetch data from the arXiv API")
