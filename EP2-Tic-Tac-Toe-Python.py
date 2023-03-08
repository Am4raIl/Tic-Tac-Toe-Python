######################################################
# Programação Funcional / Programção I (2022/2)
# EP2 - Jogo da Velha
# Nome: FELIPE KITAMOTO AMARAL
# Matrícula: 2022200987
######################################################

import random
from os import system, name 

def getMatricula():
    """
    Retorna a matricula do aluno como string
    """
    return "2022200987" 

def getNome():
    """
    Retorna o nome completo do aluno
    """
    return "FELIPE KITAMOTO AMARAL" 

def limpaTela(): 
	if name == 'nt': 
		system('cls') 
	else: 
		system('clear')

def leValor(tipo, msg = ""):
    """Essa função lê, verifica e aprova (ou reprova) uma entrada baseada em seu tipo,
e retorna a sí própria caso seja reprovada."""
    RED = '\033[31m'
    RST = '\033[00m'
    try:
        return tipo(input(msg))
    except:
        print(f"{RED}ERRO: Tipo inválido! Tente Novamente.{RST}")
        return leValor(tipo, msg)

def funcaoTabuleiro(tabuleiro):
    """ Essa função retorna o tabuleiro em seu formato ideal com suas 9 posições designadas """

    return(f'+ ----------- +\n|  {tabuleiro[7]} | {tabuleiro[8]} | {tabuleiro[9]}  |\n| ---+---+--- |\n|  {tabuleiro[4]} | {tabuleiro[5]} | {tabuleiro[6]}  |\n| ---+---+--- |\n|  {tabuleiro[1]} | {tabuleiro[2]} | {tabuleiro[3]}  |\n+ ----------- +\n')

def escolheSimbolo():
    """ Essa função determina o símbolo do usuário e o símbolo do computador dentro do jogo.
Ela funciona baseada na escolha do próprio usuário, de modo que o símbolo do computador seja
aquele que o usuário não tenha escolhido. Ela retorna ambos os símbolos, sendo o primeiro o do
usuário e o segundo o do computador """

    simboloUsuario = input('Você deseja ser X ou O? ')
    limpaTela()
    if simboloUsuario == 'x' or simboloUsuario == 'X':
        print(f'Você escolheu: X')
        print(f'Portanto, o símbolo do computador é O')
        z = input('\n[Pressione ENTER para continuar]')
        return 'X','O'
    elif simboloUsuario == 'o' or simboloUsuario == 'O':
        print(f'Você escolheu: O')
        print(f'Portanto, o símbolo do computador é X')
        z = input('\n[Pressione ENTER para continuar]')
        return 'O','X'
    else:
        return escolheSimbolo()

def quemComeca():
    """ Essa função determina, com base em um sorteio aleatório, quem começa jogando, o usuário
ou o computador, e retorna o respectivo escolhido """

    L2 = [1,2]
    a = random.choice(L2)
    if a==1:
        limpaTela()
        print('Você começa jogando!\n')
        return 'Jogador'
    elif a==2:
        limpaTela()
        print('O computador começa jogando!\n')
        return 'Computador'

def controlaJogadas(tabuleiro,simboloJogador,simboloComputador,quemJoga):
    """ Essa função controla a ordem de jogadas da partida, alternando entre a jogada do
usuário e a do computador """

    if quemJoga == 'Jogador':
        if vencedor(tabuleiro,simboloJogador,simboloComputador)==False:
            jogadaUsuario(tabuleiro,simboloJogador,simboloComputador)
            controlaJogadas(tabuleiro,simboloJogador,simboloComputador,'Computador')
    else:
        if vencedor(tabuleiro,simboloJogador,simboloComputador)==False:
            jogadaComputador(tabuleiro,simboloJogador,simboloComputador)
            controlaJogadas(tabuleiro,simboloJogador,simboloComputador,'Jogador')

