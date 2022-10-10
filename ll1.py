import pandas as pd
import graphviz

dot = graphviz.Digraph('round-table', comment='Sintax tree')

counter = 0
syntax_table = pd.read_csv("syntax_table .csv", index_col=0)

def print_stack():
  print("\nStack:")
  for e in stack:
    print(e.symbol, "-", e.is_terminal)
  print()

def print_input():
  print("\nInut:")
  for t in tokens:
    print(t['type'], ",", t['lexeme'])
  print()

  
def update_stack(stack, token_type):  
  production = syntax_table.loc[stack[0].symbol][token_type]
  #print(production)
  
  # procesar production E -> T E'  =>  T E' 
  #production=production[production.index(">")+1:]
  #print(production)   
 
  elementos = production.split(" ")
  father = elementos[0] 

  #determinamos el nombre del nodo padre
  if(elementos[0] in dot.source):  
    position = dot.source.rfind(elementos[0])
    value = dot.source[position]
    a = 1
    while(True):
      if(dot.source[position+a] == ' ' or dot.source[position+a] == '"' ):
        break
      else:
        value+= dot.source[position+a]
        a+=1
    value = value.strip()
    father = value

  elementos.pop(0)
  elementos.pop(0)

  # eliminar el ultimo elemento de la pila
  stack.pop(0)

  if elementos[0] == "''": #nulo
    return
   
  # insertar production a la stack: primero E' y luego T
  for i in range(len(elementos)-1, -1, -1):      
      symbol = node_stack(elementos[i], not elementos[i].isupper())
      stack.insert(0, symbol)

  # creamos y vinculamos el nodo padre al nodo hijo
  for i in range(0, len(elementos)):
      if(elementos[i] in dot.source):
        key = str(len(dot.source))
        dot.node(elementos[i]+key, elementos[i])
        dot.edge(father, elementos[i]+key)
        
      else:
        dot.node(elementos[i], elementos[i])
        dot.edge(father, elementos[i])

  print_stack()
  
  

class node_stack:
  def __init__(self, symbol, terminal):
    global counter
    self.id = counter
    self.symbol = symbol
    self.is_terminal = terminal
    counter += 1

class node_parser:
  def __init__(self, node_st, lexeme = None, children =[], father = None, line=None):
    self.node_st = node_st
    self.lexeme = lexeme
    self.line = line
    self.children = children
    self.father = father

stack = []
symbol_1 = node_stack('$', True)
symbol_2 = node_stack('E', False)
stack.insert(0, symbol_1)
stack.insert(0, symbol_2)


tokens = [   
            {'type':'id', 'lexeme':'x', 'line':1}, 
            {'type':'+', 'lexeme':'+', 'line':1},
            {'type':'id', 'lexeme':'y', 'line':1},
            {'type':'$', 'lexeme':'$', 'line':1}
        ]

# si el $ es igual q $
while True:
  print("ITERATION ...")
  print_stack()
  print_input()
  if stack[0].symbol == '$' and tokens[0]['type'] == '$':
    print("Todo bien!")
    break

  # si son terminales
  if stack[0].is_terminal:
    print("terminales ...")
    if stack[0].symbol == tokens[0]['type']:
      stack.pop(0)
      tokens.pop(0)
    else:
      print("ERROR sintáctico")
      break

  # sino reemplazar en la pila
  else:    
    update_stack(stack, tokens[0]['type'])
    
    

# renderizar arbol
dot.render('arbol.gv').replace('\\', '/')
dot.render('arbol.gv', view=True)

print(dot.source)