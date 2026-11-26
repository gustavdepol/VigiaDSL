# Demonstração de 15 minutos

**0 a 3 min** — Abra Regras, escolha uma regra de latência e mostre como o lexer identifica os tokens, o parser monta a AST, a análise semântica valida a declaração e o interpretador compara a regra com a medição simulada.

**3 a 5 min** — Abra o Servidor de arquivos em Equipamentos. Em Configurar alertas, edite Latência para acima de 50 ms por 5 segundos. Ative o aviso sonoro da regra e o som da aba. Confira o resumo e a linha gerada na VigiaDSL. Mostre o limite de 150 ms em outra máquina.

**5 a 7 min** — No Laboratório, aplique latência de 85 ms nas duas máquinas por 120 segundos. Apenas a máquina com limite de 50 ms deve abrir a ocorrência de latência. Mostre o tempo de persistência e a captura da abertura.

**7 a 10 min** — Inicie o procedimento da ocorrência. Consulte a conexão, leia o resultado e escolha a resposta correspondente ao atraso. Mostre a etapa seguinte. A resposta sobre falha de nome levaria à consulta DNS. Pause, retome e mostre o histórico preservado.

**10 a 12 min** — Retire a degradação simulada, compare antes/depois e aguarde a recuperação pelo intervalo exigido. Consulte a validação funcional e a condição da regra. Registre o resultado. O botão Outra solução também permite documentar uma hipótese alternativa e suas evidências.

**12 a 14 min** — Mostre a criação de rascunhos, a revisão para publicação e o feedback do operador. Explique os motivos das recomendações e mostre um relatório com o histórico.

**14 a 15 min** — Diferencie o que é simulado (equipamentos e medições) do que é executado (linguagem, persistência, transições de diagnóstico e regras temporais). Explique que um pico curto não abre alerta e mudar um limite não comprova recuperação.
