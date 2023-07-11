import datetime
import time


# Defina os horários de início e término da contagem regressiva
with open('configuracao.txt') as configs:
    infos = configs.read().splitlines()
    horario_inicio_str = infos[0].strip('horario_inicio=')
    horario_fim_str = infos[1].strip('horario_fim=')
    print(f'horario_inicio = {horario_inicio_str}', f'horario_fim = {horario_fim_str}')

# Obtenha o horário atual
horario_atual_str = datetime.datetime.now().strftime('%H:%M:%S')
horario_atual = datetime.datetime.strptime(horario_atual_str, '%H:%M:%S')

# Converta os horários de início e término para objetos datetime
horario_inicio = datetime.datetime.strptime(horario_inicio_str, '%H:%M')
horario_fim = datetime.datetime.strptime(horario_fim_str, '%H:%M')

with open('contagem_regressiva.txt', 'w') as arquivo:
        arquivo.write('')

# Aguarde até o horário de início ser alcançado
while horario_atual < horario_inicio:
    horario_atual_str = datetime.datetime.now().strftime('%H:%M:%S')
    horario_atual = datetime.datetime.strptime(horario_atual_str, '%H:%M:%S')
    print(horario_atual_str)
    time.sleep(0.5)

# Loop para atualizar o contador regressivo até o horário de término
while horario_atual < horario_fim:
    # Obtenha o horário atual
    horario_atual_str = datetime.datetime.now().strftime('%H:%M:%S')
    horario_atual = datetime.datetime.strptime(horario_atual_str, '%H:%M:%S')

    # Calcula o tempo restante
    minutos_restantes = int((horario_fim - horario_atual).total_seconds())
    minutos_restantes_str = f'{minutos_restantes//60:02}:{minutos_restantes%60:02}'


    # Atualizar o arquivo contagem_regressiva.txt
    with open('contagem_regressiva.txt', 'w') as arquivo:
        arquivo.write(minutos_restantes_str)

    # Aguardar 1 segundo antes de atualizar o contador novamente
    time.sleep(1)


# Após a contagem regressiva ter terminado
with open('contagem_regressiva.txt', 'w') as arquivo:
    arquivo.write('00:00')
