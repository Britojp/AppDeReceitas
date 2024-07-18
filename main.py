import PySimpleGUI as sg
import random

sg.theme("DefaultNoMoreNagging")


# Função tela inicial
def criar_telaInicial():
    bot_frases = [
        "Olá, meu nome é Chefinho Robô, como posso te ajudar?",
        "Bom dia, posso te ajudar com alguma receita?",
        "Procurando alguma receita por aqui?"
    ]

    layout = [
        [sg.Text(bot_frases[random.randint(0, 2)], font=("Roboto", 22, "bold"))],
        [sg.Image(filename='robot.png', key='-IMAGE-', subsample = 3)],
        [sg.Button("Escolher receitas", size=(20), font=("Roboto", 13, "bold"))],
        [sg.Button("Carregar novas receitas", size=(20), font=("Roboto", 13, "bold"))],
        [sg.Button("Exibir todas receitas", size=(20), font=("Roboto", 13, "bold"))],
        [sg.Button("Sair", size=(20), font=("Roboto", 13, "bold"))]
    ]
    return sg.Window("Bem vindo ao app", layout=layout, finalize=True, size=(1000, 600), element_justification='center')


def criar_telaTodasReceitas():
    receitas = carregandoReceitas()
    layoutTodasReceitas = [
        [sg.Text("Receitas Disponíveis:", font=("Roboto", 20, "bold"))],
        [sg.Button("Voltar", size=(20), font=("Roboto", 13, "bold"))],
        [sg.Button("Adicionar Receita", size=(20), font=("Roboto", 13, "bold"))]
    ]

    for nome in receitas.keys():
        layoutTodasReceitas.append(
            [sg.Button(nome, key=f'-RECEITA_{nome}-', size=(50, 2), font=("Roboto", 13, "bold"))])

    layoutReceitas = [
        [sg.Column(layoutTodasReceitas, scrollable=True, vertical_scroll_only=True, size=(500, 800),
                   element_justification="center")]
    ]
    return sg.Window("Todas as receitas", layout=layoutReceitas, finalize=True, size=(1000, 600),
                     element_justification='center')


def criar_telaIngredientes():
    layout = [
        [sg.Text("Escreva os ingredientes que você tem disponível", font=("Roboto", 20, "bold"))],
        [sg.Text("Se deseja pesquisar alguma receita com mais de um ingrediente, os separe por vírgulas",
                 font=("Roboto", 16, 'bold'))],
        [sg.Text("Exemplo: limão, creme de leite", font=("Roboto", 16))],
        [sg.Input(key="ingredientes", size=(100), font=("Roboto", 12, "bold"))],
        [sg.Button("Confirmar", size=(20), font=("Roboto", 12, "bold")),
         sg.Button("Voltar", size=(20), font=("Roboto", 12, "bold"))]
    ]
    return sg.Window("Bot", layout=layout, finalize=True, size=(1000, 600), element_justification='center')


def criar_telaSalvarReceita():
    layout = [
        [sg.Text("Registrar nova receita", font=("Roboto", 20, "bold"))],
        [sg.Text("Digite o nome da receita: ", font=("Roboto", 12)), sg.Input(key="nome_da_receita")],
        [sg.Text("Se a receita possuir mais de um ingrediente, os separe por vírgulas", font=("Roboto", 10, "bold"))],
        [sg.Text("Exemplo: limão, creme de leite", font=("Roboto", 10))],
        [sg.Text("Digite os ingredientes: ", font=("Roboto", 12)), sg.Input(key="ingredientes")],
        [sg.Text("De forma detalhada, explique como a receita deve ser realizada: ", font=("Roboto", 10))],
        [sg.Text("Exemplo: Coloque a água para ferver. Descascar as batatas... ", font=("Roboto", 10, "bold"))],
        [sg.Text("Digite o modo de preparo: ", font=("Roboto", 12)),
         sg.Multiline(key="modo_de_preparo", size=(50, 10), font=("Roboto", 12))],
        [sg.Button("Salvar", size=(50), font=("Roboto", 13, "bold"))],
        [sg.Button("Voltar", size=(50), font=("Roboto", 13, "bold"))]
    ]
    return sg.Window("Salvar Receita", layout=layout, finalize=True, size=(1000, 600), element_justification='center')


