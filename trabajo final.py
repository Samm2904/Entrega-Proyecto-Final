import sqlite3
from colorama import Fore, Style, Back, init
init (autoreset=True)

conexion = sqlite3.connect("inventario.db")
cursor = conexion.cursor()

#Creando la tabla
cursor.execute('''
    CREATE TABLE IF NOT EXISTS productos (
         id INTEGER PRIMARY KEY AUTOINCREMENT,
         nombre TEXT NOT NULL,
         descripcion TEXT,
         cantidad INTEGER NOT NULL,
         precio REAL NOT NULL,
         categoria TEXT
        )
''')
conexion.commit()
conexion.close()

#fijarse la documentacion

def agregar_producto():
    """
    Agrega un nuevo producto a la base de datos de inventario.

    Solicita al usuario los detalles del producto (nombre, descripción,
    cantidad, precio y categoría), valida las entradas y, si son válidas,
    inserta el producto en la tabla 'productos'. Maneja errores de base de datos
    y de entrada del usuario.
    Si la inserción es exitosa, muestra un mensaje de confirmación con la fecha y hora actual.
    Si ocurre un error, muestra un mensaje de error específico.
    Si el producto ya existe, muestra un mensaje de error de integridad.

    """
    #Conectando a la base de datos.
    conexion = sqlite3.connect('inventario.db')
    cursor = conexion.cursor()
       
    try:
        #Se ingresan los datos del producto.
        print(Fore.GREEN+Style.BRIGHT+f"\n{Back.BLACK}--- Agregar producto ---{Style.RESET_ALL}\n")  
        nombre = input(Fore.LIGHTCYAN_EX+"Ingrese el nombre del producto: "+Style.RESET_ALL).strip().capitalize() 
        descripcion = input(Fore.LIGHTCYAN_EX+"Ingrese la descripcion del producto: "+Style.RESET_ALL).strip().capitalize()
        cantidad = input(Fore.LIGHTCYAN_EX+"Ingrese la cantidad del producto: "+Style.RESET_ALL)

        #Se valida la cantidad ingresada.
        if not cantidad.isdigit():
            print(Fore.RED + "ERROR: La cantidad debe ser un número entero válido.")
            return
        cantidad = int(cantidad)
        if cantidad < 0:
            print(Fore.RED + "ERROR: La cantidad no puede ser negativa.")
            return
        
        precio = input(Fore.LIGHTCYAN_EX+"Ingrese el precio del producto: "+Style.RESET_ALL).strip()
        #Se valida el precio ingresado.
        try:
            precio = float(precio)
        except ValueError:
            print(Fore.RED + "ERROR: El precio debe ser un número válido.")    
            return    
        except Exception as e:
            print(Fore.RED + "ERROR: El precio no puede ser negativo.")
            return

        categoria = input(Fore.LIGHTCYAN_EX+"Ingrese la categoria del producto: "+Style.RESET_ALL).strip().capitalize()
        #Se valida que los campos no esten vacios.
        #Si alguno de los campos esta vacio, se muestra un mensaje de error.
        if not nombre or not descripcion or not categoria: 
            print(Fore.RED + "ERROR: Todos los campos son obligatorios y deben ser válidos.")
            return   
        
        #Se inserta el producto en la base de datos, cuidando de las posibles inyecciones en SQL.
        cursor.execute('''
                        INSERT INTO productos (nombre,descripcion,cantidad,precio,categoria) 
                        VALUES (?, ?, ?, ?, ?)
                        ''', (nombre, descripcion, cantidad, precio, categoria))
        
        conexion.commit()
        print(Fore.LIGHTGREEN_EX+Style.BRIGHT + f"\nProducto '{nombre}' agregado exitosamente el {conexion.execute('SELECT datetime("now")').fetchone()[0]}.")

    except sqlite3.Error as e:
        print(Fore.RED + f"ERROR: Al agregar el producto: {e}")
        conexion.rollback()

    except sqlite3.IntegrityError as e:
        print(Fore.RED + f"ERROR: El producto ya existe:{e}")
        conexion.rollback()

    except Exception as e:
        print(Fore.RED + f"Ocurrió un error inesperado: {e}")
        conexion.rollback()

    finally:
        #Se cierra la conexion a la base de datos.
        conexion.close()             


