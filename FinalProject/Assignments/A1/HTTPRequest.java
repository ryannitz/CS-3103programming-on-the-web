import java.io.BufferedReader;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;
import java.net.URLConnection;
import java.nio.file.Files;
import java.util.List;
import java.util.Map;
import java.util.Scanner;

public class HTTPRequest {

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        String in;
        String protocol = "https://";
        String domain = "cs3103.cs.unb.ca";
        String path = "/wightman/index.html";
        int port = 443;

        System.out.println("Select protocol: (Press enter to use default=https): ");
        System.out.println("1) https");
        System.out.println("2) http");
        in = sc.nextLine();
        if (in.isEmpty()) {
            System.out.println("\tUsing default protocol: \"https://\"");
        }
        while (!in.isEmpty()) {
            int choice = Integer.parseInt(in);
            if (choice == 1) {
                System.out.println("\tUsing default protocol: \"https://\"");
            } else if (choice == 2) {
                System.out.println("\tUsing protocol: \"http://\"");
                protocol = "http://";
            } else {
                System.out.println("Please select 1 or 2");
            }
        }

        System.out.print("Enter full domain name (E.g. cs3103.cs.unb.ca): ");
        in = sc.nextLine();
        if (!in.isEmpty()) {
            domain = in;
            System.out.println("\tDomain name: " + domain);
        } else {
            System.out.println("\tUsing default domain: \"cs3103.cs.unb.ca\"");
        }

        System.out.print("Enter full document path (Press enter to use default=/wightman/index.html): ");
        in = sc.nextLine();
        if (!in.isEmpty()) {
            path = in;
        } else {
            System.out.println("\tUsing default path: \"/wightman/index.html\"");
        }

        if (!path.startsWith("/")) {
            path = "/" + path;
        }

        System.out.print("Specify port number (Press enter to use default=443): ");
        in = sc.nextLine();
        if (!in.isEmpty()) {
            port = Integer.parseInt(in);
        } else {
            System.out.println("\tUsing default port: \"443\"");
        }

        String response = makeRequest(protocol, domain, path, port);
        createFile(path, response);
        System.out.println("\nContents:\n\n" + response);
    }

    public static String makeRequest(String protocol, String domain, String path, Integer port) {
        // port is not used when protocol is specified
        String urlString = protocol + domain + ":" + port + path;
        System.out.println(urlString);
        System.out.println("\nConnecting to: " + urlString);
        String response = "";
        try {
            URL url = new URL(urlString);
            String line;
            URLConnection conn = url.openConnection();
            response += getHeaderString(conn);
            BufferedReader br = new BufferedReader(new InputStreamReader(conn.getInputStream()));
            while ((line = br.readLine()) != null) {
                response += line;
            }
            br.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
        return response;
    }

    public static String getHeaderString(URLConnection conn){
        String headers = "";
        if(conn != null){
            for (Map.Entry<String, List<String>> entry : conn.getHeaderFields().entrySet()) {
                headers += entry.getKey() + " : " + entry.getValue() + "\n";
            }
        }
        return headers;
    }

    public static void createFile(String path, String content) {
        if (path.contains("/")) {
            path = path.substring(path.lastIndexOf("/") + 1, path.length());
        } else if (path.contains("\\")) {
            path = path.substring(path.lastIndexOf("\\") + 1, path.length());
        }
        try {
            FileWriter fw = new FileWriter((path));
            fw.write(content);
            fw.close();
            System.out.println("Wrote the request contents to: " + path);
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
