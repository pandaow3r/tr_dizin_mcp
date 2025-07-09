from mcp.server.fastmcp import FastMCP
from app import search_and_format_articles

# Initialize MCP server
mcp = FastMCP("tr-dizin-search")

@mcp.tool()
async def search_articles(query: str) -> str:
    """
    TR Dizin veritabanında makale arar ve sonuçları döndürür.

    Bu tool, kullanıcının verdiği arama terimini TR Dizin API'sine gönderir
    ve en alakalı 5 makaleyi getirir.

    Args:
        query: Aranacak makale konusu, yazar adı veya anahtar kelime

    Returns:
        JSON formatında makale listesi (başlık, yazarlar, yıl, özet, DOI, URL vb.)

    Örnek kullanım:
        - "yapay zeka"
        - "makine öğrenmesi"
        - "covid-19"
        - "Ahmet Yılmaz" (yazar adı)
    """
    try:
        if not query or query.strip() == "":
            return '{"error": "Arama terimi boş olamaz. Lütfen bir konu, yazar adı veya anahtar kelime girin."}'

        # Arama terimini temizle
        clean_query = query.strip()

        # TR Dizin'de makale ara
        result = search_and_format_articles(clean_query)

        return result

    except Exception as e:
        error_result = {
            "error": f"Arama sırasında hata oluştu: {str(e)}",
            "query": query
        }
        return json.dumps(error_result, ensure_ascii=False, indent=2)

@mcp.tool()
async def get_article_info() -> str:
    """
    TR Dizin MCP server hakkında bilgi verir.

    Returns:
        Server özellikleri ve kullanım bilgileri
    """
    info = {
        "server_name": "TR Dizin Makale Arama MCP Server",
        "description": "Türkiye'nin ulusal akademik veri tabanı TR Dizin'de makale arama",
        "api_endpoint": "https://search.trdizin.gov.tr/api/defaultSearch/publication/",
        "features": [
            "Konu bazında makale arama",
            "Yazar bazında makale arama",
            "En alakalı 5 makale getirme",
            "Makale detayları (başlık, yazarlar, yıl, özet, DOI, URL)",
            "JSON formatında düzenli çıktı"
        ],
        "usage_examples": [
            "yapay zeka",
            "makine öğrenmesi",
            "covid-19",
            "Ahmet Yılmaz"
        ]
    }

    return json.dumps(info, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    import json
    mcp.run(transport="stdio")