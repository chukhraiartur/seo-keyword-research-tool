from serpapi import GoogleSearch
from itertools import zip_longest
import json, csv, os, argparse


def get_auto_complete(query: str, country: str, lang: str):
    params = {
        'api_key': os.getenv('SERPAPI_API_KEY'),    # https://serpapi.com/manage-api-key
        'engine': 'google_autocomplete',            # search engine
        'q': query,                                 # search query
        'gl': country,                              # https://serpapi.com/google-countries
        'hl': lang                                  # https://serpapi.com/google-languages
    }

    search = GoogleSearch(params)                   # data extraction on the SerpApi backend
    results = search.get_dict()                     # JSON -> Python dict
    
    auto_complete_results = [result['value'] for result in results['suggestions']]
    
    return auto_complete_results


def get_related_searches(query: str, domain: str, country: str, lang: str):
    params = {
        'api_key': os.getenv('SERPAPI_API_KEY'),    # https://serpapi.com/manage-api-key
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


def get_related_questions(query: str, domain: str, country: str, lang: str):
    params = {
        'api_key': os.getenv('SERPAPI_API_KEY'),    # https://serpapi.com/manage-api-key
        'engine': 'google',                         # search engine
        'q': query,                                 # search query
        'google_domain': domain,                    # https://serpapi.com/google-domains
        'gl': country,                              # https://serpapi.com/google-countries
        'hl': lang                                  # https://serpapi.com/google-languages
    }

    search = GoogleSearch(params)                   # data extraction on the SerpApi backend
    results = search.get_dict()                     # JSON -> Python dict

    related_questions_results = [result['question'] for result in results['related_questions']]

    return related_questions_results


def filter_duplicates(data: dict):
    filtered_data = []

    if data.get('auto_complete'):
        for i in range(len(data.get('auto_complete', []))):    
            if data['auto_complete'][i] not in data.get('related_questions', []) + data.get('related_searches', []):
                filtered_data.append(data['auto_complete'][i])

    if data.get('related_searches'):
        for i in range(len(data.get('related_searches', []))):    
            if data['related_searches'][i] not in data.get('auto_complete', []) + data.get('related_questions', []):
                filtered_data.append(data['related_searches'][i])
    
    if data.get('related_questions'):
        for i in range(len(data.get('related_questions', []))):
            if data['related_questions'][i] not in data.get('auto_complete', []) + data.get('related_searches', []):
                filtered_data.append(data['related_questions'][i])
    
    return filtered_data


def save_to_csv(data: dict):
    with open('data.csv', 'w') as file:
        writer = csv.writer(file)
        writer.writerow(data.keys())
        writer.writerows(zip_longest(*data.values()))


def save_to_json(data: dict):
    with open('data.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=2, ensure_ascii=False)


def save_to_txt(data: dict):
    with open('data.txt', 'w') as file:
        for key in data.keys():
            file.write('\n'.join(data[key]) + '\n')


def main():
    parser = argparse.ArgumentParser(prog='SEO Keyword Research Options')
    parser.add_argument('-q','--query', metavar='', required=True, help='')
    parser.add_argument('-gd','--domain', action='store_true', default='google.com', help='')
    parser.add_argument('-gl','--country', action='store_true', default='us', help='')
    parser.add_argument('-hl','--lang', action='store_true', default='en', help='')
    parser.add_argument('-ac','--auto-complete', action='store_true', help='')
    parser.add_argument('-rs','--related-searches', action='store_true', help='')
    parser.add_argument('-rq','--related-questions', action='store_true', help='')
    parser.add_argument('-fd','--filter-duplicates', action='store_true', help='')
    parser.add_argument('-st','--save-to', action='store_true', help='')
    args, unknown = parser.parse_known_args()

    data = {}

    if args.auto_complete:
        data['auto_complete'] = get_auto_complete(args.query, args.country, args.lang)

    if args.related_searches:
        data['related_searches'] = get_related_searches(args.query, args.domain, args.country, args.lang)

    if args.related_questions:
        data['related_questions'] = get_related_questions(args.query, args.domain, args.country, args.lang)

    if args.filter_duplicates:
        data = filter_duplicates(data)

    print(json.dumps(data, indent=2, ensure_ascii=False))

    if args.save_to:
        print(f'Saving data in {args.save_to.upper()} format...')

        if args.save_to == 'csv':
            save_to_csv(data)
        elif args.save_to == 'json':
            save_to_json(data)
        elif args.save_to == 'txt':
            save_to_txt(data)

        print(f'Data successfully saved to data.{args.save_to} file')

    if unknown:
        parser.print_help()


if __name__ == "__main__":
    main()