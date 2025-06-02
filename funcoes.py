import os
import json
import re
from rich.table import Table
from time import sleep
from rich.console import Console
import shutil
import hashlib
import locale
import questionary
from uuid import uuid4
from rich import box

console = Console()
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

estilo_personalizado = questionary.Style([
    ("qmark", ""),
    ("question", "bold yellow"),
    ("pointer", "bold yellow"),
    ("highlighted", "bold yellow"),
    ("selected", "bold green"),
    ("separator", "fg:#6C6C6C"),
    ("instruction", ""),
    ])

def carregar_arquivo(nome_arquivo):
    if os.path.exists(nome_arquivo):
        try:
            with open(nome_arquivo, "r", encoding="utf-8") as f:
                conteudo = f.read().strip()
                if not conteudo:
                    return []
                return json.loads(conteudo)
        except (json.JSONDecodeError, IOError):
            return []
    return []

def salvar_arquivo(nome_arquivo, dados):
    with open(nome_arquivo, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)

def formatar_preco(preco):
    return f"R$ {preco:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def limpar_tela():
    print("\033c", end="")
    os.system("cls")
    
def hash_senha(senha):
    return hashlib.sha256(senha.encode()).hexdigest()

def validar_email(email):
    padrao = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(padrao, email) is not None

def menu_select(mensagem, opcoes):
    return questionary.select(mensagem.upper(), choices=opcoes, style=estilo_personalizado).ask()

def input_float(msg):
    while True:
        try:
            return float(input(msg.upper()))
        except ValueError:
            print("DIGITE UM NÚMERO VÁLIDO.")

def input_int(msg):
    while True:
        try:
            return int(input(msg.upper()))
        except ValueError:
            print("DIGITE UM NÚMERO INTEIRO.")

def exibir_regras_senha():
    tabela = Table(style="bold white", show_lines=True)
    tabela.add_column("REGRAS", justify="center", style="bold white")
    tabela.add_column("DESCRIÇÃO", justify="center", style="bold white")

    tabela.add_row("1°", "TER PELO MENOS 8 (OITO) CARACTERES")
    tabela.add_row("2°", "TER PELO MENOS UMA LETRA MAIÚSCULA E MINÚSCULA")
    tabela.add_row("3°", "TER PELO MENOS 1 (UM) NÚMERO")
    tabela.add_row("4°", "TER PELO MENOS 1 (UM) CARACTERE ESPECIAL")

    print("\033c", end="")
    console.print("[bold red]ATENÇÃO: [bold white]SENHA[/bold white] INVÁLIDA![/bold red]", end="")
    sleep(1.5)
    os.system("cls")

    console.print("[bold white]POR FAVOR, DIGITE UMA SENHA[/bold white] [bold green]VÁLIDA...[/bold green]", end="")
    sleep(1.5)
    os.system("cls")

    console.print("[bold white]SUA SENHA [bold red]DEVE SEGUIR[/bold red] OS SEGUINTES PADRÕES ABAIXO:[/bold white]\n")
    console.print(tabela)

def validar_senha_interativa(senha):
    while (
        len(senha) < 8 or
        not any(c.isupper() for c in senha) or
        not any(c.islower() for c in senha) or
        not any(c.isdigit() for c in senha) or
        not any(c in "!@#$%^&*()-_=+[]{}|;:'\",.<>?/`~" for c in senha)
    ):
        exibir_regras_senha()
        console.print("\n[bold white]CRIE SUA SENHA CONFORME OS PADRÕES [bold red]EXIGIDOS[/bold red] ACIMA:[/bold white]", end=" ")
        senha = input().strip()
        os.system("cls")
    return senha

def exibir_titulo_animado(titulo, intervalo_texto = 0.009, intervalo_sinais = 0.0009, estilo1="bold green", estilo2="bold black"):
    largura_terminal = shutil.get_terminal_size().columns
    linhas = titulo.split("\n")
    for char in "=" * largura_terminal:
        console.print(char, end="", style=estilo2, highlight=False)
        sleep(intervalo_sinais)
    print()
    for linha in linhas:
        linha_centralizada = linha.center(largura_terminal)
        for char in linha_centralizada:
            console.print(char, end="", style=estilo1, highlight=False)
            sleep(intervalo_texto)
        print()
    for char in "=" * largura_terminal:
        console.print(char, end="", style=estilo2, highlight=False)
        sleep(intervalo_sinais)
    print()

