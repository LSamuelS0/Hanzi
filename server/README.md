# Servidor do Professor Virtual (Cloudflare Worker)

O servidor guarda a chave do Gemini fora do app, aceita só usuários logados no Firebase e devolve a fala do professor. Funciona no plano gratuito do Cloudflare e na camada gratuita do Gemini. Nenhum dos dois pede cartão.

## 1. Criar a chave do Gemini

1. Abra https://aistudio.google.com e entre com a sua conta Google.
2. Clique em **Get API key** e depois em **Create API key**.
3. Copie a chave. Não mande essa chave para ninguém e não a cole no app.

## 2. Criar o Worker no Cloudflare

1. Crie uma conta grátis em https://dash.cloudflare.com/sign-up.
2. No menu, abra **Workers & Pages** e clique em **Create** → **Create Worker**. Escolha um nome, por exemplo `hanzi-professor`, e clique em **Deploy**.
3. Clique em **Edit code**. Apague tudo o que estiver lá, cole o conteúdo de `worker.js` e clique em **Deploy**.
4. Volte ao Worker e abra **Settings** → **Variables and Secrets** → **Add**:
   - em **Type**, escolha **Secret**;
   - em **Name**, digite `GEMINI_API_KEY`;
   - em **Value**, cole a chave do passo 1;
   - clique em **Deploy**.
5. Copie o endereço do Worker. Ele tem o formato `https://hanzi-professor.SEU-USUARIO.workers.dev`.
6. Abra esse endereço no navegador. Ele deve mostrar `"configured":true`.

Depois, envie o endereço do passo 5 para eu ligar a conversa no app. Esse endereço não é segredo.

## Variáveis opcionais

| Nome | Padrão | Para quê |
|---|---|---|
| `GEMINI_MODEL` | `gemini-2.5-flash` | Modelo principal |
| `GEMINI_FALLBACK` | `gemini-2.5-flash-lite` | Usado quando o principal estiver no limite |
| `DAILY_LIMIT` | `200` | Chamadas por usuário por dia (aproximado) |
| `ALLOWED_ORIGINS` | `https://lsamuels0.github.io` | Sites que podem chamar o servidor |
| `FIREBASE_PROJECT` | `caderno-hanzi` | Projeto do login |

## Segurança

- A chave só existe como segredo no Cloudflare.
- Cada pedido precisa do token de login do Firebase. O servidor confere a assinatura, o projeto e a validade do token.
- Os pedidos só são aceitos vindos do site do app.
- O áudio pode ter no máximo cerca de 30 segundos. Ele não é guardado em lugar nenhum.

## Privacidade

Na camada gratuita, o Google pode usar o conteúdo enviado ao Gemini para melhorar os produtos dele. Não fale dados sensíveis na conversa. Se um dia quiser evitar isso, basta ativar a cobrança no Google AI Studio, sem mudar o código.