def jogadaUsuario(tabuleiro,simboloJogador,simboloComputador):
    """ Essa função pergunta ao usuário em qual posição ele deseja jogar.
Caso a posição não esteja disponível, ela imprime um erro e pede para que o usuário insira outra.
No final da função, a função imprime o tabuleiro com a posição desejada já preenchida """

    RED = '\033[31m'
    RST = '\033[00m'
    if vencedor(tabuleiro,simboloJogador,simboloComputador) == False:
        b = leValor(int,'Em qual posição você deseja jogar? ')
        if b<1 or b>9:
            print(f'{RED}ERRO: Você deve escolher uma posição que esteja disponível! Tente novamente!{RST}')
            jogadaUsuario(tabuleiro,simboloJogador,simboloComputador)
        elif (tabuleiro[b]) != ' ':
            print(f'{RED}ERRO: Posição inválida! Tente novamente!{RST}')
            jogadaUsuario(tabuleiro,simboloJogador,simboloComputador)
        else:
            limpaTela()
            tabuleiro[b]=simboloJogador
            print(funcaoTabuleiro(tabuleiro))
            print(f'Você marcou a posição {b}!')
            z = input('\n[Pressione ENTER para continuar]')
            limpaTela()

def jogadaComputador(tabuleiro,simboloJogador,simboloComputador):
    """
    Recebe o tabuleiro e o simbolo (X ou O) do computador e determina onde o computador deve jogar
    O tabuleiro pode estar vazio (caso o computador seja o primeiro a jogar) ou com algumas posições preenchidas, 
    sendo a posição 0 do tabuleiro descartada.

    Parâmetros:
    tabuleiro: lista de tamanho 10 representando o tabuleiro
    simboloComputador: letra do computador 

    Retorno:
    Posição (entre 1 e 9) da jogada do computador

    Estratégia: 

    O computador primeiro verifica se há alguma possibilidade de vencer a partida por meio da função ataque(),
    por exemplo: se ele tiver marcado as posições 1 e 3, certamente marcará a posição 2 caso esteja disponível.
    Ele verifica todas as combinações para uma possível vitória, caso não exista nenhuma, ele passa a verificar,
    as possibilidades de evitar uma derrota, por meio da função defesa(), por exemplo: se o usuário marcou as
    posições 1 e 3, o computador, de modo a evitar a derrota, certamente marcará a posição 2 se estiver disponível.
    Caso não exista alguma possibilidade de derrota, o computador então joga numa posição aleatória que ainda
    não tenha sido marcada.
    Em resumo, ele funciona da seguinte forma:
    Ataque > Defesa > Jogada Aleatória.

    """
    return ataque(tabuleiro,simboloJogador,simboloComputador)
    

def ataque(tabuleiro,simboloJogador,simboloComputador):
    """ Essa função verifica se existe possibilidade de vencer o jogo com determinada combinação.
    Ela verifica todas as possibilidades e, caso não exista ainda uma jogada decisiva, chama a função
    defesa() para executar o mesmo processo para verificar se há possibilidade de derrota (no caso, de evitar
    a derrota por parte do computador)"""

    if combinacoes(1,2,3,tabuleiro,simboloComputador,simboloComputador)==False:
        if combinacoes(4,5,6,tabuleiro,simboloComputador,simboloComputador)==False:
            if combinacoes(7,8,9,tabuleiro,simboloComputador,simboloComputador)==False:
                if combinacoes(1,4,7,tabuleiro,simboloComputador,simboloComputador)==False:
                    if combinacoes(2,5,8,tabuleiro,simboloComputador,simboloComputador)==False:
                        if combinacoes(3,6,9,tabuleiro,simboloComputador,simboloComputador)==False:
                            if combinacoes(3,5,7,tabuleiro,simboloComputador,simboloComputador)==False:
                                if combinacoes(1,5,9,tabuleiro,simboloComputador,simboloComputador)==False:
                                    return defesa(tabuleiro,simboloJogador,simboloComputador)

