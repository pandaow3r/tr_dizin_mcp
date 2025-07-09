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

def extract_article_title(source: Dict[str, Any]) -> str:
    """
    Makale kaynağından başlığı çıkarır. Farklı başlık alanlarını kontrol eder.

    Args:
        source: Makale kaynak verisi (_source)

    Returns:
        Makale başlığı
    """
    # 1. Öncelik: abstracts[0].title (en doğru başlık)
    abstracts = source.get("abstracts", [])
    if abstracts and isinstance(abstracts, list) and len(abstracts) > 0:
        first_abstract = abstracts[0]
        if isinstance(first_abstract, dict) and "title" in first_abstract:
            title = first_abstract["title"]
            if title and title.strip():
                return title.strip()

    # 2. İkinci seçenek: orderTitle (boşluklar kaldırılmış olabilir)
    order_title = source.get("orderTitle", "")
    if order_title and order_title.strip():
        return order_title.strip()

    # 3. Üçüncü seçenek: title alanı (varsa)
    title = source.get("title", "")
    if title and title.strip():
        return title.strip()

    # 4. Son seçenek: Diğer title içeren alanları kontrol et
    for key, value in source.items():
        if "title" in key.lower() and isinstance(value, str) and value.strip():
            return value.strip()

    # Hiçbir başlık bulunamazsa
    return "Başlık bulunamadı"

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

            # Başlığı doğru şekilde çıkar
            title = extract_article_title(source)

            # Abstract'ı çıkar (abstracts[0].abstract)
            abstract = ""
            abstracts = source.get("abstracts", [])
            if abstracts and isinstance(abstracts, list) and len(abstracts) > 0:
                first_abstract = abstracts[0]
                if isinstance(first_abstract, dict) and "abstract" in first_abstract:
                    abstract = first_abstract["abstract"] or ""

            # Makale bilgilerini çıkar
            article = {
                "title": title,
                "authors": source.get("authors", []),
                "year": source.get("year", source.get("publicationYear", "")),
                "abstract": abstract,
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