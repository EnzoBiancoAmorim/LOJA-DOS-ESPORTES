from funcoes import menu_principal, exibir_titulo_animado
from rich.console import Console
from time import sleep

console = Console()

exibir_titulo_animado("SISTEMA DE GESTÃO DE PRODUTOS")
sleep(1)
menu_principal()