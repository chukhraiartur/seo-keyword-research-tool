from serpapi import GoogleSearch
from itertools import zip_longest
import json, csv, argparse


def get_auto_complete(query: str, country: str, lang: str, api_key: str):
    params = {
        'api_key': api_key,                         # https://serpapi.com/manage-api-key
        'engine': 'google_autocomplete',            # search engine
        'q': query,                                 # search query
        'gl': country,                              # https://serpapi.com/google-countries
        'hl': lang                                  # https://serpapi.com/google-languages
    }

    search = GoogleSearch(params)                   # data extraction on the SerpApi backend
    results = search.get_dict()                     # JSON -> Python dict
    
    auto_complete_results = [result['value'] for result in results['suggestions']]
    
    return auto_complete_results


def get_related_searches(query: str, domain: str, country: str, lang: str, api_key: str):
    params = {
        'api_key': api_key,                         # https://serpapi.com/manage-api-key
        'engine': 'google',                         # search engine
        'q': query,                                 # search query
        'google_domain': domain,                    # https://serpapi.com/google-domains
        'gl': country,                              # https://serpapi.com/google-countries
        'hl': lang                                  # https://serpapi.com/google-languages
    }

    search = GoogleSearch(params)                   # data extraction on the SerpApi backend
    results = search.get_dict()                     # JSON -> Python dict
    
    related_searches_results = [result['query'] for result in results['related_searches']]

    return related_searches_results


def get_related_questions(query: str, domain: str, country: str, lang: str, api_key: str, depth_limit: int):
    params = {
        'api_key': api_key,                         # https://serpapi.com/manage-api-key
        'engine': 'google',                         # search engine
        'q': query,                                 # search query
        'google_domain': domain,                    # https://serpapi.com/google-domains
        'gl': country,                              # https://serpapi.com/google-countries
        'hl': lang                                  # https://serpapi.com/google-languages
    }

    search = GoogleSearch(params)                   # data extraction on the SerpApi backend
    results = search.get_dict()                     # JSON -> Python dict

    related_questions_results = [result['question'] for result in results['related_questions']]

    if depth_limit:
        def get_depth_results(token, depth, api_key):
            ''' This function allows you to extract more data from People Also Ask.
            
            The function takes the following arguments:
            
            - `token` - allows access to additional related questions;
            
            - `depth` - limits the input depth for each related question;
            
            - `api_key` - your SerpApi API key. '''

            depth_params = {
                'api_key': api_key,
                'engine': 'google_related_questions',
                'next_page_token': token,
            }

            depth_search = GoogleSearch(depth_params)
            depth_results = depth_search.get_dict()
            
            related_questions_results.extend([result['question'] for result in depth_results.get('related_questions', [])])
            
            if depth > 1:
                for question in depth_results.get('related_questions', []):
                    if question.get('next_page_token'):
                        get_depth_results(question.get('next_page_token'), depth - 1, api_key)
                    
        for question in results.get('related_questions', []):
            if question.get('next_page_token'):
                get_depth_results(question.get('next_page_token'), depth_limit, api_key)
        
    return related_questions_results


def save_to_csv(data: dict):
    with open('data.csv', 'w') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(data.keys())
        writer.writerows(zip_longest(*data.values()))


def save_to_json(data: dict):
    with open('data.json', 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, indent=2, ensure_ascii=False)


def save_to_txt(data: dict):
    with open('data.txt', 'w') as txt_file:
        for key in data.keys():
            txt_file.write('\n'.join(data[key]) + '\n')


def main():
    parser = argparse.ArgumentParser(
        prog='SerpApi SEO Keyword Research Tool', 
        description='Extract keywrods from: Google Autocomplete, People Also Ask, and People Also Search and saves data to CSV/JSON/TXT.', 
        epilog='Found a bug? Open issue: https://github.com/chukhraiartur/seo-keyword-research-tool/issues'
    )
    parser.add_argument('-q','--query', metavar='', required=True, help='Search query (required).')
    parser.add_argument('-e','--engines', metavar='', required=False, default='all', choices=['ac', 'rs', 'rq'], help='Choices of engines to extract: Autocomplete (ac), Related Searches (rs), People Also Ask (rq). All engines are selected by default.')
    parser.add_argument('-dl','--depth-limit', metavar='', required=False, type=int, default=0, help='Depth limit for People Also Ask. Default is %(default)i, first 2-4 results.')
    parser.add_argument('-st','--save-to', metavar='', required=False, default='CSV', help='Saves the results in the current directory in the selected format (CSV, JSON, TXT). Default %(default)s.')
    parser.add_argument('-ak','--api-key', metavar='', required=False, default='5868ece26d41221f5e19ae8b3e355d22db23df1712da675d144760fc30d57988', help='Your SerpApi API key: https://serpapi.com/manage-api-key. Default is a test API key to test CLI.')
    parser.add_argument('-gd','--domain', metavar='', required=False, default='google.com', help='Google domain: https://serpapi.com/google-domains. Default %(default)s.')
    parser.add_argument('-gl','--country', metavar='', required=False, default='us', help='Country of the search: https://serpapi.com/google-countries. Default %(default)s.')
    parser.add_argument('-hl','--lang', metavar='', required=False, default='en', help='Language of the search: https://serpapi.com/google-languages. Default %(default)s.')

    args = parser.parse_args()
    
    data = {}
    
    if 'all' in args.engines:
        data['auto_complete'] = get_auto_complete(args.query, args.country, args.lang, args.api_key)
        data['related_searches'] = get_related_searches(args.query, args.domain, args.country, args.lang, args.api_key)
        data['related_questions'] = get_related_questions(args.query, args.domain, args.country, args.lang, args.api_key, args.depth_limit)
    elif 'ac' in args.engines:
        data['auto_complete'] = get_auto_complete(args.query, args.country, args.lang, args.api_key)
    elif 'rs' in args.engines:
        data['related_searches'] = get_related_searches(args.query, args.domain, args.country, args.lang, args.api_key)
    elif 'rq' in args.engines:
        data['related_questions'] = get_related_questions(args.query, args.domain, args.country, args.lang, args.api_key, args.depth_limit)
    
    # print(json.dumps(data, indent=2, ensure_ascii=False))

    if args.save_to:
        print(f'Saving data in {args.save_to.upper()} format...')

        if args.save_to.upper() == 'CSV':
            save_to_csv(data)
        elif args.save_to.upper() == 'JSON':
            save_to_json(data)
        elif args.save_to.upper() == 'TXT':
            save_to_txt(data)

        print(f'Data successfully saved to data.{args.save_to.lower()} file')


if __name__ == "__main__":
    main()