#include "SDL/SDL.h"
#include "SDL/SDL_ttf.h"
#include <string>
#include <array>
#include <iostream>
using namespace std;
class Input{
	SDL_Surface* screen;
	array<SDL_Rect,2> coords;
	int outlineSize;
	array<int,2> space;
	SDL_Color textColor;
	SDL_Color backgroundColor;
	SDL_Color outlineColor;
	string font;
	string text;
	string currentText;
	int fontSize;
	public:
	Input(array<SDL_Rect,2> coords,SDL_Color textColor,SDL_Color backgroundColor,SDL_Color outlineColor,string font,string text): 
		coords(coords),
		textColor(textColor),
		backgroundColor(backgroundColor),
		outlineColor(outlineColor),
		font(font),
		text(text)
	{
		this->fontSizeCalc();
	}
	void printSize(){
		//this->fontSize = 0;
		cout << "SKLDFH" << endl;
		cout << "HIHIHIHIHI\n";
	}
	protected:
	int fontSizeCalc(){
		int fontSizeL = 0;
		TTF_Font *fontL = NULL;
		fontL = TTF_OpenFont(this->font.c_str(),fontSizeL);
		SDL_Surface* textL;
		while(1){
			textL = TTF_RenderText_Solid(fontL,")",this->textColor);
			if(textL->h >= this->space[1]){
				fontSizeL--;
				break;
			}
			fontSizeL++;
		}
		this->fontSize = fontSizeL;
	}
};

int main(){
	cout << "POOP\n";
	array<SDL_Rect,2> coords;
	coords[0].x = 0; coords[0].y = 0;
	coords[1].x = 200; coords[1].y = 100;
	SDL_Color textColor = {255,0,255};
	SDL_Color backgroundColor = {255,255,255};
	SDL_Color outlineColor = {0,255,255};
	string font = "font.ttf";
	string text = "Hello World!";
	//Input box(coords,textColor,backgroundColor,outlineColor,font,text);
	//box.printSize();
}