def mostrar_productos():
    """
    Muestra los productos del inventario, permitiendo ver todos o buscar por nombre.

    Primero verifica si hay productos en la base de datos. Si no hay, informa al usuario y regresa. Si hay, presenta opciones para mostrar todos los productos o buscar por un nombre específico. 
    Valida la entrada del usuario y maneja posibles errores de la base de datos.

    """
    #Conectando a la base de datos.
    conexion = sqlite3.connect('inventario.db')
    cursor = conexion.cursor()
    
    try:
        print(Fore.GREEN+Style.BRIGHT+f"\n{Back.BLACK} --- Consultar productos --- {Style.RESET_ALL}\n")
        
        #Se verifica si hay productos en la base de datos.
        cursor.execute('SELECT COUNT(*) FROM productos')
        count = cursor.fetchone()[0]

        if count == 0:
            print(Fore.YELLOW + "No hay productos en la base de datos para mostrar.")
            return 
        
        #Se presentan las opciones al usuario, si hay productos en la base de datos.
        print(Fore.LIGHTCYAN_EX+"1. Mostrar todos los productos")
        print(Fore.LIGHTCYAN_EX+"2. Buscar producto por nombre") 
        opcion = input(Fore.LIGHTCYAN_EX+"\nSeleccione una opción: "+Style.RESET_ALL).strip()
        
        if opcion == '1':
            cursor.execute('SELECT * FROM productos')
            productos = cursor.fetchall()

            print(Fore.GREEN + "Lista de productos:")
            for producto in productos:
                id, nombre, descripcion, cantidad, precio, categoria = producto
                print(Fore.MAGENTA + f"\nID:{Style.RESET_ALL}{id}{Fore.MAGENTA}, Nombre:{Style.RESET_ALL}{nombre}{Fore.MAGENTA}, Descripción:{Style.RESET_ALL}{descripcion}{Fore.MAGENTA}, Cantidad:{Style.RESET_ALL}{cantidad}{Fore.MAGENTA}, Precio:{Style.RESET_ALL}${precio:.2f}{Fore.MAGENTA}, Categoría:{Style.RESET_ALL}{categoria}")

        elif opcion == '2':
            nombre_a_buscar = input(Fore.CYAN+Style.BRIGHT+"\nIngrese el nombre del producto a buscar: "+Style.RESET_ALL).strip().capitalize()

            #Se valida que el nombre no este vacio.
            if not nombre_a_buscar:
                print(Fore.RED + "ERROR: El nombre del producto no puede estar vacío.")
                return

            #Se busca el producto por nombre en la base de datos, si no esta le avisa al usuario.
            cursor.execute('SELECT * FROM productos WHERE nombre = ?', (nombre_a_buscar,))
            productos = cursor.fetchall()

            if not productos:
                print(Fore.YELLOW + f"No se encontraron productos con el nombre '{nombre_a_buscar}.")
                return

            for producto in productos:
                id, nombre, descripcion, cantidad, precio, categoria = producto
                print(Fore.MAGENTA + f"\nID:{Style.RESET_ALL}{id}{Fore.MAGENTA}, Nombre:{Style.RESET_ALL}{nombre}{Fore.MAGENTA}, Descripción:{Style.RESET_ALL}{descripcion}{Fore.MAGENTA}, Cantidad:{Style.RESET_ALL}{cantidad}{Fore.MAGENTA}, Precio:{Style.RESET_ALL}${precio:.2f}{Fore.MAGENTA}, Categoría:{Style.RESET_ALL}{categoria}")

        else:
            print(Fore.RED + "Opción no válida. Por favor, seleccione 1 o 2.")
            return
    
    except sqlite3.Error as e:
        print(Fore.RED + f"ERROR al consultar la base de datos: {e}")
    
    finally:
        #Se cierra la conexion a la base de datos.
        conexion.close()


