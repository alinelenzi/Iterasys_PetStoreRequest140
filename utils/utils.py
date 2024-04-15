import csv

def read_csv(file_csv):
    dados_csv = []

    try:
        with open(file_csv,newline='') as massa:
            tabela = csv.reader(massa, delimiter=',')
            next(tabela)
            for linha in tabela:
                dados_csv.append(linha)
        return dados_csv
    except FileNotFoundError:
        print(f'Erro: Arquivo não encontrado: {file_csv}')
    except Exception as fail:
        print(f'Erro: Falha imprevista: {fail}')