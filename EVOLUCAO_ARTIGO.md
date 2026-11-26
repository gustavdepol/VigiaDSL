# Orientação para atualizar o artigo original

O artigo anexado descrevia uma proposta ainda não implementada. Esta versão já possui interpretador e aplicação. Não entregue o texto antigo como se descrevesse o estado atual.

## Mudanças de escopo

| Primeira proposta | Versão 2 |
|---|---|
| CPU, memória, disco e ping | Acrescenta latência numérica em ms; ping continua estado |
| Execução sobre valores fixos | Laboratório contínuo com estresse e perfis simulados |
| Uma condição e um aviso | Preservado; acrescenta persistência, recuperação e gravidade opcionais |
| Sem painel ou histórico | Interface web local, gráficos e SQLite |
| Aviso no terminal | Ocorrência com atendimento, resolução e histórico |
| Sem base de soluções | Procedimentos e reaproveitamento de soluções com feedback |

## O que revisar em cada seção

**Resumo e introdução:** trocar a descrição de proposta futura por implementação de um interpretador com laboratório simulado; explicitar limites e objetivos novos.

**Fundamentação:** manter referências científicas e conceitos da disciplina; distinguir linguagem formal, simulação e recuperação de soluções por histórico. Não chamar essa ordenação de treinamento de IA.

**Metodologia:** usar a EBNF do manual, explicar lexer por expressões regulares, parser descendente manual, AST, símbolos, verificação de tipos e interpretação temporal. Descrever API local, motor único e armazenamento SQLite.

**Resultados:** usar somente testes e demonstrações efetivamente executados. Consultar RESULTADOS.md. Acrescentar capturas da execução do grupo, casos válidos/inválidos e comparação entre esperado e observado. Não inventar avaliação de usabilidade, estatísticas de desempenho ou testes em Windows que ainda não foram feitos.

**Conclusão:** o interpretador e o laboratório foram implementados; coleta em computadores reais e avaliação com usuários externos permanecem possíveis evoluções.

**Entrega:** o roteiro exige código, README e manual no GitHub, ao menos quatro artigos científicos (um sobre DSL) e template IEEE Conference. Esta entrega fornece código e documentação local. Publicação no GitHub e montagem final do artigo não foram realizadas automaticamente.

## Separação de responsabilidades

A DSL controla declarações, métricas e condições de detecção. Atendimento, procedimentos e banco de soluções são funcionalidades da aplicação que consome os resultados do interpretador. Não atribuir todas as funcionalidades da interface à gramática.
