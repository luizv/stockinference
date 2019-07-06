# stockinference

## Run

**- Instalar Redis:**
 $ brew install redis

**- Rodar o Redis:**
 $  redis-server /usr/local/etc/redis.conf

**- Rodar os scripts:**
  - Rodar o script StockInference.py (Só funcionará com o Redis rodando. Também só permite uma única única instância desse script rodando por vez.)
  - Rodar o script StockFeed.py (só funcionará com o StockInference.py rodando)