def eliminar_producto():
    """
    Elimina un producto existente de la base de datos.

    Solicita al usuario el ID del producto a eliminar. 
    Primero muestra una lista de productos existentes para facilitar la selección. 
    Valida la entrada del ID y pide una confirmación al usuario antes de proceder con la eliminación. 
    Maneja errores de base de datos y asegura que la operación se complete o se revierta correctamente.
    
    """
    #Conectando a la base de datos.
    conexion = sqlite3.connect("inventario.db")
    cursor = conexion.cursor()

    try:
        print(Fore.GREEN+Style.BRIGHT+f"\n{Back.BLACK}--- Eliminar producto ---{Style.RESET_ALL}\n")
        cursor.execute("SELECT id,nombre FROM productos")
        productos = cursor.fetchall()

        #Se verifica si hay productos en la base de datos.
        if not productos:
            print(Fore.YELLOW + "No hay productos en la base de datos para eliminar.")
            return
        
        print(Fore.GREEN + "Lista de productos:\n")
        for producto in productos:
            print(Fore.MAGENTA + f"ID:{Style.RESET_ALL}{producto[0]}{Fore.MAGENTA}, Nombre:{Style.RESET_ALL}{producto[1]}")

        #Se solicita al usuario el ID del producto a eliminar y se valida que sea un número.
        id_a_eliminar = input(Fore.LIGHTCYAN_EX+f"\nIngrese el ID del producto a eliminar:{Style.RESET_ALL} ")

        if not id_a_eliminar.isdigit():
            print(Fore.RED + "ERROR: El ID debe ser un número.")
            return
        
        id_a_eliminar = int(id_a_eliminar)   
        cursor.execute("SELECT id,nombre FROM productos WHERE id = ?",(id_a_eliminar,))
        producto = cursor.fetchone()

        if not producto:
            print(Fore.YELLOW + "ATENCIÓN! No se encontró un producto con ese ID.")
            return
        
        # Se muestra el producto a eliminar y se solicita confirmación al usuario.
        while True:
            print(Fore.YELLOW + f"¿Está seguro de que desea eliminar el producto:{Fore.BLACK}{Back.LIGHTGREEN_EX}'{producto[1]}'{Style.RESET_ALL}{Fore.YELLOW} con ID:{Fore.BLACK}{Back.LIGHTGREEN_EX}'{producto[0]}'{Style.RESET_ALL}{Fore.YELLOW}? (s/n): ")
            confirmacion = input().strip().lower()
            if confirmacion == 's':
                break
            elif confirmacion == 'n':
                print(Fore.GREEN + "\nEliminación cancelada.")
                break
            else:
                print(Fore.RED + "Opción no válida. Por favor, ingrese 's' para confirmar o 'n' para cancelar.")
           
        if confirmacion == 's':
            cursor.execute("DELETE FROM productos WHERE id = ?", (id_a_eliminar,))
            conexion.commit()
            print(Fore.GREEN + f"\nProducto con ID {id_a_eliminar} eliminado exitosamente.")

    except sqlite3.Error as e:
        print(Fore.RED + f"ERROR al eliminar el producto: {e}")
        conexion.rollback()

    finally:
        #Se cierra la conexion a la base de datos.
        conexion.close()    


