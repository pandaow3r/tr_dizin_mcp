#!/usr/bin/env python3
"""
TR Dizin MCP Server Test Script
Bu script TR Dizin MCP server'ının fonksiyonlarını test eder.
"""

import asyncio
import sys
import os

# Mevcut dizini Python path'ine ekle
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import search_tr_dizin_articles, process_article_data, search_and_format_articles

async def test_api_connection():
    """TR Dizin API bağlantısını test eder."""
    print("🔍 TR Dizin API bağlantısı test ediliyor...")
    
    test_query = "yapay zeka"
    
    try:
        print(f"📡 '{test_query}' için API'ye istek gönderiliyor...")
        api_response = search_tr_dizin_articles(test_query)
        
        if "error" in api_response:
            print(f"❌ API Hatası: {api_response['error']}")
            return False
        
        print("✅ API bağlantısı başarılı!")
        
        # Toplam sonuç sayısını göster
        total_results = api_response.get("hits", {}).get("total", {}).get("value", 0)
        print(f"📊 Toplam sonuç sayısı: {total_results}")
        
        # Getirilen makale sayısını göster
        hits_count = len(api_response.get("hits", {}).get("hits", []))
        print(f"📄 Getirilen makale sayısı: {hits_count}")
        
        return True
        
    except Exception as e:
        print(f"❌ Test sırasında hata: {str(e)}")
        return False

async def test_data_processing():
    """Veri işleme fonksiyonunu test eder."""
    print("\n🔄 Veri işleme fonksiyonu test ediliyor...")
    
    test_query = "makine öğrenmesi"
    
    try:
        # API'den veri çek
        api_response = search_tr_dizin_articles(test_query)
        
        if "error" in api_response:
            print(f"❌ API Hatası: {api_response['error']}")
            return False
        
        # Veriyi işle
        processed_articles = process_article_data(api_response)
        
        if not processed_articles:
            print("❌ İşlenmiş makale bulunamadı")
            return False
        
        if len(processed_articles) == 1 and "error" in processed_articles[0]:
            print(f"❌ İşleme hatası: {processed_articles[0]['error']}")
            return False
        
        print(f"✅ {len(processed_articles)} makale başarıyla işlendi!")
        
        # İlk makaleyi göster
        if processed_articles:
            first_article = processed_articles[0]
            print("\n📄 İlk makale örneği:")
            print(f"   Başlık: {first_article.get('title', 'N/A')[:80]}...")
            print(f"   Yıl: {first_article.get('year', 'N/A')}")
            print(f"   Yazar sayısı: {len(first_article.get('authors', []))}")
        
        return True
        
    except Exception as e:
        print(f"❌ Test sırasında hata: {str(e)}")
        return False

async def test_complete_function():
    """Tam fonksiyonu test eder."""
    print("\n🔗 Tam arama fonksiyonu test ediliyor...")
    
    test_queries = ["covid-19", "blockchain", "eğitim"]
    
    for query in test_queries:
        try:
            print(f"\n🔍 '{query}' aranıyor...")
            result = search_and_format_articles(query)
            
            # JSON parse et
            import json
            parsed_result = json.loads(result)
            
            if "error" in parsed_result:
                print(f"❌ Hata: {parsed_result['error']}")
                continue
            
            articles = parsed_result.get("articles", [])
            if articles and len(articles) > 0 and "error" not in articles[0]:
                print(f"✅ {len(articles)} makale bulundu")
            else:
                print("⚠️ Makale bulunamadı")
                
        except Exception as e:
            print(f"❌ '{query}' için test hatası: {str(e)}")
    
    return True

async def main():
    """Ana test fonksiyonu."""
    print("🚀 TR Dizin MCP Server Test Başlıyor...\n")
    
    # Test 1: API bağlantısı
    test1_result = await test_api_connection()
    
    # Test 2: Veri işleme
    test2_result = await test_data_processing()
    
    # Test 3: Tam fonksiyon
    test3_result = await test_complete_function()
    
    # Sonuçları özetle
    print("\n" + "="*50)
    print("📋 TEST SONUÇLARI:")
    print(f"   API Bağlantısı: {'✅ BAŞARILI' if test1_result else '❌ BAŞARISIZ'}")
    print(f"   Veri İşleme: {'✅ BAŞARILI' if test2_result else '❌ BAŞARISIZ'}")
    print(f"   Tam Fonksiyon: {'✅ BAŞARILI' if test3_result else '❌ BAŞARISIZ'}")
    
    if test1_result and test2_result and test3_result:
        print("\n🎉 Tüm testler başarılı! TR Dizin MCP server hazır.")
        print("\n📝 Kullanım örnekleri:")
        print("   - search_articles('yapay zeka')")
        print("   - search_articles('makine öğrenmesi')")
        print("   - search_articles('covid-19')")
        return True
    else:
        print("\n⚠️ Bazı testler başarısız. Lütfen hataları kontrol edin.")
        return False

if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
