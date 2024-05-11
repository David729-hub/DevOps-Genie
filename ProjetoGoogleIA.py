
import tkinter as tk
from tkinter import ttk, Text, Scrollbar
import tkinter.font as font
import requests
import base64
import json
import google.generativeai as genai
#Coloque Suas Credencias do Google Aqui
GOOGLE_API_KEY= 'SuaChavedeAcessoDoGoogle_AQUI'
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-pro')
janela = tk.Tk()

#Função Que pega o ID do Processo sendo ele default ou customizado
def getIdProcess(organization_url, personal_access_token, process):
  authorization = str(base64.b64encode(bytes(f":{personal_access_token}", "ascii")), "ascii")
  headers = {
    "Authorization": f"Basic {authorization}",
    "Accept": "application/json",
  }
  url = f" {organization_url}/_apis/process/processes?api-version=7.1-preview.1"
  response = requests.get(url, headers=headers)
  if response.status_code == 200:
    process_definition_data = response.json()["value"]
    for processes in process_definition_data:
      if processes["name"] == process:
        return processes["id"]
  else:
    print(f"Erro ao obter ID do processo: {response.status_code}")

#Função que Cria um projeto no Azure Devops apartir dos resultados do json
def create_project(organization_url, personal_access_token, parameters, processes):
  print(parameters)
  type(parameters)
  # Payload simplificado com propriedades obrigatórias
  authorization = str(base64.b64encode(bytes(':' + personal_access_token, 'ascii')), 'ascii')
  headers = {
    'Accept': 'application/json',
    'Authorization': 'Basic ' + authorization
  }
  if(parameters["visibility"] in ('private', 'public') and parameters["processTemplate"] in processes):
      process_id = getIdProcess(organization_url, personal_access_token, parameters["processTemplate"])
      payload = {
        "name": parameters["projectName"],
        "description": parameters["description"],
        "visibility": parameters["visibility"],
        "capabilities": {
          "versioncontrol": {
            "sourceControlType": "git"
          },
          "processTemplate": {
            "templateTypeId": process_id
          }
        }
      }
      # URL da API para criação de projetos
      url = f"{organization_url}/_apis/projects?api-version=6.0"
      # Enviar requisição POST
      response = requests.post(url, headers=headers, json=payload)
      # Verificar o status da requisição
      if response.status_code == 200 or response.status_code == 202:
        print(f"Projeto '{parameters['projectName']}' criado com sucesso!")
      else:
        print(f"Erro ao criar o projeto: {response.status_code} - {response.text}")
  else:
    return "Informações Inválidas! Por favor verifique."
# Função que lista os processos existentes na organização
def get_process_templates(organization_url, personal_access_token):
  # Gerar a autorização Basic
  processes = []
  authorization = str(base64.b64encode(bytes(':' + personal_access_token, 'ascii')), 'ascii')
  headers = {
    'Accept': 'application/json',
    'Authorization': 'Basic ' + authorization
  }
  # URL da API para listar templates de processo
  url = f"{organization_url}/_apis/process/processes?api-version=6.0"
  # Enviar requisição GET
  response = requests.get(url, headers=headers)
  # Verificar o status da requisição
  if response.status_code == 200:
    # Obter a lista de templates de processo da resposta JSON
    process_templates = response.json().get('value')
    for process in process_templates:
      # Retornar a lista de templates de processo
      processes.append(process["name"])
    return processes
  else:
    # Erro ao obter a lista de templates de processo
    raise Exception(f"Erro ao listar templates de processo: {response.status_code} - {response.text}")

#Função que pega o ID do Projeto na organização
def get_project_id(organization_url, parameters, personal_access_token):
  # Consultar a API para obter o ID do projeto com base no nome
  project_url = f'{organization_url}/_apis/projects/{parameters["projectName"]}?api-version=6.0'
  headers = {
    'Authorization': 'Basic ' + base64.b64encode(b':' + personal_access_token.encode()).decode(),
  }
  response = requests.get(project_url, headers=headers)
  if response.status_code == 200:
    project_id = response.json()['id']
    print(project_id)
    return project_id
  else:
    print(f"Erro ao obter o ID do projeto '{parameters['projectName']}': {response.status_code} : {response.text}")
    exit()

#Função que lista todos os campos exitente em um workitem
def get_work_item_fields(organization_url, project, work_item_type, personal_access_token):
  # Encode personal access token
  auth_header = 'Basic ' + base64.b64encode(b':' + personal_access_token.encode()).decode()

  # Construct the API URL
  url = f'{organization_url}/{project}/_apis/wit/workitemtypes/{work_item_type}/fields?api-version=6.0'

  # Send GET request to retrieve fields
  response = requests.get(url, headers={'Authorization': auth_header})
  if response.status_code == 200:
    # Parse JSON response
    data = json.loads(response.text)
    fields = []
    if 'value' in data:
      for field_data in data['value']:
        fields.append(field_data['referenceName'])
    else:
      print("Error: No fields found in work item type definition.")
      return []
    return fields
  else:
    print(f"Error retrieving work item fields: {response.status_code}")
    print(response.text)
    return []

