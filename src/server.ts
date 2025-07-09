#!/usr/bin/env node

/**
 * TR Dizin MCP Server - TypeScript versiyonu
 * Türkiye'nin ulusal akademik veri tabanı TR Dizin'de makale arama MCP serveri
 */

import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from '@modelcontextprotocol/sdk/types.js';
import { z } from 'zod';
import { searchAndProcessArticles } from './tr-dizin-api.js';
import { ProcessedArticle, SearchResult, TRDizinAuthor } from './types.js';

// Zod şemaları
const SearchArticlesSchema = z.object({
  query: z.string().describe('Arama yapılacak kelime veya kelime grubu'),
  page: z.number().int().min(1).default(1).describe('Sayfa numarası'),
  limit: z.number().int().min(1).max(20).default(5).describe('Döndürülecek maksimum sonuç sayısı')
});

const GetArticleSummarySchema = z.object({
  query: z.string().describe('Arama yapılacak konu'),
  max_articles: z.number().int().min(1).max(10).default(3).describe('Özetlenecek maksimum makale sayısı')
});

const SearchByAuthorSchema = z.object({
  author_name: z.string().describe('Yazar adı'),
  limit: z.number().int().min(1).max(20).default(5).describe('Döndürülecek maksimum sonuç sayısı')
});

class TRDizinMCPServer {
  private server: Server;

  constructor() {
    this.server = new Server(
      {
        name: 'tr-dizin-mcp',
        version: '1.0.0',
      },
      {
        capabilities: {
          tools: {},
        },
      }
    );

    this.setupToolHandlers();
    this.setupErrorHandling();
  }

  private setupErrorHandling(): void {
    this.server.onerror = (error) => {
      console.error('[MCP Error]', error);
    };

    process.on('SIGINT', async () => {
      await this.server.close();
      process.exit(0);
    });
  }

  private setupToolHandlers(): void {
    // List tools handler
    this.server.setRequestHandler(ListToolsRequestSchema, async () => {
      return {
        tools: [
          {
            name: 'search_articles',
            description: 'TR Dizin veritabanında makale arar ve sonuçları döndürür',
            inputSchema: {
              type: 'object',
              properties: {
                query: {
                  type: 'string',
                  description: 'Arama yapılacak kelime veya kelime grubu'
                },
                page: {
                  type: 'number',
                  description: 'Sayfa numarası (varsayılan: 1)',
                  default: 1,
                  minimum: 1
                },
                limit: {
                  type: 'number',
                  description: 'Döndürülecek maksimum sonuç sayısı (varsayılan: 5, maksimum: 20)',
                  default: 5,
                  minimum: 1,
                  maximum: 20
                }
              },
              required: ['query']
            }
          },
          {
            name: 'get_article_summary',
            description: 'Belirli bir konuda makale arayıp özet bilgiler döndürür',
            inputSchema: {
              type: 'object',
              properties: {
                query: {
                  type: 'string',
                  description: 'Arama yapılacak konu'
                },
                max_articles: {
                  type: 'number',
                  description: 'Özetlenecek maksimum makale sayısı (varsayılan: 3)',
                  default: 3,
                  minimum: 1,
                  maximum: 10
                }
              },
              required: ['query']
            }
          },
          {
            name: 'search_by_author',
            description: 'Belirli bir yazarın makalelerini arar',
            inputSchema: {
              type: 'object',
              properties: {
                author_name: {
                  type: 'string',
                  description: 'Yazar adı'
                },
                limit: {
                  type: 'number',
                  description: 'Döndürülecek maksimum sonuç sayısı (varsayılan: 5)',
                  default: 5,
                  minimum: 1,
                  maximum: 20
                }
              },
              required: ['author_name']
            }
          }
        ]
      };
    });

    // Call tool handler
    this.server.setRequestHandler(CallToolRequestSchema, async (request) => {
      const { name, arguments: args } = request.params;

      try {
        switch (name) {
          case 'search_articles':
            return await this.handleSearchArticles(args);
          case 'get_article_summary':
            return await this.handleGetArticleSummary(args);
          case 'search_by_author':
            return await this.handleSearchByAuthor(args);
          default:
            throw new Error(`Bilinmeyen tool: ${name}`);
        }
      } catch (error) {
        const errorMessage = error instanceof Error ? error.message : String(error);
        return {
          content: [
            {
              type: 'text',
              text: JSON.stringify({
                success: false,
                error: `Tool çalıştırılırken hata oluştu: ${errorMessage}`
              }, null, 2)
            }
          ]
        };
      }
    });
  }