def defesa(tabuleiro,simboloJogador,simboloComputador):
    """ Essa função verifica se existe alguma ameaça por parte do usuário que faça com que o computador
    perca o jogo. Ela verifica todas as combinações possíveis e, caso não exista uma ameaça de derrota ainda,
    ela chama a função aleatorio() e executa uma jogada aleatória no tabuleiro."""

    if combinacoes(1,2,3,tabuleiro,simboloJogador,simboloComputador)==False:
        if combinacoes(4,5,6,tabuleiro,simboloJogador,simboloComputador)==False:
            if combinacoes(7,8,9,tabuleiro,simboloJogador,simboloComputador)==False:
                if combinacoes(1,4,7,tabuleiro,simboloJogador,simboloComputador)==False:
                    if combinacoes(2,5,8,tabuleiro,simboloJogador,simboloComputador)==False:
                        if combinacoes(3,6,9,tabuleiro,simboloJogador,simboloComputador)==False:
                            if combinacoes(3,5,7,tabuleiro,simboloJogador,simboloComputador)==False:
                                if combinacoes(1,5,9,tabuleiro,simboloJogador,simboloComputador)==False:
                                    return aleatorio(tabuleiro,simboloJogador,simboloComputador)

def aleatorio(tabuleiro,simboloJogador,simboloComputador):
    """ Escolhe uma posição aleatória no tabuleiro para executar a jogada do computador.
    Caso a posição esteja indisponível, a função é chamada novamente até que seja marcada uma posição
    disponível """

    c = random.randint(1,9)
    if tabuleiro[c]!=' ':
        return aleatorio(tabuleiro,simboloJogador,simboloComputador)
    else:
        tabuleiro[c]=simboloComputador
        print(f'O computador marcou na posição {c}!\n')
        print(funcaoTabuleiro(tabuleiro))
        return c

def combinacoes(l,m,n,tabuleiro,simboloJogador,simboloComputador):
    """ Essa função ajuda a verificar todas as combinações de vitória possíveis num jogo da velha.
    Caso exista alguma possibilidade de vitória ou de se impedir a vitória do usuário, o computador
    marcará na posição designada para tal ato, imprimindo o tabuleiro e retornando True caso assim seja.
    Caso não exista essa possibilidade de vitória de nenhum dos lados, a função retorna False """

    if tabuleiro[l]==simboloJogador and tabuleiro[n]==simboloJogador and tabuleiro[m]==' ':
        tabuleiro[m]=simboloComputador
        print(f'O computador marcou na posição {m}!\n')
        print(funcaoTabuleiro(tabuleiro))
        return m
    elif tabuleiro[n]==simboloJogador and tabuleiro[m]==simboloJogador and tabuleiro[l]==' ':
        tabuleiro[l]=simboloComputador
        print(f'O computador marcou na posição {l}!\n')
        print(funcaoTabuleiro(tabuleiro))
        return l
    elif tabuleiro[l]==simboloJogador and tabuleiro[m]==simboloJogador and tabuleiro[n]==' ':
        tabuleiro[n]=simboloComputador
        print(f'O computador marcou na posição {n}!\n')
        print(funcaoTabuleiro(tabuleiro))
        return n
    else:
        return False

def teste(tabuleiro,n,simboloUsuario,simboloComputador):
    """ Auxilia na verificação das combinações para determinar o vencedor da partida.
    Imprime o tabuleiro assim que o vencedor é decidido """

    if n == simboloUsuario:
        limpaTela()
        print(f'O jogador "{simboloUsuario}" venceu!')
        print('Parabéns! Você venceu!\n')
        print(funcaoTabuleiro(tabuleiro))
    elif n == simboloComputador:
        limpaTela()
        print(f'O jogador "{simboloComputador}" venceu!')
        print('O computador venceu!\n')
        print(funcaoTabuleiro(tabuleiro))

