#include <iostream>
class Example{
	int integer;
	public:
	Example():integer (1){}
	void printStuff(std::string stuff){
		std::cout << stuff << '\n';
	}
};
