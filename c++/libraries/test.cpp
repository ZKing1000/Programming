#include "SDL/SDL.h"
#include "SDL/SDL_ttf.h"
#include <vector>
#include <array>
#include "textBox.h"
using namespace std;
int main(){
	TTF_Init();
	SDL_Surface* screen = NULL;
	array<int,2> screenSize = {400,200};
	screen = SDL_SetVideoMode(screenSize[0],screenSize[1],32,SDL_SWSURFACE);
	SDL_Rect coords1;
	coords1.x = 0;
	coords1.y = 0;
	SDL_Rect coords2;
	coords2.x = 400;
	coords2.y = 200;
	SDL_Color background = {255,255,255};
	SDL_Color outline = {0,0,0};
	SDL_Color textC = {0,0,0};
	array<SDL_Rect,2> coords = {coords1,coords2};
	Display test(screen,coords,"BLAHdsfdfafdafdfas",true,"font.ttf",background,outline,textC,false,2);
	SDL_Rect coord;
	coord.x = 0;
	coord.y = 0;
	test.draw(coord);
	SDL_Rect blahp;
	blahp.x = 200;
	blahp.y = 100;
	SDL_Surface* draw = test.drawSurface;
	SDL_BlitSurface(draw,NULL,screen,&coord);
	SDL_FillRect(screen,NULL,0x00ffff);
	SDL_Surface* second = textGen(blahp,"TESTICLES",true,true,"font.ttf",textC);
	SDL_BlitSurface(second,NULL,screen,&coord);
	SDL_Rect blaht;
	blaht.x = 200;
	blaht.y = 0;
	SDL_BlitSurface(second,NULL,screen,&blaht);
	cout << draw->w << endl;
	DynamicDisplay hi(blahp,"TESTICLES",true,true,"font.ttf",textC);
	hi.draw(screen);
	SDL_Flip(screen);
	std::cin.ignore();
	return 1;
}
