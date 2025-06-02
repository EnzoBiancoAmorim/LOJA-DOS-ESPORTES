from time import sleep
from rich.console import Console
from funcoes import (
    carregar_arquivo, salvar_arquivo, limpar_tela,
    hash_senha, validar_email, menu_select, validar_senha_interativa,
    exibir_titulo_animado, registrar_compra,
    mostrar_tabela_produtos, mostrar_tabela_carrinho, adicionar_ao_carrinho,
    carregar_carrinho_usuario, salvar_carrinho_usuario
)

console = Console()

emojis_categorias = {
    "FUTEBOL": "⚽", "BASQUETE": "🏀", "TÊNIS": "🎾"
}

emojis_subcategorias = {
    "CHUTEIRAS":  "🥾", "CAMISAS DE TIMES": "👕", "BOLAS DE FUTEBOL": "⚽", 
    "TÊNIS DE BASQUETE": "👟", "REGATAS DE TIMES DA NBA": "👕", "BOLAS DE BASQUETE": "🏀",
    "ACESSÓRIOS": "🧢", "ROUPAS": "👕", "RAQUETES": "🎾"
}


# ===== INÍCIO DO PROGRAMA =====

# Arquivos TXT (Carrega dados)
usuarios = carregar_arquivo("usuarios.txt")
produtos = carregar_arquivo("produtos.txt")
compras = carregar_arquivo("compras.txt")
carrinhos = carregar_arquivo("carrinhos.txt")

