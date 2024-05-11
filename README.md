# DevOps Genie: Seu Mago da Automação no Azure DevOps!

Cansado de tarefas repetitivas que drenam sua produtividade no Azure DevOps? DevOps Genie surge como seu aliado mágico, liberando você para se concentrar no que realmente importa: a criação estratégica!

Utilizando Azure Devops e Google AI o sistema DevOps Genie, e capaz de te auxiliar a:

Criar projetos instantaneamente: Defina nome, descrição, visibilidade, processo e workitems, tudo de uma só vez.
Gerenciar workitems com facilidade: Especifique tipo, nome, descrição, datas e prioridade, garantindo organização e clareza.
Liberar tempo precioso: Dedique-se a iniciativas estratégicas, impulsione o crescimento da equipe e otimize custos.
Desenvolvido para sua conveniência:

Linguagem Python3 (amplamente usada e fácil de aprender)
IDE PyCharm (ou sua IDE preferida)
Pacotes Python:
google-generativeai
requests
base64
Comece a automatizar em 3 passos simples:

## Pré-requisitos:

Instale o Python3 (consulte a documentação oficial para instruções).
Obtenha uma API Key do Google AI e um PAT do Azure DevOps com as permissões de criar projetos e workitems (siga as instruções de autenticação do Azure DevOps).

## Exemplo de uso do sistema: 
* Digite sua Solicitação: No campo de texto da interface, digite o que você deseja fazer, no seguinte formato:
Criar Projeto chamado [NOME DO PROJETO] com descrição [DESCRIÇÃO DO PROJETO] com processo [TIPO DO PROCESSO] com visibilidade [TIPO DE VISIBILIDADE]
### Exemplo: 
* Personalize as Configurações (Opcional):
* Visibilidade: Adicione (Público) ou (Privado) ao final da sua solicitação para definir a visibilidade do projeto.
* Processo: Adicione (Basic), (Agile), (Scrum) ao final da sua solicitação para definir o processo do projeto.
* Clique em "Enviar": Pressione o botão "Enviar" para que a IA processe sua solicitação.
* Digite sua Solicitação: No campo de texto da interface, digite o que você deseja fazer, no seguinte formato:
Criar WorkItem no projeto chamado [NOME DO PROJETO] do tipo [TIPO DO WORKITEM] com nome [NOME DO WORKITEM] com descrição [DESCRIÇÃO DO WORKITEM] com start_date [DATA DE INÍCIO] e com target_date [DATA DE TÉRMINO] e com priority [PRIORIDADE]
(Lembrando nem todos os tipos de WorkItems tem os campos start Date e target date, o sistema cria assim mesmo o work item mas sem passar os parametros de data de inicio e fim)
* Exemplo: Criar WorkItem MeuProjeto Tarefa NovaTarefa Essa é uma nova tarefa 2024-04-20 2024-05-01 
* Tipo do WorkItem: Utilize Task, Epic, Feature ou Bug.(Dependendo do tipo de processo alguns tipos de work itens podem estar indisponiveis)
* Data de Início (opcional): Utilize o formato AAAA-MM-DD.
* Data de Término (opcional): Utilize o formato AAAA-MM-DD.
* Prioridade: Utilize um número de 1 a 4.
* Clique em "Enviar": Pressione o botão "Enviar" para que a IA processe sua solicitação.

### OBS: Devido ao curto tempo para realizar o projeto não criei uma funcionalidade para perguntar se quer mesmo continuar com a criação após enviar o texto, por isso certifiquese de colocar todos as informações necessárias antes de enviar.(Solicito que na primeira execução, realize um debug(depuração) no código linha a linha para entender as funcionalidades exitentes)
