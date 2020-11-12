#include <iostream>
#include <array>
#include <vector>
#include "SDL/SDL.h"
#include "SDL/SDL_image.h"
#include "SDL/SDL_ttf.h"

class lib_fps{
	public:
		int fps;

		int start;

		lib_fps(int fps);
		void tick();
};

lib_fps::lib_fps(int fps):
	fps(fps)
{
}

void lib_fps::tick(){
	if((SDL_GetTicks()-start) < (1000/fps) ){
		SDL_Delay((1000/fps)-(SDL_GetTicks()-start));
	}
	start = SDL_GetTicks();
}

struct lib_mouse{
	int x=0;
	int y=0;

	bool inRect(SDL_Rect pos,int w,int h){
		if(x > pos.x && y > pos.y && x < (pos.x+w) && y < (pos.y+h)){
			return true;
		}else{
			return false;
		}
	}
};
