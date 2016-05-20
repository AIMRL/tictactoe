# include <iostream>

int getFirstEmptyCell(int board[])
{
	int retval = 0;
	for(int i=0;i<9;++i){
		if(board[i]==0)
		{
			retval=i;
			break;
		}
	}
	return retval;
}

int main(void)
{
	int whoIAm, board[9];
	std::cin>>whoIAm;
	while(true)
	{
		for(int i=0;i<9;++i)
			std::cin>>board[i];
		std::cout<<getFirstEmptyCell(board)<<std::endl;
	}
	return 0;
}
