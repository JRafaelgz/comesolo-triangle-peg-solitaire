<h1>Solución de problemas con expansión de árboles / Comesolo de 15 posiciones</h1>

<h2>Instrucciones:</h2>
<p></p>Para poder usar el programa, solamente debe de ejecutar el programa ya sea desde Spyder, Visual Studio Code o cualquier entorno de Python. La profundidad en la cual buscará estará por defecto en 25, si desea incrementarla o disminuirla solo debe cambiar el valor de la línea 164 (sí se coloca un nivel muy grande podría demorarse mucho tiempo en finalizar la ejecución y causar problemas de rendimiento):</p>
<code>g = a.gentree(final, 25)</code>
<p>Una vez ejecutado el programa, en la terminal o consola se mostrará el siguiente mensaje:</p>
<pre>
Solución del juego Comesolo de 15 posiciones:
    a1
   a2 b2
  a3 b3 c3
 a4 b4 c4 d4
a5 b5 c5 d5 e5
Escriba el poste que comenzara vacío (usando la notación anterior):
</pre>
<p>Primero le pedirá ingresar de manera textual en que posición se quiere colocar el poste vacío, se deberá de colocar según la notación de la figura, por lo que se podrá escribir: a1, a2, b2, a3, … o cualquier posición que se desee siempre y cuando se respete la notación teniendo como limite a: e5, además de que solo se debe de escribir una sola posición sin comas ni puntos ni espacios.</p>
<p>Después de haber escrito una posición preguntara lo siguiente:</p>
<pre>
Escriba la posición final del poste (si no importa escriba: *):
</pre>
<p>De igual manera deberá de escribirse una posición según la notación mencionada o en su defecto escribir: * para que pueda terminar en cualquier posición.</p>
<p>Una vez que se haya hecho lo anterior comenzara a buscar la solución mediante la expansión de árboles, en caso de encontrar una solución se mostraran los pasos para llegar a ella y en caso contrario mostrara que no se logró encontrar una solución.</p>
<p>Si se quiere volver a jugar, solo debe de volver a ejecutar el programa.</p>

<h3>Acomodos que se hicieron del tablero para la implementación del código.</h3>
<p>El siguiente tablero es la configuración original (O):</p>

	    a1
	   a2 b2
	  a3 b3 c3
	 a4 b4 c4 d4
	a5 b5 c5 d5 e5

<p>Ahora se acomodará como un triángulo rectángulo (en el código se le llama referencia), los a0 son solamente para completar el arreglo:</p>

	a1 a0 a0 a0 a0
	a2 b2 a0 a0 a0
	a3 b3 c3 a0 a0
	a4 b4 c4 d4 a0
	a5 b5 c5 d5 e5

<p>La configuración anterior se convertirá a ceros, unos y dos, donde 0 = Poste vacío, 1 = Existencia de poste, 2 = elemento agregado para completar el arreglo, además de agregarse filas j y columnas i:</p>

	   0 1 2 3 4 j
	i| _ _ _ _ _
	0| 1 2 2 2 2
	1| 1 1 2 2 2
	2| 1 1 1 2 2
	3| 1 1 1 1 2
	4| 1 1 1 1 1

<p>Esta configuración es a la que se hace referencia como triangulo rectángulo (TR) dentro del código y con la cual es posible generar los movimientos de manera más sencilla.</p>
