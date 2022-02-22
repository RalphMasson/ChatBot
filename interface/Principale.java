import java.io.IOException;

public class Principale {

	public static void main(String[] args) {
		// TODO Auto-generated method stub
		System.out.println("toto");
		try {
			Process p = Runtime.getRuntime().exec("python C:\\Users\\MASSON\\Desktop\\ChatBot\\chatbot.py");
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}

	}

}
