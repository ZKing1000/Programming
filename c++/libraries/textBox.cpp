#include "SDL/SDL.h"
#include "SDL/SDL_ttf.h"
#include <vector>
#include <array>
#include <iostream>
using namespace std;
class Display{
	protected:
		SDL_Surface* screen;
		vector< SDL_Rect > coords;
	public:
		Display(SDL_Surface* screen,vector< SDL_Rect > coords){
			this->screen = screen;
			this->coords = coords;
			cout << "POOP\n";
		};
};
int main(){
	TTF_Init();
	SDL_Init(SDL_INIT_EVERYTHING);
	SDL_Surface* screen = NULL;
	array<int,2> screenSize = {1,1};
	screen = SDL_SetVideoMode(screenSize[0],screenSize[1],32,SDL_SWSURFACE);
	SDL_Rect coords1;
	coords1.x = 1;
	coords1.y = 1;
	SDL_Rect coords2;
	coords2.x = 1;
	coords2.y = 1;
	vector<SDL_Rect> coords = {coords1,coords2};
	Display test(screen,coords);
	return 1;
}
