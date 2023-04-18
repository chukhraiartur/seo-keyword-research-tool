from serpapi import GoogleSearch
from itertools import zip_longest
import json, csv


class SeoKeywordResearch:
    def __init__(self, query: str, api_key: str, lang: str = 'en', country: str = 'us', domain: str = 'google.com') -> None:
        self.query = query
        self.api_key = api_key
        self.lang = lang
        self.country = country
        self.domain = domain


    def get_auto_complete(self) -> list:
        params = {
            'api_key': self.api_key,            # https://serpapi.com/manage-api-key
            'engine': 'google_autocomplete',    # search engine
            'q': self.query,                    # search query
            'gl': self.country,                 # country of the search
            'hl': self.lang                     # language of the search
        }

        search = GoogleSearch(params)           # data extraction on the SerpApi backend
        results = search.get_dict()             # JSON -> Python dict
        
        auto_complete_results = [result.get('value') for result in results.get('suggestions', [])]
        
        return auto_complete_results


    def get_related_searches(self) -> list:
        params = {
            'api_key': self.api_key,            # https://serpapi.com/manage-api-key
            'engine': 'google',                 # search engine
            'q': self.query,                    # search query
            'google_domain': self.domain,       # Google domain to use
            'gl': self.country,                 # country of the search
            'hl': self.lang                     # language of the search
        }

        search = GoogleSearch(params)           # data extraction on the SerpApi backend
        results = search.get_dict()             # JSON -> Python dict
        
        related_searches_results = [result.get('query') for result in results.get('related_searches', [])]

        return related_searches_results


    def get_related_questions(self, depth_limit: int = 0) -> list:
        params = {
            'api_key': self.api_key,            # https://serpapi.com/manage-api-key
            'engine': 'google',                 # search engine
            'q': self.query,                    # search query
            'google_domain': self.domain,       # Google domain to use
            'gl': self.country,                 # country of the search
            'hl': self.lang                     # language of the search
        }

        search = GoogleSearch(params)           # data extraction on the SerpApi backend
        results = search.get_dict()             # JSON -> Python dict

        related_questions_results = [result.get('question') for result in results.get('related_questions', [])]

        if depth_limit > 4:
            depth_limit = 4

        if depth_limit:
            def get_depth_results(token: str, depth: int) -> None:
                '''
                This function allows you to extract more data from People Also Ask.
                
                The function takes the following arguments:
                
                :param token: allows access to additional related questions.
                :param depth: limits the input depth for each related question.
                '''

                depth_params = {
                    'api_key': self.api_key,
                    'engine': 'google_related_questions',
                    'next_page_token': token,
                }

                depth_search = GoogleSearch(depth_params)
                depth_results = depth_search.get_dict()
                
                related_questions_results.extend([result.get('question') for result in depth_results.get('related_questions', [])])
                
                if depth > 1:
                    for question in depth_results.get('related_questions', []):
                        if question.get('next_page_token'):
                            get_depth_results(question.get('next_page_token'), depth - 1)
                        
            for question in results.get('related_questions', []):
                if question.get('next_page_token'):
                    get_depth_results(question.get('next_page_token'), depth_limit)
            
        return related_questions_results


    def save_to_csv(self, data: dict) -> None:
        with open(f'{self.query}.csv', 'w') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(data.keys())
            writer.writerows(zip_longest(*data.values()))


    def save_to_json(self, data: dict) -> None:
        with open(f'{self.query}.json', 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, indent=2, ensure_ascii=False)


    def save_to_txt(self, data: dict) -> None:
        with open(f'{self.query}.txt', 'w') as txt_file:
            for key in data.keys():
                txt_file.write('\n'.join(data.get(key)) + '\n')


    def print_data(self, data: dict) -> None:
        print(json.dumps(data, indent=2, ensure_ascii=False))