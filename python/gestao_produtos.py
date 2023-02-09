"""
Programa para gestão do catálogo de produtos. Este programa permite:
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
##       PRODUTOS E CATÁLOGO
##
################################################################################

PRODUCT_TYPES = {
    'AL': 'Alimentação',
    'DL': 'Detergente p/ Loiça',
    'FRL': 'Frutas e Legumes'
}

# id    : > 0 e tem que ter cinco digitos
# nome
# tipo
# quantidade
# preco

class Produto:
    def __init__(
            self, 
            id: int, 
            nome: str, 
            tipo: str, 
            quantidade: int,
            preco: dec,
    ):
        if id < 0 or len(str(id)) != 5:
            raise ValueError(f'{id=} inválido (deve ser > 0 e ter 5 dígitos)')
        if not nome:
            raise ValueError(f'Nome vazio')
        # if len(nome) == 0:
        #     raise ValueError(f'Nome vazio')
        if quantidade < 0:
            raise ValueError(f'{quantidade=} inválida (deve ser > 0)')
        if tipo not in PRODUCT_TYPES:
            raise ValueError(f'{tipo=} não reconhecido')
        if preco < 0:
            raise ValueError(f'{preco=} inválido (deve ser > 0)')

        self.id = id
        self.nome = nome
        self.tipo = tipo
        self.quantidade = quantidade
        self.preco = preco
    #:

    @property
    def desc_tipo(self):
        return PRODUCT_TYPES[self.tipo]
    #:

    def __str__(self) -> str:
        cls_name = self.__class__.__name__
        return f'{cls_name}[id= {self.id}  nome = "{self.nome}" tipo = "{self.tipo}"]'
    #:

    def __repr__(self) -> str:
        cls_name = self.__class__.__name__
        return f'{cls_name}(id={self.id}, nome="{self.nome}", tipo="{self.tipo}", '\
                f'quantidade={self.quantidade}, preco={repr(self.preco)})'
    #:
    
    def com_iva(self, taxa_iva: dec) -> dec:
        return self.preco * (1 + taxa_iva/100)
    #:
    
class InvalidProdAttribute(ValueError):
    pass
    
class CatalogoProdutos:
    def __init__(self):
        self._prods = {}
    #:
    
    
    def append(self, prod: Produto):
        if prod.id in self._prods:
            raise DuplicateValue(f'Já existe produto com id {prod.id} no catálogo')
        self._prods[prod.id] = prod
    #:
    
    def _dump(self):
        for prod in self._prods.values():
            print(prod)
    #:
    
    def obtem_por_id(self, id: int) -> Produto | None:
        return self._prods.get(id)
    #:
    
    
    def pesquisa(self, criterio) -> 'CatalogoProdutos':
        encontrados = CatalogoProdutos()
        for prod in self._prods.values():
            if criterio(prod):
                encontrados.append(prod)
        return encontrados
    #:
    
    def __len__(self):
            return len(self._prods)
    #:
    
    def __str__(self):
        class_name = self.__class__.__name__
        return f'{class_name}[#produtos = {len(self._prods)}]'
    #:
#:

class DuplicateValue(Exception):
    pass
#:

def main():
    prod1 = Produto(30987, "pão de milho", 'AL', 2, dec('1'))
    prod2 = Produto(30098, "leite mimosa", 'AL', 10, dec('2'))

    print(prod1)
    print(prod2)

    try:
        Produto(30098, "leite mimosoa", 'AL', 6, dec('-10'))
    except ValueError as ex:    
        print("ATENÇÃO: Produto inválido!")
        print(ex)
#:

if __name__ == '__main__':
    main()
#:



# class Xpto {

#     public toString() {
#         return String.format("Xpto: valor de a -> %d", a);
#     }

#     private int a;
# }

# var obj = new Xpto();
# obj.a = 100;
# System.out.println(obj);    // Xpto: valor de a -> 100

# TPC
# matricula (str), marca, modelo, data
# 10-XY-20,Opel,Corsa XL,2019-10-15
# 20-PQ-15,Mercedes,300SL,2017-05-31
