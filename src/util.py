# -*- coding: utf-8 -*-

from string import ascii_letters


class RangeX:
    def __init__(self, v0, vn=None, s=1):
        """ Classe RangeX: Extensão da função default range() com 
        novas funcionalidades.
        :param v0: Valor inicial, requer inteiro 
        :param vn: Valor Final, requer inteiro
        :param s: Intervalo, requer inteiro """
        assert isinstance(v0, int), 'v0 deve ser um inteiro'
        assert isinstance(s, int), 's deve ser um inteiro'

        if vn is None:
            self._v0, self._vn = 0, v0
        else:
            assert isinstance(vn, int), 'vn deve ser um inteiro'

            self._v0 = v0
            self._vn = vn

        self._s = s if self._v0 <= self._vn else s * -1
        _i = -1 if self._s < 0 else 1

        self._value = range(self._v0, self._vn + _i, self._s)

    def to_r(self):
        """ Converter em range().
        :return: range() """
        return self._value

    def to_l(self):
        """ Converter em lista.
        :return: list() """
        return list(self._value)

    def to_s(self):
        """ Converter em string.
        :return: str() """
        return ','.join([str(x) for x in self._value])

    def __str__(self):
        return '{}..{}:{:+d}'.format(self._v0, 
                                     self._vn,
                                     self._s)

    def __repr__(self):
        return 'RangeX: ' + self.__str__()


def range_x(*v, s=None):
    if s:
        return RangeX(*v, s=s).to_r()
    else:
        return RangeX(*v).to_r()


class RangeStr(RangeX):
    def __init__(self, v0, vn=None, s=1):
        """ Classe RangeStr: Adaṕtação da classe RangeX para letras.
        :param v0: Valor inicial, requer 1 letra 
        :param vn: Valor Final, requer 1 letra
        :param s: Intervalo, requer inteiro """
        assert v0 in ascii_letters, 'v0 deve ser uma letra'

        if vn is None:
            inicial = 'a' if v0.islower() else 'A'
            v0, vn = inicial, v0

        assert vn in ascii_letters, 'vn deve ser uma letra'

        o_v0 = ord(v0)
        o_vn = ord(vn)

        # Construtor da classe pai, alimenta o atributo _value com
        # range() correspondente aos ordinal das letras
        super().__init__(o_v0, o_vn, s)

        self._v0, self._vn = v0, vn
        self._original = self._value

        # self._value = (x for x in [chr(v) for v in self._value])
        self._value = self._make_generator(self._original)

    def to_s(self, sep=','):
        """ Converter em string.
        :return: str() """
        return sep.join([str(x) for x in self._make_generator(self._original)])

    def _make_generator(self, r):
        return (x for x in [chr(v) for v in r])


def range_str(*v, s=None):
    if s:
        return RangeStr(*v, s=s).to_r()
    else:
        return RangeStr(*v).to_r()


if __name__ == '__main__':
    r1 = RangeX(10)
    print(r1, r1.to_l(), sep='; ')

    r2 = RangeX(1, 10)
    print(r2.to_s())

    r3 = range_x(2, 10, 2)
    print(r3, list(r3), sep='; ')

    # print(help(r1))

    r4 = RangeStr('a', 'f')
    print(r4, r4.to_r(), sep='; ')

    r5 = RangeStr('h')
    print(r5, r5.to_s(), sep='; ')
    print(r5.to_s(''))

    r6 = range_str('d', 'l', 2)
    print(r6, list(r6))

    # print(help(r4))
