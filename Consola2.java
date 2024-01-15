import java.io.BufferedReader;
import java.io.File;
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

public class Consola2 {
    static boolean existenErrores = false;
    public static void main(String[] args) {
        int bandera=0;
        if (bandera==1) {
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
            
            String argumentosConcatenados = "archivo1.txt";
            

            //System.out.println("Argumento " + argumentosConcatenados);
            ejecutar(argumentosConcatenados,2);
        }
    
    }
    private static void ejecutar(String source,int opcion){
        StringBuilder resultado = new StringBuilder();
        List<String> tokensS = new ArrayList<>();
        List<Token> tokens = new ArrayList<>();

        //El siguiente try catch es para el analizador sintactico y regresa tokens
        try {
            //Obtener la ruta del directorio actual
            String directorioActual = System.getProperty("user.dir");

            // Construir la ruta al archivo AnalizadorLexico.py en el directorio actual
            String rutaPython = Paths.get(directorioActual, "AnalizadorLexico.py").toString();
            ProcessBuilder processBuilder = new ProcessBuilder();
            System.out.println(rutaPython);
            if (opcion == 1) {
                // Se le pasa como argumento al programa Python un String
                processBuilder.command("py", rutaPython, source);
            } else if (opcion == 2) {
                // Se le pasa como argumento al programa Python un archivo .txt
                //System.out.println("aqui");
                String rutaPython2 = Paths.get(directorioActual, source).toString();
                //System.out.println(rutaPython2);
                if (archivoExiste(rutaPython2)) {
                    //System.out.println("existe");
                    // El archivo existe, ahora puedes ejecutar tu proceso
                    processBuilder.command("py", rutaPython, source);
                } else {
                    System.out.println("El archivo no existe en la ruta proporcionada. Intentelo de nuevo, se ingreso a analizar la entrada incorrecta.");
                    processBuilder.command("py", rutaPython, source + " //Analizadordeentrada.");
                }
                
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
            
            //System.out.println(resultado);
            //Obtenemos la lista de tokens preparados para meter a lista
            tokensS = obtenerTokens(resultado);
            
            //System.out.println("terminamos");

            int exitCode = proceso.waitFor();
            if (exitCode != 0) {
                //System.out.println("Error al ejecutar el programa de Python, código de salida: " + exitCode);
            }
        } catch (IOException | InterruptedException e) {
            e.printStackTrace();
        }

        
        //Imprimir tokens Y CONVERSION DE STRINGS A TOKENS
        for(String token : tokensS){
            //System.out.println("A"+token);
            // Definir el patrón de la expresión regular
            Pattern pattern = Pattern.compile("<(.*?),(.*?),(.*?)>");

            // Crear un objeto Matcher y hacer coincidir la cadena de entrada con el patrón
            Matcher matcher = pattern.matcher(token);
            // Verificar si hay coincidencias y extraer los valores
            if (matcher.matches()) {
                String valor1 = matcher.group(1);
                String valor2 = matcher.group(2);
                String valor3 = matcher.group(3);
                
                // Imprimir los valores extraídos
                //System.out.println("Valor 1: " + valor1);
                //System.out.println("Valor 2: " + valor2);
                //System.out.println("Valor 3: " + valor3);
                
                // Utiliza el método valueOf() para convertir la cadena a una constante de enumeración
                TipoToken tt;
                try {
                    tt = TipoToken.valueOf(valor1);
                } catch (IllegalArgumentException e) {
                    // Maneja la excepción si el valor1 no coincide con ninguna constante de enumeración
                    tt = TipoToken.NULL;
                }
                if (valor3.equals("null")){
                    Token t = new Token(tt, valor2);
                    tokens.add(t);
                }else{
                    Token t = new Token(tt, valor2, valor3);
                    tokens.add(t);
                }
            } else {
                System.out.println("La cadena no coincide con el formato esperado.");
            }

        }
        
        Parser parser = new ASDR(tokens);
        parser.parse();
        System.out.println("ostia");
            
        //for(String token : tokensF){
            //System.out.println(token);
        //}
        
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
        Pattern pattern = Pattern.compile("<([^>]+)>");
        Matcher matcher = pattern.matcher(resultado);

        while (matcher.find()) {
            String tipoToken = matcher.group(1);
            listaTipos.add("<"+tipoToken+">"); // Agregar cada tipo de token a la lista
        }

        return listaTipos;
    }

    private static boolean archivoExiste(String rutaArchivo) {
        File archivo = new File(rutaArchivo);
        return archivo.exists() && archivo.isFile();
    }
    
}
