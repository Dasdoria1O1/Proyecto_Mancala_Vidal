#!/usr/bin/env python3

def inicializar_tablero(semillas_por_hoyo=4):
    # Índices 0 a 5: hoyos del Jugador 1, índice 6: almacén del Jugador 1.
    # Índices 7 a 12: hoyos del Jugador 2, índice 13: almacén del Jugador 2.
    tablero = [semillas_por_hoyo] * 14
    tablero[6] = 0   # almacén del Jugador 1
    tablero[13] = 0  # almacén del Jugador 2
    return tablero

def mostrar_tablero(tablero):
    # Se muestra el tablero con la numeración de los hoyos (1 a 6) tanto en la parte superior
    print("\n           [Hoyo]")
    # Numeración superior: hoyos del jugador 2 (índices 12 a 7) en orden inverso (6,5,...,1)
    print("     ", end="")
    for num in range(6, 0, -1):
        print(f" {num} ", end="")
    print("\n   ---------------------")
    
    # hoyos del Jugador 2 (índices 12 a 7)
    print("   |", end=" ")
    for i in range(12, 6, -1):
        print(f"{tablero[i]:2d}", end=" ")
    print("|")
    
    # almacén del Jugador 2 (índice 13) a la izquierda y Jugador 1 (índice 6) a la derecha.
    print(f"{tablero[13]:2d} ", end="")
    print("|" + " " * 19 + f"| {tablero[6]:2d}")
    
    # hoyos del Jugador 1 (índices 0 a 5)
    print("   |", end=" ")
    for i in range(0, 6):
        print(f"{tablero[i]:2d}", end=" ")
    print("|")
    
    print("   ---------------------")
    # Numeración inferior para el Jugador 1: hoyos (1 a 6)
    print("     ", end="")
    for num in range(1, 7):
        print(f" {num} ", end="")
    print("\n           [Hoyo]\n")

def indice_opuesto(i):
    # Relación opuesta: 0 <-> 12, 1 <-> 11, 2 <-> 10, 3 <-> 9, 4 <-> 8, 5 <-> 7.
    return 12 - i

def es_lado(jugador, i):
    # Retorna True si el hoyo i pertenece al jugador
    if jugador == 1 and 0 <= i <= 5:
        return True
    if jugador == 2 and 7 <= i <= 12:
        return True
    return False

def realizar_jugada(tablero, jug, pit):
    """
    Ejecuta una jugada para el jugador (1 o 2) seleccionando el hoyo 'pit'
    (para jugador 1: 1-6, para jugador 2: 1-6 que corresponden a índices 7-12)
    Devuelve:
      - tablero: tablero actualizado.
      - turno_extra: True si el jugador obtiene turno extra.
      - jugada_valida: True si la jugada se realizó, False en caso de error (p.ej. hoyo vacío).
    """
    # Convertir la selección de hoyo a índice del tablero
    if jug == 1:
        idx = pit - 1  # Hoyos 1-6 -> índices 0 a 5
    else:  # jugador 2
        idx = pit + 6  # Hoyos 1-6 -> índices 7 a 12

    # Revisar que el hoyo elegido tenga semillas
    if tablero[idx] == 0:
        print("Ese hoyo está vacío. Elige otro.")
        return tablero, False, False  # turno_extra=False, jugada_valida=False

    semillas = tablero[idx]
    tablero[idx] = 0
    current = idx
    while semillas > 0:
        current = (current + 1) % 14
        # Saltar el almacén del oponente:
        if jug == 1 and current == 13:
            continue
        if jug == 2 and current == 6:
            continue
        tablero[current] += 1
        semillas -= 1

    turno_extra = False

    # Verificar turno extra: la última semilla cayó en el almacén del jugador.
    if jug == 1 and current == 6:
        turno_extra = True
    elif jug == 2 and current == 13:
        turno_extra = True

    # Verificar captura: la última semilla cayó en un hoyo vacío de tu lado
    # y el hoyo opuesto (del adversario) tiene al menos una semilla.
    if not turno_extra and es_lado(jug, current) and tablero[current] == 1:
        opp = indice_opuesto(current)
        if tablero[opp] > 0:
            capturadas = tablero[opp] + tablero[current]
            tablero[opp] = 0
            tablero[current] = 0
            # Depositar en el almacén correspondiente
            if jug == 1:
                tablero[6] += capturadas
            else:
                tablero[13] += capturadas

    return tablero, turno_extra, True  # jugada_valida True

def comprobar_fin(tablero):
    # El juego termina si todos los hoyos de un jugador están vacíos.
    lado1 = sum(tablero[i] for i in range(0, 6))
    lado2 = sum(tablero[i] for i in range(7, 13))
    return lado1 == 0 or lado2 == 0

def recolectar_restantes(tablero):
    # Si el juego termina, se llevan las semillas restantes al almacén correspondiente.
    lado1 = sum(tablero[i] for i in range(0, 6))
    lado2 = sum(tablero[i] for i in range(7, 13))
    for i in range(0, 6):
        tablero[i] = 0
    for i in range(7, 13):
        tablero[i] = 0
    tablero[6] += lado1
    tablero[13] += lado2
    return tablero

def determinar_ganador(tablero):
    if tablero[6] > tablero[13]:
        return 1
    elif tablero[13] > tablero[6]:
        return 2
    else:
        return 0  # empate

def jugar():
    tablero = inicializar_tablero()
    turno = 1  # Jugador 1 comienza (se puede alternar o decidir aleatoriamente)
    print("Bienvenidos a Mancala - Jugador vs Jugador")
    while True:
        mostrar_tablero(tablero)
        print(f"Turno del Jugador {turno}")
        # Solicitar la selección de hoyo: debe ser un número 1-6.
        try:
            pit = int(input("Elige un hoyo (1-6): "))
        except ValueError:
            print("Debes introducir un número.")
            continue

        if pit < 1 or pit > 6:
            print("El número debe estar entre 1 y 6.")
            continue

        # Realizar la jugada; si la jugada no es válida se repetira jugada
        tablero, extra, jugada_valida = realizar_jugada(tablero, turno, pit)
        if not jugada_valida:
            continue

        # Verificar si el juego termina
        if comprobar_fin(tablero):
            tablero = recolectar_restantes(tablero)
            mostrar_tablero(tablero)
            ganador = determinar_ganador(tablero)
            if ganador == 0:
                print("¡El juego termina en empate!")
            else:
                print(f"¡El Jugador {ganador} gana!")
            break

        # Si se obtuvo turno extra, el mismo jugador continúa
        if extra:
            print("Obtienes un turno extra")
        else:
            turno = 2 if turno == 1 else 1

def menu_principal():
    while True:
        print("Bienvenido a Mancala")
        print("1: Jugador vs Jugador")
        print("2: Jugador vs Computadora")
        print("0: Salir")
        try:
            opcion = int(input("Elige una opción: "))
        except ValueError:
            print("Debes introducir un número.")
            continue

        if opcion == 1:
            jugar()
        elif opcion == 2:
            print("La opción Jugador vs Computadora aún no está desarrollada.")
        elif opcion == 0:
            print("Gracias por jugar")
            break
        else:
            print("Opción no válida. Intenta de nuevo.")

if __name__ == "__main__":
    menu_principal()