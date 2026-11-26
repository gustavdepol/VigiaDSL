# Manual da VigiaDSL 2

## Exemplo

```text
equipamento servidor { ip: 192.168.56.10 }
vigiar servidor { cpu memoria disco latencia ping }

quando servidor.cpu > 85 por 5 segundos recuperar 4 segundos nivel alerta {
    avisar "CPU elevada"
}
quando servidor.latencia > 150 por 5 segundos recuperar 3 segundos nivel atencao {
    avisar "Resposta lenta"
}
quando servidor.ping = offline por 3 segundos recuperar 4 segundos nivel critico {
    avisar "Sem resposta"
}
```

`por`, `recuperar` e `nivel` são opcionais, nessa ordem. Padrões: persistência 0s, recuperação 4s e nível `atencao`. A sintaxe original permanece válida. Cada regra tem uma condição e um aviso; não há `e`, `ou`, comentários ou ponto e vírgula.

## Gramática EBNF

```text
programa = { comando } ;
comando = equipamento | vigilancia | regra ;
equipamento = "equipamento", NOME, "{", "ip", ":", ENDERECO, "}" ;
vigilancia = "vigiar", NOME, "{", metrica, { metrica }, "}" ;
regra = "quando", condicao,
        [ "por", NUMERO, "segundos" ],
        [ "recuperar", NUMERO, "segundos" ],
        [ "nivel", gravidade ],
        "{", "avisar", TEXTO, "}" ;
condicao = NOME, ".", metrica, operador, valor ;
metrica = "cpu" | "memoria" | "disco" | "latencia" | "ping" ;
operador = ">" | "<" | ">=" | "<=" | "=" | "!=" ;
valor = NUMERO | "online" | "offline" ;
gravidade = "atencao" | "alerta" | "critico" ;
```

NOME inicia com letra e continua com letras/números. Não aceita `_`. Palavras reservadas não são nomes. NUMERO é inteiro ou decimal não negativo, com ponto decimal. ENDERECO tem quatro grupos de dígitos separados por pontos e depois é validado como IPv4. TEXTO usa aspas duplas, escapes JSON e não permite quebra literal de linha dentro das aspas. Espaços e quebras fora do texto são ignorados.

## Análise semântica

- Equipamento deve ser declarado antes de `vigiar` e `quando`.
- Nomes de equipamentos não podem se repetir.
- Métrica deve ser vigiada antes da condição.
- CPU, memória e disco: número entre 0 e 100.
- Latência: número entre 0 e 60000 ms.
- Ping: somente `online`/`offline`, com `=`/`!=`.
- Tempos: número entre 0 e 3600 segundos; inclusive decimais.
- IPv4 precisa ser válido.
- Repetir um bloco vigiar soma as métricas. Regras semanticamente idênticas são deduplicadas no laboratório.

## Tempo e dados ausentes

O motor amostra a cada aproximadamente 0,5 segundo. A primeira amostra verdadeira inicia a contagem. Uma amostra falsa reinicia a persistência. O alerta abre quando o tempo decorrido desde a primeira amostra verdadeira alcança `por`.

Após abrir, amostras falsas consecutivas iniciam a recuperação. Uma amostra verdadeira reinicia essa recuperação. O encerramento ocorre após `recuperar` segundos estáveis.

Quando offline, métricas numéricas ficam desconhecidas: seus contadores reiniciam, mas seus alertas ativos não são considerados resolvidos. A regra de ping continua funcionando. Lacunas de atualização maiores que 3s e reinícios interrompem a continuidade observada; o programa não presume que monitorou o intervalo ausente.

O intervalo real é medido com relógio monotônico e os registros usam horário de calendário. Os limites possuem precisão de amostragem, não de tempo real rígido.

## Aplicação e versões

Validar produz tokens, AST e símbolos sem alterar o monitoramento. Aplicar só ocorre após validação completa. Erro no editor preserva a última configuração válida.

Ao aplicar código diferente, uma nova versão é armazenada. Ocorrências ativas da versão anterior são encerradas como `Regras substituídas`, sem registrar recuperação. Contadores reiniciam. Equipamentos que continuam declarados preservam seus perfis, valores e cargas; novos nomes recebem perfil genérico. Remover uma declaração remove o equipamento do painel, mas preserva os incidentes históricos.

Se código idêntico for reaplicado, não cria outra versão. Nomes disponíveis no seletor de estresse vêm das declarações da DSL. Limite do laboratório: 24 equipamentos e 200 regras distintas.

## Extensão da versão 3 — DNS e serviço

As métricas `dns` e `servico` usam o mesmo tipo de estado de `ping`: `online` ou `offline`, somente operadores `=` e `!=`. Devem aparecer em `vigiar` antes de uma regra. Lexer, semântica e validação dos dados da CLI reconhecem ambas. O parser já usa a produção genérica METRICA.

```text
equipamento estacao { ip: 192.168.56.20 }
vigiar estacao { cpu memoria disco latencia ping dns servico }
quando estacao.dns = offline por 3 segundos recuperar 4 segundos nivel alerta {
    avisar "Falha de resolução DNS"
}
quando estacao.servico = offline por 3 segundos recuperar 4 segundos nivel alerta {
    avisar "Serviço principal parado"
}
```

`dns` indica a resolução virtual de nome; `servico` indica o estado de AppService, o serviço principal da aplicação simulada. Não é uma seleção genérica de serviços por nome. Quando o equipamento não responde, essas duas métricas também ficam desconhecidas; a falha de ping tem regra própria.

Produção atual: `metrica = cpu | memoria | disco | latencia | ping | dns | servico`. O restante da gramática temporal permanece igual. Identificadores que antes usavam dns ou servico como nome de equipamento precisam ser renomeados, pois agora são palavras reservadas.
