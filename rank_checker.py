"""
Google Rank Checker Module
Handles Google search queries and ranking position extraction using SerpAPI
"""
import requests
import time
from typing import Dict, Optional, List
from urllib.parse import urlparse
import config


class RankChecker:
    """Handles Google search queries and extracts ranking positions"""
    
    def __init__(self, api_key: str = None):
        """
        Initialize the Rank Checker
        
        Args:
            api_key: SerpAPI key. If not provided, uses config.SERPAPI_KEY
        """
        self.api_key = api_key or config.SERPAPI_KEY
        if not self.api_key:
            raise ValueError("SerpAPI key is required. Set SERPAPI_KEY in .env file")
        
        self.base_url = config.SERPAPI_URL
        self.max_results = config.MAX_RESULTS_TO_CHECK
        self.results_per_page = config.RESULTS_PER_PAGE
    
    def normalize_url(self, url: str) -> str:
        """
        Normalize URL for comparison (remove protocol, www, trailing slashes)
        
        Args:
            url: URL to normalize
            
        Returns:
            Normalized URL string
        """
        if not url:
            return ""
        
        # Remove protocol
        url = url.replace('https://', '').replace('http://', '')
        
        # Remove www.
        if url.startswith('www.'):
            url = url[4:]
        
        # Remove trailing slash
        url = url.rstrip('/')
        
        return url.lower()
    
    def extract_domain(self, url: str) -> str:
        """
        Extract domain from URL
        
        Args:
            url: Full URL
            
        Returns:
            Domain name
        """
        try:
            parsed = urlparse(url if url.startswith('http') else f'https://{url}')
            domain = parsed.netloc or parsed.path.split('/')[0]
            return self.normalize_url(domain)
        except:
            return self.normalize_url(url)
    
    def check_ranking(self, keyword: str, website_url: str, location: str = "United States") -> Dict:
        """
        Check the ranking position of a website for a given keyword
        
        Args:
            keyword: Search keyword
            website_url: Website URL to track
            location: Search location (default: United States)
            
        Returns:
            Dictionary containing ranking information
        """
        target_domain = self.extract_domain(website_url)
        ranking_position = None
        found_url = None
        serp_title = None
        serp_snippet = None
        
        # Check multiple pages if needed
        max_pages = (self.max_results // self.results_per_page) + 1
        
        for page in range(max_pages):
            start = page * self.results_per_page
            
            params = {
                'q': keyword,
                'api_key': self.api_key,
                'engine': 'google',
                'location': location,
                'num': self.results_per_page,
                'start': start
            }
            
            try:
                response = requests.get(self.base_url, params=params, timeout=30)
                response.raise_for_status()
                data = response.json()
                
                # Check for errors
                if 'error' in data:
                    return {
                        'keyword': keyword,
                        'website_url': website_url,
                        'ranking_position': 'Error',
                        'found_url': None,
                        'checked_on': time.strftime('%Y-%m-%d %H:%M:%S'),
                        'serp_title': None,
                        'serp_snippet': None,
                        'error': data['error']
                    }
                
                # Extract organic results
                organic_results = data.get('organic_results', [])
                
                if not organic_results:
                    break
                
                # Check each result
                for result in organic_results:
                    result_url = result.get('link', '')
                    result_domain = self.extract_domain(result_url)
                    
                    # Check if domain matches
                    if result_domain == target_domain:
                        ranking_position = start + organic_results.index(result) + 1
                        found_url = result_url
                        serp_title = result.get('title', '')
                        serp_snippet = result.get('snippet', '')
                        break
                
                # If found, break out of page loop
                if ranking_position:
                    break
                
                # Rate limiting - be respectful to API
                time.sleep(1)
                
            except requests.exceptions.RequestException as e:
                return {
                    'keyword': keyword,
                    'website_url': website_url,
                    'ranking_position': 'Error',
                    'found_url': None,
                    'checked_on': time.strftime('%Y-%m-%d %H:%M:%S'),
                    'serp_title': None,
                    'serp_snippet': None,
                    'error': str(e)
                }
        
        # Prepare result
        if ranking_position is None:
            ranking_position = f"> {self.max_results}"
        
        return {
            'keyword': keyword,
            'website_url': website_url,
            'ranking_position': ranking_position,
            'found_url': found_url or 'Not Found',
            'checked_on': time.strftime('%Y-%m-%d %H:%M:%S'),
            'serp_title': serp_title or '',
            'serp_snippet': serp_snippet or '',
            'error': None
        }
    
    def check_multiple_keywords(self, keywords: List[str], website_url: str, location: str = "United States") -> List[Dict]:
        """
        Check rankings for multiple keywords
        
        Args:
            keywords: List of keywords to check
            website_url: Website URL to track
            location: Search location
            
        Returns:
            List of ranking dictionaries
        """
        results = []
        
        for keyword in keywords:
            print(f"Checking keyword: {keyword}")
            result = self.check_ranking(keyword, website_url, location)
            results.append(result)
            
            # Rate limiting between keywords
            time.sleep(2)
        
        return results


