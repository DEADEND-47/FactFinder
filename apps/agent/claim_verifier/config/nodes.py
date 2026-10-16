"""Node configuration settings.

Contains settings for the claim verification pipeline nodes.
"""

import os

# Node settings
QUERY_GENERATION_CONFIG = {
    "temperature": 0.0,  # Zero temp for consistent results
}

EVIDENCE_RETRIEVAL_CONFIG = {
    "results_per_query": int(os.getenv("RESULTS_PER_QUERY", "3")),  # Number of search results to fetch per query
    "search_provider": os.getenv("SEARCH_PROVIDER", "tinyfish"),  # Search provider: "tinyfish", "tavily", or "exa"
}

EVIDENCE_EVALUATION_CONFIG = {
    "temperature": 0.0,  # Zero temp for consistent results
}

ITERATIVE_SEARCH_CONFIG = {
    "max_iterations": 5,
}
