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
            raise ValueError(f'{matricula=} inválido (deve ser > 0 e ter 5 dígitos)')
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
    
    def __len__(self):
            return len(self._viaturas)
    #:
#:
    
class DuplicateValue(Exception):
    pass
#:

def main():
    
    viaturas=CatalogoViaturas()
    viaturas.append(Viatura("10-XY-20", "OP", "Corsa","2019-10-15"))
    #viaturas.append(Viatura("10-XY-20", "MS", "300SL","2017-05-31"))
    viaturas.append(Viatura("20-PQ-15", "MS", "300SL","2017-05-31"))
    
    viaturas._dump()
    
    print(viaturas.obtem_por_matricula("10-XY-20"))
    
    #viatura1 = Viatura("10-XY-20", "OP", "Corsa","2019-10-15")
    #viatura2 = Viatura("20-PQ-15", "MS", "300SL","2017-05-31")
    

    #print(viatura1)
    #print(viatura2)

    try:
        Viatura("10-XY-20", "OP", "Corsa","2019-10-15")
    except ValueError as ex:    
        print("ATENÇÃO: Viatura inválida!")
        print(ex)
#:

if __name__ == '__main__':
    main()
#:




# TPC
# matricula (str), marca, modelo, data
# 10-XY-20,Opel,Corsa XL,2019-10-15
# 20-PQ-15,Mercedes,300SL,2017-05-31