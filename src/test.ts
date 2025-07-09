#!/usr/bin/env ts-node

/**
 * TR Dizin MCP Server Test Script - TypeScript versiyonu
 */

import { searchAndProcessArticles, searchTRDizin, processArticles } from './tr-dizin-api';
import { ProcessedArticle } from './types';

async function testSearchFunction(): Promise<boolean> {
  console.log('🔍 TR Dizin arama fonksiyonu test ediliyor...');
  
  const testQuery = 'yapay zeka';
  
  try {
    console.log(`📡 '${testQuery}' için TR Dizin API'sine istek gönderiliyor...`);
    const apiResponse = await searchTRDizin(testQuery, 1, 3);
    
    if ('error' in apiResponse) {
      console.log(`❌ API Hatası: ${apiResponse.error}`);
      return false;
    }
    
    console.log('✅ API isteği başarılı!');
    console.log(`📊 Toplam sonuç sayısı: ${apiResponse.hits?.total?.value || 0}`);
    
    console.log('🔄 Veriler işleniyor...');
    const processedArticles = processArticles(apiResponse);
    
    if (processedArticles.length === 0) {
      console.log('❌ İşlenmiş makale bulunamadı');
      return false;
    }
    
    console.log(`✅ ${processedArticles.length} makale başarıyla işlendi!`);
    
    // İlk makaleyi göster
    if (processedArticles.length > 0) {
      const firstArticle = processedArticles[0];
      console.log('\n📄 İlk makale örneği:');
      console.log(`   Başlık: ${firstArticle.title}`);
      console.log(`   Yıl: ${firstArticle.year || 'N/A'}`);
      console.log(`   Yazar sayısı: ${firstArticle.authors?.length || 0}`);
    }
    
    return true;
    
  } catch (error) {
    console.log(`❌ Test sırasında hata: ${error}`);
    return false;
  }
}

async function testCombinedFunction(): Promise<boolean> {
  console.log('\n🔗 Birleşik arama fonksiyonu test ediliyor...');
  
  const testQuery = 'makine öğrenmesi';
  
  try {
    const articles = await searchAndProcessArticles(testQuery, 1, 2);
    
    if (articles.length === 0) {
      console.log('❌ Sonuç bulunamadı');
      return false;
    }
    
    console.log(`✅ ${articles.length} makale bulundu ve işlendi!`);
    
    articles.forEach((article: ProcessedArticle, index: number) => {
      console.log(`\n📄 Makale ${index + 1}:`);
      console.log(`   Başlık: ${article.title.substring(0, 80)}...`);
      console.log(`   Yıl: ${article.year || 'N/A'}`);
      
      if (article.authors && article.authors.length > 0) {
        console.log(`   Yazar sayısı: ${article.authors.length}`);
      }
    });
    
    return true;
    
  } catch (error) {
    console.log(`❌ Test sırasında hata: ${error}`);
    return false;
  }
}

async function main(): Promise<void> {
  console.log('🚀 TR Dizin MCP Server TypeScript Test Başlıyor...\n');
  
  // Test 1: Temel arama fonksiyonu
  const test1Result = await testSearchFunction();
  
  // Test 2: Birleşik fonksiyon
  const test2Result = await testCombinedFunction();
  
  // Sonuçları özetle
  console.log('\n' + '='.repeat(50));
  console.log('📋 TEST SONUÇLARI:');
  console.log(`   Temel arama fonksiyonu: ${test1Result ? '✅ BAŞARILI' : '❌ BAŞARISIZ'}`);
  console.log(`   Birleşik fonksiyon: ${test2Result ? '✅ BAŞARILI' : '❌ BAŞARISIZ'}`);
  
  if (test1Result && test2Result) {
    console.log('\n🎉 Tüm testler başarılı! TR Dizin TypeScript MCP server hazır.');
  } else {
    console.log('\n⚠️  Bazı testler başarısız. Lütfen hataları kontrol edin.');
    process.exit(1);
  }
}

if (require.main === module) {
  main().catch((error) => {
    console.error('Test sırasında beklenmeyen hata:', error);
    process.exit(1);
  });
}