def actualizar_productos():
    """
    Actualiza los detalles de un producto existente en la base de datos.

    Solicita al usuario el ID del producto a actualizar y muestra una lista de productos existentes para facilitar la selección.
    Puede actualizar el nombre, descripción, cantidad, precio o categoría del producto, cada uno por separado o todos a la vez.
    Valida la entrada del usuario para asegurarse de que los datos sean correctos y maneja errores de base de datos.
    Si la actualización es exitosa, muestra un mensaje de confirmación.

    """
    #Se conecta a la base de datos.
    conexion = sqlite3.connect("inventario.db")
    cursor = conexion.cursor()

    try:
        print(Fore.GREEN+Style.BRIGHT+f"\n{Back.BLACK}--- Actualizar producto ---{Style.RESET_ALL}\n")
        cursor.execute("SELECT * FROM productos")
        productos = cursor.fetchall()

        #Se verifica si hay productos en la base de datos.
        if not productos:
            print(Fore.YELLOW + "No hay productos en la base de datos")
            return
        
        #Se muestra la lista de productos existentes con su ID y nombre correspondiente.
        print(Fore.GREEN + "Lista de productos:\n")
        for producto in productos:
            id, nombre, descripcion, cantidad, precio, categoria = producto
            print(Fore.MAGENTA + f"ID:{Style.RESET_ALL}{producto[0]}{Fore.MAGENTA}, Nombre:{Style.RESET_ALL}{producto[1]}")
       
       #Se solicita al usuario el ID del producto a actualizar y se valida que sea un número.
        id_a_actualizar = (input(Fore.LIGHTCYAN_EX+f"\nIngrese el ID del producto que desea actualizar:{Style.RESET_ALL}"))
    
        if not id_a_actualizar.isdigit():
            print(Fore.RED + "ERROR: El ID debe ser un número.")
            return
        id_a_actualizar = int(id_a_actualizar)

        cursor.execute("SELECT * FROM productos WHERE id = ?",(id_a_actualizar,))
        producto = cursor.fetchone()

        if not producto:
            print(Fore.YELLOW + f"ATENCION! No se encontró un producto con el ID: {id_a_actualizar}.")
            return
        
        #Se muestra el producto a actualizar y se solicita al usuario que seleccione qué datos desea actualizar.
        print(Fore.GREEN + f"Producto encontrado: {producto[1]}")
        print(Fore.LIGHTBLUE_EX+"\nQue datos desea actualizar?\n")
        print(Fore.LIGHTBLUE_EX+"1. Nombre")
        print(Fore.LIGHTBLUE_EX+"2. Descripción")
        print(Fore.LIGHTBLUE_EX+"3. Cantidad")
        print(Fore.LIGHTBLUE_EX+"4. Precio")
        print(Fore.LIGHTBLUE_EX+"5. Categoría")
        print(Fore.LIGHTBLUE_EX+"6. Todo")

        opcion = input(Fore.LIGHTCYAN_EX+f"\nIngrese su selección:{Style.RESET_ALL}").strip()

        if not opcion.isdigit():
            print(Fore.RED + "ERROR: La opción debe ser un número. Ingreselo nuevamente")
            return
        
        opcion = int(opcion)

        match opcion:
            case 1:
                #Actualiza el nombre del producto.
                while True:
                    nuevo_nombre = input(Fore.LIGHTCYAN_EX+f"\nIngrese el nuevo nombre del producto:{Style.RESET_ALL} ")
                    if nuevo_nombre and not nuevo_nombre.isdigit():
                        break
                    elif not nuevo_nombre:
                        print(Fore.RED + "ERROR: El nombre no puede estar vacío.")
                    elif nuevo_nombre.isdigit():
                        print(Fore.RED + "ERROR: El nombre no puede ser un número.")
                
                cursor.execute("UPDATE productos SET nombre = ? WHERE id = ?", (nuevo_nombre,id_a_actualizar))
                
                #Se guardan los cambios.
                conexion.commit()
                print(Fore.GREEN + f"Nombre del producto actualizado a '{nuevo_nombre}' exitosamente.\n")
                    
            case 2:
                #Actualiza la descripción del producto.
                while True:
                    nueva_descripcion = input(Fore.LIGHTCYAN_EX+f"Ingrese la nueva descripción del producto:{Style.RESET_ALL} ")
                    
                    if nueva_descripcion and not nueva_descripcion.isdigit():
                        break
                    elif not nueva_descripcion:
                        print(Fore.RED + "ERROR: La descripción no puede estar vacía.")
                    elif nueva_descripcion.isdigit():
                        print(Fore.RED + "ERROR: La descripción no puede ser un número.")
                
                cursor.execute("UPDATE productos SET descripcion = ? WHERE id = ?", (nueva_descripcion, id_a_actualizar))
                
                #Se guardan los cambios.
                conexion.commit()
                print(Fore.GREEN + f"Descripción del producto actualizada a '{nueva_descripcion}' exitosamente.\n")

            case 3:
                #Actualiza la cantidad del producto.
                while True: 
                    nueva_cantidad = input(Fore.LIGHTCYAN_EX+f"Ingrese la nueva cantidad del producto: {Style.RESET_ALL} ")
                    
                    try:
                        nueva_cantidad = int(nueva_cantidad)
                        if nueva_cantidad >= 0:
                            break
                        else:
                            print(Fore.RED + "ERROR: La cantidad no puede ser negativa. Inténtelo de nuevo.")

                    except ValueError:
                        print(Fore.RED + "ERROR: La cantidad debe ser un número válido. Inténtelo de nuevo.")
                        
                cursor.execute("UPDATE productos SET cantidad = ? WHERE id = ?", (nueva_cantidad, id_a_actualizar))

                #Se guardan los cambios.
                conexion.commit()
                print(Fore.GREEN + f"Cantidad del producto actualizada a {nueva_cantidad} exitosamente.\n")    
            
            case 4:
                #Actualiza el precio del producto.
                while True:
                    nuevo_precio = input(Fore.LIGHTCYAN_EX+f"Ingrese el nuevo precio del producto:{Style.RESET_ALL} ")
                   
                    try:
                            nuevo_precio = float(nuevo_precio) 
                            if nuevo_precio >= 0:
                                break 

                            else:
                                print(Fore.RED + "ERROR: El precio no puede ser negativo. Inténtelo de nuevo.")
                    except ValueError:
                        print(Fore.RED + "ERROR: El precio debe ser un número válido. Inténtelo de nuevo.")
                
                cursor.execute("UPDATE productos SET precio = ? WHERE id = ?", (nuevo_precio, id_a_actualizar))

                #Se guardan los cambios.
                conexion.commit()
                print(Fore.GREEN + f"Precio del producto actualizado a ${nuevo_precio:.2f} exitosamente.\n")
        
            case 5:
                #Actualiza la categoría del producto.
                while True:
                    nueva_categoria = input(Fore.LIGHTCYAN_EX+f"Ingrese la nueva categoría del producto: {Style.RESET_ALL}")
                    
                    if nueva_categoria and not nueva_categoria.isdigit():
                        break   
                    elif not nueva_categoria:
                        print(Fore.RED + "ERROR: La categoría no puede estar vacía.")
                    elif nueva_categoria.isdigit():
                        print(Fore.RED + "ERROR: La categoría no puede ser un número.")
                    
                cursor.execute("UPDATE productos SET categoria = ? WHERE id = ?", (nueva_categoria, id_a_actualizar))
                    
                #Se guardan los cambios.
                conexion.commit()
                print(Fore.GREEN + f"Categoría del producto actualizada a '{nueva_categoria}' exitosamente.\n")
                
            case 6:
                #Actualiza todos los campos del producto.
                    print(Fore.YELLOW + "\nActualizando todos los campos del producto...")

                    # Se solicita al usuario el nuevo nombre del producto y se valida que no sea un número ni esté vacío.
                    while True:
                        nuevo_nombre = input(Fore.LIGHTCYAN_EX+f"\nIngrese el nuevo nombre del producto:{Style.RESET_ALL} ")
                        if nuevo_nombre and not nuevo_nombre.isdigit():
                            break
                        elif not nuevo_nombre:
                            print(Fore.RED + "ERROR: El nombre no puede estar vacío.")
                        elif nuevo_nombre.isdigit():
                            print(Fore.RED + "ERROR: El nombre no puede ser un número.")
                
                    cursor.execute("UPDATE productos SET nombre = ? WHERE id = ?", (nuevo_nombre,id_a_actualizar))
                    print(Fore.GREEN + f"Nombre del producto actualizado a '{nuevo_nombre}' exitosamente.\n")

                    # Se solicita al usuario la nueva descripción del producto y se valida que no sea un número ni esté vacío.
                    while True:
                        nueva_descripcion = input(Fore.LIGHTCYAN_EX+f"Ingrese la nueva descripción del producto:{Style.RESET_ALL} ")
                        
                        if nueva_descripcion and not nueva_descripcion.isdigit():
                            break
                        elif not nueva_descripcion:
                            print(Fore.RED + "ERROR: La descripción no puede estar vacía.")
                        elif nueva_descripcion.isdigit():
                            print(Fore.RED + "ERROR: La descripción no puede ser un número.")
                    
                    cursor.execute("UPDATE productos SET descripcion = ? WHERE id = ?", (nueva_descripcion, id_a_actualizar))
                    print(Fore.GREEN + f"Descripción del producto actualizada a '{nueva_descripcion}' exitosamente.\n")

                    # Se solicita al usuario la nueva cantidad del producto y se valida que sea un número entero no negativo.
                    while True:
                        nueva_cantidad = input(Fore.LIGHTCYAN_EX+f"Ingrese la nueva cantidad del producto: {Style.RESET_ALL} ")
                        
                        try:
                            nueva_cantidad = int(nueva_cantidad)
                            if nueva_cantidad >= 0:
                                break
                            elif nueva_cantidad < 0:
                                print(Fore.RED + "ERROR: La cantidad no puede ser negativa. Inténtelo de nuevo.")

                        except ValueError:
                            print(Fore.RED + "ERROR: La cantidad debe ser un número válido. Inténtelo de nuevo.")
                            
                    cursor.execute("UPDATE productos SET cantidad = ? WHERE id = ?", (nueva_cantidad, id_a_actualizar))
                    print(Fore.GREEN + f"Cantidad del producto actualizada a {nueva_cantidad} exitosamente.\n")
                    
                    # Se solicita al usuario el nuevo precio del producto y se valida que sea un número no negativo.
                    while True:
                        nuevo_precio = input(Fore.LIGHTCYAN_EX+f"Ingrese el nuevo precio del producto:{Style.RESET_ALL} ")
                    
                        try:
                                nuevo_precio = float(nuevo_precio) 
                                if nuevo_precio >= 0:
                                    break 
                                elif not nuevo_precio:
                                    print(Fore.RED + "ERROR: El precio no puede estar vacío.")    
                    
                        except ValueError:
                            print(Fore.RED + "ERROR: El precio debe ser un número válido. Inténtelo de nuevo.")
                    
                    cursor.execute("UPDATE productos SET precio = ? WHERE id = ?", (nuevo_precio, id_a_actualizar))
                    print(Fore.GREEN + f"Precio del producto actualizado a ${nuevo_precio:.2f} exitosamente.\n")
       
                    #Se solicita al usuario la nueva categoría del producto y se valida que no sea un número ni esté vacío.
                    while True:
                        nueva_categoria = input(Fore.LIGHTCYAN_EX+f"Ingrese la nueva categoría del producto: {Style.RESET_ALL}")
                        
                        if nueva_categoria and not nueva_categoria.isdigit():
                            break   
                        elif not nueva_categoria:
                            print(Fore.RED + "ERROR: La categoría no puede estar vacía.")
                        elif nueva_categoria.isdigit():
                            print(Fore.RED + "ERROR: La categoría no puede ser un número.")
                        
                    cursor.execute("UPDATE productos SET categoria = ? WHERE id = ?", (nueva_categoria, id_a_actualizar))
                    print(Fore.GREEN + f"Categoría del producto actualizada a '{nueva_categoria}' exitosamente.\n")
                    
                #Se guardan los cambios.    
                    conexion.commit()
                    print(Fore.LIGHTGREEN_EX + "Todos los campos del producto han sido actualizados exitosamente.\n")    

            case _:
                print(Fore.RED + "Opción no válida. Por favor, seleccione una opción del 1 al 6.")
                return
            
    #Se intenta actualizar el producto en la base de datos y decide si es exitoso o si hace un rollback.
    except sqlite3.Error as e:
        print(Fore.RED + f"ERROR al actualizar el producto: {e}")
        conexion.rollback()

    finally:
        conexion.close()            


