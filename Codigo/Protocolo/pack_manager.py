import struct

# Mensaje que solicita desde ML guardar una página en un NM
# Desde ML hacia ID y de ID a NM
def store_package(op_code, id_page, page_size, data):
    package_format = "=BBI" + str(page_size) + "s"
    package = struct.pack(package_format, op_code, id_page, page_size, data)
    return package

# Mensaje que solicita desde ML lectura de una página en un NM
# Se usa tambien en ID para decir que se pudo guardar una página en NM
# Desde ML hacia ID y de ID a NM
# Desde ID hacia ML
def read_package_store_ok(op_code, id_page):
    package_format = "=BB"
    package = struct.pack(package_format, op_code, id_page)
    return package

# Mensaje que devuelve el NM cuando guarda para la ID
# Desde NM hacia ID
def store_answer_NM_ID(op_code, id_page, node_size):
    package_format = "=BBI"
    package = struct.pack(package_format, op_code, id_page, node_size)
    return package

# Mensaje que informa quien quiere página
# Desde ID hacia ML y de NM a ID
def read_answer(op_code, id_page, data):
    package_format = "=BB" + str(len(data)) + "s"
    package = struct.pack(package_format, op_code, id_page, data)
    return package
  
# Mensaje de broadcast que informa que un nuevo nodo se quiere agregar al sistema

def new_node(op_code, memory_size):
    package_format = "=BI"
    package = struct.pack(package_format, op_code, memory_size)
    return package

# 
def unpack_store_ID_NM(package, id_page):
    op_code_res = package[0]
    id_page_res = package[1]
    node_size = struct.unpack("I", package[2:6])
  
    if op_code_res == 4:
        print ("Hubo un error durante el guardado")
        return -1
    else:
        if id_page_res == id_page:
            print ("Se guradó exitosamente en NM")
            print ("El espacio disponible: " + str(node_size[0]))
            return node_size[0]
        else:
            print ("Hubo un error durante el guardado")
            return -1
  
# Mensaje que confirma que se guardo exitosamente una pagina
def page_saved(op_code, page_id, memory_size):
    package_format = "=BBI"
    package = struct.unpack(package_format, op_code, page_id, memory_size)
    return package

def unpack_read_response(packege, page_id, page_size):
    op_code_res = packege[0]
    id_page_res = packege[1]
    data = packege[2:(2+page_size)]

    if op_code_res == 4:

        print ("Se produjo error al devolver página")
        return 1

    else:

        if id_page_res == page_id:

            print ("Se obtuvo la página exitosamente")
            return data

        else:

            print ("Se obtuvo página incorrecta")
            return 1
