from itertools import permutations, product

class Treenode():
    def __init__(self, value=None, right=None, left=None, res=None, letter=''):
        self.__res = res
        self.right = right
        self.left = left
        self.value = value
        self.letter = letter
    def nodes_print(self):
        x = self.nodes()
        print('\n'.join(list(f'{i[0].value} --> {i[1].value} ({i[1].letter}), {i[2].value} ({i[2].letter})' for i in x if i[1] and i[2])))
    def nodes(self):
        arr = []
        l = self.left
        r = self.right
        arr.append((self, l, r))
        if l and r:
            arr += l.nodes()
            arr += r.nodes()
        return arr
    def __rm(self, res):
        del_arr = []
        if self.left:
            l = self.left
            del_arr.append(l)
            l.__rm(res)
        if self.right:
            r = self.right
            del_arr.append(r)
            r.__rm(res)
        return del_arr
    def letters(self, x, y):
        if len(x) != len(y): raise AttributeError('The length of array "x" is different from the length of array "y"')
        for i in sorted(x, key=len):
            for j in sorted(x, key=len):
                if i!=j and j[:len(i)]==i:
                    raise ValueError(f'Added item to closed node. Changes reset')
        del_arr = []
        dump_res = self.__res.copy()
        for i in range(len(self.__res)):
            if self.__res[i].value in x:
                self.__res[i].letter = y[x.index(self.__res[i].value)]
                c = self.__res[i]
                del_arr += c.__rm(self.__res)
                c.left = None
                c.right = None
                y.pop(x.index(self.__res[i].value))
                x.pop(x.index(self.__res[i].value))
        try:
            for i in del_arr:
                self.__res.pop(self.__res.index(i))
        except ValueError:
            self.__res = dump_res
            raise ValueError('Added item to closed node. Changes reset')
        if len(x) != 0:
            raise ValueError(f'Elements {x} no longer exist')
    def find_letters(self, x, word=""):
        arr = [i.letter for i in self.__res]
        alph = sorted(list(set(x)), key=lambda j: x.count(j))
        del_arr = []
        for i in alph:
            if i in arr:
                del_arr.append(i)
        for i in del_arr:
            alph.pop(alph.index(i))
        mn = 10**23
        for i in permutations(self.nodes(), r=len(alph)):
            res = {i.letter : i.value for i in self.__res if i.letter != ''}
            k = 0
            f = 1 
            for j in range(len(i)):
                for z in range(j+1, len(i)):
                    f *= (i[j][0].value != i[z][0].value[:len(i[j][0].value)]) and (i[z][0].value != i[j][0].value[:len(i[z][0].value)]) and ('.' not in (i[j][0].value, i[z][0].value)) and i[j][0].value not in res.values() and i[z][0].value not in res.values()
                    f *= all((i[j][0].value != r[:len(i[j][0].value)]) and (r != i[j][0].value[:len(r)]) and (i[z][0].value != r[:len(i[z][0].value)]) and (r != i[z][0].value[:len(r)]) for r in res.values())
            if f:
                for j in range(len(alph)):
                    res[alph[j]] = i[j][0].value
                for j in word:
                    k += len(res[j])
                mn= min(k,mn)
        return mn


    @staticmethod
    def __get_related_nodes(res, i):
        nodes = [None, None]
        for j in res:
            if j.value == i+'0':
                nodes[0] = j
            elif j.value == i+'1':
                nodes[1] = j
        return nodes
    @staticmethod
    def create_tree(k):
        res = []
        x = Treenode('.')
        arr = ["".join(j) for i in range(1,k+1) for j in product('01', repeat=i)][::-1]
        for i in arr:
            if len(i) > 1 and len(i) < k:
                nodes = Treenode.__get_related_nodes(res,i)
                c = Treenode(i, nodes[0], nodes[1])
                res.append(c)
            elif len(i) == 1:
                    if i == '0':
                        nodes = Treenode.__get_related_nodes(res,i)
                        c = Treenode(i, nodes[0], nodes[1])
                        x.left = c
                        res.append(c)
                    elif i == '1':
                        nodes = Treenode.__get_related_nodes(res,i)
                        c = Treenode(i, nodes[0], nodes[1])
                        x.right = c
                        res.append(c)

            else:
                c = Treenode(i)
                res.append(c)
        x.__res = res
        return x

if __name__ == "__main__":
    x = Treenode.create_tree(4) # Создание дерева
    x.nodes_print() # Вывод узлов
    x.letters(['010', '011'], ['б','в']) # Закрытие узлов буквами, которые известны
    print()
    x.nodes_print() # Вывод оставшихся узлов
    print(x.find_letters(['а', "д", "т", "о"], "водоотвод")) # Поиск минимальной длины кодировки слова для известного алфавита
    '''
        Вся проблема в том, что не могу вывести зависимость максимальной длины кодов при создании дерева
        от кол-ва букв в алфавите. Максимальная длина дерева определяется "пальцем в небо".
        Начинать надо с наибольшей длины известного алфавита. В примере это 3. Потом пробуем на 1 больше и так до тех пор,
        пока ответ уменьшается, а программа не уходит в ебеня(то есть, не начинает чересчур долго работать).
        В примере решена задача 4 егэ №687 из базы КЕГЭ. Ответ при данных значениях верный.
    '''