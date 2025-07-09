# 🔬 TR Dizin MCP Server (TypeScript)

<div align="center">

![TypeScript](https://img.shields.io/badge/TypeScript-5.0+-blue.svg)
![Node.js](https://img.shields.io/badge/Node.js-18+-green.svg)
![MCP](https://img.shields.io/badge/MCP-Compatible-green.svg)
![Docker](https://img.shields.io/badge/docker-ready-blue.svg)
![Smithery](https://img.shields.io/badge/Smithery-Deploy%20Ready-orange.svg)

**TR Dizin akademik makale arama MCP serveri - TypeScript versiyonu**

*Türkiye'nin ulusal akademik veri tabanı TR Dizin'de makale arama ve analiz yapın!*

[🎯 Quick Start](#-quick-start) • [📦 Features](#-features) • [🚀 Deploy](#-deploy) • [🛠️ Tools](#️-tools)

</div>

---

## ✨ Features

- 🔬 **TR Dizin Integration** - Türkiye'nin ulusal akademik veri tabanına doğrudan erişim
- 📚 **Academic Search** - Makale, yazar ve konu bazında gelişmiş arama
- ⚡ **TypeScript Performance** - Tip güvenliği ve yüksek performans
- 🎯 **Zero-Config Deployment** - Smithery ve diğer MCP platformları için hazır
- 🟢 **Node.js 18+** - Modern JavaScript runtime
- 🐳 **Docker Ready** - Konteyner tabanlı kolay deployment
- 📊 **Structured Data** - JSON formatında düzenli makale verileri
- 🔒 **Type Safety** - TypeScript ile tam tip güvenliği

## 🎯 Quick Start

### 1. Clone & Setup

```bash
git clone https://github.com/yourusername/tr-dizin-mcp-ts.git
cd tr-dizin-mcp-ts
npm install
```

### 2. Build

```bash
npm run build
```

### 3. Run Locally

```bash
npm start
# veya development için:
npm run dev
```

### 4. Test Your Tools

```bash
npm test
# TR Dizin TypeScript MCP server is now running!
```

## 📦 What's Included

```
tr-dizin-mcp-ts/
├── 📁 src/
│   ├── 🟦 server.ts        # MCP server ana dosyası
│   ├── 🟦 tr-dizin-api.ts  # TR Dizin API entegrasyonu
│   ├── 🟦 types.ts         # TypeScript tip tanımları
│   └── 🟦 test.ts          # Test dosyası
├── 📋 package.json         # Node.js dependencies
├── ⚙️ tsconfig.json        # TypeScript konfigürasyonu
├── 🐳 Dockerfile.ts        # TypeScript container konfigürasyonu
├── ⚙️ smithery-ts.yaml     # Smithery deployment config
└── 📖 README-TypeScript.md # Bu dokümantasyon
```

## 🛠️ Available Tools

### 1. search_articles

TR Dizin veritabanında makale arar ve detaylı sonuçları döndürür.

```typescript
// Kullanım örneği
await searchArticles({
  query: "yapay zeka",
  page: 1,
  limit: 5
});
```

**Parametreler:**
- `query` (string): Arama yapılacak kelime veya kelime grubu
- `page` (number): Sayfa numarası (varsayılan: 1)
- `limit` (number): Döndürülecek maksimum sonuç sayısı (varsayılan: 5, maksimum: 20)

### 2. get_article_summary

Belirli bir konuda makale arayıp özet bilgiler döndürür.

```typescript
// Kullanım örneği
await getArticleSummary({
  query: "makine öğrenmesi",
  max_articles: 3
});
```

**Parametreler:**
- `query` (string): Arama yapılacak konu
- `max_articles` (number): Özetlenecek maksimum makale sayısı (varsayılan: 3)

### 3. search_by_author

Belirli bir yazarın makalelerini arar.

```typescript
// Kullanım örneği
await searchByAuthor({
  author_name: "Ahmet Yılmaz",
  limit: 5
});
```

**Parametreler:**
- `author_name` (string): Yazar adı
- `limit` (number): Döndürülecek maksimum sonuç sayısı (varsayılan: 5)

## 🚀 Deploy

### Smithery Deployment (TypeScript)

Bu TypeScript versiyonu **Smithery-ready**! `smithery-ts.yaml` konfigürasyonu hazır:

1. TypeScript kodunu build edin: `npm run build`
2. Kodu GitHub'a push edin
3. Smithery'de repository'yi bağlayın
4. `smithery-ts.yaml` dosyasını kullanarak deploy edin! 🎉

### Docker Deployment (TypeScript)

```bash
# TypeScript container'ı build et
docker build -f Dockerfile.ts -t tr-dizin-mcp-ts .

# Container'ı çalıştır
docker run -p 3000:3000 tr-dizin-mcp-ts
```

### Manual Deployment

```bash
npm install
npm run build
npm start
```

## 🔧 Development

### Scripts

```bash
npm run build      # TypeScript'i compile et
npm run dev        # Development modunda çalıştır
npm test          # Testleri çalıştır
npm run clean     # Build dosyalarını temizle
```

### Environment Variables

```bash
export NODE_ENV="production"
export DEFAULT_LIMIT="5"
export TIMEOUT="30"
```

## 📊 TypeScript Advantages

- **🔒 Type Safety**: Compile-time hata kontrolü
- **⚡ Performance**: V8 engine optimizasyonları
- **🛠️ Developer Experience**: IntelliSense ve auto-completion
- **📚 Better Documentation**: Tip tanımları ile self-documenting kod
- **🔄 Refactoring**: Güvenli kod değişiklikleri

## 🤝 Python vs TypeScript

| Özellik | Python | TypeScript |
|---------|--------|------------|
| Performance | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| Type Safety | ⭐⭐ | ⭐⭐⭐⭐⭐ |
| Development Speed | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| Memory Usage | ⭐⭐⭐ | ⭐⭐⭐⭐ |
| Ecosystem | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |

## 📄 License

Bu proje MIT License altında lisanslanmıştır.

---

<div align="center">

**TypeScript ile ❤️ ile geliştirildi**

*Modern, hızlı ve güvenli MCP server deneyimi* 🚀

</div>
