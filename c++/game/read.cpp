#include <fstream>
#include "read.h"
#include "SDL/SDL.h"
#include "SDL_image"
using namespace std;
vector<string> readLines(string file){
	fstream f(file.c_str());
	vector<std::string> lines;
	string line;
	while(getline(f,line)){
		lines.push_back(line);
	}
	return lines;
}
struct Surfaces{
	vector< SDL_SURFACE* > surfaces;
	vector< SDL_Rect > coords;
};
Surfaces readLevel(level){
