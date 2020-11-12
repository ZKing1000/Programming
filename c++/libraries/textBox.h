#include "SDL/SDL.h"
#include "SDL/SDL_ttf.h"
#include <vector>
#include <array>
#include <iostream>

class Display{
public:
	SDL_Surface* screen;
	std::array<SDL_Rect,2> coords;
	std::string text;
	bool center;
	std::string font;
	SDL_Color background;
	SDL_Color outline;
	SDL_Color textC;
	bool cutMidLine;
	int outlineSize;
	//<cache for updating
	int fontSize = 0;
	std::vector<SDL_Surface*> lines;
	std::vector<SDL_Rect> positions;
	///>
	std::array<int,2> dimentions;
	std::array<int,2> space;
	SDL_Surface* drawSurface;

	SDL_Surface* textGen(std::string text,bool center,bool transition);
	void draw(SDL_Rect coord);
	Display(SDL_Surface* screen,std::array<SDL_Rect,2> coords,std::string text,bool center,std::string font,SDL_Color background,SDL_Color outline,SDL_Color textC,bool cutMidLine,int outlineSize);
};

Display::Display(SDL_Surface* screen,std::array<SDL_Rect,2> coords,std::string text,bool center,std::string font,SDL_Color background,SDL_Color outline,SDL_Color textC,bool cutMidLine,int outlineSize):
	screen(screen),
	coords(coords),
	text(text),
	font(font),
	background(background),
	outline(outline),
	textC(textC),
	cutMidLine(cutMidLine),
	outlineSize(outlineSize),
	dimentions{coords[1].x-coords[0].x,coords[1].y-coords[0].y},
	space{dimentions[0]-(outlineSize*2),dimentions[1]-(outlineSize*2)}
{
	drawSurface = textGen(text,center,true);
	std::cout << "POOP\n";
}

SDL_Surface* Display::textGen(std::string text,bool center,bool transition){
	TTF_Init();
	SDL_Surface* crap;
	std::vector< SDL_Surface* > previousLines = {crap};
	std::vector< SDL_Surface* > lines;
	int blp = 0;
	int blp2 = 0;
	int blp3 = 0;
	int finl = 0;
	while(1){
		std::string line;
		TTF_Font *font = NULL;
		font = TTF_OpenFont(this->font.c_str(),this->fontSize);
		std::cout << this->fontSize << std::endl;
		lines.clear();
		for(int i=0;i<this->text.size();i++){
			line += this->text[i];
			SDL_Surface* text = TTF_RenderText_Solid(font,line.c_str(),this->textC);
			if(text->w >= space[0]){
				i--;
				//std::cout << line.substr(0,line.size()-1).c_str() << "<>" << "PP\n";
				blp2++;
				if(blp2>1000){
					std::cout << "blp2\n";
					break;
				}
				lines.push_back(TTF_RenderText_Solid(font,line.substr(0,line.size()-1).c_str(),this->textC));
				line = "";
			}
			if(line.size() > 0 && i == this->text.size()-1){
				lines.push_back(TTF_RenderText_Solid(font,line.c_str(),this->textC));
			}
		}
		int sizeY = 0;
		int sizeX = 0;
		for(int i=0;i<lines.size();i++){
			sizeY += lines[i]->h;
			sizeX += lines[i]->w;
		}
		std::cout << sizeX << "><" << sizeY << std::endl;
		std::cout << space[1] << " SSSSSSSSSSSSSSPSPSPSPSPSP\n";
		if(sizeY >= this->space[1]){
			finl = 1;
			if(transition){
				this->fontSize -= 2;
			}
		}else if(finl == 2){
			std::cout << "SLKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKK\n";
			SDL_Surface* tmp;
			tmp = SDL_CreateRGBSurface(0,this->dimentions[0],this->dimentions[1],32,0,0,0,255);
			SDL_FillRect(tmp,NULL,SDL_MapRGB(tmp->format,outline.r,outline.g,outline.b));
			std::cout << tmp << std::endl;
			SDL_Surface* backgroundS;
			backgroundS = SDL_CreateRGBSurface(0,this->dimentions[0]-(this->outlineSize*2),this->dimentions[1]-(this->outlineSize*2),32,0,0,0,255);
			SDL_FillRect(backgroundS,NULL,SDL_MapRGB(backgroundS->format,background.r,background.g,background.b));
			SDL_Rect offset;
			offset.x = this->outlineSize;
			offset.y = this->outlineSize;
			SDL_BlitSurface(backgroundS,NULL,tmp,&offset);
			//SDL_BlitSurface(previousLines[0],NULL,tmp,&offset);
			std::cout << "CODE " << lines.size() << std::endl;
			int pH = 0;
			for(int i=0;i<lines.size();i++){
				blp3++;
				if(blp3>500){
					std::cout << "blp3\n";
					break;
				}
				SDL_Rect offset;
				if(this->center){
					offset.x = (space[0]-lines[i]->w)/2;
				}else{
					offset.x = 0;
				}
				offset.y = pH;
				std::cout << lines[i]->w << "PPOPOPOPOPOPOPOPOPO\n";
				SDL_BlitSurface(lines[i],NULL,tmp,&offset);
				std::cout << "boop\n";
				std::cout << lines[i]->w << std::endl;
				std::cout << this->fontSize << std::endl;
				pH += lines[i]->h;
			}
			std::cout << "HUH? HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH\n";
			return tmp;
			break;
		}
		if(finl == 1){
			finl = 2;
		}
		if(blp3>500){
			break;
		}
		if(transition){
			this->fontSize++;
		}else{
			this->fontSize--;
		}
		std::cout << lines[0]->w << ',' << previousLines[0]->w << std::endl;
		std::vector< SDL_Surface* > previousLines = lines;
		std::cout << lines[0]->w << ',' << previousLines[0]->w << std::endl;
		std::cout << "LLL " << lines.size() << ',' << previousLines.size() << std::endl;
	}
}

