// my first program in C++
#include <iostream>
#include <sstream>
using namespace std;
#define PI 3.14159
#include <png.h>
namespace myNamespace
{
	int a = 10;
	string b = "dlf";
	bool c = false;
	double d = 3.4;
	char e = 'e';
}
namespace kdl { int a; };
//! means not
//&& is like AND gate with bolean values
//|| is like OR
//&:AND;|:OR;^:XOR;~:NOT;<<:SHL;>>:SHR
int addition(int a, int b)
{
	return a+b;
}
void lap(int& a)
{
	a = 921;
}
inline void boope(int& a) //duplicates code at site, meant for short things
{
	a = 0;
}
template <class T> //could also be <int N>
T sum(T a, T b) //can declare type for default
{
	return a+b;
}
int scope(){
	int x = 10;
	int y = 20;
	{
		int x;
		x = 50;
		y = 50;
		cout << x << endl; //prints 50
		cout << y << endl; //prints 50
	}
	cout << x << endl; //prints 10
	cout << y << endl; //prints 50
}
int list [5] = {0,1,2,3,4};
int foo[]{0,1,2};
int listParse(int arg[])
{
	for(int n=0; n<sizeof(arg); ++n)
	{
		cout << arg[n] << endl;
	}
}
char lolz[] = "Hello peoples";
int helloz = 10;
int boobz = 1000;
int boobs; //boobs is a pointer!
int myvar;
int baz, boomz;
int a[5];
int main()
{
	char *mychar; //1000
	short *myshort; //2000
	long *mylong;  //3000
	++mychar; //1001 //takes up one byte
	++myshort; //2002 //takes up 2 bytes
	++mylong; //3004 //takes up 4 bytes
//	*p++   // same as *(p++): increment pointer, and dereference unincremented address
//	*++p   // same as *(++p): increment pointer, and dereference incremented address
//	++*p   // same as ++(*p): dereference pointer, and increment the value it points to
//	(*p)++ // dereference pointer, and post-increment the value it points to 
	a[5] = 0;
	*(a+5) = 0;
	int firstvalue, secondvalue;
	int * mypointer; //my pointer can be assigned a different address
	mypointer = &firstvalue;
	*mypointer = 10;
	mypointer = &secondvalue;
	*mypointer = 20;
	//firstvalue == 10, secondvalue == 20
	boobs = &myvar; //adress of
	baz = *boobs; //value stored at location boobs
	boomz = *myvar; //returns value of myvar
	cout << &lolz << endl;
	cout << boobs << endl;
	//baz = *boobz; //gets stuff at memory cell 1000
	//boomz = &helloz; //gets memory address
	cout << lolz[2] << endl;
	cout << list[1] << endl;
	cout << "Hello World!\n";
	string poop = "poop";
	int a, b, result;
	double blab = 3.4;
	cout << blab << endl;
	a = 5;
	b = 2;
	a += 1;
	for(char c : "abcde")
	{
	        cout << c << endl;
	}
	cout << myNamespace::c << endl;	//using does good
	string as = to_string(a); //like str
	cout << as << endl;
	result = a - b;
	cout << result;
	cout << poop;
	cout << ++b; //-- worksa
	if(1<10&&++a<1000);{cout << "POOPZ";};
	int c = (a>b) ? a : b; //return a or b?
	cout << c;
	cout << poop; 
	cout << sizeof(poop) << endl;
	string i;
	cin >> i; //input
	cout << i;
	string mystr;
	getline(cin,mystr); //gets everything like \n and whitespace
	cout << mystr << endl;
	string myster ("1204");
	int myint;
	stringstream(myster) >> myint; //have no idea
	cout << to_string(myint) << endl;
	cout << "####################";
	if(true)
		cout << "shit" << endl;
	else if(true)
		cout << "shart";
	else
		cout << "shirt";
	int strap = 1;
	while(strap < 11)
	{
		cout << strap;
		++strap;
	}
	int count = 0;
	do
	{
		++count;
		--count;
	}while(false);
	while(count < 100)
	{
		++count;
	}
	cout << "C++ DONE!" << endl;
	for (int n=0; n<10; n++) 
	{
		cout << n << ", ";
	}
	cout << endl;
	string str = "Hello!";
	for(char c : str)
	{
		if(c == 'l')
			break;
		else if(c == 'H')
			continue;
		cout << "{" << c << "]";
	}
	cout << endl;
	switch(true)
	{
		case 1:
			cout << 'a';
			break;
		default:
			cout << 'd';
	}
	cout << addition(5,3) << endl;
	lap(count);
	cout << count;
	boope(count);
	cout << sum<int>(7,8) << endl;
	listParse(list);
	return 0;
}
