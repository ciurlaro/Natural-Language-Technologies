import csv
from Radicioni.Esercizio_3.sem_eval_mapper import cognome
from pathlib import Path


def main():
    lines = cognome().split('-')

    with open(Path.cwd() / "it.test.data.txt", encoding='utf-8') as input_file:

        writer = csv.writer(open("output.csv", "w", newline='', encoding='utf-8'))
        input_reader = input_file.readlines()

        for i in range(int(lines[0]) - 1, int(lines[1])):
            w_line = input_reader[i][:-1].split('\t')

            flag = True
            while flag:
                input_name = input("Punteggio della coppia " + w_line[0] + " - " + w_line[1] + ": " + "\n")
                if input_name.isnumeric() and 0 <= float(input_name) <= 4:
                    flag = False

            w_line.append(input_name)
            print(w_line)
            # writer.writerow(w_line)


main()
