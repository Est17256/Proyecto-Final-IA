#Universidad del Valle de Guatemala
#Inteligencia Artificial
#Proyecto Totito Chino
#Luis Esturbán 17256
#02/06/2020

#Se importan las librerias necesarias para el funcionamiento
import random
import math
import socketio
#Datos para la conexion con el servidor
sio = socketio.Client()
address = 'http://localhost:4000'
sio.connect(address)
userName = 'LuisEsturban'
tournamentID = 1
#Funcion que implementa el max
def Minimax_MAX(BRD, PN, alpha, beta, look):
    SCR1 = -math.inf
    BTM = []
    SCR2 = CNT2 = 0
    if look > 2:
        SCR,x = PTS(BRD, PN, [0,0])
        return SCR, []
    for i in BRD:
        CNT3 = 0
        for j in i:
            if j == 99:
                NBRD = GME(BRD, PN, [CNT2, CNT3])
                SCR2,x = PTS(BRD, PN, [CNT2, CNT3])
                SCR1 = SCR2
                BTM =  [CNT2, CNT3]
                if PN == 1:
                    PN = 2
                else:
                    PN = 1
                look = look + 1
                SCR, x = Minimax_MIN(NBRD,PN,alpha,beta, look)
                if SCR >= alpha:
                    alpha = SCR
                    SCR1 = SCR
            CNT3 = CNT3 + 1
        CNT2 = CNT2 + 1
    return SCR1, BTM  
#Funcion que se encarga de controlar las jugadas para el tablero
def GME(BRD, PN, MOV):
    PNT1 = PNT2 = 0
    PNT2,PNT1=PTS(BRD, PN, MOV)
    if PNT1 < PNT2:
        if PN == 1:
            if (PNT2 - PNT1) == 2:
                BRD[MOV[0]][MOV[1]] = 2
            elif (PNT2 - PNT1) == 1:
                BRD[MOV[0]][MOV[1]] = 1
        elif PN == 2:
            if (PNT2 - PNT1) == 2:
                BRD[MOV[0]][MOV[1]] = -2
            elif (PNT2 - PNT1) == 1:
                BRD[MOV[0]][MOV[1]] = -1
    return BRD
#Funcion que implementa el min
def Minimax_MIN(BRD, PN, alpha, beta, look):
    SCR1 = math.inf
    BTM = []
    SCR2 = 0
    if look > 2:
        SCR,x = PTS(BRD, PN, [0,0])
        return SCR, []
    CNT2 = 0
    SCR1 = math.inf
    for i in BRD:
        CNT3 = 0
        for j in i:
            if j == 99:
                NBRD = GME(BRD, PN, [CNT2, CNT3])
                SCR2,x = PTS(BRD, PN, [CNT2, CNT3])
                SCR1 = SCR2
                BTM =  [CNT2, CNT3]
                if PN == 1:
                    PN = 2
                else:
                    PN = 1
                SCR, x = Minimax_MAX(NBRD,PN,0,0,look + 1)
                if SCR < beta:
                    SCR1 = SCR
                    beta = SCR2
            CNT3 = CNT3 + 1
        CNT2 = CNT2 + 1
    return SCR1, BTM
#Funcion que se encarga de llevar a cabo el control del punteo
def PTS(BRD, PN, MOV):
    PNT1 = PNT2 = CNT1 = CNT2 = 0
    for i in range(len(BRD[0])):
        if ((i + 1) % 6) != 0:
            if BRD[0][i] != 99 and BRD[0][i + 1] != 99 and BRD[1][CNT2 + CNT1] != 99 and BRD[1][CNT2 + CNT1 + 1] != 99:
                PNT1 = PNT1 + 1
            CNT1 = CNT1 + 6
        else:
            CNT2 = CNT2 + 1
            CNT1 = 0
    BRD[MOV[0]][MOV[1]] = 0
    CNT1 = CNT2 = 0
    for i in range(len(BRD[0])):
        if ((i + 1) % 6) != 0:
            if BRD[0][i] != 99 and BRD[0][i + 1] != 99 and BRD[1][CNT2 + CNT1] != 99 and BRD[1][CNT2 + CNT1 + 1] != 99:
                PNT2 = PNT2 + 1
            CNT1 = CNT1 + 6
        else:
            CNT2 = CNT2 + 1
            CNT1 = 0
    return PNT2,PNT1
#Funcion para poder conectarse al servidor
@sio.on('connect')
def connect():
    sio.emit('signin', {'user_name' : userName,'tournament_id' : tournamentID,'user_role' : 'player'})
    print("La conexion fue exitosa")
#Funcion para poder indicar que ya esta listo para jugar y poder enviar el movimiento al servidor
@sio.on('ready')
def ready(data):
    MOV = []
    x, MOV = Minimax_MAX(data['board'], data['player_turn_id'], 0, 0, 0)
    sio.emit('play', {'player_turn_id' : data['player_turn_id'],'tournament_id' : tournamentID,'game_id' : data['game_id'],'movement': MOV})
#Funcion para poder indicar que ya se termino el juego y esta listo para volver a jugar
@sio.on('finish')
def finish(data):
    print("La partida termino, listo para volver a jugar")
    sio.emit('player_ready', {'tournament_id' : tournamentID,'game_id' : data['game_id'],'player_turn_id': data['player_turn_id']})