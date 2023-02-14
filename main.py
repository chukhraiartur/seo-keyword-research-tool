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
    parser = argparse.ArgumentParser(prog='SEO Keyword Research Options')
    parser.add_argument('-q','--query', metavar='', required=True, help='search query')
    parser.add_argument('-e','--engines', metavar='', required=True, help='choice of engines to extract: Autocomplete (auto-complete), Related Searches (related-searches), People Also Ask (related-questions)')
    parser.add_argument('-dl','--depth-limit', metavar='', required=False, type=int, default=0, help='depth limit for People Also Ask')
    parser.add_argument('-st','--save-to', metavar='', required=False, default='CSV', help='saves the results in the current directory in the selected format (CSV, JSON, TXT)')
    parser.add_argument('-ak','--api-key', metavar='', required=False, default='5868ece26d41221f5e19ae8b3e355d22db23df1712da675d144760fc30d57988', help='your SerpApi API key')
    parser.add_argument('-gd','--domain', metavar='', required=False, default='google.com', help='google domain')
    parser.add_argument('-gl','--country', metavar='', required=False, default='us', help='country of the search')
    parser.add_argument('-hl','--lang', metavar='', required=False, default='en', help='language of the search')

    args = parser.parse_args()

    data = {}

    if 'auto-complete' in args.engines:
        data['auto_complete'] = get_auto_complete(args.query, args.country, args.lang, args.api_key)

    if 'related-searches' in args.engines:
        data['related_searches'] = get_related_searches(args.query, args.domain, args.country, args.lang, args.api_key)

    if 'related-questions' in args.engines:
        data['related_questions'] = get_related_questions(args.query, args.domain, args.country, args.lang, args.api_key, args.depth_limit)
    
    print(json.dumps(data, indent=2, ensure_ascii=False))

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