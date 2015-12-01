#!/usr/bin/env python
"""	Lee el .csv que genera-como-output la app index.html.
	
	Todos los ids que fueron cambiados por la app index.html aparecen en el output .csv que genera la app.

	Luego escribe el contenido del archivo input <input_indexhtml.csv> de index.html ('../Comments.csv')
	en otro archivo .csv, pero reemplaza los valores de comment__class que fueron modificados por index.html (estos valores que fueron
	modificados se encuentran en el output que genera index.html).
	Ademas, no escribe las lineas <input_indexhtml.csv> que tienen un valor de id_sub==0, porque estas
	lineas contienen un comentario completo (no solo una frase como para los con el id_sub>0)
	"""
fdout = open("Comments_WebOutput.csv","w")


loops = 0 #put 0 for loop until end (infinite)


# en myset guardo la info del <input>.csv.  por ejemplo:
#id,id_sub,comment__class
#1004,3,1
#1004,4,2
#(esas lineas del input) queda guardado en myset como myset[1004] == {3:1,4:2}
#el bloque de codigo siguiente se encarga de llenar myset.
myset = {}
with open("out_web-JFace-Gabo.csv") as fdWebOutput:
	i = 1
	for line in fdWebOutput:
		if i>1:
			L = line.split(",")
			if L[0] not in myset.keys():
				try:
					if len(L[2])>1:
						myset[L[0]] = {L[1]:L[2][:-1]}
					else:
						myset[L[0]] = {L[1]:L[2][:]}
				except IndexError as e:
					print('myError: \'{2}\'  ... la linea {0} tiene {1} valores'.format(i,len(L),e))

				
			else:
				if L[1] not in myset[L[0]].keys():
					if len(L[2])>1:#@TODO: esto esconde un futuro bug. el '>1' hace que el maximo numero de clases de comentarios (o is_directive) sea 10
						myset[L[0]][L[1]] = L[2][:-1]
					else:
						myset[L[0]][L[1]] = L[2][:]
				elif L[2][:-1] != myset[L[0]][L[1]]: #si ya existe el par id-subId, y además el valor ya existente es distinto del valor nuevo, error
					print('myError: esto no deberia pasar, se repitió un par id-subId (y tienen distinto valor de comment__class) en la linea {0} del <input>.csv... por defecto quedo el 1er valor leido de arriba a abajo'.format(i))
					#sys.exit()
			
		i+=1


#lee el archivo que usa index.html como input.
#Para todos los ids de este archivo que no existen en 'myset', se escribe la linea original de este archivo al <output>.csv
#Para los que si existen en 'myset' si algun valor de este archivo como input (refiriendonos
#	al valor de comment__class (un int)) es distinto
#	al valor que está en la variable myset (que representa el output .csv que genera index.html)
# 	entonces se escribe (al archivo de <output>.csv) el valor de myset. Si el valor es igual también
#  	se escribe el de myset (daría igual cual escribir porque son iguales). Se escribe toda la linea originar
#   pero con los valores comment__class cambiado.
differentValueCount = 0
sameValueCount = 0
othernum = 0
with open("dataset---jface---ordered.csv") as fdDataset:
	i = 1
	for line in fdDataset:
		if i==1:
			fdout.write(line)
		elif i>1:
			if loops<1 and i%10000==0:
				print(i)
			if loops>=1 and i>=loops:
				break

			line_splitted = line.split(",",maxsplit=5)

			theid = line_splitted[0]
			thesubid = line_splitted[1]
			thedirectivevalue = line_splitted[2]

			if theid in myset.keys() and thesubid in myset[theid]:
				if thedirectivevalue != myset[theid][thesubid]:
					differentValueCount += 1
				else:
					sameValueCount += 1
				valueToWrite = myset[theid][thesubid]
			else:
				othernum += 1
				valueToWrite = thedirectivevalue

			if thesubid!='0':
				fdout.write(','.join([line_splitted[0],line_splitted[1],valueToWrite,line_splitted[3],line_splitted[4],line_splitted[5]]))


		i += 1

fdout.close()

print(str(differentValueCount) + ' values were changed.')
print(str(sameValueCount) + ' values left the same as before because the new value was the same as the old.')
print(str(othernum) + ' values were never modified in the web app.')