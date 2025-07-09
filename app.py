import requests
import json
from typing import Dict, List, Any

def search_tr_dizin_articles(query: str) -> Dict[str, Any]:
    """
    TR Dizin API'sinden makale arama fonksiyonu.

    Args:
        query: Kullanıcının arama terimi

    Returns:
        API'den dönen veri veya hata mesajı
    """
    try:
        # TR Dizin API endpoint'i
        url = "https://search.trdizin.gov.tr/api/defaultSearch/publication/"

        # API parametreleri
        params = {
            "q": query,
            "order": "relevance-DESC",
            "page": 1,
            "limit": 5
        }

        # API'ye istek gönder
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()

        # JSON yanıtını döndür
        return response.json()

    except requests.exceptions.RequestException as e:
        return {"error": f"API isteği başarısız: {str(e)}"}
    except json.JSONDecodeError as e:
        return {"error": f"JSON parse hatası: {str(e)}"}
    except Exception as e:
        return {"error": f"Beklenmeyen hata: {str(e)}"}

def process_article_data(api_response: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    TR Dizin API'sinden gelen ham veriyi işleyip düzenli formata çevirir.

    Args:
        api_response: API'den gelen ham veri

    Returns:
        İşlenmiş makale listesi
    """
    # Hata kontrolü
    if "error" in api_response:
        return [{"error": api_response["error"]}]

    try:
        # API yanıtından makale verilerini çıkar
        hits = api_response.get("hits", {}).get("hits", [])

        if not hits:
            return [{"message": "Arama sonucu bulunamadı"}]

        processed_articles = []

        for item in hits:
            source = item.get("_source", {})

            # Makale bilgilerini çıkar
            article = {
                "title": source.get("title", "Başlık bulunamadı"),
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

def search_and_format_articles(query: str) -> str:
    """
    Kullanıcının arama terimini alıp TR Dizin'den makale arar ve formatlar.

    Args:
        query: Arama terimi

    Returns:
        Formatlanmış makale listesi (JSON string)
    """
    # API'den veri çek
    api_response = search_tr_dizin_articles(query)

    # Veriyi işle
    processed_articles = process_article_data(api_response)

    # Sonucu formatla
    result = {
        "query": query,
        "total_found": len(processed_articles),
        "articles": processed_articles
    }

    return json.dumps(result, ensure_ascii=False, indent=2)