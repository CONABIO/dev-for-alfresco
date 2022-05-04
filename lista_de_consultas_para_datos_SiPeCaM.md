## Consultas sobre campos de anotaciones

**Por Usuario:**

- Obtener las fotos etiquetadas por los usuarios con nivel X (p.e. curador) ó por un usuario específico (p.e. Marcelo)
- Obtener las fotos que No hayan sido etiquetadas por ningún usuario con nivel X (p.e. para mostrar las fotos que no han sido curadas). *Esta no se puede hacer directamente con el esquema de Solr que manejamos actualmente*

**Por Modelo:**

- Obtener las fotos en las que el modelo X haya encontrado detecciones de animal con score ≥ Y
- Obtener las fotos en las que el modelo X NO haya encontrado detecciones de animal con score ≥ Y (p.e. para saber cuáles fotos el modelo considera vacías, maximizando el recall). Esta no se puede hacer directamente con el esquema de Solr que manejamos actualmente
- Obtener las fotos que No hayan sido etiquetadas por el modelo X (p.e. para obtener las fotos que no han sido procesadas por el Megadetector). *Esta no se puede hacer directamente con el esquema de Solr que manejamos actualmente*

**Por Taxonomía:**

- Obtener las fotos etiquetadas con la especie/género/familia/... X
- Etiqueta
- Obtener las fotos etiquetadas como vacías

**Por Datos adicionales:**

- Obtener las fotos con etiquetas de calidad X (p.e. las de buena calidad para subirlas a Naturalista), ó las de individuos de Edad X (p.e. crías)


## Consultas sobre campos de las fotos

- Obtener las fotos de los conglomerados/cúmulos X
- Obtener las fotos del ecosistema X
- Obtener las fotos de los nodos degradados del ecosistema X
- Obtener las fotos tomadas entre los años X y Y, o entre los meses X y Y (estaciones), o entre las horas X y Y (p.e. en la noche)


## Consultas que combinen campos de anotaciones y campos de las fotos

- P.e. obtener las fotos de la especie X que sean del ecosistema Y


### Nota

Las que se indica que no se pueden hacer con el esquema de Solr actual nosotros se realizan con algún script de python, pero dependiendo del esquema que elijan usar quizás se podrían hacer directamente
