# 🔬 TR Dizin MCP Server

<div align="center">

![Python](https://img.shields.io/badge/python-3.11+-blue.svg)
![MCP](https://img.shields.io/badge/MCP-Compatible-green.svg)
![Docker](https://img.shields.io/badge/docker-ready-blue.svg)
![Smithery](https://img.shields.io/badge/Smithery-Deploy%20Ready-orange.svg)

**TR Dizin akademik makale arama MCP serveri**

*Türkiye'nin ulusal akademik veri tabanı TR Dizin'de makale arama yapın!*

[🎯 Quick Start](#-quick-start) • [📦 Features](#-features) • [🚀 Deploy](#-deploy) • [🛠️ Tools](#️-tools)

</div>

---

## ✨ Features

- 🔬 **TR Dizin Integration** - Türkiye'nin ulusal akademik veri tabanına doğrudan erişim
- 📚 **Academic Search** - Konu, yazar ve anahtar kelime bazında makale arama
- 🎯 **5 Makale Limit** - En alakalı 5 makaleyi getirir
- 🐍 **Modern Python** - Python 3.11+ ve FastMCP ile geliştirildi
- 🐳 **Docker Ready** - Konteyner tabanlı kolay deployment
- ⚡ **Fast API** - Hızlı ve güvenilir TR Dizin API entegrasyonu
- 📊 **Structured Data** - JSON formatında düzenli makale verileri

## 🎯 Quick Start

### 1. Use This Template

Click the **"Use this template"** button at the top of this repository to create your own MCP server.

### 2. Clone & Setup

```bash
git clone https://github.com/yourusername/your-mcp-server.git
cd your-mcp-server
pip install -r requirements.txt
```

### 3. Run Locally

```bash
python server.py
```

### 4. Test Your Tools

```bash
# Your MCP server is now running and ready to accept connections!
```

## 📦 What's Included

```
mcp-template/
├── 🐍 app.py           # Your tool implementations
├── 🚀 server.py        # MCP server configuration
├── 📋 requirements.txt # Python dependencies
├── 🐳 Dockerfile       # Container configuration
├── ⚙️ smithery.yaml    # Smithery deployment config
└── 📖 README.md        # This beautiful documentation
```

## 🛠️ Available Tools

### 1. search_articles

TR Dizin veritabanında makale arar ve en alakalı 5 makaleyi döndürür.

```python
# Kullanım örnekleri
search_articles("yapay zeka")
search_articles("makine öğrenmesi")
search_articles("covid-19")
search_articles("Ahmet Yılmaz")  # Yazar adı
```

**Parametre:**
- `query` (str): Aranacak makale konusu, yazar adı veya anahtar kelime

**Döndürür:**
- JSON formatında makale listesi
- Her makale için: başlık, yazarlar, yıl, özet, DOI, URL, dergi, anahtar kelimeler

### 2. get_article_info

TR Dizin MCP server hakkında bilgi verir.

```python
get_article_info()
```

**Döndürür:**
- Server özellikleri
- Kullanım örnekleri
- API endpoint bilgileri

## 📊 API Details

- **Endpoint**: `https://search.trdizin.gov.tr/api/defaultSearch/publication/`
- **Method**: GET
- **Parameters**:
  - `q`: Arama terimi (kullanıcı girişi)
  - `order`: relevance-DESC (sabit)
  - `page`: 1 (sabit)
  - `limit`: 5 (sabit)

## 🔍 Search Examples

- **Konu arama**: "yapay zeka", "makine öğrenmesi", "blockchain"
- **Yazar arama**: "Ahmet Yılmaz", "Fatma Demir"
- **Anahtar kelime**: "covid-19", "eğitim", "sağlık"

## 🚀 Deploy

### Smithery Deployment

This template is **Smithery-ready**! The `smithery.yaml` configuration is already set up:

1. Push your customized code to GitHub
2. Connect your repository to Smithery
3. Deploy with one click! 🎉

### Docker Deployment

```bash
# Build the container
docker build -t my-mcp-server .

# Run the container
docker run -p 8000:8000 my-mcp-server
```

### Manual Deployment

Deploy to any platform that supports Python applications:

```bash
pip install -r requirements.txt
python server.py
```

## 🔧 Configuration

### Environment Variables

Customize your MCP server behavior:

```bash
export MCP_SERVER_NAME="my-awesome-mcp"
export LOG_LEVEL="INFO"
```

### Dependencies

Add your required packages to `requirements.txt`:

```
requests>=2.28.0
mcp
your-additional-package>=1.0.0
```

## 📚 Examples

### HTTP API Tool

```python
def fetchData(url: str) -> dict:
    """Fetch data from an API endpoint."""
    response = requests.get(url)
    return response.json()

@mcp.tool()
async def fetch_api_data(url: str) -> str:
    """Fetch and return data from a URL."""
    data = fetchData(url)
    return json.dumps(data, indent=2)
```

### File Processing Tool

```python
def processFile(content: str) -> str:
    """Process file content."""
    # Your processing logic
    return content.upper()

@mcp.tool()
async def process_text(text: str) -> str:
    """Process and transform text content."""
    return processFile(text)
```

## 🤝 Contributing

Found a bug or have a feature request? 

1. 🍴 Fork the repository
2. 🌱 Create a feature branch
3. 💻 Make your changes
4. 🧪 Test thoroughly
5. 📝 Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🌟 Show Your Support

If this template helped you build something awesome, please consider:

- ⭐ **Starring this repository** - it makes me happy! 😊
- 🐦 **Sharing it** with other developers
- 🛠️ **Contributing** improvements back to the community

---

<div align="center">

**Made with ❤️ by [Alperen Koçyiğit](https://github.com/alperenkocyigit)**

*Building the future of AI tool integration, one MCP server at a time* 🚀

[![GitHub](https://img.shields.io/badge/GitHub-alperenkocyigit-black?style=flat&logo=github)](https://github.com/alperenkocyigit)

</div>
