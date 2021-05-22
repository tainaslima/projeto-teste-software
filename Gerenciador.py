import random

ESQUERDA = -1
DIREITA = 1
TERMINAROJOGO = False

class Gerenciador:

  def __init__(self):
    self.n_de_jogadores = 2
    self.jogadores = []
    self.orientacao_jogo = DIREITA
    self.pilha_compra = []
    self.pilha_mesa = []
    self.jogou_carta_preta = False
  
    while True:
      self.n_de_jogadores = input("Digite o número de jogadores:")

      if int(self.n_de_jogadores) not in list(range(2,10)):
          print("Número inválido de jogadores.")
      else:
          break

    for n in range(int(self.n_de_jogadores)):
      self.jogadores.append(Jogador(cartas=[])) # Consertar aqui: classe Player depende do outro grupo fazer.

  def verificarVencedor(self, jogador):
    """
        Verifica se o jogador venceu, ou seja, se ele não possui mais cartas em mãos.
        :param jogador: Objeto do tipo Jogador.
        :return: Booleano
    """
    return True if(len(jogador.cartas) == 0) else False # Consertar aqui: classe Player depende do outro grupo fazer.

  def virarPilhaMesaParaCompra(self):
    """
        Transforma a pilha de cartas da mesa na pilha de compra. As cartas são embaralhadas.
    """

    topo_pilha_mesa = self.pilha_mesa.pop()

    self.pilha_compra = self.pilha_mesa.copy()
    random.shuffle(self.pilha_compra)

    self.pilha_mesa = [topo_pilha_mesa]

  def calcularProxJogador(self, atual_jogador, jogou_carta_especial=False, jogou_reverso=False):
    """
        Calcula o próximo jogador baseado no que foi jogado pelo atual.
        :param atual_jogador: Posição na lista do atual jogador.
        :param jogou_carta_especial: Booleano que indica se o atual jogador jogou uma carta especial.
        :param jogou_reverso: Booleano que indica se o atual jogador jogou uma carta reverso.
        :return Posição na lista do próximo jogador
    """
    if (not jogou_carta_especial):
      return (atual_jogador + self.orientacao_jogo) % self.n_de_jogadores
    elif (jogou_carta_especial and jogou_reverso):
      return (atual_jogador + self.orientacao_jogo) % self.n_de_jogadores
    else  :
      return (atual_jogador + 2*self.orientacao_jogo) % self.n_de_jogadores

  def inicializarJogo(self): # Consertar aqui: função inicializer depende do outro grupo fazer
    """
        Inicializa o jogo: cria as cartas e as distribui para os jogadores e as pilhas.
    """   
    # Utilizar o self para pegar o conteúdo das variáveis jogadores, pilha_compra e pilha_mesa
    pass

  def acaoJogada(atual_jogador, carta):
    prox_jogador = self.calcularProxJogador(atual_jogador)

    if carta.tipo == "mais":
      prox_jogador.comprar(2, pilha_compra)
      prox_jogador = self.calcularProxJogador(atual_jogador, True, False)

    elif carta.tipo == "vaivolta":
      prox_jogador = self.calcularProxJogador(atual_jogador, True, True)

    elif carta.tipo == "bloq":
      prox_jogador = self.calcularProxJogador(atual_jogador, True, False)

    elif carta.tipo == "preto":
      cor = atual_jogador.escolher_cor_de_coringa()
      carta.cor = cor

    elif carta.tipo == "pretomais":
      prox_jogador.comprar(4, pilha_compra)
      prox_jogador = self.calcularProxJogador(atual_jogador, True, False)
      cor = atual_jogador.escolher_cor_de_coringa()
      carta.cor = cor

    return prox_jogador

  def gerenciarJogo(self):
    """
        Gerencia o jogo: chama as funções do jogador e faz o efeito de suas ações, dá a vez para o próximo jogador.
        Nesta lógica, as variáveis primeiro_jogador, atual_jogador e prox_jogador indicam a posição do objeto Jogador na lista jogadores.
    """
    primeiro_jogador = random.randint(0, self.n_de_jogadores-1)

    atual_jogador = primeiro_jogador

    while not TERMINAROJOGO:
      
      #### Código das ações do jogador atual ####
      
      print("-----------------------------------------------")
      print("Jogador " + str(atual_jogador) + ", é a sua vez!")
      print("O topo da pilha da mesa é: " + self.pilha_mesa[0])

      print("Suas cartas são: " + str(self.jogadores[atual_jogador].cartas)) # Consertar aqui: classe Player depende do outro grupo fazer. Retornar uma lista printável de cartas.
      
      possiveis_cartas_para_jogar = self.jogadores[atual_jogador].selecionar(pilha_mesa[0])
      print("Suas possíveis cartas a jogar são: " + str(possiveis_cartas_para_jogar)) # Consertar aqui: classe Player depende do outro grupo fazer. Retornar uma lista printável de cartas.
      
      # Caso o jogador não tenha cartas para jogar, o gerente compra uma para ele. Caso a pilha de compra esteja vazia, a pilha de mesa
      # vira a de compra antes de passar uma carta para o jogador atual.
      if(not possiveis_cartas_para_jogar):
        print("Você não tem cartas possíveis a jogar. Vamos comprar uma para você!")

        if(len(self.pilha_compra) < 1):
          self.virarPilhaMesaParaCompra()
        
        self.jogadores[atual_jogador].comprar(1, self.pilha_compra) # Consertar aqui: classe Player depende do outro grupo fazer.
        
        possiveis_cartas_para_jogar = self.jogadores[atual_jogador].selecionar(self.pilha_mesa[0])

      # Verifica se agora tem cartas a jogar e caso sim, o jogador joga, caso contrário ele é dado a vez ao próximo.
      if(possiveis_cartas_para_jogar):
        carta_escolhida = int(input("Escolha qual carta irá jogar. Digite um número de 1 a " + str(len(possiveis_cartas_para_jogar)) + ", que corresponde a posição da carta na listagem de possíveis cartas a jogar acima."))-1
        prox_jogador = acaoJogada(atual_jogador)

        self.jogadores[atual_jogador].jogar(possiveis_cartas_para_jogar[carta_escolhida], self.pilha_mesa)
      else:
        print("Você não tem cartas a jogar mesmo se teve que comprar uma nova. Por isso a vez será passada.")
        atual_jogador = self.calcularProxJogador(atual_jogador)
        continue
      
      # Verifica se o jogador atual é o vencedor. Caso seja, acaba o jogo.
      if(self.verificarVencedor(self.jogadores[atual_jogador])):
        TERMINAROJOGO = True
        print("Jogador " + str(atual_jogador) + " ganhou!!! Parabéns!")
        break

      atual_jogador = prox_jogador

if __name__ == "__main__":
  gerenciador = Gerenciador()
  gerenciador.inicializarJogo()
  gerenciador.gerenciarJogo()