  private async handleSearchArticles(args: any) {
    const { query, page = 1, limit = 5 } = SearchArticlesSchema.parse(args);

    try {
      const articles = await searchAndProcessArticles(query, page, Math.min(limit, 20));

      const result: SearchResult = {
        success: true,
        query,
        page,
        limit,
        total_results: articles.length,
        articles
      };

      return {
        content: [
          {
            type: 'text',
            text: JSON.stringify(result, null, 2)
          }
        ]
      };
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : String(error);
      return {
        content: [
          {
            type: 'text',
            text: JSON.stringify({
              success: false,
              error: `Arama sırasında hata oluştu: ${errorMessage}`
            }, null, 2)
          }
        ]
      };
    }
  }

  private async handleGetArticleSummary(args: any) {
    const { query, max_articles = 3 } = GetArticleSummarySchema.parse(args);

    try {
      const articles = await searchAndProcessArticles(query, 1, max_articles);

      if (articles.length === 0) {
        return {
          content: [
            {
              type: 'text',
              text: `'${query}' konusunda makale bulunamadı.`
            }
          ]
        };
      }

      let summary = `'${query}' konusunda ${articles.length} makale bulundu:\n\n`;

      articles.forEach((article, index) => {
        summary += `${index + 1}. ${article.title}\n`;

        if (article.authors && article.authors.length > 0) {
          const authorNames = article.authors
            .map((author: TRDizinAuthor) => author.name || '')
            .filter(name => name.length > 0);
          if (authorNames.length > 0) {
            summary += `   Yazarlar: ${authorNames.join(', ')}\n`;
          }
        }

        if (article.year) {
          summary += `   Yıl: ${article.year}\n`;
        }

        if (article.abstract) {
          const shortAbstract = article.abstract.length > 200 
            ? article.abstract.substring(0, 200) + '...' 
            : article.abstract;
          summary += `   Özet: ${shortAbstract}\n`;
        }

        summary += '\n';
      });

      return {
        content: [
          {
            type: 'text',
            text: summary
          }
        ]
      };
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : String(error);
      return {
        content: [
          {
            type: 'text',
            text: `Özet oluşturulurken hata oluştu: ${errorMessage}`
          }
        ]
      };
    }
  }

  private async handleSearchByAuthor(args: any) {
    const { author_name, limit = 5 } = SearchByAuthorSchema.parse(args);

    try {
      // Yazar adını sorgu olarak kullan
      const query = `author:${author_name}`;
      const articles = await searchAndProcessArticles(query, 1, limit);

      const result: SearchResult = {
        success: true,
        query: author_name,
        total_results: articles.length,
        articles
      };

      return {
        content: [
          {
            type: 'text',
            text: JSON.stringify(result, null, 2)
          }
        ]
      };
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : String(error);
      return {
        content: [
          {
            type: 'text',
            text: JSON.stringify({
              success: false,
              error: `Yazar arama sırasında hata oluştu: ${errorMessage}`
            }, null, 2)
          }
        ]
      };
    }
  }

  async run(): Promise<void> {
    const transport = new StdioServerTransport();
    await this.server.connect(transport);
    console.error('TR Dizin MCP Server başlatıldı');
  }
}

// Server'ı başlat
async function main() {
  const server = new TRDizinMCPServer();
  await server.run();
}

if (require.main === module) {
  main().catch((error) => {
    console.error('Server başlatılırken hata oluştu:', error);
    process.exit(1);
  });
}
