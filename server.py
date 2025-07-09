from mcp.server.fastmcp import FastMCP
from app import search_and_process_articles, search_tr_dizin, process_articles
import json

# Initialize MCP server
mcp = FastMCP("tr-dizin-mcp")

@mcp.tool()
async def search_articles(query: str, page: int = 1, limit: int = 5) -> str:
    """
    TR Dizin veritabanında makale arar ve sonuçları döndürür.

    Args:
        query: Arama yapılacak kelime veya kelime grubu
        page: Sayfa numarası (varsayılan: 1)
        limit: Döndürülecek maksimum sonuç sayısı (varsayılan: 5, maksimum: 20)

    Returns:
        JSON formatında makale listesi
    """
    try:
        # Limit kontrolü
        if limit > 20:
            limit = 20
        if limit < 1:
            limit = 1
        if page < 1:
            page = 1

        # Makale arama ve işleme
        articles = search_and_process_articles(query, page, limit)

        # JSON formatında döndür
        return json.dumps({
            "success": True,
            "query": query,
            "page": page,
            "limit": limit,
            "total_results": len(articles),
            "articles": articles
        }, ensure_ascii=False, indent=2)

    except Exception as e:
        return json.dumps({
            "success": False,
            "error": f"Arama sırasında hata oluştu: {str(e)}"
        }, ensure_ascii=False, indent=2)

@mcp.tool()
async def get_article_summary(query: str, max_articles: int = 3) -> str:
    """
    Belirli bir konuda makale arayıp özet bilgiler döndürür.

    Args:
        query: Arama yapılacak konu
        max_articles: Özetlenecek maksimum makale sayısı (varsayılan: 3)

    Returns:
        Makalelerin özet bilgileri
    """
    try:
        articles = search_and_process_articles(query, 1, max_articles)

        if not articles or (len(articles) == 1 and "error" in articles[0]):
            return f"'{query}' konusunda makale bulunamadı."

        summary = f"'{query}' konusunda {len(articles)} makale bulundu:\n\n"

        for i, article in enumerate(articles, 1):
            if "error" in article:
                continue

            summary += f"{i}. {article.get('title', 'Başlık yok')}\n"

            authors = article.get('authors', [])
            if authors:
                author_names = [author.get('name', '') for author in authors if isinstance(author, dict)]
                if author_names:
                    summary += f"   Yazarlar: {', '.join(author_names)}\n"

            year = article.get('year', '')
            if year:
                summary += f"   Yıl: {year}\n"

            abstract = article.get('abstract', '')
            if abstract:
                # Abstract'ı kısalt
                short_abstract = abstract[:200] + "..." if len(abstract) > 200 else abstract
                summary += f"   Özet: {short_abstract}\n"

            summary += "\n"

        return summary

    except Exception as e:
        return f"Özet oluşturulurken hata oluştu: {str(e)}"

@mcp.tool()
async def search_by_author(author_name: str, limit: int = 5) -> str:
    """
    Belirli bir yazarın makalelerini arar.

    Args:
        author_name: Yazar adı
        limit: Döndürülecek maksimum sonuç sayısı

    Returns:
        JSON formatında yazar makaleleri
    """
    try:
        # Yazar adını sorgu olarak kullan
        query = f"author:{author_name}"
        articles = search_and_process_articles(query, 1, limit)

        return json.dumps({
            "success": True,
            "author": author_name,
            "total_results": len(articles),
            "articles": articles
        }, ensure_ascii=False, indent=2)

    except Exception as e:
        return json.dumps({
            "success": False,
            "error": f"Yazar arama sırasında hata oluştu: {str(e)}"
        }, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    mcp.run(transport="stdio")