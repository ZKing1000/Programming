#include "SDL/SDL.h"
#include "iostream"
#include "vector"
#include "SDL/SDL_image.h"
#include "SDL/SDL_ttf.h"
using namespace std;

int main(){
	TTF_Init();
	const int FPS = 60;
	int frame;
	SDL_Surface* hello = NULL;
	SDL_Surface* screen = NULL;
	SDL_Surface* message = NULL;
	SDL_Color textColor = { 255,0,255 };
	SDL_Rect offset;
	offset.x = 100;
	offset.y = 100;
	SDL_Init(SDL_INIT_EVERYTHING);
	screen = SDL_SetVideoMode(1024,576,32,SDL_SWSURFACE);
	hello = IMG_Load("img.png");
	SDL_BlitSurface(hello,NULL,screen,&offset);
	SDL_Flip(screen);
	SDL_Event event;
	bool on = true;
	vector< vector<float> > floatPositions;
	cout << "\n\n\n\n\n";
	vector< SDL_Rect > myrect;
	for(int i=0;i<myrect.size();i++){
		myrect[i].x = i*100;
		myrect[i].y = i*100;
	}
	struct Mouse{
		int x,y;
	};
	Mouse mouse;
	SDL_Rect screenRect;
	screenRect.x = screenRect.y = 0;
	screenRect.w = screen->w;
	screenRect.h = screen->h;
	TTF_Font *font = NULL;
	font = TTF_OpenFont( "font.ttf", 10 );
	message = TTF_RenderText_Solid( font, "The quick brown fox jumps over the lazy dog", textColor );
	int start;
	SDL_Rect textPos;
	textPos.x = 100; textPos.y = 100;
	while(on){
		start = SDL_GetTicks();
		//cout << "EXE " << start;
		while(SDL_PollEvent(&event)){
			if(event.type == SDL_QUIT){
				on = false;
			}else if(event.type == SDL_KEYDOWN){
				myrect.push_back(SDL_Rect());
				int size = myrect.size()-1;
				myrect[size].x = 0;
				myrect[size].y = 0;
				floatPositions.push_back(vector<float>(2));
			}
		}
		SDL_GetMouseState(&mouse.x,&mouse.y);
		offset.x++;
		offset.y++;
		SDL_FillRect(screen, NULL, 0x00FFFF);
		SDL_BlitSurface(hello,NULL,screen,&offset);
		SDL_BlitSurface( message, NULL, screen, &textPos );
		for(int i=0;i<myrect.size();i++){
			//cout << "#######\n";
			//cout << "mouse: " << mouse.x << ',' << mouse.y << endl;
			int dif[2];
			dif[0] = abs(myrect[i].x-mouse.x);
			dif[1] = abs(myrect[i].y-mouse.y);
			float sum = dif[0]+dif[1];
			//cout << "dif: " << dif[0] << ',' << dif[1] << ',' << sum << endl;
			float incrament[2];
			incrament[0] = dif[0]/sum;
			incrament[1] = dif[1]/sum;
			if(myrect[i].x>mouse.x){
				incrament[0] = -incrament[0];
			}
			if(myrect[i].y>mouse.y){
				incrament[1] = -incrament[1];
			}
			//cout << "incrament: " << incrament[0] << ',' << incrament[1] << endl;
			floatPositions[i][0] += incrament[0];
			floatPositions[i][1] += incrament[1];
			myrect[i].x = int(floatPositions[i][0]+0.5);
			myrect[i].y = int(floatPositions[i][1]+0.5);
			//cout << "myrect: " << myrect[i].x << ',' << myrect[i].y << endl;
			SDL_BlitSurface(hello,NULL,screen,&myrect[i]);
		}
		cout << hello << endl;
		SDL_Flip(screen);
		if( (SDL_GetTicks()-start) < (1000/FPS) ){
			SDL_Delay( (1000/FPS) - (SDL_GetTicks()-start) );
		}

	}
	SDL_FreeSurface(hello);
	SDL_Quit();
	return 0;
}
