/**
 * TR Dizin API entegrasyonu - TypeScript versiyonu
 */

import axios from 'axios';
import { 
  TRDizinSearchResponse, 
  ProcessedArticle, 
  APIResponse, 
  TRDizinHit,
  TRDizinAuthor,
  TRDizinAbstract 
} from './types';

/**
 * TR Dizin API'sinden makale arama fonksiyonu
 */
export async function searchTRDizin(
  query: string, 
  page: number = 1, 
  limit: number = 5
): Promise<APIResponse> {
  try {
    const url = 'https://search.trdizin.gov.tr/api/defaultSearch/publication/';
    const params = {
      q: query,
      order: 'relevance-DESC',
      page: page.toString(),
      limit: limit.toString()
    };

    const response = await axios.get<TRDizinSearchResponse>(url, {
      params,
      timeout: 30000,
      headers: {
        'User-Agent': 'TR-Dizin-MCP-Server/1.0'
      }
    });

    return response.data;

  } catch (error: any) {
    if (error.response) {
      // Axios response error
      return { error: `API hatası: ${error.response.status} - ${error.response.statusText}` };
    } else if (error.request) {
      // Axios request error
      return { error: 'API isteği başarısız: Sunucuya ulaşılamıyor' };
    } else if (error.message) {
      // General error with message
      return { error: `İstek hatası: ${error.message}` };
    } else {
      // Unknown error
      return { error: `Beklenmeyen hata: ${String(error)}` };
    }
  }
}

/**
 * TR Dizin API'sinden gelen veriyi işleyip düzenli format haline getirir
 */
export function processArticles(apiResponse: APIResponse): ProcessedArticle[] {
  // Hata kontrolü
  if ('error' in apiResponse) {
    console.error('API Error:', apiResponse.error);
    return [];
  }

  try {
    const hits = apiResponse.hits?.hits || [];

    if (hits.length === 0) {
      return [];
    }

    const processedArticles: ProcessedArticle[] = [];

    for (const item of hits) {
      const source = item._source || {};

      // Abstract'tan title alma
      const abstracts: TRDizinAbstract[] = source.abstracts || [];
      const titleFromAbstract = abstracts.length > 0 ? abstracts[0].title || '' : '';

      // Title belirleme
      const title = titleFromAbstract || source.title || 'İsim bulunamadı';

      // Yıl belirleme
      const year = String(source.year || source.publicationYear || '');

      // Authors array'ini düzelt
      const authors: TRDizinAuthor[] = Array.isArray(source.authors) ? source.authors : [];

      const article: ProcessedArticle = {
        title,
        authors,
        year,
        abstract: source.abstract || '',
        doi: source.doi || '',
        url: source.url || '',
        journal: source.journal || '',
        keywords: Array.isArray(source.keywords) ? source.keywords : []
      };

      processedArticles.push(article);
    }

    return processedArticles;

  } catch (error) {
    console.error('Veri işleme hatası:', error);
    return [];
  }
}

/**
 * TR Dizin'de makale arayıp işlenmiş sonuçları döndürür
 */
export async function searchAndProcessArticles(
  query: string, 
  page: number = 1, 
  limit: number = 5
): Promise<ProcessedArticle[]> {
  // API'den veri çek
  const apiResponse = await searchTRDizin(query, page, limit);

  // Veriyi işle
  const processedArticles = processArticles(apiResponse);

  return processedArticles;
}
