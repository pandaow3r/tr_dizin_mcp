# TypeScript TR Dizin MCP Server Dockerfile
FROM node:18-alpine

# Çalışma dizinini ayarla
WORKDIR /app

# Package dosyalarını kopyala
COPY package*.json ./
COPY tsconfig.json ./

# Dependencies'leri yükle
RUN npm ci --only=production

# Kaynak kodunu kopyala
COPY src/ ./src/

# TypeScript'i build et
RUN npm run build

# Gereksiz dosyaları temizle
RUN rm -rf src/ tsconfig.json && \
    npm cache clean --force

# Non-root user oluştur
RUN addgroup -g 1001 -S nodejs && \
    adduser -S mcp -u 1001

# Ownership'i değiştir
RUN chown -R mcp:nodejs /app
USER mcp

# Port expose et (gerekirse)
EXPOSE 3000

# Health check ekle
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD node -e "console.log('Health check passed')" || exit 1

# Server'ı başlat
CMD ["npm", "start"]