def registrar_compra(email, carrinho):
    compras = carregar_arquivo("compras.txt")
    compras.append({"email": email, "itens": carrinho})
    salvar_arquivo("compras.txt", compras)

def mostrar_tabela_produtos(produtos):
    limpar_tela()
    tabela = Table(title="", show_lines=True)
    tabela.add_column("NOME", justify="center", style = "bold white")
    tabela.add_column("PREÇO", justify="center", style = "bold green")
    tabela.add_column("DESCRIÇÃO", justify="center", style = "bold white")
    tabela.add_column("ESTOQUE", justify="center", style = "bold green")
    for p in produtos:
        tabela.add_row(p["nome"], formatar_preco(p["preco"]), p["descricao"], str(p["estoque"]))
    console.print(tabela)

def adicionar_ao_carrinho(carrinho, produto):
    for item in carrinho:
        if item["nome"] == produto["nome"]:
            item["quantidade"] += 1
            return
    produto_com_quantidade = produto.copy()
    produto_com_quantidade["quantidade"] = 1
    carrinho.append(produto_com_quantidade)

def mostrar_tabela_carrinho(carrinho):
    tabela = Table(title="", show_lines=True)
    tabela.add_column("NOME", justify="center", style="bold white")
    tabela.add_column("PREÇO UNIT.", justify="center", style="bold green")
    tabela.add_column("QUANTIDADE", justify="center", style="bold yellow")
    tabela.add_column("TOTAL", justify="center", style="bold green")
    tabela.add_column("DESCRIÇÃO", justify="center", style="bold white")
    for p in carrinho:
        total = p["preco"] * p["quantidade"]
        tabela.add_row(
            p["nome"].upper(),
            formatar_preco(p["preco"]),
            str(p["quantidade"]),
            formatar_preco(total),
            p["descricao"].upper()
        )
    console.print(tabela)

def carregar_carrinho_usuario(email):
    todos = carregar_arquivo("carrinhos.txt")
    carrinho_usuario = next((c for c in todos if c["email"] == email), None)
    return carrinho_usuario["itens"] if carrinho_usuario else []

def salvar_carrinho_usuario(email, carrinho):
    todos = carregar_arquivo("carrinhos.txt")
    atualizado = False
    for c in todos:
        if c["email"] == email:
            c["itens"] = carrinho
            atualizado = True
            break
    if not atualizado:
        todos.append({"email": email, "itens": carrinho})
    salvar_arquivo("carrinhos.txt", todos)

def gerar_id_unico(produtos):
    novo_id = f"P{str(uuid4().int)[:4]}"
    while any(produto.get('id') == novo_id for produto in produtos):
        novo_id = f"P{str(uuid4().int)[:4]}"
    return novo_id

def atualizar_produtos_com_id(arquivo="produtos.txt"):
    produtos = carregar_arquivo(arquivo)
    for produto in produtos:
        if "id" not in produto:
            produto["id"] = gerar_id_unico(produtos)
    salvar_arquivo(arquivo, produtos)


def adicionar_ids_ao_json(arquivo="produtos.txt"):
    try:
        with open(arquivo, 'r', encoding='utf-8') as f:
            produtos = json.load(f)
        for produto in produtos:
            if 'id' not in produto:
                produto['id'] = gerar_id_unico(produtos)
        with open(arquivo, 'w', encoding='utf-8') as f:
            json.dump(produtos, f, ensure_ascii=False, indent=4)
        print("IDs adicionados com sucesso!")
    except FileNotFoundError:
        print(f"Erro: O arquivo {arquivo} não foi encontrado.")
    except json.JSONDecodeError:
        print(f"Erro: O arquivo {arquivo} não está em formato JSON válido.")


