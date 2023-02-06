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
        if len(str(data)) < 0 or len(str(data)) != 10:
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

    def __str__(self):
        return f"Viatura[marca: {self.marca} modelo: {self.modelo}]"
    #:
#:

# TPC
# matricula (str), marca, modelo, data
# 10-XY-20,Opel,Corsa XL,2019-10-15
# 20-PQ-15,Mercedes,300SL,2017-05-31

def main():
    viatura1 = Viatura("10-XY-20", "OP", "Corsa","2019-10-15")
    viatura2 = Viatura("20-PQ-15", "MS", "300SL","2017-05-31")
    

    print(viatura1)
    print(viatura2)

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