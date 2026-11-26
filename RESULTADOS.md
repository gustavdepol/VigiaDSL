# Verificação da versão final

69 testes passaram em Python 3.12 no Linux. A suíte inclui linguagem, simulação, casos de correção ineficaz, recuperação sustentada, valores desconhecidos quando offline e histórico de procedimentos.

Os testes em tests/test_central.py cobrem a configuração de duas máquinas com limites diferentes, a geração de regras interpretáveis, desativação e reativação, manutenção de incidentes de outras regras, ramos de CPU distintos, rejeição de ações fora da etapa, comparação de evidências, validação técnica, registro de alternativa em execução pausada e migração com retomada após reinício.

O teste de interface em Chromium abriu a configuração da máquina, editou o limite e verificou o código aplicado. No laboratório, gerou latência, verificou um único disparo do áudio para uma nova ocorrência e nenhuma repetição após novas coletas. Também acionou teste e silenciamento do som, abriu a fila, consultou evidências, avançou pelo ramo de latência, pausou, registrou outra solução, recarregou, retomou, corrigiu a falha e chegou à verificação funcional. Foi verificada a largura da página em tela móvel.

O teste de áudio observa o disparo da Web Audio API no navegador. Volume físico e reprodução em alto-falantes Windows dependem do computador de apresentação. O inicializador BAT requer Python instalado e não foi executado nativamente no Windows durante esta validação.