def cadastrar_produto():
    produtos = carregar_arquivo("produtos.txt")

    while True:
        limpar_tela()
        console.print("[bold yellow]CADASTRO DE PRODUTO\n[/bold yellow]")
        while True:
            console.print("[bold white]DIGITE O NOME DO PRODUTO:[/bold white] ", end="")
            nome = input().strip().upper()
            existe = any(p["nome"].upper() == nome for p in produtos)
            if existe:
                console.print("[bold red]ESTE PRODUTO JÁ ESTÁ CADASTRADO![/bold red]", end="")
                sleep(2)
                limpar_tela()
                console.print("[bold yellow]CADASTRO DE PRODUTO\n[/bold yellow]")
            else:
                break
        console.print("[bold white]DIGITE A DESCRIÇÃO DO PRODUTO:[/bold white] ", end="")
        descricao = input().strip().upper()

        console.print("[bold white]DIGITE O PREÇO DO PRODUTO:[/bold white] ", end="")
        preco = float(input())

        console.print("[bold white]DIGITE A QUANTIDADE EM ESTOQUE DO PRODUTO:[/bold white] ", end="")
        estoque = int(input())

        console.print("[bold white]DIGITE A CATEGORIA DO PRODUTO:[/bold white] ", end="")
        categoria = input().strip().upper()

        console.print("[bold white]DIGITE A SUBCATEGORIA DO PRODUTO:[/bold white] ", end="")
        subcategoria = input().strip().upper()

        console.print("[bold white]DIGITE A SUBSUBCATEGORIA DO PRODUTO:[/bold white] ", end="")
        subsubcategoria = input().strip().upper()

        novo_produto = {
            "id": gerar_id_unico(produtos),
            "nome": nome,
            "descricao": descricao,
            "preco": preco,
            "estoque": estoque,
            "categoria": categoria,
            "subcategoria": subcategoria,
            "subsubcategoria": subsubcategoria
        }

        produtos.append(novo_produto)
        salvar_arquivo("produtos.txt", produtos)
        console.print(f"[bold white]\nPRODUTO [bold yellow]'{nome}'[/bold yellow] CADASTRADO COM[/bold white] [bold green]SUCESSO![/bold green]", end="")
        sleep(2)
        limpar_tela()
        console.print("[bold white]VOLTANDO AO[/bold white] [bold yellow]MENU PRINCIPAL...[/bold yellow]", end="")
        sleep(2)
        return

def alterar_produto():
    while True:
        produtos = carregar_arquivo("produtos.txt")

        if not produtos:
            console.print("[bold red]NENHUM PRODUTO ENCONTRADO![/bold red]")
            sleep(2)
            return

        limpar_tela()
        console.print("[bold yellow]ALTERAÇÃO DE PRODUTO[/bold yellow]\n")
        console.print("[bold white]DIGITE O ID DO PRODUTO QUE DESEJA ALTERAR:[/bold white] ", end="")
        id_alvo = input().strip().upper()
        produto = next((p for p in produtos if str(p["id"]).upper() == id_alvo), None)

        if not produto:
            console.print("[bold red]PRODUTO NÃO ENCONTRADO![/bold red]", end="")
            sleep(2)
            continue

        limpar_tela()
        console.print(f"[bold white]PRODUTO SELECIONADO:[/bold white] [bold yellow]{produto['nome']}[/bold yellow]\n")

        campos = [
            ("nome", "NOME"),
            ("descricao", "DESCRIÇÃO"),
            ("preco", "PREÇO"),
            ("estoque", "ESTOQUE"),
            ("categoria", "CATEGORIA"),
            ("subcategoria", "SUBCATEGORIA"),
            ("subsubcategoria", "SUBSUBCATEGORIA")
        ]

        for chave, label in campos:
            valor_atual = produto[chave]
            if chave == "preco":
                valor_atual = formatar_preco(valor_atual)
            console.print(f"[bold white]{label} ATUAL:[/bold white] [bold yellow]{valor_atual}[/bold yellow]")
            console.print(f"[bold white]DESEJA ALTERAR O(A) {label}? (S/N):[/bold white] ", end="")
            alterar = input().strip().lower()
            if alterar == "s":
                console.print(f"[bold white]DIGITE O NOVO(A) {label}:[/bold white] ", end="")
                novo_valor = input().strip().upper()
                if chave == "preco":
                    try:
                        novo_valor = float(novo_valor.replace(",", "."))
                    except ValueError:
                        console.print("[bold red]VALOR INVÁLIDO![/bold red]")
                        continue
                elif chave == "estoque":
                    try:
                        novo_valor = int(novo_valor)
                    except ValueError:
                        console.print("[bold red]VALOR INVÁLIDO![/bold red]")
                        continue
                else:
                    novo_valor = novo_valor.upper()
                produto[chave] = novo_valor

        salvar_arquivo("produtos.txt", produtos)
        limpar_tela()
        console.print("[bold white]\nPRODUTO ALTERADO COM[/bold white] [bold green]SUCESSO![/bold green]", end="")
        sleep(2)
        menu_principal()
        break
 
