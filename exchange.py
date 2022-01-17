import csv
from ntpath import join
import os
from datetime import datetime
from pprint import pprint
import pandas as pd

class Exchange():
    def __init__(self, nombre = "billetera", cripto = "BTC"):
        '''
        Recibe el nombre que tendrá el archivo .csv y define su ruta
        Tambien recibe la primer criptomoneda que registrará, además de USDT.
        Los parámetros son opcionales
        '''
        self.cripto = cripto.upper()
        self.nombre = f'{nombre}.csv'
        self.directorio_actual = os.path.dirname(os.path.realpath(__file__))
    
    def __str__(self):
        return f'Billetera de criptomonedas, iniciada con {self.cripto}'

    def crearBilletera(self):
        '''
        Primer método que se ejecuta. Crea el archivo CSV y el encabezado.
        Si el archivo ya está creado, devuelve un comentario 
        '''
        os.chdir(self.directorio_actual)
        if self.nombre in os.listdir(self.directorio_actual):
            return print("La billetera ya ha sido creada =)")

        with open(self.nombre, "w", newline="") as billetera:
            writer = csv.writer(billetera)
            writer.writerow(["Tenencia en USDT", f"Tenencia en {self.cripto}", "Ultima modificacion"])

        with open(f'Transacciones-{self.cripto}.csv', "w", newline="") as transacciones:
            writer = csv.writer(transacciones)
            writer.writerow(["Fecha", "Orden", f"Monto {self.cripto}", "Precio", f"Monto USDT"])

    def estaVacia(self):
        '''
        Verifica si la billetera no posee ningún registro.
        '''
        os.chdir(self.directorio_actual)
        with open(self.nombre, "r") as billetera:
            filas = billetera.readlines() 
            return True if len(filas) < 2 else False       

    def poseeTransacciones(self, cripto):
        '''
        Recibe una criptomoneda
        Verifica si el registro de transacciones con esa cripto posee ningún registro.
        '''
        cripto = cripto.upper()
        os.chdir(self.directorio_actual)
        with open(f'Transacciones-{self.cripto}.csv', "r") as transacciones:
            filas = transacciones.readlines() 
            return False if len(filas) < 2 else True 

    def fondos(self):
        '''
        Devuelve un diccionario, con el resumen de los fondos disponibles
        key = encabezados, values = valores última fila
        '''
        os.chdir(self.directorio_actual)
        with open(self.nombre, "r") as billetera:
            filas = billetera.readlines() 
            encabezados = filas[0].split(",")
            encabezados[-1] = encabezados[-1].replace('\n', "")

            if self.estaVacia():
                ultima_fila = [0,0,"-"]
            else:
                ultima_fila = filas[-1].split(",")
                ultima_fila[-1] = ultima_fila[-1].replace('\n', "")

            tenencia = dict(zip(encabezados, ultima_fila))

            for k, v in tenencia.items():
                try:
                    tenencia[k] = round(float(v), 7)
                except:
                    continue
            return tenencia

    def tenencia(self, cripto):
        '''
        Recibe un tipo de criptomoneda y devuelve la tenencia actual registrada
        '''
        cripto = cripto.upper()
        tenencia = self.fondos()
        return tenencia[f'Tenencia en {cripto}']

    def ingresar(self, cripto, monto, fecha):
        '''
        Recibe un tipo de criptomoneda y el monto ingresado a la billetera
        Suma esta moneda al total de la billetera
        '''
        cripto = cripto.upper()
        tenencia = self.fondos()

        if self.estaVacia() == True: # Creo primer registro  
            tenencia[f'Tenencia en {cripto}'] = monto 
        else: # Aumento el monto de la cripto
            tenencia[f'Tenencia en {cripto}'] += monto

        if cripto=="USDT":
            tenencia[f'Tenencia en {cripto}'] = round (tenencia[f'Tenencia en {cripto}'], 2)
        tenencia[f'Ultima modificacion'] = fecha
        registro = list(tenencia.values()) 

        with open(self.nombre, "a", newline="") as billetera: # "a": agregar fila nueva, newline="" evita creacion salto de linea
            writer = csv.writer(billetera)
            writer.writerow(registro)   

    def retirar(self, cripto, monto):
        '''
        Recibe un tipo de criptomoneda y el monto ingresado a la billetera
        Verifica si hay fondos suficientes
        Resta esta moneda al total de la billetera
        '''
        # Verifica
        if self.tenencia(cripto) < monto:
        # tenencia = self.fondos()
        # if tenencia[f'Tenencia en {cripto}'] < monto:
            return print("Fondos insuficientes para retirar ese monto.")
        else:
        # Retira
            self.ingresar(cripto, -monto)


    def agregarCripto(self, cripto):
        '''
        Agrega una nueva criptomoneda a la billetera.
        Los campos anteriores se completan en cero.
        '''
        pass

    
    def registrar(self, cripto, monto_cripto, monto_usdt, fecha):
        '''
        Recibe una transacción y registra los cambios en la billetera.
        Si el monto es positivo se toma como compra, si es negativo se toma como venta.
        '''
        # Validacion por si la billetera está vacia
        if self.estaVacia() == True:
            return print("Primero es necesario ingresar dinero a tu billetera")

        # Obtengo ultimo registro
        tenencia = self.fondos()

        # Convierto a float los valores para poder sumarlos
        tenencia_cripto = float((tenencia[f'Tenencia en {cripto}']))
        tenencia_usdt = float(tenencia[f'Tenencia en USDT'])
        tenencia_cripto += monto_cripto
        tenencia_usdt -= monto_usdt
        

        # Creo nuevo tenencia, actualizado
        tenencia[f'Tenencia en {cripto}'] = tenencia_cripto
        tenencia[f'Tenencia en USDT'] = round(tenencia_usdt,2)
        tenencia[f'Ultima modificacion'] = fecha
        registro = list(tenencia.values())
        
        # Agrego registro al archivo
        with open(self.nombre, "a", newline="") as billetera: # "a" para que agrege fila nueva, newline="" para que no cree un salto de linea
            writer = csv.writer(billetera)
            writer.writerow(registro)    
    
    def comprar(self, cripto, monto_usdt, precio, fecha):
        '''
        Recibe una cripto, el monto a desembolsar y el precio de compra y lo registra en el csv de transacciones.
        '''
        # Validaciones
        if self.estaVacia() == True:
            return print("Primero es necesario ingresar dinero a tu billetera")

        if self.tenencia("USDT") < monto_usdt:
            return print("No hay fondos suficientes para hacer esta compra")              

        # Armo el registro
        cripto = cripto.upper()
        monto_usdt = round(float(monto_usdt), 7)
        precio = float(precio)
        fee = 0.001 # Comisión del exchange, en este caso Binance
        monto_cripto = monto_usdt / precio * (1-fee)
        monto_cripto = round(monto_cripto, 7) 
        registro = [fecha, "Compra", monto_cripto, precio, monto_usdt]

        # Agrego registro al archivo
        with open(f'Transacciones-{self.cripto}.csv', "a", newline="") as transacciones: # "a" para que agrege fila nueva, newline="" para que no cree un salto de linea
            writer = csv.writer(transacciones)
            writer.writerow(registro)
        
        # Actualizo billetera
        self.registrar(cripto, monto_cripto, monto_usdt, fecha)

        return print("¡Compra realizada exitosamente!")

    def vender(self, cripto, monto_cripto, precio, fecha):
        '''
        Recibe una cripto, el monto de la misma a vender y el precio de venta y lo registra en el csv de transacciones.
        '''
        cripto = cripto.upper()
        # Validaciones
        if self.estaVacia() == True:
            return print("Primero es necesario ingresar dinero a tu billetera")

        if self.tenencia(cripto) == 0:
            return print("No hay fondos suficientes para hacer esta compra")              
        elif self.tenencia(cripto) < monto_cripto:
            monto_cripto = self.tenencia(cripto) 
        
        # Armo el registro
        monto_cripto = round(float(monto_cripto), 7)
        precio = float(precio)
        fee = 0.001 # Comisión del exchange, en este caso Binance
        monto_usdt = monto_cripto * precio * (1-fee)
        monto_usdt = round(monto_usdt, 7) 
        
        registro = [fecha, "Venta", monto_cripto, precio, monto_usdt]
        
        # Agrego registro al archivo
        with open(f'Transacciones-{self.cripto}.csv', "a", newline="") as transacciones: # "a" para que agrege fila nueva, newline="" para que no cree un salto de linea
            writer = csv.writer(transacciones)
            writer.writerow(registro)
        
        # Actualizo billetera
        self.registrar(cripto, -monto_cripto, -monto_usdt, fecha)

        return print("Venta realizada exitosamente!")

    
    def tenenciaMaximaEn(self, cripto, fecha = False):
        '''
        Recibe un tipo de criptomoneda y devuelve:
        1) El valor maximo de tenencia en esa cripto
        2) Dataframe con fechas de los picos historicos de tenencia de esa cripto
        '''
        # Validación
        if self.estaVacia() == True:
            return print("No hay registros aún")

        # Busqueda del maximo
        os.chdir(self.directorio_actual)
        df = pd.read_csv(self.nombre)
        maximoValor = df[f'Tenencia en {cripto}'].max()
        fechas_pico = df[df[f'Tenencia en {cripto}'] == maximoValor]

        if fecha:
            return fechas_pico
        else:
            return round(maximoValor, 7) 

    def mayorCompra(self, cripto, orden = "Compra"):
        '''
        Recibe un tipo de criptomoneda
        Devuelve un dataframe con el o los registros de las compras mas grandes
        '''
        # Validación
        if self.poseeTransacciones(cripto) == False:
            return print("No hay registros aún")

        # Busqueda de la maxima compra
        os.chdir(self.directorio_actual)
        df = pd.read_csv(f'Transacciones-{self.cripto}.csv')
        df_compras = df[df['Orden'] == orden]
        maximoValor = df_compras[f'Monto {cripto.upper()}'].max()
        registro = df[df[f'Monto {cripto.upper()}'] == maximoValor]
        return registro                

    def mayorVenta(self, cripto):
        '''
        Recibe un tipo de criptomoneda
        Devuelve un dataframe con el o los registros de las ventas mas grandes
        '''
        return self.mayorCompra(cripto,"Venta")
    
    
