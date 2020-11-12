#include "SDL/SDL.h"
#include "SDL/SDL_ttf.h"
#include <vector>
#include <array>
#include <iostream>

SDL_Surface* textBox_Gen(SDL_Rect size,std::string textS,bool center,bool cutMidLine,std::string fontS,SDL_Color textC,int *giveFontSize=nullptr){
	if(textS.find(' ') == std::string::npos){
		cutMidLine = true; //prevents infinite loop
	}
	std::vector< std::string > lines;
	int fontSize = 0;
	if(giveFontSize == nullptr){
		fontSize = 0;
	}else{
		fontSize = *giveFontSize;
	}
	int finl = 0;
	int w=0,h=0;
	int sizeY=0,sizeX=0;
	if(textS.size() == 0){finl = 2;}
	while(1){
		std::cout << fontSize << std::endl;
		std::string line;
		TTF_Font *font = NULL;
		font = TTF_OpenFont(fontS.c_str(),fontSize);
		if(font == NULL){
			std::cout << TTF_GetError() << std::endl;
			SDL_Surface* surface;
			return surface;
		}
		lines.clear();
		for(int i=0;i<textS.size();i++){
			line += textS[i];
			if(textS[i] == '\n'){
				line = line.substr(0,line.size()-1);
				lines.push_back(line);
				line = "";
				continue;
			}
			w=0;
			TTF_SizeText(font,line.c_str(),&w,nullptr);
			if(w >= size.x){
				i--;
				line = line.substr(0,line.size()-1);
				if(!cutMidLine){
					std::string putBack;
					bool didFind = false;
					for(int i=line.size()-1;i>(-1);i--){
						if(line[i] == ' '){
							didFind = true;
							line = line.substr(0,line.size()-1);
							break;
						}
						putBack += line[i];
						line = line.substr(0,line.size()-1);
					}
					putBack = std::string ( putBack.rbegin(), putBack.rend() );
					if(didFind){
						lines.push_back(line);
						line = putBack;
					}else{
						lines.push_back(putBack);
						line = "";
					}
				}else{
					lines.push_back(line);
					line = "";
				}
			}
			if(line.size() > 0 && i == textS.size()-1){
				lines.push_back(line);
			}
		}
		w=0;
		h=0;
		sizeY = 0;
		sizeX = 0;
		for(int i=0;i<lines.size();i++){
			TTF_SizeText(font,lines[i].c_str(),&w,&h);
			sizeY += h;
			sizeX += w;
		}
		if(giveFontSize == nullptr || *giveFontSize == 0){
			if(sizeY >= size.y){
				finl = 1;
				fontSize -= 2;
			}
		}else{
			if(sizeY <= size.y){
				finl = 2;
			}
		}
		if(finl == 2){
			std::vector< SDL_Surface* > tmpLines;
			for(int i=0;i<lines.size();i++){
				tmpLines.push_back(TTF_RenderText_Solid(font,lines[i].c_str(),textC));
				//std::cout << i << ',' << lines[i] << std::endl;
			}
			std::vector< SDL_Surface* > lines = tmpLines;
			SDL_Surface* tmp;
			tmp = SDL_CreateRGBSurface(0,size.x,size.y,32,0xFF000000, 0x00FF0000, 0x0000FF00, 0x000000FF);
			SDL_FillRect(tmp,NULL,SDL_MapRGBA(tmp->format,0,0,0,0));
			int pH = 0;
			for(int i=0;i<lines.size();i++){
				SDL_Rect offset;
				int yCenter = (size.y-sizeY)/2;
				if(center){
					//std::cout << i << std::endl;
					offset.x = (size.x-lines[i]->w)/2;
					offset.y = yCenter+pH;
				}else{
					offset.x = 0;
					offset.y = pH;
				}
				SDL_BlitSurface(lines[i],NULL,tmp,&offset);
				pH += lines[i]->h;
			}
			//std::cout << fontSize << std::endl;
			if(giveFontSize != nullptr){
				*giveFontSize = fontSize;
			}
			return tmp;
			break;
		}
		if(finl == 1){
			finl = 2;
		}
		if(giveFontSize == nullptr || *giveFontSize == 0){
			fontSize++;
		}else{
			fontSize--;
		}
	}
}


