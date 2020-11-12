#include "SDL/SDL.h"
#include "iostream"
#include <cstdlib>
#include "vector"
#include "SDL/SDL_image.h"
#include "SDL/SDL_ttf.h"
#include <ctime>
#include <map>
#include <cmath>
using namespace std;

const int screenSize[2] = {1024,576};

float reputation = 0.0;

const float maxReputation = 70.0;

int weather = 50;

const float maxWeather = 100.0;

const int difficulty = 12;

int price = 200;

const float maxPrice = 200.0;

float likeRange = 0.4;

bool doSrand(){
	srand(time(0));
	return true;
}
bool initRand = doSrand();

map<string,float> recipie =
{
	{"coffee",0.5},
	{"milk",0.3},
	{"sugar",0.2}
};

map<string,int> inventory =
{
	{"cups",0},
	{"coffee",0},
	{"milk",0},
	{"sugar",0}
};

float no1 = (rand()%10)/10.0;
float no2 = (rand()%(10-int(no1*10)))/10.0;

map<string,float> preferences =
{
	{"coffee",no1},
	{"milk",no2},
	{"sugar",(1.0-no1-no2)/1.0}
};


int main(){
	TTF_Init();
	SDL_Init(SDL_INIT_EVERYTHING);
	cout << preferences["coffee"] << endl;
	cout << preferences["milk"] << endl;
	cout << preferences["sugar"] << endl;

	const int FPS = 60;
	int frame;
	SDL_Surface* hello = NULL;
	SDL_Surface* screen = NULL;
	SDL_Surface* message = NULL;
	SDL_Surface* shop = NULL;
	SDL_Color textColor = { 255,0,255 };
	SDL_Rect offset;
	offset.x = 100;
	offset.y = 100;
	screen = SDL_SetVideoMode(screenSize[0],screenSize[1],32,SDL_SWSURFACE);
	hello = IMG_Load("img.png");
	SDL_BlitSurface(hello,NULL,screen,&offset);
	SDL_Flip(screen);
	SDL_Event event;
	bool on = true;
	vector< vector<float> > floatPositions;
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
	cout << "test" << endl;
	shop = IMG_Load("shop.png");
	SDL_Rect shopPos;
	shopPos.x = (screenSize[0]-shop->w)/2;
	shopPos.y = (screenSize[1]-64-shop->h);
	struct Person{
		SDL_Rect coords;
		int increment;
		int skin;
		int status;
		int howLong;
		int stopPos;
		int decision;
		SDL_Rect expresionPos;
		int expression;
		Person(){
			coords.y = screenSize[1]-96;
			coords.x = 0;
			increment = 1; //right = negative, left = positive;
			if(rand()%2 == 0){
				increment = -increment;
				coords.x = screenSize[0];
			}
			skin = rand()%3; //index in array of surfaces;
			status = 0; //If they are deciding;
			howLong = 0; //Counts how long they have been deciding status;
			stopPos = 432+(rand()%(4*32));
			decision = rand()%int(((((weather/maxWeather)*difficulty)*.3)+(((price/maxPrice)*difficulty)*((70-reputation)/100.0))+((((maxReputation-reputation)/maxReputation)*difficulty)*(reputation/100.0)))+0.5);
			//cout << int(((((weather/maxWeather)*difficulty)*.3)+(((price/maxPrice)*difficulty)*((70-reputation)/100.0))+((((maxReputation-reputation)/maxReputation)*difficulty)*(reputation/100.0)))+0.5) << endl;
			float value = ((((weather/maxWeather)*difficulty)*.3)+(((price/maxPrice)*difficulty)*((70-reputation)/100.0))+((((maxReputation-reputation)/maxReputation)*difficulty)*(reputation/100.0)))+0.5;
			value = value * difficulty;
			// decision = pick random number within range
			expresionPos.y = coords.y-32;
			float dif = float(rand()%7);
			if(dif==0){
				dif = 0.0;
			}else if(dif<=3){
				dif = 0.1;
			}else if(dif<=6){
				dif = 0.3;
			}else if(dif==7){
				dif = 1.2;
			}
			float fullDif = fabsf(recipie["coffee"]-(preferences["coffee"]+dif))+fabsf(recipie["milk"]-preferences["milk"])+fabsf(recipie["sugar"]-preferences["sugar"])+dif;
			expression = 3;
			if(decision==1){
				cout << fullDif << endl;
				cout << reputation << " ########\n";
				if(fullDif <= likeRange){
					reputation += likeRange-fullDif;
					expression = 1;
				}else if(fullDif >= likeRange*2){
					reputation -= fullDif-(likeRange*2);
					expression = 2;
				}
				if(reputation>=70){
					reputation = 70;
				}else if(reputation<=0){
					reputation = 0;
				}
			}

		}
	};
	while(on){
	}
	vector< Person > people;
	SDL_Surface* skins[3] = {IMG_Load("person0.png"),IMG_Load("person1.png"),IMG_Load("person2.png")};
	SDL_Surface* expresions[4] = {IMG_Load("nah.png"),IMG_Load("good.png"),IMG_Load("ew.png"),IMG_Load("ok.png")};
	int cache = 0;
	while(on){
		start = SDL_GetTicks();
		//cout << "EXE " << start;
		while(SDL_PollEvent(&event)){
			if(event.type == SDL_QUIT){
				on = false;
			}else if(event.type == SDL_KEYDOWN){
			people.push_back(Person());
			}
		}
		SDL_GetMouseState(&mouse.x,&mouse.y);
		offset.x++;
		offset.y++;
		SDL_FillRect(screen, NULL, 0x00FFFF);
		//SDL_BlitSurface(hello,NULL,screen,&offset);
		//SDL_BlitSurface( message, NULL, screen, &textPos );
		SDL_BlitSurface(shop,NULL,screen,&shopPos);
		for(int i=0;i<people.size();i++){
			if(people[i].status == 1){
				if(people[i].howLong == 180){
					if(people[i].decision <= 1){
						people[i].status = 2;
					}else{
						people[i].status = 6;
					}
					people[i].howLong = -1;
				}
				people[i].howLong++;
				people[i].coords.x -= people[i].increment;
			}else if(people[i].status == 2 || people[i].status == 4){
				if(people[i].howLong == 64){
					people[i].status++;
					people[i].howLong = 0;
				}
				people[i].howLong++;
				if(people[i].howLong%2 == 0){
					if(people[i].status == 2){
						people[i].coords.y--;
					}else{
						people[i].coords.y++;
					}
				}
				people[i].coords.x -= people[i].increment;
			}else if(people[i].status == 3){
				if(people[i].howLong == 60){
					people[i].status = 4;
					people[i].howLong = -1;
				}
				people[i].howLong++;
				people[i].coords.x -= people[i].increment;
			}else if(people[i].status == 6){
				SDL_BlitSurface(expresions[0],NULL,screen,&people[i].expresionPos);
			}else if(people[i].status == 5){
				SDL_BlitSurface(expresions[people[i].expression],NULL,screen,&people[i].expresionPos);
			}
			SDL_BlitSurface(skins[people[i].skin],NULL,screen,&people[i].coords);
			people[i].coords.x += people[i].increment;
			if(people[i].coords.x == people[i].stopPos && people[i].status == 0){
				people[i].status = 1;
			}
			people[i].expresionPos.x = people[i].coords.x;
			if(people[i].increment>0){
				if(people[i].coords.x > screenSize[0]){
					people.erase(people.begin()+i);
					i--;
				}
			}else{
				if(people[i].coords.x == 0){
					people.erase(people.begin()+i);
					i--;
				}
			}
		}
		cache++;
		if(cache == 60){
			people.push_back(Person());
			cache = 0;
		}
		SDL_Flip(screen);
		if( (SDL_GetTicks()-start) < (1000/FPS) ){
			SDL_Delay( (1000/FPS) - (SDL_GetTicks()-start) );
		}

	}
	SDL_FreeSurface(hello);
	SDL_Quit();
	return 0;
}