# ----------- PRUEBAS -------------

if __name__=="__main__":
    '''
    ## Billetera

    ex = Exchange("billetera", "BTC")

    print(ex)

    ex.crearBilletera()
    print("Fondos al momento cero: ", ex.fondos())

    ex.ingresar("USDT", 250, "01/01/2021 00:00)
    ex.ingresar("BTC", 0.0005, "01/01/2021 00:00)
    print("Fondos luego de ingresos: ", ex.fondos())

    ex.retirar("USDT", 50)
    print("Fondos luego de retiro: ", ex.fondos())

    print("Tenencia en Bitcoin: ", ex.tenencia("BTC"))

    ## Transacciones (Corregir metodos)

    ex.comprar("BTC",0.00025, 61521.37)
    print("Fondos luego de comprar: ", ex.fondos())

    ex.vender("BTC",0.00004, 68821.12)
    print("Fondos luego de vender: ", ex.fondos())

    ex.comprar("BTC",0.00015, 63521.77)
    ex.vender("BTC",0.00020, 79821.12)
    ex.comprar("BTC",0.00035, 55521.34)
    ex.vender("BTC",0.00030, 69821.18)

    print(ex.tenenciaMaximaEn("BTC", fecha = True))
    print(ex.tenenciaMaximaEn("BTC"))

    print(ex.mayorCompra("BTC"))
    print(ex.mayorVenta("USDT"))
    '''