#!usr/bin/python3
# -*- coding: utf-8 -*-


class Fibonacci:
    def __init__(self):
        self._conjunto = self.listar(1, 10)

    def gerar_recursivo(self, n):
        if n < 2:
            return n
        else:
            return self.gerar_recursivo(n - 1) + self.gerar_recursivo(n - 2)

    def gerar_iterativo(self, n):
        i, j = 0, 1
        for x in range(n):
            i, j = j, (i + j)

        return i

    def gerar_generator(self):
        i, j = 0, 1
        while True:
            yield i
            i, j = j, (i + j)

    def listar(self, inicio, fim):
        if inicio > fim:
            inicio, fim = fim, inicio
        lista = []

        for i in range(inicio, (fim + 1)):
            lista.append(self.gerar_iterativo(i))

        return lista

    def __repr__(self):
        conj = str(self._conjunto)[1:-1]
        return "{" + conj + ", ...}"



if __name__ == "__main__":
    f = Fibonacci()

    n = 20
    print("Iteração: ")
    for x in range(1, n):
        print(f.gerar_iterativo(x), end=", ")

    print("\nRecursão: ")
    for x in range(1, n):
        print(f.gerar_recursivo(x), end=", ")

    print("\nGenerator: ")
    g = f.gerar_generator()
    next(g)
    for x in range(1, n):
        print(next(g), end=", ")