import java.util.Scanner;

public class SampleAgent {

	private static int getFirstEmptySpace(int board[])
	{
		int retval = 0;
		for(int i=0;i<board.length;++i){
			if (board[i] == 0){
				retval = i;
				break;
			}
		}
		return retval;
	}
	
	public static void main(String[] args) {
		// TODO Auto-generated method stub
		int whoIAM, board[];
		board = new int[9];
		Scanner s = new Scanner(System.in);
		whoIAM = s.nextInt();
		while(true){
			for(int i=0;i<9;++i)
				board[i] = s.nextInt();
			System.out.println(getFirstEmptySpace(board));			
		}
	}

}