SDL_Surface* textBox_background(SDL_Surface* text,SDL_Color outline,SDL_Color color,int outlineSize=2){
	SDL_Surface* tmp = SDL_CreateRGBSurface(0,text->w,text->h,32,0,0,0,255);
	SDL_FillRect(tmp,NULL,SDL_MapRGB(tmp->format,outline.r,outline.g,outline.b));
	SDL_Surface* forground = SDL_CreateRGBSurface(0,text->w-(outlineSize*2),text->h-(outlineSize*2),32,0,0,0,255);
	SDL_FillRect(forground,NULL,SDL_MapRGB(forground->format,color.r,color.g,color.b));
	SDL_Rect pos = {outlineSize,outlineSize};
	SDL_BlitSurface(forground,NULL,tmp,&pos);
	SDL_Rect pos2 = {0,0};
	SDL_BlitSurface(text,NULL,tmp,&pos2);
	return tmp;
}



class textBox_DynamicDisplay{
	public:
		SDL_Rect size;
		std::string text;
		bool center;
		bool cutMidLine;
		std::string font;
		SDL_Color textC;

		int fontSize = 0;
		SDL_Surface* surface;
		struct keepBackground{
			SDL_Color outline;
			SDL_Color color;
			int outlineSize;
		};
		keepBackground back;
		bool sessionBackground = false; //did person set background
		std::string addThis;

		textBox_DynamicDisplay(SDL_Rect size,std::string text,bool center,bool cutMidLine,std::string font,SDL_Color textC);
		SDL_Surface* background(SDL_Color outline,SDL_Color color,int outlineSize=2);
		void add(std::string text);
		void draw(SDL_Surface* screen,SDL_Rect* position);
};
textBox_DynamicDisplay::textBox_DynamicDisplay(SDL_Rect size,std::string text,bool center,bool cutMidLine,std::string font,SDL_Color textC):
	size(size),
	text(text),
	center(center),
	cutMidLine(cutMidLine),
	font(font),
	textC(textC)
{
	surface = textBox_Gen(size,text,center,cutMidLine,font,textC,&fontSize);
}

SDL_Surface* textBox_DynamicDisplay::background(SDL_Color outline,SDL_Color color,int outlineSize){
	back = {outline,color,outlineSize};
	surface = textBox_background(surface,outline,color,outlineSize);
	sessionBackground = true;
}

void textBox_DynamicDisplay::add(std::string textA){
	text += textA;
	surface = textBox_Gen(size,text,center,cutMidLine,font,textC,&fontSize);
	if(sessionBackground){
		surface = textBox_background(surface,back.outline,back.color,back.outlineSize);
	}
}

void textBox_DynamicDisplay::draw(SDL_Surface* screen,SDL_Rect* position){
	SDL_BlitSurface(surface,NULL,screen,position);
}

class textBox_AddOverTime{
	public:
		textBox_DynamicDisplay* display;
		std::string text;
		int interval;

		int cache = 0;
		int pos = 0;
		int whenDone;
		std::string convert;

		textBox_AddOverTime(textBox_DynamicDisplay* display,std::string text,int interval=15);
		bool add();
};

textBox_AddOverTime::textBox_AddOverTime(textBox_DynamicDisplay* display,std::string text,int interval):
	display(display),
	text(text),
	interval(interval),
	whenDone(text.size()*interval)
{
}

bool textBox_AddOverTime::add(){
	if(cache%interval == 0){
		display->add(convert+text[pos]);
		pos++;
	}
	cache++;
	if(cache-1 == whenDone){
		return true;
	}else{return false;}
	//std::cout << cache << ',' << whenDone << "   " << cache%interval << std::endl;
}

/*};
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
}*/