def criar_telaModoPreparo(nome_receita):
    ingredientes = identificarIngredientes(nome_receita)
    modo_preparo = identificarModoPreparo(nome_receita)
    layout = [
        [sg.Text(f"Modo de Preparo da Receita: {nome_receita}", font=("Roboto", 20, "bold"))],
        [sg.Text(f"Ingredientes: {ingredientes}", font=("Roboto", 16,))],
        [sg.Multiline(default_text=modo_preparo, font=("Roboto", 16), size=(50, 15), disabled=True, no_scrollbar=True)],
        [sg.Button("Voltar", size=(20), font=("Roboto", 13, "bold"))]
    ]
    return sg.Window("Modo de Preparo", layout=layout, finalize=True, size=(1000, 600), element_justification='center')


def criar_telaReceitasIngredientes(receitas_encontradas):
    layoutReceitasEncontradas = [
        [sg.Text("Receitas Encontradas:", font=("Roboto", 20, "bold"))],
        [sg.Button("Voltar", size=(20), font=("Roboto", 13, "bold"))]
    ]

    for nome_receita in receitas_encontradas:
        layoutReceitasEncontradas.append(
            [sg.Button(nome_receita, key=f'-RECEITA_{nome_receita}-', size=(50, 2), font=("Roboto", 13, "bold"))])

    layout = [
        [sg.Column(layoutReceitasEncontradas, scrollable=True, vertical_scroll_only=True, size=(500, 800),
                   element_justification="center")]
    ]
    return sg.Window("Receitas Encontradas", layout=layout, finalize=True, size=(1000, 600),
                     element_justification='center')


def carregandoReceitas():
    receitas = {}
    try:
        with open("receitas.txt", "r", encoding="utf-8") as receita:
            for linha in receita.readlines():
                partes = linha.split(':')
                nome_receita = partes[0].strip()
                ingredientes_e_preparo = partes[1].strip().split('|')
                ingredientes = ingredientes_e_preparo[0].split(', ')
                modo_preparo = ingredientes_e_preparo[1] if len(ingredientes_e_preparo) > 1 else ""
                receitas[nome_receita] = {"ingredientes": ingredientes, "modo_preparo": modo_preparo}
    except FileNotFoundError:
        pass
    return receitas


def salvarReceita(nome, ingredientes, modo_preparo):
    with open("receitas.txt", "a", encoding="utf-8") as receita:
        receita.write(f"{nome}: {', '.join(ingredientes)} \n")
        receita.close()
    with open("modoPreparo.txt", "a", encoding="utf-8") as modoPreparo:
        modoPreparo.write(f"{nome}: {modo_preparo} \n")
        modoPreparo.close()


def carregarIngredientes():
    receitas = carregandoReceitas()
    ingredientes = set()
    for lista in receitas.values():
        ingredientes.update(lista["ingredientes"])
    return list(ingredientes)


def receberIngredientes(ingredientes):
    listaIngredientes = []
    for ingrediente in ingredientes.split(","):
        listaIngredientes.append(ingrediente.strip())
    return listaIngredientes


def buscarIngredientes(ingredientesRecebidos):
    listaEncontrados = []
    listaIngredientesRecebidos = receberIngredientes(ingredientesRecebidos)
    receitas = carregandoReceitas()

    for nome_receita, dados_receita in receitas.items():
        ingredientes_receita = dados_receita["ingredientes"]
        for ingredienteRecebido in listaIngredientesRecebidos:
            if ingredienteRecebido in ingredientes_receita and nome_receita not in listaEncontrados:
                listaEncontrados.append(nome_receita)
                break

    return listaEncontrados


