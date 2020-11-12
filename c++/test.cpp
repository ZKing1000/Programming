#include <iostream>
#include <cmath>

/*int main(){
	std::string crap = "here";
	std::cout << crap << std::endl;
	crap = std::string ( crap.rbegin(), crap.rend() );
	std::cout << crap << std::endl;
	return 1;
}*/

int main(){
	int blah = 4;
	std::cout << blah << std::endl;
	blah = -blah;
	std::cout << blah << std::endl;
	blah = std::abs(blah);
	std::cout << blah << std::endl;
	return 1;
}