# Título de Boas-Vindas
# Exibe o título de boas-vindas com animação
limpar_tela()
exibir_titulo_animado("SEJA BEM-VINDO(A) À LOJA DOS ESPORTES!")
sleep(1.2)
limpar_tela()
# Loop principal:
while True:
    console.print("[bold yellow]DIGITE SEU E-MAIL:[/bold yellow] ", end="")
    email = input().strip()
    carrinho = carregar_carrinho_usuario(email)
    limpar_tela()

    if not validar_email(email):  
        console.print("[bold red]E-MAIL INVÁLIDO![/bold red] [bold white]TENTE NOVAMENTE...[/bold white]", end="")
        sleep(2)
        limpar_tela()
        continue 

    usuario = next((u for u in usuarios if u["email"] == email), None)
    
    # LOGIN
    if usuario: 
        limpar_tela()
        console.print("[bold white]FAÇA[/bold white] [bold green]SEU LOGIN[/bold green], [bold white]DIGITANDO[/bold white] [bold green]SUA SENHA...[/bold green]", end="")
        sleep(1.5)
        limpar_tela()

        # REQUERIMENTO DE SENHA
        while True:
            console.print("[bold yellow]DIGITE SUA SENHA:[/bold yellow] ", end="")
            senha = input().strip()
            limpar_tela()
            if usuario["senha"] == hash_senha(senha):
                console.print(f"[bold white]SEJA BEM-VINDO(A) DE VOLTA,[/bold white] [bold green]{usuario['nome'].upper()}![/bold green]", end="")
                sleep(2)
                limpar_tela()
                break
            else:
                console.print("[bold red]SENHA INCORRETA.[/bold red] [bold white]TENTE NOVAMENTE...[/bold white]", end="")
                sleep(2)
                limpar_tela()
    else: # CADASTRO
        console.print("[bold white]VOCÊ AINDA[/bold white] [bold red]NÃO[/bold red] [bold white]POSSUI CADASTRO NA[/bold white] [bold green]LOJA DOS ESPORTES![/bold green]", end="")
        sleep(2)
        limpar_tela()

        console.print("[bold white]DESEJA REALIZAR O SEU[/bold white] [bold yellow]CADASTRO?[/bold yellow]")
        console.print("[bold white]Use as setas do teclado para navegar e pressione [bold yellow]ENTER[/bold yellow] para selecionar uma opção.[/bold white]")
        escolha = menu_select("", ["✅ - SIM, DESEJO ME CADASTRAR NA LOJA DOS ESPORTES", "❌ - NÃO, DESEJO SAIR DA LOJA DO ESPORTES"])
        if escolha == "✅ - SIM, DESEJO ME CADASTRAR NA LOJA DOS ESPORTES":
            print("\033c", end="")
            console.print("[bold white]CARREGANDO...[/bold white]", end="")
            sleep(1.5)
            limpar_tela()
            console.print("[bold yellow]DIGITE SEU NOME:[/bold yellow]", end=" ")
            nome = input().strip().capitalize()
            limpar_tela()
            console.print(f"[bold white]CRIE SUA SENHA,[/bold white] [bold yellow]{nome.upper()}:[/bold yellow]", end=" ")
            senha = validar_senha_interativa(input().strip())
            novo_usuario = {"nome": nome, "email": email, "senha": hash_senha(senha)}
            usuarios.append(novo_usuario)
            salvar_arquivo("usuarios.txt", usuarios)
            limpar_tela()
            console.print("[bold white]CADASTRO REALIZADO COM[/bold white] [bold green]SUCESSO![/bold green]", end="")
            sleep(2)
            limpar_tela()
        if escolha == "❌ - NÃO, DESEJO SAIR DA LOJA DO ESPORTES":
            print("\033c", end="")
            console.print("[bold red]SAINDO...[/bold red]", end="")
            sleep(1.5)
            limpar_tela()
            exit()

    # MENU PRINCIPAL
    categorias = sorted(set(p["categoria"] for p in produtos))

    while True:
        console.print("[bold yellow]SELECIONE UMA OPÇÃO:[/bold yellow]")
        console.print("[bold white]Use as setas do teclado para navegar e pressione [bold yellow]ENTER[/bold yellow] para selecionar uma opção.[/bold white]")
        
        opção = menu_select(
             "",
            [
            "🛍️  - VER PRODUTOS POR CATEGORIA",
            "🛒 - VER CARRINHO",
            "❌ - SAIR"
        ])
            
        if "CATEGORIA" in opção:
            while True:
                print("\033c", end="")
                console.print("[bold white]SELECIONE A [bold yellow]CATEGORIA[/bold yellow] QUE DESEJA. OU ENTÃO ESCOLHA A OPÇÃO '🔙', PARA VOLTAR:[/bold white]")
                console.print("[bold white]Use as setas do teclado para navegar e pressione [bold yellow]ENTER[/bold yellow] para selecionar uma opção.[/bold white]")
                cat_escolhida = menu_select("", [f"{emojis_categorias.get(c, '')} {c}" for c in categorias] + ["🔙"])
                if cat_escolhida == "🔙":
                    limpar_tela()
                    break 

                categoria = cat_escolhida.split(" ", 1)[-1]
                produtos_categoria = [p for p in produtos if p["categoria"] == categoria]

                subcategorias = sorted(set(p["subcategoria"] for p in produtos_categoria))

                while True:
                    print("\033c", end="")
                    console.print(f"[bold white]SELECIONE A[/bold white] [bold yellow]SUBCATEGORIA[/bold yellow] [bold white]DA CATEGORIA[/bold white] [bold orange1]{categoria.upper()}[/bold orange1]. [bold white]OU ENTÃO ESCOLHA A OPÇÃO '🔙', PARA VOLTAR[/bold white]:")
                    console.print("[bold white]Use as setas do teclado para navegar e pressione [bold yellow]ENTER[/bold yellow] para selecionar uma opção.[/bold white]")
                    subcat_escolhida = menu_select("", [f"{emojis_subcategorias.get(c, '')} {c}" for c in subcategorias] + ["🔙"])
                    if subcat_escolhida == "🔙":
                        limpar_tela()
                        break

                    subcategoria = subcat_escolhida.split(" ", 1)[-1]
                    produtos_subcategoria = [p for p in produtos_categoria if p["subcategoria"] == subcategoria]

                    if subcategoria == "REGATAS DE TIMES DA NBA":
                        while True:
                            times_nba = sorted(set(p.get("subsubcategoria", "OUTROS") for p in produtos_subcategoria))
                            print("\033c", end="")
                            console.print("[bold white]SELECIONE O[/bold white] [bold yellow]TIME DA NBA[/bold yellow] [bold white]DESEJADO. OU ENTÃO ESCOLHA A OPÇÃO '🔙', PARA VOLTAR:[/bold white]")
                            console.print("[bold white]Use as setas do teclado para navegar e pressione [bold yellow]ENTER[/bold yellow] para selecionar uma opção.[/bold white]")
                            time_escolhido = menu_select("", times_nba + ["🔙"])
                            if time_escolhido == "🔙":
                                limpar_tela()
                                break
                            produtos_filtrados = [p for p in produtos_subcategoria if p.get("subsubcategoria", "OUTROS") == time_escolhido]
                            if not produtos_filtrados:
                                console.print("[bold red]NENHUM PRODUTO ENCONTRADO.[/bold red]", end="")
                                sleep(2)
                                limpar_tela()
                                continue
                            mostrar_tabela_produtos(produtos_filtrados)
                            console.print("\n[bold white]ADICIONE AO [bold yellow]CARRINHO[/bold yellow] O PRODUTO DESEJADO. OU ENTÃO ESCOLHA A OPÇÃO '🔙', PARA VOLTAR: [/bold white]")
                            console.print("[bold white]Use as setas do teclado para navegar e pressione [bold yellow]ENTER[/bold yellow] para selecionar uma opção.[/bold white]")
                            escolhido = menu_select("", [p["nome"] for p in produtos_filtrados] + ["🔙"])
                            if escolhido == "🔙":
                                limpar_tela()
                                continue
                            produto = next(p for p in produtos_filtrados if p["nome"] == escolhido)
                            adicionar_ao_carrinho(carrinho, produto)
                            salvar_carrinho_usuario(email, carrinho)
                            print("\033c", end="")
                            console.print(f"[bold yellow]{produto['nome'].upper()}[/bold yellow] [bold white]ADICIONADO AO CARRINHO COM[/bold white] [bold green]SUCESSO![/bold green]", end="")
                            sleep(2)
                            limpar_tela()
                            console.print("[bold white]VOLTANDO AO[/bold white] [bold yellow]MENU PRINCIPAL...[/bold yellow]", end="")
                            sleep(1.5)
                            limpar_tela()
                            break
                        break

                    else:
                        while True:
                            subsubcategorias = sorted(set(p.get("subsubcategoria", "OUTROS") for p in produtos_subcategoria))
                            print("\033c", end="")
                            console.print(f"[bold white]SELECIONE A[/bold white] [bold yellow]MARCA[/bold yellow] [bold white]DE[/bold white] [bold green]{subcat_escolhida.upper()}[/bold green] [bold white]DESEJADA. OU ENTÃO ESCOLHA A OPÇÃO '🔙', PARA VOLTAR[/bold white]:")
                            console.print("[bold white]Use as setas do teclado para navegar e pressione [bold yellow]ENTER[/bold yellow] para selecionar uma opção.[/bold white]")
                            subsubcat_escolhida = menu_select("", subsubcategorias + ["🔙"])
                            if subsubcat_escolhida == "🔙":
                                limpar_tela()
                                break
                            produtos_filtrados = [p for p in produtos_subcategoria if p.get("subsubcategoria", "OUTROS") == subsubcat_escolhida]
                            if not produtos_filtrados:
                                console.print("[bold red]NENHUM PRODUTO ENCONTRADO.[/bold red]", end="")
                                sleep(2)
                                limpar_tela()
                                continue
                            mostrar_tabela_produtos(produtos_filtrados)
                            console.print("\n[bold white]ADICIONE AO [bold yellow]CARRINHO[/bold yellow] O PRODUTO DESEJADO. OU ENTÃO ESCOLHA A OPÇÃO '🔙', PARA VOLTAR[/bold white]")
                            console.print("[bold white]Use as setas do teclado para navegar e pressione [bold yellow]ENTER[/bold yellow] para selecionar uma opção.[/bold white]")
                            escolhido = menu_select("", [p["nome"] for p in produtos_filtrados] + ["🔙"])
                            if escolhido == "🔙":
                                limpar_tela()
                                continue 
                            produto = next(p for p in produtos_filtrados if p["nome"] == escolhido)
                            adicionar_ao_carrinho(carrinho, produto)
                            salvar_carrinho_usuario(email, carrinho)
                            print("\033c", end="")
                            console.print(f"[bold yellow]{produto['nome'].upper()}[/bold yellow] [bold white]ADICIONADO AO CARRINHO COM[/bold white] [bold green]SUCESSO![/bold green]", end="")
                            sleep(2)
                            limpar_tela()
                            console.print("[bold white]VOLTANDO AO[/bold white] [bold yellow]MENU PRINCIPAL...[/bold yellow]", end="")
                            sleep(1.5)
                            limpar_tela()
                            break
                        break
                break
        elif "CARRINHO" in opção:
            if not carrinho:
                print("\033c", end="")
                console.print("[bold yellow]CARRINHO[/bold yellow] [bold white]VAZIO.[/bold white]", end="")
                sleep(1.3)
                limpar_tela()
                console.print("[bold white]VOLTANDO AO[/bold white] [bold yellow]MENU PRINCIPAL...[/bold yellow]", end="")
                sleep(1.5)
                limpar_tela()
                continue
            
            print("\033c", end="")
            mostrar_tabela_carrinho(carrinho)

            console.print("[bold white]DESEJA [bold yellow]FINALIZAR[/bold yellow] A COMPRA DO(S) PRODUTO(S) EM QUESTÃO?[/bold white]")
            console.print("[bold white]Use as setas do teclado para navegar e pressione [bold yellow]ENTER[/bold yellow] para selecionar uma opção.[/bold white]")
            opção_carrinho = menu_select("", ["✅ - SIM, GOSTARIA DE FINALZAR MINHA COMPRA", "🧹 - GOSTARIA DE ESVAZIAR MEU CARRINHO", "🔙 - GOSTARIA DE VOLTAR AO MENU PRINCIPAL"])
            if opção_carrinho == "✅ - SIM, GOSTARIA DE FINALZAR MINHA COMPRA": 
                print("\033c", end="")   
                erro_estoque = False
                for item in carrinho:
                    produto = next((p for p in produtos if p["nome"] == item["nome"]), None)
                    if produto is None or produto.get("estoque", 0) < item.get("quantidade", 1):
                        erro_estoque = True
                        console.print(f"[bold white]INFELIZMENTE O PRODUTO [bold yellow]{item['nome']}[/bold yellow] SE ENCONTRA [bold red]EM FALTA[/bold red] DENTRO DE NOSSOS ESTOQUES.[/bold white]", end="")
                        break
                if erro_estoque:
                    sleep(2)
                    limpar_tela()
                    continue
                for item in carrinho:
                    for p in produtos:
                        if p["nome"] == item["nome"]:
                            p["estoque"] -= item["quantidade"]
                registrar_compra(email, carrinho)
                salvar_arquivo("produtos.txt", produtos)
                salvar_carrinho_usuario(email, [])
                console.print("[bold white]COMPRA FINALIZADA COM[/bold white] [bold green]SUCESSO![/bold green]", end="")
                carrinho.clear()
                sleep(1.5)
                limpar_tela()
                console.print("[bold white]VOLTANDO AO[/bold white] [bold yellow]MENU PRINCIPAL...[/bold yellow]", end="")
                sleep(1.5)
                limpar_tela()
                continue
            elif opção_carrinho == "🧹 - GOSTARIA DE ESVAZIAR MEU CARRINHO":
                print("\033c", end="")
                console.print("[bold white]CARRINHO ESVAZIADO COM[/bold white] [bold green]SUCESSO![/bold green]", end="")
                carrinho.clear()
                salvar_carrinho_usuario(email, [])
                sleep(1.5)
                limpar_tela()
                console.print("[bold white]VOLTANDO AO[/bold white] [bold yellow]MENU PRINCIPAL...[/bold yellow]", end="")
                sleep(1.5)
                limpar_tela()
            else:
                print("\033c", end="")
                limpar_tela()
                continue
            print("\033c", end="")            
        elif "SAIR" in opção:
            print("\033c", end="")
            console.print("[bold white]OBRIGADO POR VISITAR A[/bold white] [bold green]LOJA DOS ESPORTES![/bold green]", end="")
            sleep(1.5)
            limpar_tela()
            console.print("[bold red]SAINDO...[/bold red]", end="")
            sleep(2)
            limpar_tela()
            exit()