#include <iostream>
#include <SDL/SDL.h>
#include <GL/gl.h>
#include <GL/glu.h>
#include <array>
#include <time.h>

int rot = 0;
float blockS = 0.01;
float speed = 0.008;
float fallSpeed = 0.008;

float playerHeight = blockS*25;
 
void init()
{
        glClearColor(0.0,0.0,0.0,1.0);
	glEnable(GL_DEPTH);
	glEnable(GL_DEPTH_TEST);
        glMatrixMode(GL_PROJECTION);
        glLoadIdentity();
        gluPerspective(60.0,640.0/480.0,0.0000005,10.0);
        glMatrixMode(GL_MODELVIEW);
}
 
void display(float degrees, float degreesY,float viewZ,float viewY,float viewX)
{
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
        glLoadIdentity();
	//gluLookAt(viewX,viewY,viewZ,pos,0,0,0,1,0);
	//glTranslatef(pos,0,0);
	//glTranslatef(0.0,0.0,pos - 2.0);
	//glTranslatef(viewX,viewY,viewZ);
	//glRotatef(degrees,0,1,0);
	//glPushMatrix();
	glRotatef(degreesY, 1.0, 0.0, 0.0);
	glRotatef(degrees, 0.0, 1.0, 0.0);
	glTranslatef(viewX, viewY, viewZ);
	//glRotatef(rot,0,1,0);
	//rot++;
	//if(rot > 360) rot = 0;
	//std::cout << -viewX << -viewY << -viewZ << std::endl;
        /*glBegin(GL_TRIANGLES);
		glColor3f(0,0,1);
		glVertex3f(0,0,0);
		glColor3f(0,1,0);
		glVertex3f(0,0.75,0);
		glColor3f(1,0,0);
		glVertex3f(0.75,0,0);
		glVertex3f(0,0,0);
		glColor3f(0,1,0);
		glVertex3f(0,0.75,0);
		glColor3f(0,0,1);*
		glVertex3f(-0.75,0,0);*/
                /*glVertex3f(0.0,0.0,0.0);
                glVertex3f(-5.0,-5.0,0.0);
                glVertex3f(5.0,5.0,0.0);
		glColor3f(0,1,1);
		glVertex3f(0.0,0.0,0.0);
		glVertex3f(-5.0,-5.0,-5.0);
		glVertex3f(5.0,5.0,-5.0);
		glVertex3f(0.5,0.5,0.0);
		glVertex3f(1.0,1.0,-0.5);
		glVertex3f(0.0,0.0,-0.5);*/
	/*glBegin(GL_QUADS);
		glColor3f(1,0,0); //front
		glVertex3f(-0.5,0.5,0);
		glVertex3f(-0.5,-0.5,0);
		glVertex3f(0.5,-0.5,0);
		glVertex3f(0.5,0.5,0);
		glColor3f(0,1,0); //left
		glVertex3f(-0.5,0.5,0);
		glVertex3f(-0.5,-0.5,0);
		glVertex3f(-0.5,-0.5,-1);
		glVertex3f(-0.5,0.5,-1);
		glColor3f(0,0,1); //back
		glVertex3f(-0.5,0.5,-1);
		glVertex3f(-0.5,-0.5,-1);
		glVertex3f(0.5,-0.5,-1);
		glVertex3f(0.5,0.5,-1);
		glColor3f(1,0,1); //right
		glVertex3f(0.5,0.5,0);
		glVertex3f(0.5,-0.5,0);
		glVertex3f(0.5,-0.5,-1);
		glVertex3f(0.5,0.5,-1);
        glEnd();
	glPopMatrix();*/
	//glPushMatrix();
	//glTranslatef(0,0,0);
	glBegin(GL_QUADS);
                glColor3f(1,0,0); //front
                glVertex3f(-blockS,blockS,0);
                glVertex3f(-blockS,-blockS,0);
                glVertex3f(blockS,-blockS,0);
                glVertex3f(blockS,blockS,0);
                glColor3f(0,1,0); //left
                glVertex3f(-blockS,blockS,0);
                glVertex3f(-blockS,-blockS,0);
                glVertex3f(-blockS,-blockS,-blockS*2);
                glVertex3f(-blockS,blockS,-blockS*2);
                glColor3f(0,0,1); //back
                glVertex3f(-blockS,blockS,-blockS*2);
                glVertex3f(-blockS,-blockS,-blockS*2);
                glVertex3f(blockS,-blockS,-blockS*2);
                glVertex3f(blockS,blockS,-blockS*2);
                glColor3f(1,0,1); //right
                glVertex3f(blockS,blockS,0);
                glVertex3f(blockS,-blockS,0);
                glVertex3f(blockS,-blockS,-blockS*2);
                glVertex3f(blockS,blockS,-blockS*2);
		for(int z=1;z<100;z++){
			for(int x=1;x<100;x++){
				glColor3f(rand()/(RAND_MAX+0.0),rand()/(RAND_MAX+0.0),rand()/(RAND_MAX+0.0));
				glVertex3f(-blockS*x,blockS,-blockS*(z-1));
				glVertex3f(-blockS*(x-1),blockS,-blockS*(z-1));
				glVertex3f(-blockS*(x-1),blockS,(-blockS)*z);
				glVertex3f(-blockS*x,blockS,(-blockS)*z);
			}
		}
		glColor3f(0,1,1);
		glVertex3f(-blockS,blockS,0);
		glVertex3f(blockS,blockS,0);
		glVertex3f(blockS,blockS,-blockS*2);
		glVertex3f(-blockS,blockS,-blockS*2);

		/*glColor3f(rand()/(RAND_MAX+0.0),rand()/(RAND_MAX+0.0),rand()/(RAND_MAX+0.0));
		glVertex3f(-blockS*6,blockS,-blockS*4);
		glVertex3f(blockS*2,blockS,-blockS*4);
		glVertex3f(blockS,blockS,-blockS*2);
		glVertex3f(-blockS,blockS,-blockS*2);*/
        glEnd();
	//glPopMatrix();
}

