# # from django.http import HttpResponse
# # import csv
# # import requests
# # import io
# # from urllib.parse import urlencode

# # def get_news_data(request):
# #     base_url = "https://newsapi.org/v2/everything"
# #     api_key = "4030f9dcb51049ee84e383bf0b5dcf00"

# #     # Accept queries as input from the user in the terminal
# #     user_input = input("Enter queries separated by commas: ")

# #     # Split the input by commas
# #     raw_queries = user_input.split(',')

# #     # Separate combined queries with 'AND' and individual queries
# #     combined_queries = []
# #     individual_queries = []

# #     for query in raw_queries:
# #         if 'AND' in query.upper():
# #             combined_queries.append(query.strip())
# #         else:
# #             individual_queries.extend(query.strip().split())

# #         # Combine entities in combined_queries into a single query string
# #         combined_query_string = " AND ".join(['(' + q.replace(' AND ', ' AND ') + ')' for q in combined_queries])

# #     # Combine all queries into a single list
# #     all_queries = individual_queries + [combined_query_string]

# #     headers = {
# #         "api-key": api_key,
# #         "host": "newsapi.org"
# #     }

# #     # Create or open the CSV file in append mode
# #     with io.StringIO() as memory_file:
# #         csv_writer = csv.writer(memory_file)

# #         # Write CSV headers
# #         csv_writer.writerow(['source', 'author', 'title', 'description', 'url', 'publishedAt' ,'content','Query'])

# #         for query in all_queries:
# #             query_params = {
# #                 "q": query.strip(),
# #                 "language": "en",
# #                 "apiKey": api_key
# #             }

# #             url = f"{base_url}?{urlencode(query_params)}"
# #             response = requests.get(url, headers=headers)

# #             if response.status_code == 200:
# #                 news_data = response.json().get('articles', [])

# #                 # Append news data to the CSV file
# #                 for article in news_data:
# #                     csv_writer.writerow([
# #                         article['source']['name'],
# #                         article['author'],
# #                         article['title'],
# #                         article['description'],
# #                         article['url'],
# #                         article['publishedAt'],
# #                         article['content'],
# #                         query.strip()  # Include query in each row
# #                     ])
# #             else:
# #                 return HttpResponse(f"Failed to fetch data for query: {query}", status=500)

# #         # Get the existing CSV content if it exists
# #         existing_content = ""
# #         try:
# #             existing_content_response = requests.get("<URL of your existing CSV>")
# #             if existing_content_response.status_code == 200:
# #                 existing_content = existing_content_response.text
# #         except requests.RequestException as e:
# #             print(f"Failed to fetch existing content: {e}")

# #         # Concatenate existing content and new content
# #         final_content = existing_content + memory_file.getvalue()

# #         # Set response headers for file download
# #         response = HttpResponse(final_content, content_type='text/csv')
# #         response['Content-Disposition'] = 'attachment; filename=news_data.csv'

# #         return response


# from django.http import HttpResponse
# import csv
# import requests
# import io
# from urllib.parse import urlencode
# import re

# def get_news_data(request):
#     base_url = "https://newsapi.org/v2/everything"
#     api_key = "4030f9dcb51049ee84e383bf0b5dcf00"

#     # Directly defining user input separated by commas
#     user_input = "crypto AND bitcoin,Ai AND cyber,sports"

#     # Split the input by commas outside parentheses
#     individual_queries = re.split(r',\s*(?![^()]*\))', user_input)

#     # Process individual queries to format them
#     formatted_queries = []
#     for query in individual_queries:
#         formatted_query = ', '.join(word.capitalize() if word.lower() != 'and' else word for word in query.split(', '))
#         formatted_queries.append(formatted_query)

#     # Combine all formatted queries into a single string
#     combined_query_string = ', '.join(formatted_queries)

#     headers = {
#         "api-key": api_key,
#         "host": "newsapi.org"
#     }

#     # Create or open the CSV file in append mode
#     with io.StringIO() as memory_file:
#         csv_writer = csv.writer(memory_file)

#         # Write CSV headers
#         csv_writer.writerow(['source', 'author', 'title', 'description', 'url', 'publishedAt', 'content', 'Query'])

#         for query in formatted_queries:  # Iterate over formatted queries
#             query_params = {
#                 "q": query.strip(),
#                 "language": "en",
#                 "apiKey": api_key
#             }

#             url = f"{base_url}?{urlencode(query_params)}"
#             response = requests.get(url, headers=headers)

#             if response.status_code == 200:
#                 news_data = response.json().get('articles', [])

#                 # Append news data to the CSV file
#                 for article in news_data:
#                     csv_writer.writerow([
#                         article['source']['name'],
#                         article['author'],
#                         article['title'],
#                         article['description'],
#                         article['url'],
#                         article['publishedAt'],
#                         article['content'],
#                         query.strip()  # Include query in each row
#                     ])
#             else:
#                 return HttpResponse(f"Failed to fetch data for query: {query}", status=500)

#         # Get the existing CSV content if it exists
#         existing_content = ""
#         try:
#             existing_content_response = requests.get("<URL of your existing CSV>")
#             if existing_content_response.status_code == 200:
#                 existing_content = existing_content_response.text
#         except requests.RequestException as e:
#             print(f"Failed to fetch existing content: {e}")

#         # Concatenate existing content and new content
#         final_content = existing_content + memory_file.getvalue()

#         # Set response headers for file download
#         response = HttpResponse(final_content, content_type='text/csv')
#         response['Content-Disposition'] = 'attachment; filename=news_data.csv'

#         return response

import csv
import requests
from django.http import HttpResponse
from django.shortcuts import render
from io import StringIO

def get_news_data(request):
    api_key = 'pub_34840bef06de1e0b5d05d7c71db58fe41af8c'
    url = 'https://newsdata.io/api/1/news'
    query_params = {
        'apikey': 'pub_34840bef06de1e0b5d05d7c71db58fe41af8c',
        'q': 'cryptocurrency'
    }

    response = requests.get(url, params=query_params)
    data = response.json().get('results', [])

    # Prepare CSV data in memory
    csv_data = StringIO()
    fieldnames = ['title', 'author', 'content', 'description', 'full_description']
    writer = csv.DictWriter(csv_data, fieldnames=fieldnames)
    writer.writeheader()
    for article in data:
        writer.writerow({
            'title': article.get('title', ''),
            'author': article.get('author', ''),
            'content': article.get('content', ''),
            'description': article.get('description', ''),  # Assuming 'description' is a field in the API response
            'full_description': article.get('full_description', '')  # Assuming 'full_description' is a field in the API response
        })

    # Create a response with the CSV file as an attachment
    response = HttpResponse(csv_data.getvalue(), content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=news_data.csv'

    return response
