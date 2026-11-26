# VigiaDSL 4

## Abrir no Windows

Extraia o ZIP inteiro. Na pasta vigiadsl_v4, abra **Iniciar_Windows.bat**. Requer Python 3.9 ou superior instalado. O terminal exibe o endereço local http://127.0.0.1:8765 e deve permanecer aberto durante o uso. Encerre com Ctrl+C.

Também é possível executar `py -3 app.py` ou `python app.py`. Em Linux ou macOS use `python3 app.py`. SQLite, servidor e simulação utilizam a biblioteca padrão. O navegador precisa suportar Web Audio para tocar avisos.

## Utilizar os dados existentes

Feche a versão anterior e **copie** a pasta `dados` dela para dentro de `vigiadsl_v4` antes de iniciar. Em uma instalação nova o programa cria dados de demonstração. Se preferir manter as bases em locais separados, use `py -3 app.py --dados "C:\Vigia\copia\laboratorio.sqlite3"`.

A primeira migração cria uma cópia SQLite ao lado da base, com sufixo `.antes-v4.bak`. Para voltar, abra uma cópia desse backup com a versão de origem. Preserve as duas versões. O conteúdo das ocorrências, soluções, documentos, passos e anotações anteriores fica na base migrada. Um roteiro iniciado na v3 mantém o documento original e retoma na primeira etapa pendente. As novas execuções dos procedimentos iniciais usam o fluxo ramificado. O histórico preserva qual versão foi usada.

Ao reiniciar, as cargas temporárias são interrompidas e o motor volta a medir a partir da nova sessão. Uma interrupção de coleta não conta como tempo contínuo de recuperação. Os registros de atendimento permanecem no SQLite.

## Configurar um aviso

1. Em Equipamentos abra Servidor de arquivos e escolha **Configurar alertas**.
2. Edite Latência e configure “acima de”, 50 ms, persistência 5 s, recuperação 4 s. Marque aviso sonoro se desejar.
3. Confira o resumo e salve. O limite é o tempo absoluto de resposta. Zero na persistência significa alerta na primeira coleta que satisfizer a condição.
4. Use **Ativar som** nessa aba do navegador e **Testar som** para conferir a saída. **Silenciar** mantém os avisos visuais. As novas ocorrências elegíveis disparam um toque por atualização, mesmo quando várias abrem juntas.
5. Em Regras, confira o código gerado, os tokens, a AST, os símbolos e a avaliação ao vivo. As regras de outros equipamentos conservam seu conteúdo, contadores e ocorrências. Alterar uma condição encerra o monitoramento daquela versão e registra o motivo. A recuperação exige observação da condição técnica.

A regra desativada fica guardada para reativação e sai do código em execução. Sons e desativação são preferências persistentes. O formulário preserva trechos não editados e rejeita edições ambíguas de regras duplicadas.

## Atender uma ocorrência

Abra **Laboratório**, selecione uma máquina e inicie um cenário de CPU, RAM, disco, latência, desconexão, DNS ou serviço parado. Em Equipamentos, o índice lateral permite alternar máquinas. Em Ocorrências, a fila permanece acessível enquanto a área central mostra a investigação e o painel lateral traz o contexto.

No diagnóstico guiado, realize a consulta ou ação disponível, leia a evidência e registre o resultado. A resposta decide qual será a próxima etapa. Para CPU concentrada em uma tarefa, o sistema pede identificação da tarefa. Para consumo distribuído, passa à investigação de atividades concorrentes. Para DNS, compare alcance por IP e resolução de nome. A etapa de aplicação verifica o serviço independentemente do atraso da rede.

O roteiro registra data, resposta, nota e evidência da etapa. Pode ser pausado e retomado. Em **Outra solução**, registre observação, ação, solução e resultado. Pode anexar evidências e decidir se encerra o roteiro. Na ocorrência, use “Criar rascunho de procedimento” para editar, revisar e publicar essa solução. O estado técnico continua sob controle da VigiaDSL. O diagnóstico pode terminar com escalonamento ou evidência insuficiente mesmo com a ocorrência ainda aberta.

As recomendações mostram motivos considerando sistema, métrica, evidências, contexto de atendimento e votos. O histórico diferencia relato do operador, retorno funcional e normalização da regra. A comparação de intervenção mostra duas capturas tomadas antes e logo após a ação. O intervalo de recuperação ainda precisa transcorrer.

## Procedimentos Windows e escopo

A documentação de cada procedimento traz fontes, sistemas, revisão, impacto, reversão e escalonamento. As orientações sobre Performance Monitor e CPU do Windows Server foram adaptadas ao modelo simulado. Para Windows cliente, as referências cobrem consulta de recursos, armazenamento e diagnóstico de resolução DNS. A consulta de conexão separa alcance por IP, porta de aplicação e resposta por nome. Somente as ações internas do laboratório são executadas.

Leituras oficiais usadas na revisão:

- [CPU sustentada em Windows Server](https://learn.microsoft.com/en-us/troubleshoot/windows-server/performance/troubleshoot-high-cpu-usage-guidance)
- [Desempenho e memória em Windows Server](https://learn.microsoft.com/en-us/troubleshoot/windows-server/performance/troubleshoot-performance-problems-in-windows)
- [Recursos e desempenho no Windows cliente](https://support.microsoft.com/en-us/windows/experience/performance-optimization/tips-to-improve-pc-performance-in-windows)
- [Espaço livre em Windows cliente](https://support.microsoft.com/en-us/windows/experience/storage-filemanagement/free-up-drive-space-in-windows)
- [Diagnóstico de DNS no Windows cliente](https://learn.microsoft.com/en-us/troubleshoot/windows-client/networking/troubleshoot-dns-client-resolution-issues)
- [Test-NetConnection](https://learn.microsoft.com/en-us/powershell/module/nettcpip/test-netconnection)
- [Get-Service](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.management/get-service)

## Limitações e verificação

Aplicação local de um operador. Equipamentos, processos e medições são simulados. O benchmark é uma comparação idealizada de perfis. O áudio depende da aba aberta, do gesto de ativação e da saída do navegador. As sugestões utilizam critérios explícitos. As execuções mantêm o documento e o fluxo congelados. Documentos locais novos e revisões feitas pelo editor de etapas usam a sequência editada, com saídas para impedimento e verificação final. Os sete procedimentos iniciais possuem os caminhos específicos da v4.

Para executar os testes use `py -3 -m unittest discover -s tests -v`. Consulte RESULTADOS.md e GUIA_APRESENTACAO.md.
