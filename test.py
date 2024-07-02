from model.model import Model

myModel = Model()
myModel._crea_grafo("circle", 2010)
print(myModel.get_dettagli_grafo())
path, distanza = myModel._handle_percorso()
print("Distanza: ", distanza)
for p in path:
    print(p)
