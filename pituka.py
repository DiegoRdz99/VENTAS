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
        CHOICE: str = input('\n###########################\n\nInserte 1 para iniciar una COMPRA\n\nInserte 2 para PAGAR una DEUDA\n\nInserte 3 para CONSULTAR el SALDO\n\nInserte 4 PARA CAMBIAR DINERO\n\nInserte 5 para recibir mercancía\n\nInserte 6 para hacer un conteo de caja con desglose\n\nInserte ENTER para salir\n\n########################\n\n')
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
                # snapshot()
            case '5':
                acquisition(productos=productos)
            case '6':
                contar_caja()
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
                cash(PAID,True) # Para el conteo de monedas
                DEBT: float = (PREVIOUS_DEBT + TOTAL) - PAID  # Deuda acumulada
                if DEBT < 0.0:
                    CHANGE = DEBT * -1
                    print(f'\n\nSu cambio es de $ {CHANGE:.2f}\n')
                    cash(CHANGE,False)
                    input(f'\n(Inserte ENTER para continuar)\n')
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
            print(f'{CLIENT} debe un total de $ {PREVIOUS_DEBT:.2f}\n\n--------------------------------\n')
            PAID: str = input(
                'Inserte CANTIDAD a pagar:\n(Teclee ENTER para cancelar y volver al menú principal.\n\n')
            PAID: float = 0.0 if (PAID == '') else float(
                PAID)  # Lo que se paga en el momento
            cash(PAID,True)
            DEBT: float = PREVIOUS_DEBT - PAID  # Deuda acumulada
            if DEBT < 0.0:
                CHANGE = DEBT * -1
                print(f'\n\nSu cambio es de $ {CHANGE:.2f}\n')
                cash(CHANGE,False)
                input(f'\n(Inserte ENTER para continuar)\n')
                clientes.iat[where(clientes == CLIENT)[0][0], 1] = 0
            else:
                clientes.iat[where(clientes == CLIENT)[0][0], 1] = DEBT
            # Abrir documento de ventas solo en modo append
            depositos = open('depositos.csv', 'a')
            ORDER = f'"{CLIENT}","{TIME}",{PAID:.2f},{CHANGE:.2f}'
            depositos.write(ORDER + '\n')
            depositos.close()
            CURRENT_DEBT = clientes.iat[where(clientes == CLIENT)[0][0], 1]
            clientes.to_csv('clientes.csv', index=False)
            print(f'-------------------------------------\nAhora {CLIENT} debe un total de $ {CURRENT_DEBT:.2f}\n\n====================\n')
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
            'Escanee el elemento recibido:\n(Teclee ENTER para cerrar surtido)\n\n')
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


def donation():
    SPONSOR: str = input('Inserte el nombre del patrocinador:\n\n')


def contar_caja():
    caja = read_csv("caja.csv")
    SUM = 0.0
    print('\n\n=======================\n\nActualmente en caja:\n')
    print(f'{int(caja.iat[0, 1])}\tmonedas de $ 0.50')  # Monedas de 0.50
    SUM += caja.iat[0, 1] * 0.50  # Suma de cada denominación
    for i in range(1, 10):
        CURRENCY = caja.iat[i, 0]
        QUANTITY = caja.iat[i, 1]
        CASH_MODE = 'monedas' if CURRENCY < 20 else 'billetes'
        print(f'{int(QUANTITY)}\t{CASH_MODE} de $ {int(CURRENCY)}')
        SUM += CURRENCY * QUANTITY  # Suma de cada denominación
    print(
        f'\n------------------\n\nTOTAL: ${SUM:.2f}\n\n======================')
    input('\nPresione ENTER para continuar')


def cash(QUANTITY,ADDITIVE):
    ADDITIVE : int = 1 if ADDITIVE else -1
    caja = read_csv("caja.csv")
    currencies = [500, 200, 100, 50, 20, 10, 5, 2, 1, 0.5]
    while QUANTITY > 0:
        for CURRENCY in currencies:
            if QUANTITY >= CURRENCY:
                CASH_MODE = 'monedas' if CURRENCY < 20 else 'billetes'
                COIN_NUMBER: str = input(f'Cantidad de {CASH_MODE} de $ {CURRENCY}:\t')
                COIN_NUMBER: float = 0 if COIN_NUMBER == '' else int(COIN_NUMBER)
                SUBSTRACT = COIN_NUMBER * CURRENCY
                QUANTITY -= SUBSTRACT
                caja.iat[where(caja == CURRENCY)[0][0], 1] += ADDITIVE * COIN_NUMBER
        if QUANTITY > 0:
            print(f'Todavía faltan $ {QUANTITY:.2f}!\n')
    caja.to_csv('caja.csv',index=False)


main()
