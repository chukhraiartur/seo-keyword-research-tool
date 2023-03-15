from seo_keyword_research import SeoKeywordResearch

keyword_research = SeoKeywordResearch(
    query='starbucks coffee',
    api_key='5868ece26d41221f5e19ae8b3e355d22db23df1712da675d144760fc30d57988',
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