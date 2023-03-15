from seo_keyword_research import SeoKeywordResearch
import argparse


def main():
    parser = argparse.ArgumentParser(
        prog='SerpApi SEO Keyword Research Tool', 
        description='Extract keywrods from: Google Autocomplete, People Also Ask, and People Also Search and saves data to CSV/JSON/TXT.', 
        epilog='Found a bug? Open issue: https://github.com/chukhraiartur/seo-keyword-research-tool/issues'
    )
    parser.add_argument('-q','--query', metavar='', required=True, help='Search query (required).')
    parser.add_argument('-e','--engines', metavar='', required=False, type=str, default=['ac', 'rs', 'rq'], nargs='+', help='Choices of engines to extract: Autocomplete (ac), Related Searches (rs), People Also Ask (rq). You can select multiple engines. All engines are selected by default.')
    parser.add_argument('-dl','--depth-limit', metavar='', required=False, type=int, default=0, help='Depth limit for People Also Ask. Default is %(default)i, first 2-4 results.')
    parser.add_argument('-st','--save-to', metavar='', required=False, default='CSV', help='Saves the results in the current directory in the selected format (CSV, JSON, TXT). Default %(default)s.')
    parser.add_argument('-ak','--api-key', metavar='', required=False, default='5868ece26d41221f5e19ae8b3e355d22db23df1712da675d144760fc30d57988', help='Your SerpApi API key: https://serpapi.com/manage-api-key. Default is a test API key to test CLI.')
    parser.add_argument('-gd','--domain', metavar='', required=False, default='google.com', help='Google domain: https://serpapi.com/google-domains. Default %(default)s.')
    parser.add_argument('-gl','--country', metavar='', required=False, default='us', help='Country of the search: https://serpapi.com/google-countries. Default %(default)s.')
    parser.add_argument('-hl','--lang', metavar='', required=False, default='en', help='Language of the search: https://serpapi.com/google-languages. Default %(default)s.')
    args = parser.parse_args()
    
    keyword_research = SeoKeywordResearch(
        query=args.query,
        api_key=args.api_key,
        lang=args.lang,
        country=args.country,
        domain=args.domain
    )

    data = {}
    
    for engine in args.engines:
        if engine.lower() == 'ac':
            data['auto_complete'] = keyword_research.get_auto_complete()
        elif engine.lower() == 'rs':
            data['related_searches'] = keyword_research.get_related_searches()
        elif engine.lower() == 'rq':
            data['related_questions'] = keyword_research.get_related_questions(args.depth_limit)

    if data:
        # keyword_research.print_data(data)
        print(f'Saving data in {args.save_to.upper()} format...')

        if args.save_to.upper() == 'CSV':
            keyword_research.save_to_csv(data)
        elif args.save_to.upper() == 'JSON':
            keyword_research.save_to_json(data)
        elif args.save_to.upper() == 'TXT':
            keyword_research.save_to_txt(data)

        print(f'Data successfully saved to data.{args.save_to.lower()} file')


if __name__ == "__main__":
    main()