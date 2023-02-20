"""
Programa para gestão de viaturas. Este programa permite:
    - Listar o catálogo
    - Pesquisar por alguns campos 
    - Eliminar um registo do catálogo
    - Guardar o catálogo em ficheiro
"""
import subprocess
import sys
from typing import TextIO
import csv

CSV_DEFAULT_DELIM = ','
DEFAULT_INDENTATION = 3

################################################################################
##
##       VIATURAS E CATÁLOGO
##
################################################################################

VIATURA_MARCAS = {
    'Opel': 'Marca Opel',
    'Mercedes': 'Marca Mercedes',
    'Ford': 'Marca Ford',
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
            raise InvalidCarAttribute(f'{matricula=} inválido (deve ser > 0 e ter 8 dígitos)')
        if marca not in VIATURA_MARCAS:
            raise InvalidCarAttribute(f'{marca} não reconhecida')
        if not modelo:
            raise InvalidCarAttribute(f'Modelo não especificado')
        if len(data) < 0 or len(data) != 10:
            raise InvalidCarAttribute(f'{matricula=} inválido (deve ser > 0 e ter 10 dígitos)')
        

        self.matricula = matricula
        self.marca = marca
        self.modelo = modelo
        self.data = data
    #:
    
    @classmethod
    def from_csv(cls, linha: str, delim = CSV_DEFAULT_DELIM) -> 'Viatura':
        attrs = linha.split(delim)
        return cls (
            matricula = attrs[0],
            marca = attrs[1],
            modelo = attrs[2],
            data = attrs[3],
        )
       

    @property
    def desc_marca(self):
        return VIATURA_MARCAS[self.marca]
    #:

    def __str__(self) -> str:
        cls_name = self.__class__.__name__
        return f'{cls_name}(matricula="{self.matricula}", marca="{self.marca}", modelo="{self.modelo}", data="{self.data}")'
    #:
#:


class InvalidCarAttribute(ValueError):
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
    
    def remover_por_matricula(self, matricula: str) -> Viatura | None:
        viatura = self._viaturas.get(matricula)
        if viatura in viaturas:
            del self._viaturas[matricula]
        return viatura
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
            yield viatura
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
        opcao = entrada("OPÇÃO >  ").strip().upper()
        
        if opcao == '1':
            exec_listar()
        elif opcao == '2':
           exec_pesquisar()
        elif opcao == '3':
            exec_adicionar()
        elif opcao == '4':
            exec_remover()
        elif opcao == '5':
           exec_actualizar_catalogo()
        #:elif opcao == '6':
           #: exec_recarregar_catalogo()
        elif opcao in ('T', 'TERMINAR'):
            exec_terminar()
        else:
            exibe_msg(f"Opção {opcao} inválida!")
            pause()
        #:
    #:
#:
            
            
            
            
            
def exec_listar():
    cabecalho = f'{"Matricula":^10}|{"Marca":^10}|{"Modelo":^10}|{"Data":^15}'
    separador = f'{"-" * 10}+{"-" * 10}+{"-" * 10}+{"-" * 15}'
    print()
    exibe_msg(cabecalho)
    exibe_msg(separador)
    for viatura in viaturas:
        linha = f'{viatura.matricula:^10}|{viatura.marca:^10}|{viatura.modelo:^10}|{viatura.data:^15}'
        exibe_msg(linha)
    #:
    exibe_msg(separador)
    print()
    pause()
#:

def exec_pesquisar():
    matricula = entrada("Indique a matricula a pesquisar: ")

    viatura = viaturas.obtem_por_matricula(matricula.strip().upper()) 
    if viatura:
        exibe_msg("Viatura localizada")
        exibe_msg(viatura)
    else:
        exibe_msg("Não foi encontrada viatura com a matricula {matricula}")
    #:
    print()
    pause()
#:

def exec_adicionar():
    matricula = entrada("Indique a matricula da viatura a adicionar catálogo: ")
    marca = entrada("Indique a marca da viatura a adicionar ao catálogo: ")
    modelo = entrada("Indique o modelo da viatura a adicionar ao catálogo: ")
    data = entrada("Indique a data da viatura a adicionar ao catálogo: ")
    

    viaturas.append(Viatura(matricula, marca, modelo, data))
    
    if Viatura:
        exibe_msg("Viatura adicionada ao catálogo")
        exec_listar()
    else:
        exibe_msg("ERRO")
    #:
    print()
    pause()
#:


def exec_remover():
    matricula = entrada("Indique a matricula da viatura a remover do catálogo: ")

    viatura = viaturas.remover_por_matricula(matricula.strip().upper()) 
    if viatura:
        exibe_msg("Viatura removida")
        exibe_msg(viatura)
        exec_listar()
    else:
        exibe_msg("Não foi encontrada viatura com a matricula {matricula}")
        print()
        
    #:
#:

def exec_actualizar_catalogo():
    with open("./python/viaturas.csv","w") as f:
        for viatura in viaturas:
            car=str(viatura[1:])
            f.writelines(car)
            
    
    
    #produtos_file= open("./python/viaturas.csv","r")
    
    #print(produtos_file.read())
#:


def exec_terminar():
    separador = f'{"-" * 50}'
    exibe_msg(separador)
    exibe_msg(f"O programa vai terminar...")
    exibe_msg(separador)
    sys.exit(0)
#:


def main():
    global viaturas
    viaturas = le_viaturas("./python/viaturas.csv")
    exec_menu()
    
    #produtos_file= open("./python/viaturas.csv","r")
    
    #print(produtos_file.read())
#
    
    

if __name__ == '__main__':
    main()
#:




# TPC
# matricula (str), marca, modelo, data
# 10-XY-20,Opel,Corsa XL,2019-10-15
# 20-PQ-15,Mercedes,300SL,2017-05-31