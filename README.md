# Projeto Extensão para certificados de cursos
## __Construido por: Eduardo Frisch Sousa__
## Tecnologias usadas: HTML, CSS, Javascript,Python
* BootsTrap 5 (Css e Javascript)
* Python Blibiotecas:  
  &emsp;Flask com blueprints  
  &emsp;Templates JINJA
# Instalação:
* USE python.exe -m  Antes dos pip se necessario colocar na raiz do terminal(Pode esta errado a descrição)
* pip install --pre Flask
* pip install --pre blueprintpy
* pip install --pre Jinja2
* pip install --pre SQLAlchemy 
* pip install --pre ntplib 
* alterar variavel root path

<!--
<div align="center">
  <img width="800" height="400" alt="CampoMinadoGame" src="https://github.com/user-attachments/assets/6041fa2f-702d-43a2-b954-6e970a642ab5" /
</div> 

# Mecanismos:
## Geração do mapa:  
&emsp; Feito no Back-end com a matriz dupla(x,y), o campo com as minas e sorteio das bombas e Criada uma função para contar as minas envolta de cada celula. For dentro de For e IFS para ver os 9 possiveis cenarios.  
* Grade do Jogo foi feito:  
As Celulas foram feitas Com botões dentro de linhas e colunas da table:  
# eventos: Javascript
# Opções do Mouse Click 
## Botão esquerdo - Left Click
* Revela os valores da celula  
&emsp; caso o valor da celula for 0(nulo) ativa a funçao de __AbrirAoRedor()__ que abrirar ate o proximo numero de fronteira de minas.
## Botão direito - Right Click
* Em area __Cujo valor não foi revelada__ ainda:   
&emsp; podem Ser posicionadas:   
&emsp;&emsp; As  __Bandeiras__: usadas para marcar minas para ajudar a encontrar a solução.
* Em locais Ja revelados pelo jogador o e sinalizados com __Bandeira__ as __minas__.  
 o click do mouse Abrirar as casas adjacentes caso contrario vai abrir o a redor e fara a explosão das minas. 
 # Modais Bootstrap
 * Foram usados para emitir Notificações para:   
 * __Derrotas__
 * Avisos de __bandeiras__:  
 &emsp;&emsp; Quando numero de bandeiras passou do numero de minas no jogo.
-->