void Display::draw(SDL_Rect coord){
	SDL_FillRect(this->screen, NULL, 0x00FFFF);
	SDL_BlitSurface(this->drawSurface,NULL,this->screen,&coord);
	std::cout << this->drawSurface << std::endl;
}




SDL_Surface* textGen(SDL_Rect size,std::string textS,bool center,bool cutMidLine,std::string fontS,SDL_Color textC,int *giveFontSize=nullptr){
	TTF_Init();
	SDL_Surface* crap;
	std::vector< SDL_Surface* > previousLines = {crap};
	std::vector< SDL_Surface* > lines;
	int fontSize = 0;
	if(giveFontSize == nullptr){
		int fontSize = 0;
	}else{
		std::cout << "DD\n";
		int fontSize = *giveFontSize;
	}
	int finl = 0;
	while(1){
		std::string line;
		TTF_Font *font = NULL;
		font = TTF_OpenFont(fontS.c_str(),fontSize);
		lines.clear();
		for(int i=0;i<textS.size();i++){
			line += textS[i];
			SDL_Surface* text = TTF_RenderText_Solid(font,line.c_str(),textC);
			if(text->w >= size.x){
				i--;
				//std::cout << line.substr(0,line.size()-1).c_str() << "<>" << "PP\n";
				lines.push_back(TTF_RenderText_Solid(font,line.substr(0,line.size()-1).c_str(),textC));
				line = "";
			}
			if(line.size() > 0 && i == textS.size()-1){
				lines.push_back(TTF_RenderText_Solid(font,line.c_str(),textC));
			}
		}
		int sizeY = 0;
		int sizeX = 0;
		for(int i=0;i<lines.size();i++){
			sizeY += lines[i]->h;
			sizeX += lines[i]->w;
		}
		if(giveFontSize == nullptr || *giveFontSize == 0){
			if(sizeY >= size.y){
				std::cout << "Hi2\n";
				finl = 1;
				fontSize -= 2;
			}
		}else{
			std::cout << "KMS\n";
			if(sizeY <= size.y){
				std::cout << "BLoue\n";
				finl = 1;
				fontSize += 2;
			}
		}
		if(finl == 2){
			std::cout << "NOOOOoo\n";
			SDL_Surface* tmp;
			tmp = SDL_CreateRGBSurface(0,size.x,size.y,32,0xFF000000, 0x00FF0000, 0x0000FF00, 0x000000FF);
			SDL_FillRect(tmp,NULL,SDL_MapRGBA(tmp->format,0,0,0,0));
			int pH = 0;
			for(int i=0;i<lines.size();i++){
				SDL_Rect offset;
				if(center){
					offset.x = (size.x-lines[i]->w)/2;
				}else{
					offset.x = 0;
				}
				offset.y = pH;
				SDL_BlitSurface(lines[i],NULL,tmp,&offset);
				pH += lines[i]->h;
			}
			if(giveFontSize != nullptr){
				*giveFontSize = fontSize;
			}
			return tmp;
			break;
		}
		if(finl == 1){
			finl = 2;
		}
		if(giveFontSize != nullptr){
			fontSize--;
		}else{
			fontSize++;
		}
	}
}



class DynamicDisplay{
	public:
		SDL_Rect size;
		std::string text;
		bool center;
		bool cutMidLine;
		std::string font;
		SDL_Color textC;

		int fontSize = 0;
		SDL_Surface* surface;

		DynamicDisplay(SDL_Rect size,std::string text,bool center,bool cutMidLine,std::string font,SDL_Color textC);
		void add(std::string text);
		void draw(SDL_Surface* screen);
};
DynamicDisplay::DynamicDisplay(SDL_Rect size,std::string text,bool center,bool cutMidLine,std::string font,SDL_Color textC):
	size(size),
	text(text),
	center(center),
	cutMidLine(cutMidLine),
	font(font),
	textC(textC)
{
	std::cout << "##################\n";
	surface = textGen(size,text,center,cutMidLine,font,textC,&fontSize);
}

void DynamicDisplay::add(std::string textA){
	surface = textGen(size,text+textA,center,cutMidLine,font,textC,&fontSize);
}

void DynamicDisplay::draw(SDL_Surface* screen){
	SDL_Rect crap;
	crap.x = 200;
	crap.y = 100;
	SDL_BlitSurface(surface,NULL,screen,&crap);
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
