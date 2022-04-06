Para anotaciones de imágenes:

- Id de imagen (o alguna forma para ligar una anotación con su imagen)
- Etiqueta: lo que el usuario/modelo etiquetó, ya sea nombre científico, nombre común, grupo funcional, etc.
- Id de anotador
- Tipo anotador: (curador/usuario/modelo)
- bbox: ("x,y,width,height" ó "x1,y1,x2,y2")
- Clase de anotación: (imagen completa, bbox, máscara de segmentación, etc.)
- Datos del Modelo: Id/Versión/Probabilidad de la predicción
- Id del taxón en el catálogo que se use de referencia (SNIB, GBIF, etc.)
- Todos los niveles taxonómicos: reino/phylum/clase/orden/familia/genero/especie/subespecie
- Calidad: esto se refiere a qué tan bien aparecen el/los individuo(s) etiquetado(s)
- Tipo de anotación: (espécimen/huella/restos/excreta)
- Datos adicionales: Edad/Sexo/Comportamiento/Numero de individuos/Certeza de anotación
- Fecha anotación original
- Fecha de última modificación
- Observaciones: (alguna observación que hace el anotador sobre la foto/etiqueta)

Para imágenes que recibimos:

- Path relativo al archivo (para poder cambiar de host sin problema)
- Fecha de la foto
- Localización: Latitud y longitud, de preferencia en grados decimales
- Identificador de locación y sub-locación: conglomerado-sitio/cúmulo-nodo
- Estado y municipio (En el SNMB también se usaba ANP e institución)
- Información de la secuencia a la que pertenece cada foto:
- Sequence id
- Número de frames en la secuencia
- Número del frame dentro de la secuencia

Si no se cuenta con los datos de las secuencias, conocer la tasa de muestreo (cada cuánto se toma una foto), para calcular las secuencias a partir de la hora. Lo anterior ¿depende de la cámara o del proyecto en general?
