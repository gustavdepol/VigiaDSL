# Modelo do laboratório v4

CPU e memória são a soma dos componentes exclusivos dos processos virtuais. CargaCPU.exe cria demanda de CPU; RetencaoRAM.exe cresce em quatro pontos percentuais por segundo até seu alvo; BackupTeste.exe aumenta ocupação em até cinco pontos percentuais por segundo e também contribui CPU/RAM. Totais são limitados a 100% com escala proporcional e ajuste de arredondamento.

Disco significa percentual ocupado da capacidade. Parar o backup não remove os dados já gravados. Limpar arquivos virtuais devolve a ocupação à base. Não são simulados IOPS, temperatura ou desgaste físico.

Latência converge para o alvo com resposta exponencial; retirada a degradação, converge para a base. Offline impede novas medições numéricas e consultas remotas. Adaptador é uma inspeção local simulada. DNS pode falhar com host disponível; AppService pode parar sem afetar ping. Spooler é independente da aplicação monitorada.

A leitura de cada regra passa pelo interpretador temporal. Métricas numéricas offline são desconhecidas e não validam recuperação. Um intervalo de coleta superior a três segundos reinicia os contadores de continuidade. A amostragem do servidor ocorre aproximadamente a cada 0,5s; a interface consulta o estado a cada 1,5s. Durante edição de campos, a tela pode manter a apresentação para preservar o formulário; o motor continua coletando.

Cada métrica contribui com o maior peso de suas regras ativas: atenção 1, alerta 2, crítico 3. Soma ≥4 ou qualquer regra crítica produz Crítico; soma ≥2 produz Alerta; soma 1 ou condição ainda em observação produz Atenção. Ausência de resposta é exibida como Offline. Arquivar uma ocorrência não remove sua contribuição técnica enquanto a condição estiver ativa.

Registros de captura e versões de procedimento são cópias persistidas. Consultas e ações realizadas dentro da ocorrência incluem evidências; ações diretas no equipamento constam de seus eventos e da auditoria. Ações não relacionadas podem não resolver a falha. O operador deve testar uma hipótese e verificar o resultado.

Recomendação: procedimento publicado, métrica compatível, sistema compatível; base 10 para procedimento específico, 2 para genérico; feedback soma no intervalo -3 a +3; processo relacionado na captura soma 3; mesmo equipamento de origem soma 2. A v4 também utiliza sintomas simultâneos, estado do serviço na captura, respostas e resultados de investigações anteriores para ordenar os procedimentos. Empates por título. O feedback é substituível por ocorrência/procedimento; não multiplica votos por cliques. Não é aprendizado de máquina.

Benchmark: 50×min(núcleos/8,1) + 35×min(RAM/16,1) + 15×min(disco/512,1). A rampa virtual dura 12s em cenário isolado. A pontuação depende do perfil, não da carga atual. Serve apenas para comparação didática.

A base local é um documento de estado persistido transacionalmente em SQLite. Não é uma arquitetura para grande volume: histórico de métricas retém 240 amostras por equipamento, eventos de máquina 150, auditoria 2000. Ocorrências e execuções permanecem até intervenção explícita no arquivo. Interface mostra as últimas 100 entradas de auditoria.