def reportar_productos():
    """
    Reporta productos según su cantidad, permitiendo al usuario elegir entre productos con cantidad menor o igual a un valor específico.
    
    Primero verifica si hay productos en la base de datos.
    Luego presenta las dos opciones mencionadas y se solicita al usuario que elija una.
    Muestra los productos que cumplen con el criterio seleccionado.
    Maneja errores de base de datos y de entrada del usuario.
    
    """
    #Se conecta a la base de datos.
    conexion = sqlite3.connect("inventario.db")
    cursor = conexion.cursor()
    print(Fore.GREEN+Style.BRIGHT+f"\n{Back.BLACK}--- Reportar producto/s ---{Style.RESET_ALL}\n")

    try:
        #Se verifica si hay productos en la base de datos.
        cursor.execute('SELECT COUNT(*) FROM productos')
        count = cursor.fetchone()[0]

        if count == 0:
            print(Fore.YELLOW + "No hay productos en la base de datos para reportar.")
            return 
      
        #Si hay productos, se presentan las opciones al usuario y se valida la entrada.
        print(Fore.BLUE+Style.BRIGHT+f"1. Reportar productos con cantidad menor a un valor")
        print(Fore.BLUE+Style.BRIGHT+f"2. Reportar productos con cantidad igual a un valor")

        opcion = input(Fore.LIGHTCYAN_EX+f"\nSeleccione una opción: {Style.RESET_ALL}").strip()

        if not opcion.isdigit():
            print(Fore.RED + "ERROR: La opción debe ser un número.")
            return
        
        opcion = int(opcion)

        
        if opcion == 1:
            #Reporta productos con cantidad menor a un valor y valida la entrada del usuario.
            cantidad_minima = input(Fore.LIGHTCYAN_EX+f"Ingrese la cantidad maxima que puede tener el producto:{Style.RESET_ALL} ").strip()

            if not cantidad_minima.isdigit():
                print(Fore.RED + "ERROR: La cantidad debe ser un número.")
                return
            
            cantidad_minima = int(cantidad_minima)

            cursor.execute("SELECT * FROM productos WHERE cantidad < ?", (cantidad_minima,))
            productos = cursor.fetchall()

            if not productos:
                print(Fore.YELLOW + f"No hay productos con cantidad menor a {cantidad_minima}.")
                return

            print(Fore.GREEN + f"\nProductos con cantidad menor a {cantidad_minima}:")
            for producto in productos:
                id, nombre, descripcion, cantidad, precio, categoria = producto
                print(Fore.MAGENTA + f"\nID:{Style.RESET_ALL}{id}{Fore.MAGENTA}, Nombre:{Style.RESET_ALL}{nombre}{Fore.MAGENTA}, Descripción:{Style.RESET_ALL}{descripcion}{Fore.MAGENTA}, Cantidad:{Style.RESET_ALL}{cantidad}{Fore.MAGENTA}, Precio:{Style.RESET_ALL}${precio:.2f}{Fore.MAGENTA}, Categoría:{Style.RESET_ALL}{categoria}")

        elif opcion == 2:
            #Reporta productos con cantidad igual a un valor y valida la entrada del usuario.
            cantidad_exacta = input(Fore.LIGHTCYAN_EX+f"Ingrese la cantidad exacta:{Style.RESET_ALL} ").strip()

            if not cantidad_exacta.isdigit():
                print(Fore.RED + "ERROR: La cantidad debe ser un número.")
                return
            
            cantidad_exacta = int(cantidad_exacta)

            cursor.execute("SELECT * FROM productos WHERE cantidad = ?", (cantidad_exacta,))
            productos = cursor.fetchall()

            if not productos:
                print(Fore.YELLOW + f"No hay productos con cantidad igual a {cantidad_exacta}.")
                return

            print(Fore.GREEN + f"\nProductos con cantidad igual a {cantidad_exacta}:")
            for producto in productos:
                id, nombre, descripcion, cantidad, precio, categoria = producto
                print(Fore.MAGENTA + f"\nID:{Style.RESET_ALL}{id}{Fore.MAGENTA}, Nombre:{Style.RESET_ALL}{nombre}{Fore.MAGENTA}, Descripción:{Style.RESET_ALL}{descripcion}{Fore.MAGENTA}, Cantidad:{Style.RESET_ALL}{cantidad}{Fore.MAGENTA}, Precio:{Style.RESET_ALL}${precio:.2f}{Fore.MAGENTA}, Categoría:{Style.RESET_ALL}{categoria}")

        else:
            print(Fore.RED + "Opción no válida. Por favor, seleccione 1 o 2.")

    except sqlite3.Error as e:
        print(Fore.RED + f"ERROR al consultar la base de datos: {e}")

    finally:
        #Se cierra la conexion a la base de datos.
        conexion.close()


