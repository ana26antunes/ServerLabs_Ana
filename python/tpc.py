"""
Programa para gestão de viaturas. Este programa permite:
    - Listar o catálogo
    - Pesquisar por alguns campos 
    - Eliminar um registo do catálogo
    - Guardar o catálogo em ficheiro
"""

from decimal import Decimal as dec
import subprocess
import sys
from typing import TextIO

CSV_DEFAULT_DELIM = ','
DEFAULT_INDENTATION = 3

################################################################################
##
##       VIATURAS E CATÁLOGO
##
################################################################################


# TPC
# matricula (str), marca, modelo, data
# 10-XY-20,Opel,Corsa XL,2019-10-15
# 20-PQ-15,Mercedes,300SL,2017-05-31

PRODUCT_MARCAS = {
    'OP': 'Opel',
    'MS': 'Mercedes',
   
}

class Viatura:
    def __init__(
            self, 
            matricula: str,
            marca: str, 
            modelo: str, 
            data: str,
           
    ):
        if len(str(matricula)) < 0 or len(str(matricula)) != 8:
            raise ValueError(f'{matricula=} inválido (deve ser > 0 e ter 8 dígitos)')
        if not marca:
            raise ValueError(f'Marca não especificada')
        if not modelo:
            raise ValueError(f'Modelo não especificado')
        if marca not in PRODUCT_MARCAS:
            raise ValueError(f'{marca=} não reconhecida')
        if len(data) < 0 or len(data) != 10:
            raise ValueError(f'{matricula=} inválido (deve ser > 0 e ter 10 dígitos)')
        

        self.matricula = matricula
        self.marca = marca
        self.modelo = modelo
        self.data = data
      
    #:
    
    @classmethod
    def from_csv(cls, linha: str, delim = CSV_DEFAULT_DELIM) ->  'Viatura':
        attrs = linha.split(delim)
        return cls(
            matricula = attrs[0],
            marca = attrs[1],
            modelo = attrs[2],
            data = attrs[3],
        )
    #:    
    
    
  
    

    @property
    def desc_marca(self):
        return PRODUCT_MARCAS[self.marca]
    #:
    
    

    def __str__(self) -> str:
        cls_name = self.__class__.__name__
        return f"Viatura[Matricula: {self.matricula} Marca: {self.marca} Modelo: {self.modelo} Data: {self.data}]"
    #:
    
    def __repr__(self) -> str:
        cls_name = self.__class__.__name__
        return f'{cls_name}(matricula={self.matricula}, marca="{self.marca}", modelo="{self.modelo}", '\
                f'data={self.data})'
    #:
#:

# TPC
# matricula (str), marca, modelo, data
# 10-XY-20,Opel,Corsa XL,2019-10-15
# 20-PQ-15,Mercedes,300SL,2017-05-31

class InvalidCardAttribute(ValueError):
    pass

class CatalogoViaturas:
    def __init__(self):
        self._viaturas = {}
    #:
    
    def append(self, viatura: Viatura):
        if viatura.matricula in self._viaturas:
            raise DuplicateValue(f'Já existe viatura com matrícula {viatura.matricula} no catálogo')
        self._viaturas[viatura.matricula] = viatura
    #:
  
    
    def _dump(self):
        for viatura in self._viaturas.values():
            print(viatura)
    #:
    
    def obtem_por_matricula(self, matricula: str) -> Viatura | None:
        return self._viaturas.get(matricula)
    #:
    
    
    def pesquisa(self, criterio) -> 'CatalogoViaturas':
        encontrados = CatalogoViaturas()
        for viatura in self._viaturas.values():
            if criterio(viatura):
                encontrados.append(viatura)
        return encontrados
    #:
    
    def __str__(self):
        class_name = self.__class__.__name__
        return f'{class_name}[#viaturas = {len(self._viaturas)}]'
    #:
    
    
    def __iter__(self):
        for viatura in self._viaturas.values():
            yield Viatura
        #:
    #:
    
    def __len__(self):
            return len(self._viaturas)
    #:
#:
    
class DuplicateValue(Exception):
    pass
#:


################################################################################
##
##       LEITURA DOS FICHEIROS
##
################################################################################


def le_viaturas(caminho_fich: str, delim = CSV_DEFAULT_DELIM) -> CatalogoViaturas:
    viaturas = CatalogoViaturas()
     
    with open(caminho_fich, 'rt') as fich:
        for linha in linhas_relevantes(fich):
            viaturas.append(Viatura.from_csv(linha, delim))
    return viaturas
#:

def linhas_relevantes(fich: TextIO):
    for linha in fich:
        linha = linha.strip()
        if len(linha) == 0 or linha[0] == '#':
            continue
        yield linha
#:


################################################################################
##
##       MENU, OPÇÕES E INTERACÇÃO COM UTILIZADOR
##
################################################################################

def exibe_msg(*args, indent = DEFAULT_INDENTATION, **kargs):
    print(' ' * (indent - 1), *args, **kargs)
#:

def entrada(msg: str, indent = DEFAULT_INDENTATION) -> str:
    return input(f"{' ' * DEFAULT_INDENTATION}{msg}")
#:

def cls():
    if sys.platform == 'win32':
        subprocess.run(['cls'], shell=True, check=True)
    elif sys.platform in ('darwin', 'linux', 'bsd', 'unix'):
        subprocess.run(['clear'], check=True)
    #:
#:

def pause(msg: str="Pressione ENTER para continuar...", indent = DEFAULT_INDENTATION):
    input(f"{' ' * indent}{msg}")
#:

viaturas = CatalogoViaturas()

def exec_menu():
    """
    - Listar Viaturas
    - Pesquisar Viaturas
    - Adicionar Viatura
    - Remover Viatura
    - Actualizar Catálogo
    - Recarregar Catálogo
    - Terminar
    """
    
    while True:
        cls()
        exibe_msg("*******************************************")
        exibe_msg("* 1 - Listar Viaturas                     *")
        exibe_msg("* 2 - Pesquisar Viaturas                  *")
        exibe_msg("* 3 - Adicionar Viatura                   *")
        exibe_msg("* 4 - Remover Viatura                     *")
        exibe_msg("* 5 - Actualizar Catálogo                 *")
        exibe_msg("* 6 - Recarregar Catálogo                 *")
        exibe_msg("*                                         *")
        exibe_msg("* T - Terminar programa                   *")
        exibe_msg("*******************************************")
        
        print()
        opcao = entrada("OPCAO> ").strip().upper()

def main():
    #global viaturas
    #produtos = le_viaturas('viaturas.csv')
    #exec_menu()
    
    produtos_file= open("./python/viaturas.csv","r")
    
    print(produtos_file.read())
#
    
    

if __name__ == '__main__':
    main()
#:




# TPC
# matricula (str), marca, modelo, data
# 10-XY-20,Opel,Corsa XL,2019-10-15
# 20-PQ-15,Mercedes,300SL,2017-05-31