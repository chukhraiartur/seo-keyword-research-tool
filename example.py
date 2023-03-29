from seo_keyword_research import SeoKeywordResearch

keyword_research = SeoKeywordResearch(
    query='starbucks coffee',
    api_key='<your_serpapi_api_key>',
    lang='en',
    country='us',
    domain='google.com'
)

auto_complete_results = keyword_research.get_auto_complete()
related_searches_results = keyword_research.get_related_searches()
related_questions_results = keyword_research.get_related_questions()

data = {
    'auto_complete': auto_complete_results,
    'related_searches': related_searches_results,
    'related_questions': related_questions_results
}

keyword_research.print_data(data)