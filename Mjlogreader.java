import java.io.*;
import java.nio.*;
import java.util.*;
/**
 * Reads the mjlog and outputs mahjong data. Only takes the player 3's data for now.
 * @author Kochi Nakajima
 */

/** Hais array
 0 ~ 8 Manzu 1,2,3.....9
 9 ~ 17 Pinzu
 18 ~ 26 Souzu
 27 ~ 30 Directions E, S, W, N
 31 ~ 33 Dragons W, G, R
 test
*/

public class Mjlogreader{
  int[] hand;
  int[] discardPile;
  int discarded;
  Integer PLAYERID = 0;
  String data;
  BufferedReader br;
  String TSUMO;
  String DAHAI;
  final static String ENDSIGN = "/>";
  String[] temp;
  int[] startGame;
  int junme;
  int curr_game;
  int curr_ptr;

  public Mjlogreader(String filename){
    hand = new int[34];
    discardPile = new int[34];
    startGame = new int[20];
    switchPlayer();
    try{
      br = new BufferedReader(new FileReader(filename));
      data = br.readLine();
      if(PLAYERID != 3){
        temp = data.substring(data.indexOf("hai" + PLAYERID.toString() +  "=") + 6, data.indexOf("hai" + (PLAYERID + 1) + "=") - 2).split(",");
      }else{
        temp = data.substring(data.indexOf("hai" + PLAYERID.toString() +  "=") + 6, data.indexOf(ENDSIGN, data.indexOf("hai" + PLAYERID.toString() +  "=")) - 1).split(",");
      }
      for(int i = 0; i < temp.length; i++){
        hand[tileConverter(Integer.parseInt(temp[i]))]++;
      }
      int idx = 0;
      startGame[idx] = data.indexOf("<INIT");
      while(data.indexOf("<INIT", startGame[idx] + 1) != -1){
        idx++;
        startGame[idx] = data.indexOf("<INIT", startGame[idx - 1] + 1);
      }
      junme = 0;
    }catch(IOException e){
      System.out.println("error");
    }
  }

  private void switchPlayer(){
    switch(PLAYERID){
      case 0:
        TSUMO = "<T";
        DAHAI = "<D";
        break;
      case 1:
        TSUMO = "<U";
        DAHAI = "<E";
        break;
      case 2:
        TSUMO = "<V";
        DAHAI = "<F";
        break;
      case 3:
        TSUMO = "<W";
        DAHAI = "<G";
        break;
    }
  }


  public int tileConverter(int mjlognumber){
    return mjlognumber >> 2;
  }


  public int[] getHand(){
    return hand;
  }

  public int[] getDiscardPile(){
    return discardPile;
  }

  public int getDiscardedTile(){
    return discarded;
  }

  /**
   * Goes around all the players
   * For naki, just come back.
   * When junme == 0, it will only TSUMO
   * When junme > 0, it will discard and Tsumo.
   */
  public boolean next(){
    int tsumo;
    if(junme == 0){
      junme++;
      curr_ptr = startGame[curr_game];
      tsumo = getNextTile(true);
      System.out.println("Tsumo: " + tsumo);
      hand[tsumo]++;
    }else if(curr_ptr > startGame[curr_game + 1] || curr_ptr == -1){
      System.out.println("--------");
      System.out.println("End of Kyoku");
      System.out.println("--------");
      curr_game++;
      if(startGame[curr_game] == 0){
        System.out.println("--------");
        System.out.println("--------");
        System.out.println("END OF THE GAME");
        return false;
      }else{
        System.out.println("Press enter to continue");
        Scanner s = new Scanner(System.in);
        if(s.nextLine() != null){
          newGame();
        }
      }
    }else{
      junme++;
      discarded = getNextTile(false);
      System.out.println("Discard: " + discarded);
      System.out.println("Junme: " + junme);
      hand[discarded]--;
      discardPile[discarded]++;
      tsumo = getNextTile(true);
      System.out.println("Tsumo: " + tsumo);
      hand[tsumo]++;
    }
    return true;
  }

  private void newGame(){
    temp = data.substring(data.indexOf("hai2=", startGame[curr_game]) + 6, data.indexOf("hai3=", startGame[curr_game]) - 2).split(",");
    Arrays.fill(hand, 0);
    Arrays.fill(discardPile, 0);
    for(int i = 0; i < temp.length; i++){
      hand[tileConverter(Integer.parseInt(temp[i]))]++;
    }
    junme = 0;
  }

  private void printHandArray(){
    System.out.println("---------");

    for(int i = 0; i < 34; i++) {
    			if(i == 0) System.out.print("M: ");
    			if(i == 9) System.out.print("\nP: ");
    			if(i == 18) System.out.print("\nS: ");
    			if(i == 27) System.out.print("\nW: ");
    			if(i == 31) System.out.print("\nD: ");
    			System.out.print(hand[i] + ", ");
    		}
    	System.out.println("\n---------");
  }

  private int getNextTile(boolean isTsumo){
    String indicator;
    indicator = (isTsumo)? TSUMO : DAHAI;
    curr_ptr = data.indexOf(indicator, curr_ptr);
    int returnVal = tileConverter(Integer.parseInt(data.substring(data.indexOf(indicator, curr_ptr) + 2, data.indexOf(ENDSIGN, curr_ptr))));
    return returnVal;
  }
  
  private void toCSV(String filename){
    //Need shantensuu
    //Write out in format of Junme, Shanten, Tehai, Sutehai

    String data = "dataToWrite";
    try{
      FileWriter fw = new FileWriter(filename + ".csv");
      fw.append(data);
      fw.flush();
      fw.close();
    }catch(IOException e){
      e.printStackTrace();
    }
  }

  public static void main(String[] args){
    Mjlogreader mr = new Mjlogreader("sample2.mjlog");
    do{
      mr.printHandArray();
    }while(mr.next());
    mr.toCSV("test");
  }
  
  

}
