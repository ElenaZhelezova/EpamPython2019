"""
Реализовать метод __str__, позволяющий выводить все папки и файлы из данной, например так:

> print(folder1)

V folder1
|-> V folder2
|   |-> V folder3
|   |   |-> file3
|   |-> file2
|-> file1

А так же возможность проверить, находится ли файл или папка в другой папке:
> print(file3 in folder2)
True

"""
import os


class PrintableFolder:
    def __init__(self, name, content):
        self.name = name
        self.content = content
        self.full_content = []
        self.get_full_content()

    def get_full_content(self):
        for i in self.content:
            self.full_content.append(i)
            if isinstance(i, PrintableFolder):
                for j in PrintableFolder(i.name, i.content):
                    self.full_content.append(j)
        return self.full_content

    def __iter__(self):
        return iter(self.full_content)

    def __str__(self):
        result = []
        folder_name = f"V {self.name}"
        result.append(folder_name)
        for item in self.content:
            if isinstance(item, PrintableFolder):
                for i in (str(PrintableFolder(item.name, item.content)).split('\n')):
                    result.append(f"|    {i}")

            else:
                result.append(f"|-> {item.name}")

        return '\n'.join(result)


class PrintableFile:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        pass


file3 = PrintableFile('file3')
file2 = PrintableFile('file2')
file1 = PrintableFile('file1')
folder3 = PrintableFolder('folder3', [file3])
folder2 = PrintableFolder('folder2', [folder3, file2])
folder1 = PrintableFolder('folder1', [folder2, file1])
print(folder1)
print(file2 in folder2)
print(file3 in folder2)
print(file3 in folder1)

