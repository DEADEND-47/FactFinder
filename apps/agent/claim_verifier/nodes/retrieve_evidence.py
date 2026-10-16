"""Retrieve evidence node - fetches evidence for claims using Exa AI Search.

Uses search queries to retrieve relevant evidence snippets from the web using neural search.
"""

import logging
from typing import Any, Dict, List

import os
from langchain_exa import ExaSearchRetriever
from langchain_tavily import TavilySearch
from tinyfish import AsyncTinyFish

from claim_verifier.config import EVIDENCE_RETRIEVAL_CONFIG
from claim_verifier.schemas import ClaimVerifierState, Evidence

logger = logging.getLogger(__name__)

# Retrieval settings
RESULTS_PER_QUERY = EVIDENCE_RETRIEVAL_CONFIG["results_per_query"]
SEARCH_PROVIDER = EVIDENCE_RETRIEVAL_CONFIG["search_provider"]


class SearchProviders:
    @staticmethod
    async def tinyfish(query: str) -> List[Evidence]:
        """Search the web for claim evidence using TinyFish live web intelligence."""
        logger.info(f"Searching with TinyFish: '{query}'")

        try:
            api_key = os.getenv("TINYFISH_API_KEY")
            client = AsyncTinyFish(api_key=api_key) if api_key else AsyncTinyFish()

            response = await client.search.query(
                query=query,
                purpose="Fact-checking and evidence verification for claim validation",
            )

            results = getattr(response, "results", []) or []
            if not results:
                logger.info(f"TinyFish returned 0 results for '{query}'")
                return []

            evidence: List[Evidence] = []
            for result in results[:RESULTS_PER_QUERY]:
                title = getattr(result, "title", None) or getattr(result, "site_name", "") or "Search Result"
                url = getattr(result, "url", "") or ""
                snippet = getattr(result, "snippet", "") or ""

                # Beautify metadata attribution header
                meta_tags = []
                site_name = getattr(result, "site_name", None)
                if site_name:
                    meta_tags.append(f"Source: {site_name}")
                publisher = getattr(result, "publisher", None)
                if publisher and publisher != site_name:
                    meta_tags.append(f"Publisher: {publisher}")
                date = getattr(result, "date", None)
                if date:
                    meta_tags.append(f"Date: {date}")
                authors = getattr(result, "authors", None)
                if authors:
                    meta_tags.append(f"Authors: {', '.join(authors)}")

                meta_header = " | ".join(meta_tags)
                clean_snippet = snippet.strip()
                if meta_header:
                    formatted_text = f"[{meta_header}]\n{clean_snippet}"
                else:
                    formatted_text = clean_snippet

                evidence.append(
                    Evidence(
                        url=url,
                        text=formatted_text[:2000],
                        title=title,
                    )
                )

            logger.info(f"TinyFish retrieved {len(evidence)} evidence items")
            return evidence

        except Exception as e:
            logger.error(f"TinyFish search failed for '{query}': {e}")
            return []

    @staticmethod
    async def exa(query: str) -> List[Evidence]:
        logger.info(f"Searching with Exa: '{query}'")

        try:
            retriever = ExaSearchRetriever(
                k=RESULTS_PER_QUERY,
                text_contents_options={"max_characters": 2000},
                type="neural",
            )

            results = await retriever.ainvoke(query)

            evidence = [
                Evidence(
                    url=doc.metadata.get("url", ""),
                    text=doc.page_content[:2000],
                    title=doc.metadata.get("title"),
                )
                for doc in results
            ]

            logger.info(f"Retrieved {len(evidence)} evidence items")
            return evidence

        except Exception as e:
            logger.error(f"Exa search failed for '{query}': {e}")
            return []

    @staticmethod
    async def tavily(query: str) -> List[Evidence]:
        logger.info(f"Searching with Tavily: '{query}'")

        try:
            search = TavilySearch(
                max_results=RESULTS_PER_QUERY,
                topic="general",
                include_raw_content="markdown",
            )

            results = await search.ainvoke(query)
            evidence = SearchProviders._parse_tavily_results(results)

            logger.info(f"Retrieved {len(evidence)} evidence items")
            return evidence

        except Exception as e:
            logger.error(f"Tavily search failed for '{query}': {e}")
            return []

    @staticmethod
    def _parse_tavily_results(results: Any) -> List[Evidence]:
        match results:
            case {"results": search_results} if isinstance(search_results, list):
                return [
                    Evidence(
                        url=result.get("url", ""),
                        text=result.get("raw_content") or result.get("content", ""),
                        title=result.get("title", ""),
                    )
                    for result in search_results
                    if isinstance(result, dict)
                ]
            case str():
                return [Evidence(url="", text=results, title="Tavily Search Result")]
            case _:
                return []


async def _search_query(query: str) -> List[Evidence]:
    provider = SEARCH_PROVIDER.lower() if SEARCH_PROVIDER else "tinyfish"
    match provider:
        case "tinyfish":
            evidence = await SearchProviders.tinyfish(query)
            if not evidence:
                # Graceful fallback to Tavily or Exa if TinyFish has no results
                if os.getenv("TAVILY_API_KEY"):
                    logger.info("TinyFish returned no results, falling back to Tavily")
                    evidence = await SearchProviders.tavily(query)
                elif os.getenv("EXA_API_KEY"):
                    logger.info("TinyFish returned no results, falling back to Exa")
                    evidence = await SearchProviders.exa(query)
            return evidence
        case "tavily":
            return await SearchProviders.tavily(query)
        case _:
            return await SearchProviders.exa(query)


async def retrieve_evidence_node(
    state: ClaimVerifierState,
) -> Dict[str, List[Evidence]]:
    if not state.query:
        logger.warning("No search query to process")
        return {"evidence": []}

    evidence = await _search_query(state.query)
    logger.info(f"Retrieved {len(evidence)} total evidence snippets")

    return {"evidence": [item.model_dump() for item in evidence]}