def mostrar_menu():
    """
    Muestra el menú principal del programa y permite al usuario seleccionar una opción.
    """

    while True:
        print(Fore.CYAN+Style.BRIGHT + f"\n{Back.BLACK}--- Menú de Inventario ---{Style.RESET_ALL}\n")
        print(Fore.BLUE+Style.BRIGHT+"1. Agregar producto")
        print(Fore.BLUE+Style.BRIGHT+"2. Mostrar productos")
        print(Fore.BLUE+Style.BRIGHT+"3. Eliminar producto")
        print(Fore.BLUE+Style.BRIGHT+"4. Actualizar producto")
        print(Fore.BLUE+Style.BRIGHT+"5. Reportar productos")
        print(Fore.BLUE+Style.BRIGHT+"6. Salir\n")

        #Validación de la opción ingresada por el usuario.
        while True:
            opcion = input(Fore.CYAN+Style.BRIGHT+"Seleccione una opción: "+ Style.RESET_ALL).strip()

            if not opcion.isdigit():
                print(Fore.RED + "ERROR: La opción debe ser un número.")
                continue
            opcion = int(opcion)

            if opcion < 1 or opcion > 6:
                print(Fore.RED + "ERROR: Por favor, seleccione una opción del 1 al 6.")
                continue
            
            if opcion >= 1 or opcion <= 6:
                break

        #Se ejecuta la opción seleccionada por el usuario.
        match opcion:
            case 1:
                agregar_producto()
            case 2:
                mostrar_productos()
            case 3:
                eliminar_producto()
            case 4:
                actualizar_productos()
            case 5:
                reportar_productos()
            case 6:
                print(Fore.LIGHTGREEN_EX+Style.BRIGHT + f"\n{Back.BLACK}Gracias por elegirnos, nos vemos pronto!{Style.RESET_ALL}\n")
                break                

mostrar_menu()