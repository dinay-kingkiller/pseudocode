/*
SudokuSolver.cpp
Written by David Hann
This is the source file for SudokuSolver.exe, which solves a sudoku using ONLY logic (no guessing)
*/
#include <iostream>
#include <vector>
using namespace std;
const int MAXIGNORE=200;//for cin failure
const int SIZE=9;//size of the sudoku (regular 9x9)
const int NOBOX=3;//number of boxes per row
void define(vector<vector<vector<int> > > &sudoku);//defines the values originally given and assigns them
bool iteration(vector<vector<vector<int> > > &sudoku);//an iteration of trials; returns false if nothing can be done with current methods
void print(vector<vector<vector<int> > > &sudoku);//prints the sudoku where it's defined
//int check(vector<vector<vector<int> > > &sudoku);//checks for solved squares (ones that have only one possibility left)
bool eliminate(vector<vector<vector<int> > > &sudoku);//eliminates values that are already solved within the row, column or box
bool nakedPair(vector<vector<vector<int> > > &sudoku);//finds naked pairs in a row, column or box
bool nakedTriple(vector<vector<vector<int> > > &sudoku);//finds naked pairs in a box
bool inSameBox(int i1, int j1, int i2, int j2);//checks if (i1,j1) is in the same square as (i2,j2)
int inBox(int i, int j);//returns which box (i,j) is in// names go as follows:[[1 2 3] [4 5 6] [7 8 9]]
int pow(int num);//returns 10^num
bool add(vector<int> &vec, int added);//adds int added to vector vec if it's missing and adds it to the vec
bool remove(vector<int> &possible, int impossible);//removes integer impossible from possible, returns false if impossible isn't in possible 
int searchHole(vector<int> vec, int integer);//searches a vector to see if it has a value and returns the index of that value. returns -1 if fail
int search(vector<int> vec, int integer);//searches a vector to see if it has a value and returns the index of that value. returns -1 if fail
void match(vector<int> vec1, vector<int> vec2, vector<int> &similar);//finds a vector<int> &similar, where vec1 and vec2 intersect
void switchf(vector<int> &vec1, vector<int> &vec2);
void cinfail();//handles cin failure
int main()
{
	vector<int> vI1Matrix(SIZE);
	for (int i=0; i<SIZE; i++)
	{
		vI1Matrix[i]=i+1;
	}
	vector< vector<int> > vI2Matrix(SIZE, vI1Matrix);
	vector< vector< vector<int> > > sudoku(SIZE, vI2Matrix);
	define(sudoku);
	while (iteration(sudoku))
	print(sudoku);
	return 0;
}
void define(vector<vector<vector<int> > > &sudoku)
{
	int line[SIZE];
	bool fail;
	//cout<<"Type the values for the sudoku"<<endl
	//	<<"Type '0' if you don't know a value"<<endl;
	for (int i=0; i<SIZE; i++)
	{
		do
		{
			fail=false;
			//cout<<"Line "<<i+1<<" : ";
			//cin>>line[i];
			if (!cin)
			{
				cout<<"Error: Improper Value for Line "<<i+1<<"."<<endl;
				cinfail();
				fail=true;
			}
			if (line[i]/pow(SIZE)>0)
			{
				cout<<"Error: You entered too many values"<<endl;
				fail=true;
			}
		}while (fail);
	}
	line[0]=427100006;
	line[1]=    72000;
	line[2]=103060200;
	line[3]= 10900500;
	line[4]=670308092;
	line[5]=  9006010;
	line[6]=  1020904;
	line[7]=   780000;
	line[8]=900001725;
	for (int i=0; i<SIZE; i++)
	{
		for (int j=0; j<SIZE; j++)
		{
			if (line[i]/pow(SIZE-1-j)!=0)
			{
				sudoku[i][j].clear();
				sudoku[i][j].push_back(line[i]/pow(SIZE-1-j));
			}
			line[i]=line[i]%pow(SIZE-1-j);
		}
	}
}
bool iteration(vector<vector<vector<int> > > &sudoku)
{
	bool change=false;
	if (!change)
	{
		if (eliminate(sudoku))
		{
			change=true;
		}
	}
	if (!change)
	{
		if (nakedPair(sudoku))
		{
			change=true;
		}
	}
	if (!change)
	{
		return false;
	}
	else return true;
}
void print(vector<vector<vector<int> > > &sudoku)
{
	cout<<"-------------------"<<endl;
	for (int i=0; i<SIZE; i++)
	{
		for (int j=0; j<SIZE; j++)
		{
			if ((j+1)%3==1)
			{
				cout<<"|";
			}
			else cout<<" ";
			if (sudoku[i][j].size()==1)
			{
				cout<<sudoku[i][j][0];
			}
			else
			{
				cout<<" ";
			}
		}
		cout<<"|"<<endl;
		if (i%3==2)
		{
			cout<<"-------------------"<<endl;
		}
		else
		{
			//cout<<endl;
		}
	}
	cout<<endl;
}
bool eliminate(vector<vector<vector<int> > > &sudoku)
{
	bool change=false;
	for (int i=0; i<SIZE; i++)
	{
		for (int j=0; j<SIZE; j++)
		{
			for (int k=0; k<SIZE; k++)
			{
				if (sudoku[i][k].size()==1 && j!=k)
				{
					if (remove(sudoku[i][j],sudoku[i][k][0]))
					{
						change=true;
					}
				}
				if (sudoku[k][j].size()==1 && i!=k)
				{
					if (remove(sudoku[i][j],sudoku[k][j][0]))
					{
						change=true;
					}
				}
				for (int l=0; l<SIZE; l++)
				{
					if (sudoku[k][l].size()==1 && inSameBox(i,j,k,l) && i!=k && j!=l)
					{
						if (remove(sudoku[i][j],sudoku[k][l][0]))
						{
							change=true;
						}
					}
				}
			}
		}
	}
	if (change)
	{
		return true;
	}
	else return false;
}
bool nakedPair(vector<vector<vector<int> > > &sudoku)
{
	bool change=false;
	for (int i=0; i<SIZE; i++)
	{
		for (int j=0; j<SIZE; j++)
		{
			if (sudoku[i][j].size()==2)
			{
				for (int k=0; k<SIZE; k++)
				{
					if (j!=k && sudoku[i][k].size()==2 && sudoku[i][j][0]==sudoku[i][k][0] && sudoku[i][j][1]==sudoku[i][k][1])
					{//[i][j] and [i][k] are naked pairs
						for (int l=0; l<SIZE; l++)
						{
							if (l!=j && l!=k)
							{
								if (remove(sudoku[i][l],sudoku[i][j][0]))
								{
									change=true;
								}
								if (remove(sudoku[i][l],sudoku[i][j][1]))
								{
									change=true;
								}
							}
						}
					}
					if (i!=k && sudoku[k][j].size()==2 && sudoku[i][j][0]==sudoku[k][j][0] && sudoku[i][j][1]==sudoku[k][j][1])
					{//[i][j] and [k][j] are naked pairs
						for (int l=0; l<SIZE; l++)
						{
							if (l!=i && l!=k)
							{
								if (remove(sudoku[l][j],sudoku[i][j][0]))
								{
									change=true;
								}
								if (remove(sudoku[l][j],sudoku[i][j][1]))
								{
									change=true;
								}
							}
						}
					}
					for (int l=0; l<SIZE; l++)
					{
						if (inSameBox(i,j,k,l) && i!=k && j!=l && sudoku[k][l].size()==2 && sudoku[i][j][0]==sudoku[k][l][0] && sudoku[i][j][1]==sudoku[k][l][1])
						{
							for (int m=0; m<SIZE; m++)
							{
								for (int n=0; n<SIZE; n++)
								{
									if (inSameBox(i,j,m,n))
									{
										if (remove(sudoku[m][n],sudoku[i][j][0]))
										{
											change=true;
										}
										if (remove(sudoku[m][n],sudoku[i][j][1]))
										{
											change=true;
										}
									}
								}
							}
						}
					}
				}
			}	
		}
	}
	if (change)
	{
		return true;
	}
	else return false;
}
bool nakedTriple(vector<vector<vector<int> > > &sudoku)
{
	vector<int> matchvec;
	bool change=false;
	for (int i=0; i<SIZE; i++)	{
		for (int j=0; j<SIZE; j++)		{
			if (sudoku[i][j].size()==3)			{
				for (int k=0; k<SIZE; k++)				{
					if (i!=k)					{
						match(sudoku[i][j], sudoku[k][j], matchvec);
						if (matchvec.size()<3) {
							for (int l=0; l<SIZE; l++)
							{
								matchvec.clear();
								if (i!=l && k!=l)
								{
									match(sudoku[i][j], sudoku[l][j], matchvec);
									if (matchvec.size()<3)
									{
										for (int m=0; m<SIZE; m++)
										{
											if (m!=i && m!=k && m!=l)
											{
												if (remove(sudoku[m][j],sudoku[i][j][0]))
												{
													change=true;
												}
												if (remove(sudoku[m][j],sudoku[i][j][1]))
												{
													change=true;
												}
												if (remove(sudoku[m][j],sudoku[i][j][2]))
												{
													change=true;
												}
											}
										}
									}
								}
							}
						}
						matchvec.clear();
					}
					if (j!=k)
					{
						match(sudoku[i][j], sudoku[i][k], matchvec);
						if (matchvec.size()<3)
						{
							for (int l=0; l<SIZE; l++)
							{
								matchvec.clear();
								if (j!=l && k!=l)
								{
									match(sudoku[i][j], sudoku[i][l], matchvec);
									if (matchvec.size()<3)
									{
										for (int m=0; m<SIZE; m++)
										{
											if (m!=j && m!=k && m!=l)
											{
												if (remove(sudoku[i][m],sudoku[i][j][0]))
												{
													change=true;
												}
												if (remove(sudoku[i][m],sudoku[i][j][1]))
												{
													change=true;
												}
												if (remove(sudoku[i][m],sudoku[i][j][2]))
												{
													change=true;
												}
											}
										}
									}
								}
							}
						}
						matchvec.clear();
					}
					for (int l=0; l<SIZE; l++)
					{
						if ((i!=k || j!=l) && inSameBox(i,j,k,l))
						{
						}
					}
				}
			}
		}
	}
	if (change)
	{
		return true;
	}
	else return false;
}
bool inSameBox(int i1, int j1, int i2, int j2)
{
	if (inBox(i1,j1)==inBox(i2,j2))
	{
		return true;
	}
	else return false;
}
int inBox(int i, int j)//returns 0 if failure
{
	switch (i/NOBOX)
	{
	case 0:
		switch (j/NOBOX)
		{
		case 0:
			return 1;
			break;
		case 1:
			return 2;
			break;
		case 2:
			return 3;
			break;
		default:
			cout<<"Bound 'j' is not within sudoku"<<endl;
			return 0;
			break;
		}
		break;
	case 1:
		switch (j/NOBOX)
		{
		case 0:
			return 4;
			break;
		case 1:
			return 5;
			break;
		case 2:
			return 6;
			break;
		default:
			cout<<"Bound 'j' is not within sudoku"<<endl;
			return 0;
			break;
		}
		break;
	case 2:
		switch (j/NOBOX)
		{
		case 0:
			return 7;
			break;
		case 1:
			return 8;
			break;
		case 2:
			return 9;
			break;
		default:
			cout<<"Bound 'j' is not within sudoku"<<endl;
			return 0;
			break;
		}
		break;
	default:
		cout<<"Bound 'i' is not within sudoku"<<endl;
		return 0;
		break;
	}
}
int pow(int num)//10^num
{
	int n=1;
	for (int i=0; i<num; i++)
	{
		n=n*10;
	}
	return n;
}
bool add(vector<int> &vec, int added)
{
	int length;
	int add;
	vector<int> temp;
	if (searchHole(vec, added)!=-1)
	{
		length=vec.size();
		add=searchHole(vec,added);
		temp.resize(length+1);
		for (int i=0; i<length+1; i++)
		{
			if (i<add)
			{
				temp[i]=vec[i];
			}
			else if (i==add)
			{
				temp[i]=added;
			}
			else if (i>add)
			{
				temp[i]=vec[i-1];
			}
		}
		vec.clear();
		vec.resize(length+1);
		for (int i=0; i<length+1; i++)
		{
			vec[i]=temp[i];
		}
	}
	else return false;
}
bool remove(vector<int> &possible, int impossible)
{
	int length;
	int removed;
	vector<int> temp;
	if (search(possible, impossible)!=-1)
	{
		length=possible.size();
		removed=search(possible,impossible);
		temp.resize(length-1);
		for (int i=0; i<length; i++)
		{
			if (i<removed)
			{
				temp[i]=possible[i];
			}
			else if (i>removed)
			{
				temp[i-1]=possible[i];
			}
		}
		possible.clear();
		possible.resize(length-1);
		for (int i=0; i<length-1; i++)
		{
			possible[i]=temp[i];
		}
		return true;
	}
	else return false;
}
int search(vector<int> vec, int integer)
{
	bool found=false;
	for (int i=0; i<vec.size(); i++)
	{
		if (vec[i]==integer)
		{
			return i;
			break;
		}
	}	
	if (!found)
	{
		return -1;
	}
}
int searchHole(vector<int> vec, int integer)
{
	bool found=false;
	for (int i=0; i<vec.size(); i++)
	{
		if (vec[i]>integer)
		{
			return i;
			break;
		}
	}	
	if (!found)
	{
		return -1;
	}
}
void match(vector<int> vec1, vector<int> vec2, vector<int> &similar)
{
	int length;
	if (vec1.size()<vec2.size())
	{
		switchf(vec1, vec2);
	}
	length=vec1.size();
	for (int i=0; i<length; i++)
	{
		if (search(vec2,vec1[i]))
		{
			similar.push_back(vec1[i]);
		}
	}
}
void switchf(vector<int> &vec1, vector<int> &vec2)
{
	vector<int> vectemp(vec2.size(), 0);
	for (int i=0; i<vec2.size(); i++)
	{
		vectemp[i]=vec2[i];
	}
	vec2.clear();
	vec2.resize(vec1.size());
	for (int i=0; i<vec1.size(); i++)
	{
		vec2[i]=vec1[i];
	}
	vec1.clear();
	vec1.resize(vectemp.size());
	for (int i=0; i<vectemp.size(); i++)
	{
		vec1[i]=vectemp[i];
	}
}
void cinfail()
{
	cin.clear(); // changes input state to ok
	cin.ignore(MAXIGNORE,'\n'); // gets beyond bad input characters
}
