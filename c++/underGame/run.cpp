#include <iostream>
#include "./lib/game.h"
#include "SDL/SDL.h"
#include "SDL/SDL_ttf.h"

using namespace std;
int main(){
	array<int,2> screenSize = {1024,576};
	Game game(screenSize);
	game.menu();
	game.play();
	cout << "SUCCESS\n";
	return 1;
}
