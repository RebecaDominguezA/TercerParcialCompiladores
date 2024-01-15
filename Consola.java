import java.io.BufferedReader;
//import java.io.File;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
//import java.util.LinkedList;

public class Consola {
    static boolean existenErrores = false;
    public static void main(String[] args) {
        if (args.length == 0) {
            // Si no se proporcionaron argumentos, realizar cierta acción
            //System.out.println("No se proporcionaron argumentos. Realizar acción A");
            // Realizar la acción correspondiente a la falta de argumentos aquí
            Scanner scanner = new Scanner(System.in);

            System.out.print(">>>");
            String entrada = scanner.nextLine(); // Lee una línea de texto

            //System.out.println("Ha ingresado: " + entrada);
            ejecutar(entrada,1);
            scanner.close(); // Cierra el Scanner al finalizar
        } else {
            // Si se proporcionaron argumentos, realizar otra acción basada en los argumentos
            System.out.println("Se proporcionaron argumentos. Realizar acción B");
            // Procesar los argumentos y realizar la acción correspondiente a los argumentos aquí
            // Puedes acceder a los argumentos usando args[0], args[1], etc.
            // Por ejemplo, args[0] contendrá el primer argumento, args[1] el segundo, y así sucesivamente.
            String argumentosConcatenados = "";

            for (String arg : args) {
                //System.out.println("Argumento: " + arg);
                argumentosConcatenados += arg + " ";
            }

            System.out.println("Argumento" + argumentosConcatenados);
            ejecutar(argumentosConcatenados,2);
        }
    
    }
    private static void ejecutar(String source,int opcion){
        StringBuilder resultado = new StringBuilder();
        List<String> tokens = new ArrayList<>();
        try {
            //Obtener la ruta del directorio actual
            String directorioActual = System.getProperty("user.dir");

            // Construir la ruta al archivo AnalizadorLexico.py en el directorio actual
            String rutaPython = Paths.get(directorioActual, "AnalizadorLexico.py").toString();
            ProcessBuilder processBuilder = new ProcessBuilder();
            
            if (opcion == 1) {
                // Se le pasa como argumento al programa Python un String
                processBuilder.command("py", rutaPython, source);
            } else if (opcion == 2) {
                // Se le pasa como argumento al programa Python un archivo .txt
                processBuilder.command("py", rutaPython, source);
            } else {
                System.out.println("Opción inválida.");
                return;
            }
            
            Process proceso = processBuilder.start();
            
            // Obtener el flujo de entrada del proceso (output del programa Python)
            InputStream inputStream = proceso.getInputStream();
            BufferedReader reader = new BufferedReader(new InputStreamReader(inputStream));
            
            String linea;
            while ((linea = reader.readLine()) != null) {
                resultado.append(linea).append("\n");
            }
            
            System.out.println(resultado);
            //Obtenemos la lista de tokens preparados para meter a lista
            tokens = obtenerTokens(resultado);
            
            System.out.println("terminamos");

            int exitCode = proceso.waitFor();
            if (exitCode != 0) {
                System.out.println("Error al ejecutar el programa de Python, código de salida: " + exitCode);
            }
        } catch (IOException | InterruptedException e) {
            e.printStackTrace();
        }

        //Imprimir tokens
        for(String token : tokens){
            System.out.println(token);
        }

        //for(String token : tokensF){
            //System.out.println(token);
        //}
        


        Parser parser = new AS(tokens);
        parser.parse();
    }

    /*
    El método error se puede usar desde las distintas clases
    para reportar los errores:
    Interprete.error(....);
     */
    static void error(int linea, String mensaje){
        reportar(linea, "", mensaje);
    }

    private static void reportar(int linea, String donde, String mensaje){
        System.err.println(
                "[linea " + linea + "] Error " + donde + ": " + mensaje
        );
        existenErrores = true;
    }

    public static List<String> obtenerTokens(StringBuilder resultado) {
        List<String> listaTipos = new ArrayList<>();
        Pattern pattern = Pattern.compile("<(\\w+),");
        Matcher matcher = pattern.matcher(resultado);

        while (matcher.find()) {
            String tipoToken = matcher.group(1);
            //System.out.println(tipoToken);
            listaTipos.add(tipoToken); // Agregar cada tipo de token a la lista
        }

        return listaTipos;
    }
    
}
