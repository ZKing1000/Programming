#include "SDL/SDL.h"
#include <iostream>
#include "SDL/SDL_ttf.h"

int main(){
	SDL_Surface* surface;
	TTF_Init();
	int width = 100;
	int height = 100;
#if SDL_BYTEORDER == SDL_BIG_ENDIAN
	surface = SDL_CreateRGBSurface(SDL_HWSURFACE,width,height,32, 0, 0, 0, 255);
#else
	surface = SDL_CreateRGBSurface(SDL_HWSURFACE,width,height,32, 0, 0, 0, 100);
#endif
	std::cout << surface->w << std::endl;
	SDL_FillRect(surface,NULL,0xffffff);
	SDL_Surface* screen;
	screen = SDL_SetVideoMode(1024,576,32,SDL_SWSURFACE);
	SDL_Rect coord;
	coord.x = 0; coord.y = 0;
	SDL_FillRect(screen, NULL, 0x00FFFF);
	SDL_BlitSurface(surface,NULL,screen,&coord);
	TTF_Font *font = NULL;
	font = TTF_OpenFont("font.ttf",10);
	SDL_Color color = {0,0,0};
	SDL_Surface* text = TTF_RenderText_Solid(font,"test",color);
	SDL_BlitSurface(text,NULL,screen,&coord);
	SDL_Flip(screen);
	std::cin.ignore();
	return 1;
}
