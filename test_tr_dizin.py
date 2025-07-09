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

from app import search_and_process_articles, search_tr_dizin, process_articles

async def test_search_function():
    """TR Dizin arama fonksiyonunu test eder."""
    print("🔍 TR Dizin arama fonksiyonu test ediliyor...")
    
    # Test sorgusu
    test_query = "yapay zeka"
    
    try:
        # API'den veri çek
        print(f"📡 '{test_query}' için TR Dizin API'sine istek gönderiliyor...")
        api_response = search_tr_dizin(test_query, page=1, limit=3)
        
        if "error" in api_response:
            print(f"❌ API Hatası: {api_response['error']}")
            return False
        
        print("✅ API isteği başarılı!")
        print(f"📊 Toplam sonuç sayısı: {api_response.get('hits', {}).get('total', {}).get('value', 0)}")
        
        # Veriyi işle
        print("🔄 Veriler işleniyor...")
        processed_articles = process_articles(api_response)
        
        if not processed_articles:
            print("❌ İşlenmiş makale bulunamadı")
            return False
        
        print(f"✅ {len(processed_articles)} makale başarıyla işlendi!")
        
        # İlk makaleyi göster
        if processed_articles and "error" not in processed_articles[0]:
            first_article = processed_articles[0]
            print("\n📄 İlk makale örneği:")
            print(f"   Başlık: {first_article.get('title', 'N/A')}")
            print(f"   Yıl: {first_article.get('year', 'N/A')}")
            print(f"   Yazar sayısı: {len(first_article.get('authors', []))}")
        
        return True
        
    except Exception as e:
        print(f"❌ Test sırasında hata: {str(e)}")
        return False

async def test_combined_function():
    """Birleşik arama ve işleme fonksiyonunu test eder."""
    print("\n🔗 Birleşik arama fonksiyonu test ediliyor...")
    
    test_query = "makine öğrenmesi"
    
    try:
        articles = search_and_process_articles(test_query, page=1, limit=2)
        
        if not articles:
            print("❌ Sonuç bulunamadı")
            return False
        
        if len(articles) == 1 and "error" in articles[0]:
            print(f"❌ Hata: {articles[0]['error']}")
            return False
        
        print(f"✅ {len(articles)} makale bulundu ve işlendi!")
        
        for i, article in enumerate(articles, 1):
            print(f"\n📄 Makale {i}:")
            print(f"   Başlık: {article.get('title', 'N/A')[:80]}...")
            print(f"   Yıl: {article.get('year', 'N/A')}")
            
            authors = article.get('authors', [])
            if authors:
                author_count = len(authors)
                print(f"   Yazar sayısı: {author_count}")
        
        return True
        
    except Exception as e:
        print(f"❌ Test sırasında hata: {str(e)}")
        return False

async def main():
    """Ana test fonksiyonu."""
    print("🚀 TR Dizin MCP Server Test Başlıyor...\n")
    
    # Test 1: Temel arama fonksiyonu
    test1_result = await test_search_function()
    
    # Test 2: Birleşik fonksiyon
    test2_result = await test_combined_function()
    
    # Sonuçları özetle
    print("\n" + "="*50)
    print("📋 TEST SONUÇLARI:")
    print(f"   Temel arama fonksiyonu: {'✅ BAŞARILI' if test1_result else '❌ BAŞARISIZ'}")
    print(f"   Birleşik fonksiyon: {'✅ BAŞARILI' if test2_result else '❌ BAŞARISIZ'}")
    
    if test1_result and test2_result:
        print("\n🎉 Tüm testler başarılı! TR Dizin MCP server hazır.")
        return True
    else:
        print("\n⚠️  Bazı testler başarısız. Lütfen hataları kontrol edin.")
        return False

if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
