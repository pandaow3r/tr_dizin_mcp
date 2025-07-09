/**
 * TR Dizin API ve MCP Server için TypeScript tip tanımları
 */

export interface TRDizinAuthor {
  name?: string;
  id?: string;
  affiliation?: string;
}

export interface TRDizinAbstract {
  title?: string;
  content?: string;
  language?: string;
}

export interface TRDizinArticleSource {
  title?: string;
  authors?: TRDizinAuthor[];
  year?: string | number;
  publicationYear?: string | number;
  abstract?: string;
  abstracts?: TRDizinAbstract[];
  doi?: string;
  url?: string;
  journal?: string;
  keywords?: string[];
}

export interface TRDizinHit {
  _source: TRDizinArticleSource;
  _id?: string;
  _score?: number;
}

export interface TRDizinSearchResponse {
  hits: {
    hits: TRDizinHit[];
    total: {
      value: number;
      relation: string;
    };
  };
  took?: number;
  timed_out?: boolean;
}

export interface ProcessedArticle {
  title: string;
  authors: TRDizinAuthor[];
  year: string;
  abstract: string;
  doi: string;
  url: string;
  journal: string;
  keywords: string[];
}

export interface SearchResult {
  success: boolean;
  query?: string;
  page?: number;
  limit?: number;
  total_results?: number;
  articles?: ProcessedArticle[];
  error?: string;
}

export interface APIError {
  error: string;
}

export type APIResponse = TRDizinSearchResponse | APIError;
