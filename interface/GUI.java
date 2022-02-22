import java.awt.Color;
import java.awt.EventQueue;
import java.awt.Font;
import java.awt.Image;
import java.awt.image.BufferedImage;
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.MalformedURLException;
import java.net.URL;
import java.util.List;

import javax.sound.sampled.AudioInputStream;
import javax.sound.sampled.AudioSystem;
import javax.sound.sampled.Clip;
import javax.sound.sampled.LineUnavailableException;
import javax.sound.sampled.UnsupportedAudioFileException;
import javax.swing.BorderFactory;
import javax.swing.ImageIcon;
import javax.swing.JButton;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JScrollPane;
import javax.swing.JTextArea;
import javax.swing.SwingWorker;


public class GUI {

	private JFrame frmJarvis;
	public JLabel lblNewLabel_1 = new JLabel("Ne parlez pas");
	JTextArea textArea = new JTextArea();
	
	public static void main(String[] args) {
		EventQueue.invokeLater(new Runnable() {
			public void run() {
				try {
					GUI window = new GUI();
					window.frmJarvis.setVisible(true);
				} catch (Exception e) {
					e.printStackTrace();
				}
			}
		});
	}


	public GUI() {
		initialize();
	}


	private void initialize() {
		frmJarvis = new JFrame();
		frmJarvis.setTitle("Jarvis");
		frmJarvis.setBounds(100, 100, 869, 494);
		frmJarvis.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		frmJarvis.getContentPane().setLayout(null);
		
		BufferedImage myPicture;
		//URL url = new URL("file://C:/Users/MASSON/Desktop/jarvis_gif.gif");
		ImageIcon imageIcon = new ImageIcon("C:\\Users\\MASSON\\Desktop\\jarvis_intro.gif");
		
		Clip clip;
		try {
			clip = AudioSystem.getClip();
			URL url = new URL("file:\\C:\\Users\\MASSON\\Desktop\\jarvis_intro.wav");
			AudioInputStream ais = AudioSystem.getAudioInputStream(url);
			clip.open(ais);
			//clip.loop(0);
			
		} catch (LineUnavailableException | UnsupportedAudioFileException | IOException e1) {
			// TODO Auto-generated catch block
			e1.printStackTrace();
		}
		
		Image image = imageIcon.getImage(); // transform it 
		Image newimg = image.getScaledInstance(120, 120,  java.awt.Image.SCALE_SMOOTH); // scale it the smooth way  
		JLabel picLabel = new JLabel(imageIcon);

		picLabel.setForeground(Color.RED);
		picLabel.setFont(new Font("Tahoma", Font.PLAIN, 21));
		picLabel.setBounds(424, 30, 405, 321);
		frmJarvis.getContentPane().add(picLabel);



		JLabel lblNewLabel = new JLabel("Jarvis AI");
		lblNewLabel.setForeground(Color.RED);
		lblNewLabel.setFont(new Font("Tahoma", Font.PLAIN, 21));
		lblNewLabel.setBounds(238, 11, 131, 41);
		frmJarvis.getContentPane().add(lblNewLabel);

		JScrollPane scrollPane = new JScrollPane();
		scrollPane.setBounds(21, 116, 397, 235);
		frmJarvis.getContentPane().add(scrollPane);
		JTextArea textAreaMain = new JTextArea(20, 20);

		JButton button = new JButton("Lancer le chatbot");
		button.addActionListener(e -> {
			SwingWorker<Void, String> worker = new SwingWorker<Void, String>() {
				@Override
				protected Void doInBackground() throws Exception {

					String s = null;
					String ss = null;
					
					Process p = Runtime.getRuntime().exec("python C:\\Users\\MASSON\\Desktop\\ChatBot\\chatbot.py");
					
					BufferedReader stdInput = new BufferedReader(new InputStreamReader(p.getInputStream()));
					BufferedReader stdErrInput = new BufferedReader(new InputStreamReader(p.getErrorStream()));

					while ((s = stdInput.readLine()) != null) {
						ss = s;
						publish(ss);
					}
					/*while ((s = stdErrInput.readLine()) != null) {
						ss = s;
						publish(ss);
					}
					*/

					return null;
				}


				public void process(List<String> chuncks) {
					textArea.append(chuncks.get(0)+"\n");
					
					
				}
			};
			worker.execute();
		});


		button.setBounds(133, 60, 194, 45);
		frmJarvis.getContentPane().add(button);
		scrollPane.setColumnHeaderView(lblNewLabel_1);
				scrollPane.setViewportView(textArea);
		
				textArea.setEditable(false);
				textArea.setLineWrap(true);
				textArea.setOpaque(false);
				textArea.setBorder(BorderFactory.createEmptyBorder());

	}
}