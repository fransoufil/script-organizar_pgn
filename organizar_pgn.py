import os
import chess.pgn
import re

# Caminho do diretório onde estão os arquivos PGN
path_pgn = r"C:\teste - origem"

# Caminho do diretório onde você quer salvar as partidas organizadas
path_destino = r"C:\teste - destino"

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

for filename in os.listdir(path_pgn):
    if filename.endswith('.pgn'):
        with open(os.path.join(path_pgn, filename)) as pgn_file:
            game = chess.pgn.read_game(pgn_file)

            # Fecha explicitamente o arquivo aqui
            pgn_file.close()

            if game is None:
                continue

            # Extraia a data do primeiro jogo no arquivo
            date = game.headers["Date"]
            # Use a função re.split para dividir a data
            year, month, day = re.split('[./-]', date)

            # Traduzir o número do mês para o nome do mês
            month_name = month_names[month.zfill(2)]

            # Concatenar o número do mês e o nome do mês
            month_folder = f"{month.zfill(2)}_{month_name}"

            last_dir = f"{day}{month}{year[2:]}"

            # Cria o diretório se ele não existir
            new_dir = os.path.join(path_destino, year, month_folder, last_dir)
            os.makedirs(new_dir, exist_ok=True)

            # Move o arquivo para o novo diretório
            os.rename(os.path.join(path_pgn, filename), os.path.join(new_dir, filename))
