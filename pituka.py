from pandas import read_csv
from datetime import datetime
from numpy import where


def get_client():
    CLIENT: str = input(
        '\nNombre del Cliente:\n(Teclee ENTER para volver al menu principal)\n\n')
    return CLIENT


def get_time():
    return datetime.now().strftime("%Y/%m/%d %H:%M:%S")  # Tiempo de compra


def main():
    while True:
        productos = read_csv("productos.csv")
        clientes = read_csv("clientes.csv")
        CHOICE: str = input('\n###########################\n\nInserte 1 para iniciar una COMPRA\n\nInserte 2 para PAGAR una DEUDA\n\nInserte 3 para CONSULTAR el SALDO\n\nInserte 4 para hacer un respaldo de la base de datos\n\nInserte 5 para recibir mercancía\n\nInserte ENTER para salir\n\n########################\n\n')
        match CHOICE:
            case '1':
                CLIENT = get_client()
                purchase(CLIENT=CLIENT, productos=productos, clientes=clientes)
            case '2':
                CLIENT = get_client()
                payment(CLIENT=CLIENT, clientes=clientes)
            case '3':
                CLIENT = get_client()
                consult(CLIENT=CLIENT, clientes=clientes)
            case '4':
                snapshot()
            case '5':
                acquisition(productos=productos)
            case '':
                break
            case _:
                print('\nIngrese una opción válida!\n\n')


def purchase(CLIENT, productos, clientes):
    while CLIENT != '':
        if CLIENT in clientes.values:
            print('====================\n')
            TOTAL = 0.0  # $
            BOUGHT_PRODUCTS = []  # Lista de productos comprados
            TIME = get_time()  # Tiempo de compra
            ID = '123456789'  # Sample ID
            while ID != '':
                ID = input(
                    'Escanee el elemento a cobrar:\n(Teclee ENTER para cerrar el pedido)\n\n')
                if ID in productos.values:
                    print('--------------------------------------\n')
                    PRODUCT = productos[productos['ID'] == ID]
                    PRICE = float(PRODUCT["PRICE"].iloc[0])
                    NAME: str = str(PRODUCT["NAME"].iloc[0])
                    print(f'{NAME} : $ {PRICE}\n\n')
                    TOTAL += PRICE
                    BOUGHT_PRODUCTS += [ID]
                elif ID != '':
                    print(
                        '\nEse producto no existe\nIntente de nuevo\n!!!!!!!!!!!!!\nO pulse ENTER para cerrar el pedido\n')
            if BOUGHT_PRODUCTS == []:
                pass
            else:
                print(f'\nTotal : $ {TOTAL:.2f}\n\n')
                PREVIOUS_DEBT = clientes.iat[where(
                    clientes == CLIENT)[0][0], 1]
                print(f'{CLIENT} deberá un acumulado de {
                      PREVIOUS_DEBT + TOTAL} al finalizar esta compra.\n\n-------------------------------------------\n\n')
                PAID: str = input(
                    'Inserte CANTIDAD a pagar:\n(Teclee "0" o ENTER en caso de que no la cuenta se abone a crédito\n\n')
                PAID: float = 0.0 if (PAID == '') else float(
                    PAID)  # Lo que se paga en el momento
                DEBT: float = (PREVIOUS_DEBT + TOTAL) - PAID  # Deuda acumulada
                if DEBT < 0.0:
                    input(f'\n\nSu cambio es de $ {
                          DEBT * -1:.2f}\n\n(Inserte ENTER para continuar)')
                    clientes.iat[where(clientes == CLIENT)[0][0], 1] = 0
                else:
                    clientes.iat[where(clientes == CLIENT)[0][0], 1] = DEBT
                CURRENT_DEBT = clientes.iat[where(clientes == CLIENT)[0][0], 1]
                clientes.to_csv('clientes.csv', index=False)
                print(f'-------------------------------------\n\n¡Gracias por su compra!\n\n{
                      CLIENT} debe un total de $ {CURRENT_DEBT:.2f}\n\n====================\n')
                input('Pulse ENTER para continuar')
                # Almacenar pedido
                # Abrir documento de ventas solo en modo append
                ventas = open('ventas.csv', 'a')
                for GOOD in BOUGHT_PRODUCTS:
                    productos.iat[where(productos == GOOD)[0][0], 4] -= 1
                    productos.to_csv('productos.csv', index=False)
                    ORDER = f'"{CLIENT}",{GOOD},"{TIME}",{PAID}'
                    ventas.write(ORDER + '\n')
                ventas.close()
                break
        else:
            print('\nEse cliente no existe\nIntente de nuevo\n!!!!!!!!!!!!!\nO pulse ENTER para volver al menu principal\n')
            CLIENT = get_client()


