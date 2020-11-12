#include <iostream>
#include <vector>
#include <array>
#include "SDL/SDL.h"
#include "SDL/SDL_image.h"
#include "SDL/SDL_ttf.h"
#include "SDL/SDL_opengl.h"
#include "textBox.h"
#include "lib.h"

class Game{
public:
std::array<int,2> screenSize;
SDL_Surface* screen;

int mode = 0;
int on = true;

std::string mainFontPath = "./graphics/fonts/font.ttf";

Game(std::array<int,2> screenSize);
void menu();
void play();
};

Game::Game(std::array<int,2> screenSize):
	screenSize(screenSize),
	screen(SDL_SetVideoMode(screenSize[0],screenSize[1],32,SDL_SWSURFACE))
{
	SDL_Init(SDL_INIT_EVERYTHING);
	TTF_Init();
}

void Game::menu(){
	SDL_FillRect(screen,NULL,0x00ffff);
	SDL_Rect size = {screenSize[0]/2,screenSize[1]/8};
	SDL_Color textC = {255,0,255};
	textBox_DynamicDisplay dynamic(size,"",true,false,mainFontPath,textC);
	SDL_Rect where = {(screenSize[0]-size.x)/2,0};
	SDL_FillRect(screen,NULL,0x00ffff);
	SDL_Color color = {255,255,255,255};
	dynamic.background(textC,color);
	lib_fps fps(12);
	textBox_AddOverTime display(&dynamic,"Welcome to my game!",1);
	bool on = true;
	bool runText = true;
	lib_mouse mouse;
	SDL_Event event;
	while(on){
		fps.tick();
		while(SDL_PollEvent(&event)){
			if(event.type == SDL_QUIT){
				on = false;
				this->on = false;
			/*}else if(event.type == SDL_KEYDOWN){
			}*/
			}else if(event.type == SDL_MOUSEBUTTONDOWN){
				SDL_GetMouseState(&mouse.x,&mouse.y);
				if(mouse.inRect(where,dynamic.surface->w,dynamic.surface->h)){
					std::cout << "mouse in rect\n";
					this->mode = 1;
					on = false;
				}
			}
		}
		SDL_FillRect(screen,NULL,0xff00ff);
		if(runText){
			if(display.add()){runText = false;}
		}
		dynamic.draw(screen,&where);
		SDL_Flip(screen);
	}
	/*std::string data = " added";
	std::string use;
	for(int i=0;i<data.size();i++){
		SDL_FillRect(screen,NULL,0x00ffff);
		dynamic.add(use+data[i]);
		//dynamic.surface = background(dynamic.surface,color,color);
		dynamic.draw(screen,&where);
		SDL_Flip(screen);
		SDL_Delay(2000);
	}*/
}

void Game::play(){
	SDL_Delay(5000);
	std::cout << "you made it!\n";
	this->on = false;
}
