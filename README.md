# Vespa WebSocket Helper Server

Servidor Flask com interface web para controlar a [Placa Vespa](https://www.robocore.net/loja/produtos/placa-vespa.html) via WebSocket temporário, compatível com o joystick oficial.

## Requisitos

- Python 3.10+
- Placa Vespa conectada na mesma rede (ou no modo AP em `192.168.4.1`)

## Instalação

```bash
git clone <url-do-repositorio>
cd server

python -m venv venv
source venv/bin/activate   # Linux/macOS
# venv\Scripts\activate    # Windows

pip install -r requirements.txt
```

## Configuração

Copie o arquivo de exemplo e ajuste se necessário:

```bash
cp .env.example .env
```

| Variável   | Padrão                  | Descrição                          |
|------------|-------------------------|------------------------------------|
| `VESPA_WS` | `ws://192.168.4.1/ws`   | URL WebSocket da Vespa             |
| `PORT`     | `5000`                  | Porta do servidor webui           |

## Execução

```bash
python server.py
```

Acesse no navegador: **http://localhost:5000**

## Funcionalidades

- **Movimento:** frente, ré, esquerda, direita e parar
- **Servos:** controle dos 4 servos (0–180°)
- **Logs:** histórico em tempo real na interface

## API

| Método | Rota                    | Descrição              |
|--------|-------------------------|------------------------|
| GET    | `/`                     | Interface web          |
| POST   | `/cmd/<comando>`        | `frente`, `tras`, `esquerda`, `direita`, `parar` |
| POST   | `/servo/<id>/<angulo>`  | Move servo (1–4)       |
| GET    | `/logs`                 | Retorna logs recentes  |

## Troubleshooting

**Vespa não responde**
- Confirme que a Vespa está ligada e no modo correto (AP ou Wi-Fi)
- Verifique se `VESPA_WS` aponta para o IP correto
- Conecte o PC na rede da Vespa (`192.168.4.1` no modo AP)

**Erro de conexão WebSocket**
- A Vespa precisa estar acessível na rede
- Firewall pode bloquear conexões — teste desabilitar temporariamente

## Licença

Projeto de uso livre para fins educacionais.
