import os
import chess.pgn
import re
import datetime
import shutil
import chardet

# pip install chardet --user

# Caminho do diretório onde estão os arquivos PGN
path_pgn = r"C:\pgn_origem"

# Caminho do diretório onde você quer salvar as partidas organizadas
path_destino = r"C:\pgn_destino"

# Mapeamento de números de mês para nomes
month_names = {
    '1': 'janeiro', '01': 'janeiro',
    '2': 'fevereiro', '02': 'fevereiro',
    '3': 'março', '03': 'março',
    '4': 'abril', '04': 'abril',
    '5': 'maio', '05': 'maio',
    '6': 'junho', '06': 'junho',
    '7': 'julho', '07': 'julho',
    '8': 'agosto', '08': 'agosto',
    '9': 'setembro', '09': 'setembro',
    '10': 'outubro',
    '11': 'novembro',
    '12': 'dezembro'
}

# Contadores
successes = 0
failures = 0


def process_file(filename, path_pgn, path_destino):
    try:
        # Detectar a codificação do arquivo
        with open(os.path.join(path_pgn, filename), 'rb') as pgn_file:
            raw_data = pgn_file.read()
            encoding = chardet.detect(raw_data)['encoding']

        # Abrir o arquivo com a codificação detectada
        with open(os.path.join(path_pgn, filename), encoding=encoding) as pgn_file:
            game = chess.pgn.read_game(pgn_file)
            # Fecha explicitamente o arquivo aqui
            pgn_file.close()

            if game is None:
                return False

            # Extrai a data do cabeçalho "Date" ou obtém a data de modificação do arquivo
            if "Date" in game.headers:
                date = game.headers["Date"]
            else:
                date = os.path.getmtime(os.path.join(path_pgn, filename))
                # Converter o timestamp da data de modificação em uma string de data
                date = datetime.datetime.fromtimestamp(date).strftime('%Y-%m-%d')

            # Use a função re.split para dividir a data
            year, month, day = re.split('[./-]', date)

            # Traduzir o número do mês para o nome do mês
            if month.zfill(2) in month_names:
                month_name = month_names[month.zfill(2)]
            else:
                # Se o número do mês for inválido, use o mês atual
                now = datetime.datetime.now()
                month = str(now.month).zfill(2)
                month_name = month_names[month]

            # Concatenar o número do mês e o nome do mês
            month_folder = f"{month.zfill(2)}_{month_name}"

            last_dir = f"{day}{month}{year[2:]}"

            # Cria o diretório se ele não existir
            new_dir = os.path.join(path_destino, year, month_folder, last_dir)
            os.makedirs(new_dir, exist_ok=True)

            # Move o arquivo para o novo diretório
            shutil.move(os.path.join(path_pgn, filename), os.path.join(new_dir, filename))
            return True
    except Exception as e:
        print(f"Erro ao mover o arquivo {filename}: {e}")
        return False


def process_directory(directory, path_pgn, path_destino):
    global successes, failures
    for root, dirs, files in os.walk(directory):
        for filename in files:
            if filename.endswith('.pgn'):
                success = process_file(filename, root, path_destino)
                if success:
                    successes += 1
                else:
                    failures += 1


process_directory(path_pgn, path_pgn, path_destino)

print(f"Arquivos movidos com sucesso: {successes}")
print(f"Arquivos não movidos: {failures}")