def payment(CLIENT, clientes):
    while CLIENT != '':
        if CLIENT in clientes.values:
            TIME = get_time()  # Tiempo de compra
            print('====================\n\n')
            PREVIOUS_DEBT = clientes.iat[where(clientes == CLIENT)[0][0], 1]
            print(f'{CLIENT} debe un total de $ {
                  PREVIOUS_DEBT:.2f}\n\n--------------------------------\n')
            PAID: str = input(
                'Inserte CANTIDAD a pagar:\n(Teclee ENTER para cancelar y volver al menú principal.\n\n')
            PAID: float = 0.0 if (PAID == '') else float(
                PAID)  # Lo que se paga en el momento
            DEBT: float = PREVIOUS_DEBT - PAID  # Deuda acumulada
            if DEBT < 0.0:
                input(f'\n\nSu cambio es de $ {
                      DEBT * -1:.2f}\n\n(Inserte ENTER para continuar)')
                clientes.iat[where(clientes == CLIENT)[0][0], 1] = 0
            else:
                clientes.iat[where(clientes == CLIENT)[0][0], 1] = DEBT
            GOOD = 'depósito'
            # Abrir documento de ventas solo en modo append
            ventas = open('ventas.csv', 'a')
            ORDER = f'"{CLIENT}",{GOOD},"{TIME}",{PAID}'
            ventas.write(ORDER + '\n')
            ventas.close()
            CURRENT_DEBT = clientes.iat[where(clientes == CLIENT)[0][0], 1]
            clientes.to_csv('clientes.csv', index=False)
            print(f'-------------------------------------\nAhora {
                  CLIENT} debe un total de $ {CURRENT_DEBT:.2f}\n\n====================\n')
            input('Pulse ENTER para continuar')
            break
        else:
            print('\nEse cliente no existe\nIntente de nuevo\n!!!!!!!!!!!!!\n')
            CLIENT = get_client()


def consult(CLIENT, clientes):
    while CLIENT != '':
        if CLIENT in clientes.values:
            print('====================\n\n')
            TOTAL_DEBT = clientes.iat[where(clientes == CLIENT)[0][0], 1]
            clientes.to_csv('clientes.csv', index=False)
            print(f'{CLIENT} debe un total de $ {
                  TOTAL_DEBT:.2f}\n\n====================\n')
            input('Pulse ENTER para continuar')
            break
        else:
            print('\nEse cliente no existe\nIntente de nuevo\n!!!!!!!!!!!!!\n')
            CLIENT = get_client()


def acquisition(productos):
    TIME = get_time()
    ID = '12345'
    BOUGHT_PRODUCTS = []
    while ID != '':
        ID = input(
            'Escanee el elemento a cobrar:\n(Teclee ENTER para cerrar surtido)\n\n')
        if ID in productos.values:
            print('--------------------------------------\n')
            PRODUCT = productos[productos['ID'] == ID]
            # UNIT_PRICE = float(PRODUCT["UNIT_PRICE"].iloc[0])
            NAME: str = str(PRODUCT["NAME"].iloc[0])
            QUANTITY: str = input(f'Inserte la cantidad de {
                                  NAME} que se recibieron:\n\n')
            QUANTITY: int = 0 if (QUANTITY == '') else int(QUANTITY)
            BOUGHT_PRODUCTS += [ID]
            # Abrir documento de ventas solo en modo append
            inventario = open('inventario.csv', 'a')
        elif ID != '':
            print('\nEse producto no existe\nIntente de nuevo\n!!!!!!!!!!!!!\nO pulse ENTER para cerrar el pedido\n')
    if BOUGHT_PRODUCTS == []:
        pass
    else:
        for GOOD in BOUGHT_PRODUCTS:
            ORDER = f'"{GOOD}",{QUANTITY},"{TIME}"'
            productos.iat[where(productos == GOOD)[0][0], 4] += QUANTITY
            productos.to_csv('productos.csv', index=False)
            inventario.write(ORDER + '\n')
            inventario.close()


def snapshot():
    clientes_backup = read_csv("clientes.csv")
    ventas_backup = read_csv("ventas.csv")
    print('DONE ')
    TIME = get_time()
    clientes_backup.to_csv(f'Snapshots/clientes/{TIME}.csv', index=False)
    ventas_backup.to_csv(f'Snapshots/ventas/{TIME}.csv', index=False)

def donation():
    SPONSOR : str = input('Inserte el nombre del patrocinador:\n\n')
    


main()