def excluir_produto():
    produtos = carregar_arquivo("produtos.txt")
 
    if not produtos:
        print("bold red]NENHUM PRODUTO ENCONTRADO![/bold red]")
        sleep(2)
        return
    limpar_tela()
    console.print("[bold yellow]EXCLUSÃO DE PRODUTO[/bold yellow]\n")
    console.print("[bold white]DIGITE O ID DO PRODUTO QUE DESEJA EXCLUIR:[/bold white] ", end="")
    id_alvo = input().strip().upper()
    produto = next((p for p in produtos if str(p["id"]) == id_alvo), None)
 
    if not produto:
        print("[bold red]NENHUM PRODUTO ENCONTRADO![/bold red]")
        sleep(2)
        return
    
    limpar_tela()
    console.print(f"[bold white]PRODUTO SELECIONADO:[/bold white] [bold yellow]{produto['nome']}[/bold yellow]", end="")
    sleep(1.5)
    limpar_tela()
 
    console.print(f"[bold white]DESEJA REALMENTE EXCLUIR O PRODUTO '[bold yellow]{produto['nome']}[/bold yellow]'?[/bold white]")
    console.print("[bold white]Use as setas do teclado para navegar e pressione [bold yellow]ENTER[/bold yellow] para selecionar uma opção.[/bold white]")
    confirmar = questionary.select(
        "",
        choices=["✅ - SIM", "❌ - NÃO"],
        style=estilo_personalizado
    ).ask()

    if confirmar == "✅ - SIM":
        print("\033c", end="")
        console.print(f"[bold white]O PRODUTO [bold yellow]{produto['nome']}[/bold yellow] FOI EXCLUÍDO COM[/bold white] [bold green]SUCESSO![/bold green]", end="")
        sleep(2)
        limpar_tela()
        console.print("[bold white]VOLTANDO AO MENU PRINCIPAL...[/bold white]", end="")
        sleep(2)
        limpar_tela()
        menu_principal()
    else:
        print("\033c", end="")
        console.print("[bold red]OPERAÇÃO CANCELADA![/bold red]", end="")
        sleep(2)
        limpar_tela()
        console.print("[bold white]VOLTANDO AO MENU PRINCIPAL...[/bold white]", end="")
        sleep(2)
        limpar_tela()  
        menu_principal() 

def relatorio_geral():
    print("\033c", end="")
    produtos = carregar_arquivo("produtos.txt")
    if not produtos:
        console.print("[bold red]NENHUM PRODUTO CADASTRADO![/bold red]")
        sleep(2)
        return
    
    tabela = Table(title="RELATÓRIO GERAL DE PRODUTOS", show_lines=True, header_style="bold cyan")
    tabela.add_column("ID", justify="center", style="bold red")
    tabela.add_column("Nome", justify="center", style="bold blue")
    tabela.add_column("Descrição", justify="center", style="bold white")
    tabela.add_column("Preço", justify="center", style="bold green")
    tabela.add_column("Estoque", justify="center", style="bold magenta")
    tabela.add_column("Categoria", justify="center", style="bold yellow")
    tabela.add_column("Subcategoria", justify="center", style="bold yellow")
    tabela.add_column("Subsubcategoria", justify="center", style="bold yellow")

    for p in produtos:
        tabela.add_row(
            str(p["id"]),
            p.get("nome", "N/A"),
            p["descricao"],
            formatar_preco(p["preco"]),
            str(p["estoque"]),
            p["categoria"],
            p["subcategoria"],
            p["subsubcategoria"]
        )

    console.print("\n[bold cyan]RELATÓRIO GERAL DE PRODUTOS:[/bold cyan]\n")
    console.print(tabela)

    console.print("\n[bold white]PRESSIONE [bold yellow]ENTER[/bold yellow] PARA VOLTAR AO[/bold white] [bold yellow]MENU PRINCIPAL...[/bold yellow]", end="")
    input()
    limpar_tela()

