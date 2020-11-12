#include <fstream>
#include "read.h"
#include "SDL/SDL.h"
#include "SDL/SDL_image.h"
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