def identificarModoPreparo(nomeReceita):
    try:
        with open("modoPreparo.txt", "r", encoding="utf-8") as modoPreparo:
            for linha in modoPreparo:
                partes = linha.split(':')
                nome_receita = partes[0].strip()
                modo_preparo = partes[1].strip("\n")
                if nomeReceita == nome_receita:
                    return modo_preparo
        return "Modo de preparo não encontrado."
    except FileNotFoundError:
        return "Arquivo modoPreparo.txt não encontrado."


def identificarIngredientes(nomeReceita):
    try:
        with open("receitas.txt", "r", encoding="utf-8") as receitas:
            for linha in receitas:
                partes = linha.split(':')
                nome_receita = partes[0].strip()
                ingredientes = partes[1].strip("\n")
                if nomeReceita == nome_receita:
                    return ingredientes
        return "Ingredientes não encontrados."
    except FileNotFoundError:
        return "Arquivo modoPreparo.txt não encontrado."


# Inicializar a tela inicial
telaInicial = criar_telaInicial()
telaIngredientes = None
telaTodasReceitas = None
telaReceitas = None
telaModoPreparo = None
telaSalvarReceita = None

while True:
    window, event, values = sg.read_all_windows()

    if event == sg.WINDOW_CLOSED or event == "Sair":
        break

    if window == telaInicial:
        window['-IMAGE-'].update_animation('robot.gif', time_between_frames=60)

        if event == "Exibir todas receitas":
            telaInicial.hide()
            telaTodasReceitas = criar_telaTodasReceitas()

        elif event == "Carregar novas receitas":
            telaInicial.hide()
            telaSalvarReceita = criar_telaSalvarReceita()

        elif event == "Escolher receitas":
            telaInicial.hide()
            telaIngredientes = criar_telaIngredientes()

    elif window == telaTodasReceitas:
        if event.startswith('-RECEITA_'):
            nome_receita = event.split('-RECEITA_')[1].strip('-')
            receitas = carregandoReceitas()
            telaModoPreparo = criar_telaModoPreparo(nome_receita.strip())
            telaTodasReceitas.hide()

        elif event == "Adicionar Receita":
            telaTodasReceitas.hide()
            telaSalvarReceita = criar_telaSalvarReceita()

        elif event == "Voltar":
            telaTodasReceitas.close()
            telaInicial.un_hide()
            telaTodasReceitas = None

    elif window == telaIngredientes:
        if event == "Confirmar":
            ingredientes = values['ingredientes']
            resultados = buscarIngredientes(ingredientes.lower())
            if resultados:
                telaIngredientes.hide()
                telaReceitas = criar_telaReceitasIngredientes(resultados)
            else:
                sg.popup("Nenhuma receita com esses ingredientes foi encontrada.")

        elif event == "Voltar":
            telaIngredientes.close()
            telaInicial.un_hide()
            telaIngredientes = None

    elif window == telaSalvarReceita:
        if event == "Salvar":
            nome = values['nome_da_receita']
            ingredientes = values['ingredientes'].lower()
            modo_preparo = values['modo_de_preparo']
            if nome and ingredientes and modo_preparo:
                salvarReceita(nome, ingredientes.split(", "), modo_preparo)
                sg.popup("Receita salva com sucesso!")
                telaSalvarReceita.hide()
                telaInicial.un_hide()
            else:
                sg.popup("Por favor, preencha o nome da receita, ingredientes e o modo de preparo.")

        elif event == "Voltar":
            telaSalvarReceita.close()
            telaInicial.un_hide()
            telaSalvarReceita = None

    elif window == telaModoPreparo:
        if event == "Voltar":
            telaModoPreparo.close()
            telaTodasReceitas = criar_telaTodasReceitas()
            telaModoPreparo = None

    elif window == telaReceitas:
        if event.startswith('-RECEITA_'):
            nome_receita = event.split('-RECEITA_')[1].strip('-')
            telaModoPreparo = criar_telaModoPreparo(nome_receita.strip())
            telaReceitas.close()

        elif event == "Voltar":
            telaReceitas.close()
            telaInicial.un_hide()
            telaReceitas = None

telaInicial.close()