float stuff = 0;
void fall(float *viewY){
	stuff = -(blockS+playerHeight);
	if(stuff > *viewY){
		*viewY += fallSpeed;
	}else if((+stuff) - (+*viewY) < fallSpeed){
		*viewY = stuff;
	}
}

int main(int main,char** argv)
{
	srand(time(NULL));
        SDL_Init(SDL_INIT_EVERYTHING);
        SDL_Surface* screen=SDL_SetVideoMode(640,480,32,SDL_SWSURFACE|SDL_OPENGL);
        bool running=true;
        Uint32 start;
        SDL_Event event;
        init();
	float degrees = 0.0;
	float degreesY = 0;
	float pos = 0;
	float incrament = 0.01;
	float incrementZ = 0;
	float incrementY = 0;
	float incrementX = 0;
	float viewZ = 0;
	float viewY = -2;
	float viewX = 0;

	bool bodo = false;

	float toat = 0;
	float left = 0;
	float right = 0;

	bool kUp = false;

	bool kStart = false;

	std::array<int,2> mouse = {0,0};
	std::array<int,2> prevMouse = {0,0};

        while(running)
        {
                start=SDL_GetTicks();
                while(SDL_PollEvent(&event))
                {
                        switch(event.type)
                        {
                                case SDL_QUIT:
                                        running=false;
                                        break;
				case SDL_KEYDOWN:
					switch(event.key.keysym.sym){
						case SDLK_UP:
							kUp = true;
							kStart = true;
							/*if(degrees == 0){
								incrementZ = speed;
							}
							else if(degrees <= 90){
								toat = 90;
								left = toat-degrees;
								right = toat-left;
								toat /= 2;
								if(right > toat){
									right = toat;
								}else if(left > toat){
									left = toat;
								}
								incrementX = -((right/toat)*speed);
								incrementZ = (left/toat)*speed;
								std::cout << "left " << left/toat << " , " << (left/toat)*speed << std::endl;
								std::cout << "right " << right/toat << " , " << (right/toat)*speed << std::endl;
							}else if(degrees <= 180){
								toat = 180;
							}else if(degrees <= 270){
								toat = 270;
							}else if(degrees <= 360){
								toat = 360;
							}
							
							left = toat-degrees;
                                                        right = toat-left;
                                                        toat /= 2;
                                                        if(right > toat){
                                                                right = toat;
                                                        }else if(left > toat){
                                                                left = toat;
                                                        }
							incrementX = ((right/toat)*speed);
							incrementZ = (left/toat)*speed;
							std::cout << incrementX << " , " << incrementZ << std::endl;

							if(toat == 45){
								incrementX = -incrementX;
							}else if(toat == 90){
								incrementX = -incrementX;
								incrementZ = -incrementZ;
							}else if(toat == 135){
								incrementZ = -incrementZ;
							}*/
							break;
						case SDLK_DOWN:
							incrementZ = -incrementZ;
							incrementX = -incrementX;
							break;
						case SDLK_SPACE:
							incrementY = -speed;
							break;
						case SDLK_m:
							incrementY = speed;
							break;
						case SDLK_RIGHT:
							incrementX = -speed;
							break;
						case SDLK_LEFT:
							incrementX = speed;
							break;
					}
					break;
				case SDL_KEYUP:
					kUp = false;
					incrementZ = 0;
					incrementY = 0;
					incrementX = 0;
			}
                }
		fall(&viewY);
                display(degrees,degreesY,viewZ,viewY,viewX);
		/*if(pos > 0.75){
			incrament = -0.01;
		}else if(pos < 0){
			incrament = 0.01;
		}*/
		viewZ += incrementZ;
		viewY += incrementY;
		viewX += incrementX;
		SDL_GetMouseState(&mouse[0],&mouse[1]);
		degrees += ((mouse[0]-prevMouse[0])/640.0)*360;
		degreesY += ((mouse[1]-prevMouse[1])/640.0)*360;
		if((kUp && mouse[0] != prevMouse[0]) || kStart){
			kStart = false;
			if(degrees <= 90){
				toat = 90;
									/*left = toat-degrees;
								right = toat-left;
								toat /= 2;
								if(right > toat){
									right = toat;
								}else if(left > toat){
									left = toat;
								}
								incrementX = -((right/toat)*speed);
								incrementZ = (left/toat)*speed;
								std::cout << "left " << left/toat << " , " << (left/toat)*speed << std::endl;
								std::cout << "right " << right/toat << " , " << (right/toat)*speed << std::endl;*/
			}else if(degrees <= 180){
				toat = 180;
			}else if(degrees <= 270){
				toat = 270;
			}else if(degrees <= 360){
				toat = 360;
			}
									
			left = toat-degrees;
			toat = 90;
			right = toat-left;
			toat /= 2;
			if(right > toat){
				right = toat;
			}else if(left > toat){
				left = toat;
			}
			incrementX = ((right/toat)*speed);
			incrementZ = (left/toat)*speed;

			std::cout << incrementX << " , " << incrementZ << std::endl;

			if(degrees <= 90){
				incrementX = -incrementX;
			}else if(degrees <= 180){
				incrementX = -incrementX;
				incrementZ = -incrementZ;
			}else if(degrees <= 270){
				incrementZ = -incrementZ;
			}
		}
		//std::cout << ((mouse[0]-prevMouse[0])/640.0)*360 << std::endl;
		//pos += (mouse[0]-prevMouse[0])/640.0;
		/*if(pos > 360) pos = pos - 360;
		if(pos < 0) pos = pos + 360;*/
		pos++;
		if(pos > 360) pos =0;
		if(degrees > 360){
			degrees = 0;
		}else if(degrees < 0){
			degrees = 360;
		}
		if(degreesY > 360){
			degreesY = 0;
		}else if(degreesY < 0){
			degreesY = 360;
		}
		/*if(pos > 1){
			pos = -1;
		}else if(pos < -1){
			pos = 1;
		}*/
		if(mouse[0] >= 600 || mouse[0] <= 40 || mouse[1] >= 440 || mouse[1] <= 40){
			SDL_WarpMouse(320,240);
			bodo = true;
		}
		SDL_GetMouseState(&prevMouse[0],&prevMouse[1]);
		if(bodo){
			prevMouse = {320,180};
			bodo = false;
		}
                SDL_GL_SwapBuffers();
                if(1000/30>(SDL_GetTicks()-start))
                        SDL_Delay(1000/30-(SDL_GetTicks()-start));
        }
        SDL_Quit();
        return 0;
}
