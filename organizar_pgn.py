import os
import chess.pgn

# Caminho do diretório onde estão os arquivos PGN
path_pgn = r"C:\teste - origem"

# Caminho do diretório onde você quer salvar as partidas organizadas
path_destino = r"C:\teste - destino"

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
            year, month, day = date.split("/")

            last_dir = f"{day}{month}{year[2:]}"

            # Cria o diretório se ele não existir
            new_dir = os.path.join(path_destino, year, month, last_dir)
            os.makedirs(new_dir, exist_ok=True)

            # Move o arquivo para o novo diretório
            os.rename(os.path.join(path_pgn, filename), os.path.join(new_dir, filename))
