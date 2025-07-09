import requests
import json
from typing import List, Dict, Any, Optional

def search_tr_dizin(query: str, page: int = 1, limit: int = 5) -> Dict[str, Any]:
    """
    TR Dizin API'sinden makale arama fonksiyonu.

    Args:
        query: Arama sorgusu
        page: Sayfa numarası (varsayılan: 1)
        limit: Sonuç limiti (varsayılan: 5)

    Returns:
        API'den dönen ham veri
    """
    try:
        url = "https://search.trdizin.gov.tr/api/defaultSearch/publication/"
        params = {
            "q": query,
            "order": "relevance-DESC",
            "page": page,
            "limit": limit
        }

        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()

        return response.json()

    except requests.exceptions.RequestException as e:
        return {"error": f"API isteği başarısız: {str(e)}"}
    except json.JSONDecodeError as e:
        return {"error": f"JSON parse hatası: {str(e)}"}
    except Exception as e:
        return {"error": f"Beklenmeyen hata: {str(e)}"}

def process_articles(api_response: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    TR Dizin API'sinden gelen veriyi işleyip düzenli format haline getirir.

    Args:
        api_response: TR Dizin API'sinden gelen ham veri

    Returns:
        İşlenmiş makale listesi
    """
    if "error" in api_response:
        return [{"error": api_response["error"]}]

    try:
        hits = api_response.get("hits", {}).get("hits", [])

        if not hits:
            return [{"message": "Arama sonucu bulunamadı"}]

        processed_articles = []

        for item in hits:
            source = item.get("_source", {})

            # Abstract'tan title alma
            abstracts = source.get("abstracts", [])
            title_from_abstract = abstracts[0].get("title", "") if abstracts else ""

            # Title belirleme
            title = title_from_abstract or source.get("title", "İsim bulunamadı")

            article = {
                "title": title,
                "authors": source.get("authors", []),
                "year": source.get("year", source.get("publicationYear", "")),
                "abstract": source.get("abstract", ""),
                "doi": source.get("doi", ""),
                "url": source.get("url", ""),
                "journal": source.get("journal", ""),
                "keywords": source.get("keywords", [])
            }

            processed_articles.append(article)

        return processed_articles

    except Exception as e:
        return [{"error": f"Veri işleme hatası: {str(e)}"}]

def search_and_process_articles(query: str, page: int = 1, limit: int = 5) -> List[Dict[str, Any]]:
    """
    TR Dizin'de makale arayıp işlenmiş sonuçları döndürür.

    Args:
        query: Arama sorgusu
        page: Sayfa numarası
        limit: Sonuç limiti

    Returns:
        İşlenmiş makale listesi
    """
    # API'den veri çek
    api_response = search_tr_dizin(query, page, limit)

    # Veriyi işle
    processed_articles = process_articles(api_response)

    return processed_articles