#Lista os tipos de WorkItens existentes no projeto
def get_typesWK(organization_url, parameters, personal_access_token):
  authorization = str(base64.b64encode(bytes(f":{personal_access_token}", "ascii")), "ascii")
  headers = {
    "Authorization": f"Basic {authorization}",
    "Accept": "application/json",
  }
  url = f"{organization_url}/{parameters['projectName']}/_apis/wit/workitemtypes?api-version=7.1-preview.2"
  response = requests.get(url, headers=headers)
  if response.status_code == 200:
    process_definition_data = response.json()
    work_item_types = process_definition_data["value"]
    types = []
    for work_item_type in work_item_types:
      types.append(work_item_type['name'])
    return types
  else:
    print(f"Erro ao obter tipos de work items: {response.status_code}")

#Valida e Cria Novos WorkItens no Projeto
def create_workItem(organization_url, parameters, project_id):
  types = get_typesWK(organization_url, parameters, personal_access_token)
  for parameter in parameters["work_items"]:
    # Endpoint para criar work items no projeto específico
    if parameter["workitemtype"] in types:
          url = f'{organization_url}/{project_id}/_apis/wit/workitems/${parameter["workitemtype"]}?api-version=6.0'
          fields = get_work_item_fields(organization_url, parameters["projectName"], parameter["workitemtype"],
                                        personal_access_token)
        # Corpo da solicitação para criar um novo work item
          data = [
            {
              "op": "add",
              "path": "/fields/System.Title",
              "from": None,
              "value": parameter["title"]
            },
            {
              "op": "add",
              "path": "/fields/System.Description",
              "from": None,
              "value": parameter["description"]
            },
          ]
          if "start_date" in parameter and "Microsoft.VSTS.Scheduling.StartDate" in fields:
            data.append({
              "op": "add",
              "path": "/fields/Microsoft.VSTS.Scheduling.StartDate",
              "from": None,
              "value": parameter["start_date"]
            })
          if "target_date" in parameter and "Microsoft.VSTS.Scheduling.TargetDate" in fields:
            data.append({
              "op": "add",
              "path": "/fields/Microsoft.VSTS.Scheduling.TargetDate",
              "value": parameter["target_date"]
            })
          if "priority" in parameter and "Microsoft.VSTS.Common.Priority" in fields and int(parameter["priority"]) in (
                  1, 2, 3, 4):
            data.append({
              "op": "add",
              "path": "/fields/Microsoft.VSTS.Common.Priority",
              "value": parameter["priority"]
            })
          # Cabeçalhos da requisição
          headers = {
            'Content-Type': 'application/json-patch+json',
            'Authorization': 'Basic ' + base64.b64encode(b':' + personal_access_token.encode()).decode(),
          }
          response = requests.post(url, json=data, headers=headers)

          # Verifique se a solicitação foi bem-sucedida
          if response.status_code == 200:
            print(f"Work item {parameter['title']} foi criado com sucesso!")
          else:
            print(f"Erro ao criar work item {parameter['title']}: ", response.status_code)
            print(response.text)
    else:
      print(
        f"Tipo de WorkItem {parameter['workitemtype']} não está diponivel para o projeto {parameters['projectName']}")

#Função que cria os projetos e workitens
def CreateProjectAndWorkItems(organization_url,personal_access_token, parameters):
    processes = get_process_templates(organization_url,personal_access_token)
    create_project(organization_url,personal_access_token, parameters, processes)
    project_id = get_project_id(organization_url,parameters,personal_access_token)
    create_workItem(organization_url,parameters,project_id)
#Função que cria os workitens em um Projeto
def CreateWorkItems(organization_url, parameters, personal_access_token):
    project_id = get_project_id(organization_url, parameters, personal_access_token)
    create_workItem(organization_url, parameters, project_id)



#Coloque Suas Credenciais do Azure Devops
organization_url = "https://dev.azure.com/{SuaOrganizacao}"
personal_access_token = 'Sua_PAT_do_Azure_Devops_deve_ser_colocada_aqui'


def format_text_remove_quotes(text):
  text = text.strip()
  text = text.replace('"', '').replace("'", "")
  return text


#Função que gera o json com a resposta da intencao do Projeto
def gere_intencao(texto):
    response = model.generate_content(texto)
    try:
      data_json = json.loads(response.text)
    except:
      data = response.text
      stripped_text = data[7:-4]
      data_json = json.loads(stripped_text)
    return data_json

#Função que gera o json com todos os parametros necessários para criação do projeto e work itens
def gere_parametros(texto):
  response = model.generate_content(texto)
  data = response.text
  stripped_text = data[7:-3]
  data_json = json.loads(stripped_text)
  return data_json

