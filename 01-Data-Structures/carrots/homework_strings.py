""""

Задание 1

0) Повторение понятий из биологии (ДНК, РНК, нуклеотид, протеин, кодон)

1) Построение статистики по входящим в последовательность ДНК нуклеотидам 
для каждого гена (например: [A - 46, C - 66, G - 23, T - 34])

2) Перевод последовательности ДНК в РНК (окей, Гугл)

3) Перевод последовательности РНК в протеин*


*В папке files вы найдете файл rna_codon_table.txt - 
в нем содержится таблица переводов кодонов РНК в аминокислоту, 
составляющую часть полипептидной цепи белка.


Вход: файл dna.fasta с n-количеством генов

Выход - 3 файла:
 - статистика по количеству нуклеотидов в ДНК
 - последовательность РНК для каждого гена
 - последовательность кодонов для каждого гена

 ** Если вы умеете в matplotlib/seaborn или еще что, 
 welcome за дополнительными баллами за
 гистограммы по нуклеотидной статистике.
 (Не забудьте подписать оси)

P.S. За незакрытый файловый дескриптор - караем штрафным дезе.

"""

from collections import Counter
import matplotlib.pyplot as plt
import json


def translate_from_dna_to_rna(dna):
    rna = 'files/rna.txt'

    with open(dna) as d, open(rna, 'a') as r:
        for line in d:
            if line.startswith('>'):
                r.write('>\n')
            rna_line = line.replace('T', 'U')
            r.write(rna_line)

    return rna


def count_nucleotides(dna):
    num_of_nucleotides_file = 'files/num_of_nucleotides.json'

    with open(dna) as d:
        lst_of_nucleotides_stat = []
        nucleotides_stat = {}
        nucleotides = ('A', 'C', 'G', 'T')
        for line in d:
            if line.startswith('>') and not nucleotides_stat:
                continue
            if line.startswith('>') and nucleotides_stat:
                lst_of_nucleotides_stat.append(nucleotides_stat)
                nucleotides_stat = {}
                continue
            for key in Counter(line):
                if key not in nucleotides:
                    continue
                if key in nucleotides_stat:
                    nucleotides_stat[key] += Counter(line)[key]
                else:
                    nucleotides_stat[key] = Counter(line)[key]
        lst_of_nucleotides_stat.append(nucleotides_stat)

    with open(num_of_nucleotides_file, 'a') as n:
        for stat in lst_of_nucleotides_stat:
            json.dump(stat, n)
            n.write('\n')

    return num_of_nucleotides_file


def get_stat_diagram(stat_file):
    stat_diagram_file = 'files/stat_nucleotides_diagram.png'
    with open('files/num_of_nucleotides.json') as s:
        statistics = []
        for line in s:
            statistics.append(json.loads(line))

    names1 = list(statistics[0].keys())
    values1 = list(statistics[0].values())

    fig, [axs1, axs2] = plt.subplots(1, 2)
    axs1.bar(names1, values1)
    axs1.set_xlabel('nucleotide')
    axs1.yaxis.set_label_position('left')
    axs1.set_ylabel('count')
    fig.suptitle('stat of nucleotides')

    names2 = list(statistics[1].keys())
    values2 = list(statistics[1].values())

    axs2.bar(names2, values2)
    axs2.set_xlabel('nucleotide')
    axs2.yaxis.set_label_position('left')
    axs2.set_ylabel('count')

    plt.savefig(stat_diagram_file)

    return stat_diagram_file


def translate_rna_to_protein(rna, codons):
    protein_file = 'files/protein.txt'

    with open(codons) as c:
        codons_dict = {}
        for line in c:
            for i in range(0, len(line.split()), 2):
                codons_dict[line.split()[i]] = line.split()[i + 1]

    with open(rna) as r, open(protein_file, 'a') as p:
        for line in r:
            if line.startswith('>'):
                p.write('>\n')
            for i in range(0, len(line), 3):
                if line[i:i+3] not in codons_dict:
                    continue
                p.write(codons_dict[line[i:i + 3]])
                p.write(' ')
            p.write('\n')

    return protein_file


def main(dna_file, codons_file):
    nucleotides_stat_file = count_nucleotides(dna_file)
    nucleotides_stat_diagram = get_stat_diagram(nucleotides_stat_file)
    rna_file = translate_from_dna_to_rna(dna_file)
    protein_file = translate_rna_to_protein(rna_file, codons_file)


if __name__ == '__main__':
    d_file = 'files/dna.fasta'
    c_file = 'files/rna_codon_table.txt'
    main(d_file, c_file)