def pesquisa_parcial():
    print("\033c", end="")
    produtos = carregar_arquivo("produtos.txt")

    if not produtos:
        console.print("[bold red]NENHUM PRODUTO CADASTRADO![/bold red]")
        sleep(2)
        return

    console.print("[bold white]POR QUAL [bold yellow]CAMPO[/bold yellow] DESEJA PESQUISAR?[/bold white]")
    console.print("[bold white]Use as setas do teclado para navegar e pressione [bold yellow]ENTER[/bold yellow] para selecionar uma opção.[/bold white]")
    opcoes = [
        questionary.Choice(title="✍️  - NOME", value="nome"),
        questionary.Choice(title="🗂️  - CATEGORIA", value="categoria"),
    ]
    campo = questionary.select("", choices=opcoes, style=estilo_personalizado).ask()
        
    print("\033c", end="")
    console.print(f"[bold white]DIGITE PARTE DO(A) [bold yellow]{campo.upper()}[/bold yellow] PARA BUSCAR:[/bold white] ", end="")
    termo = input().strip().upper()

    resultados = [
        p for p in produtos if termo in str(p.get(campo, "")).upper()
    ]

    if not resultados:
        console.print("[bold red]NENHUM PRODUTO ENCONTRADO COM ESSE CRITÉRIO![/bold red]")
        sleep(2)
        return

    print("\033c", end="")
    console.print(f"[bold white]RESULTADOS DA PESQUISA POR '[bold yellow]{termo}[/bold yellow]'[/bold white]\n")

    tabela = Table(
        title="PRODUTOS ENCONTRADOS",
        show_lines=True,
        box=box.SQUARE,
        header_style="bold white"
    )

    tabela.add_column("ID", justify="center", style="bold red")
    tabela.add_column("Nome", justify="center", style="bold blue")
    tabela.add_column("Descrição", justify="center", style="bold white")
    tabela.add_column("Preço", justify="center", style="bold green")
    tabela.add_column("Estoque", justify="center", style="bold magenta")
    tabela.add_column("Categoria", justify="center", style="bold yellow")
    tabela.add_column("Subcategoria", justify="center", style="bold yellow")
    tabela.add_column("SubSubcategoria", justify="center", style="bold yellow")

    for p in resultados:
        tabela.add_row(
            str(p["id"]),
            p.get("nome", "N/A"),
            p["descricao"],
            formatar_preco(p["preco"]),
            str(p["estoque"]),
            p["categoria"],
            p["subcategoria"],
            p["subsubcategoria"]
        )

    console.print(tabela)

    console.print("\n[bold white]PRESSIONE [bold yellow]ENTER[/bold yellow] PARA VOLTAR AO[/bold white] [bold yellow]MENU PRINCIPAL...[/bold yellow]", end="")
    input()
    menu_principal()


def menu_principal():
    while True:
        limpar_tela()
        console.print("[bold yellow]SELECIONE UMA OPÇÃO:[/bold yellow]")
        console.print("[bold white]Use as setas do teclado para navegar e pressione [bold yellow]ENTER[/bold yellow] para selecionar uma opção.[/bold white]")

        opcao = questionary.select(
            "",
            choices=[
                "1 - INCLUIR PRODUTO ➕",
                "2 - ALTERAÇÃO POR ID ✏️",
                "3 - EXCLUSÃO POR ID ❌",
                "4 - RELATÓRIO GERAL 📊",
                "5 - PESQUISA PARCIAL 🔍",
                "6 - SAIR DO SISTEMA 🔙",
            ],
            style=estilo_personalizado
        ).ask()

        if opcao.startswith("1"):
            cadastrar_produto()
        elif opcao.startswith("2"):
            alterar_produto()
        elif opcao.startswith("3"):
            excluir_produto()
        elif opcao.startswith("4"):
            relatorio_geral()
        elif opcao.startswith("5"):
            pesquisa_parcial()
        elif opcao.startswith("6"):
            console.print("[bold red]SAINDO[/bold red] [bold white]DO[/bold white] [bold green]SISTEMA...[/bold green]")
            break