#Função Enviar Texto
def enviar_texto():
  texto_digitado = entrada_descricao.get("1.0", "end-1c")  # Obter texto completo do campo Text
  #Texto com as regras a serem passadas pro Gemini criar o Json com a intenção do texto Se Quer Criar um Work Item ou Projeto
  texto_regras = "Diga qual a intenção do texto? Retorne uma resposta seguindo as regras: Se A intenção do texto é Criar um Projeto então retorne: 'Crie um Projeto do Zero', Se for Criar uma Tarefa ou WorkItem (a um projeto existente) retornar: 'Crie uma WorkItem' Retorne a resposta em formato json, trazendo apenas o campo intencao_texto: resposta"
  texto_regras = format_text_remove_quotes(texto_regras)
  texto_pedido = texto_digitado
  texto_pedido = format_text_remove_quotes(texto_pedido)
  texto_pedido = format_text_remove_quotes(texto_pedido)
  #Texto com as regras a serem passadas pro Gemini criar o Json com os Parametros necessários para criação do projteo e WorkItens
  texto_regras_Projeto = "De acordo com o texto retorne uma estrutura em json com os parametros do texto ,seguindo esse json como exemplo: 'projectName': 'ProjetoApi', 'description': 'Descrição do ProjetoApi', 'visibility': 'private', 'processTemplate': 'Basic','work_items': [ { 'workitemtype': 'Epic', 'title': 'Tarefa Epic', 'description': 'Descrição da Tarefa Epic' }]"
  texto_regras_WorkItems = "De acordo com o texto retorne uma estrutura em json com os parametros do texto ,seguindo esse json como exemplo 'projectName': 'ProjetoApi', 'work_items': [ { 'workitemtype': 'Epic', 'title': 'Tarefa Epic', 'description': 'Descrição da Tarefa Epic' }"
  texto = f'{texto_pedido} {texto_regras}'
  parameters = gere_intencao(texto)
  match parameters['intencao_texto']:
    case "Crie uma WorkItem":
      try:
        texto = f'{texto_pedido} {texto_regras_WorkItems}'
        parameters = gere_parametros(texto)
        print(parameters)
        CreateWorkItems(organization_url, parameters, personal_access_token)
        print("Executado com Sucesso")
      except:
        print("Ops! Ocorreu um Erro")
        janela.destroy()
    case "Crie um Projeto do Zero":
      try:
        texto = f'{texto_pedido} {texto_regras_Projeto}'
        parameters = gere_parametros(texto)
        CreateProjectAndWorkItems(organization_url,personal_access_token, parameters)
        print("Executado com Sucesso")
      except:
        print("Ops! Ocorreu um Erro")
        janela.destroy()
    case _:
      print("Intenção Inválida")


janela.title("Crie Projetos e Work Items Automatizados no Azure DevOps")
janela.geometry("1000x800")
janela.config(bg="#3498db")  # Cor de fundo clara

# Frame para o título
frame_titulo = ttk.Frame(janela, borderwidth=5, relief="ridge")
frame_titulo.pack(fill="x", padx=10, pady=10)

# Título principal (fonte grande e negrita)
titulo_principal = tk.Label(frame_titulo, text="Crie Projetos e Work Items Automatizados no Azure DevOps", font=font.Font(family="Arial", size=24, weight="bold"))
titulo_principal.pack(pady=5)

# Frame para a descrição
frame_descricao = ttk.Frame(janela, borderwidth=5, relief="ridge")
frame_descricao.pack(fill="x", padx=10, pady=10)

# Descrição do projeto (fonte média e itálico)
descricao_projeto = tk.Label(frame_descricao, text="Automatize a criação de projetos e work items no Azure DevOps, economizando tempo e esforço.", font=font.Font(family="Arial", size=14, slant="italic"))
descricao_projeto.pack(pady=5)

# Frame para o campo de descrição
frame_campo_descricao = ttk.Frame(janela, borderwidth=5, relief="ridge")
frame_campo_descricao.pack(fill="x", padx=10, pady=10)

# Campo de descrição multiline (barra de rolagem opcional)
entrada_descricao = Text(frame_campo_descricao, bg="white", width=100, height=20, font=font.Font(family="Arial", size=12))
entrada_descricao.pack(pady=5)

# Frame para o botão e o rótulo de resultado
frame_botao_resultado = ttk.Frame(janela, borderwidth=5, relief="ridge")
frame_botao_resultado.pack(fill="x", padx=10, pady=10)

# Botão "Enviar" (estilo personalizado, centralizado, cor azul)
botao_enviar = ttk.Button(frame_botao_resultado, text="Enviar", style="blue.TButton", command=enviar_texto)
botao_enviar.pack(side=tk.TOP, padx=20, pady=10)  # Centralizado na parte superior

# Rótulo para exibir o resultado (vazio inicialmente)
rotulo_resultado = ttk.Label(frame_botao_resultado, text="", style="gray.TLabel")
rotulo_resultado.pack(side="left", padx=5, pady=5)

# Executar o loop principal da interface
janela.mainloop()