def vencedor(tabuleiro,simboloUsuario,simboloComputador):
    """ Faz o trabalho de verificar todas as combinações e determinar se já existe um vencedor ou um empate 
    na partida. Caso exista, retorna True, caso contrário, retorna False.
    Faz uso da função teste() para facilitar na análise e evitar replicações """

    if (tabuleiro[7]==tabuleiro[8] and tabuleiro[8]==tabuleiro[9]) and (tabuleiro[8]=='x' or tabuleiro[8]=='X' or tabuleiro[8]=='o' or tabuleiro[8]=='O'):
        teste(tabuleiro,tabuleiro[8],simboloUsuario,simboloComputador)
        return True
    elif (tabuleiro[4]==tabuleiro[5] and tabuleiro[5]==tabuleiro[6]) and (tabuleiro[5]=='x' or tabuleiro[5]=='X' or tabuleiro[5]=='o' or tabuleiro[5]=='O'):
        teste(tabuleiro,tabuleiro[5],simboloUsuario,simboloComputador)
        return True
    elif (tabuleiro[1]==tabuleiro[2] and tabuleiro[2]==tabuleiro[3]) and (tabuleiro[2]=='x' or tabuleiro[2]=='X' or tabuleiro[2]=='o' or tabuleiro[2]=='O'):
        teste(tabuleiro,tabuleiro[2],simboloUsuario,simboloComputador)
        return True
    elif (tabuleiro[1]==tabuleiro[4] and tabuleiro[4]==tabuleiro[7]) and (tabuleiro[4]=='x' or tabuleiro[4]=='X' or tabuleiro[4]=='o' or tabuleiro[4]=='O'):
        teste(tabuleiro,tabuleiro[4],simboloUsuario,simboloComputador)
        return True
    elif (tabuleiro[2]==tabuleiro[5] and tabuleiro[5]==tabuleiro[8]) and (tabuleiro[5]=='x' or tabuleiro[5]=='X' or tabuleiro[5]=='o' or tabuleiro[5]=='O'):
        teste(tabuleiro,tabuleiro[5],simboloUsuario,simboloComputador)
        return True
    elif (tabuleiro[3]==tabuleiro[6] and tabuleiro[6]==tabuleiro[9]) and (tabuleiro[6]=='x' or tabuleiro[6]=='X' or tabuleiro[6]=='o' or tabuleiro[6]=='O'):
        teste(tabuleiro,tabuleiro[6],simboloUsuario,simboloComputador)
        return True
    elif (tabuleiro[1]==tabuleiro[5] and tabuleiro[5]==tabuleiro[9]) and (tabuleiro[5]=='x' or tabuleiro[5]=='X' or tabuleiro[5]=='o' or tabuleiro[5]=='O'):
        teste(tabuleiro,tabuleiro[5],simboloUsuario,simboloComputador)
        return True
    elif (tabuleiro[3]==tabuleiro[5] and tabuleiro[5]==tabuleiro[7]) and (tabuleiro[5]=='x' or tabuleiro[5]=='X' or tabuleiro[5]=='o' or tabuleiro[5]=='O'):
        teste(tabuleiro,tabuleiro[5],simboloUsuario,simboloComputador)
        return True
    elif (tabuleiro[1])!=' ' and (tabuleiro[2])!=' ' and (tabuleiro[3])!=' ' and (tabuleiro[4])!=' ' and (tabuleiro[5])!=' ' and (tabuleiro[6])!=' ' and (tabuleiro[7])!=' ' and (tabuleiro[8])!=' ' and (tabuleiro[9])!=' ':
        limpaTela()
        print('    EMPATE!')
        print('   DEU VELHA!\n')
        print(funcaoTabuleiro(tabuleiro))
        return True
    else:
        return False

def main():
    """ Essa função é o pilar do código, que realiza todo o processo que rege o jogo da velha a partir
da definição das variáveis e chamada das respectivas funções para que executem seus comandos de forma
organizada a fim de dar vida ao código """

    limpaTela()
    simboloJogador, simboloComputador = escolheSimbolo()
    quemJoga = quemComeca()
    tabuleiro = [' ']*10
    print(funcaoTabuleiro(tabuleiro))
    ENTER = input('[Pressione ENTER para continuar]')
    limpaTela()
    controlaJogadas(tabuleiro[:],simboloJogador,simboloComputador,quemJoga)



################################
## NÃO ALTERE O CÓDIGO ABAIXO ##
################################
if __name__ == "__main__":
    main()