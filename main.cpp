//
//		          Programming Assignment #2 CPSC4050/6050
//
//					Daljit Singh Dhillon 
//
//
/***************************************************************************/

/* Include needed files */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include <GL/gl.h>
#include <GL/glu.h>
#include <GL/glut.h>   

#include <math.h>

#define WIDTH 800
#define HEIGHT 600

#define CP_WIDTH 10

int currExample = 1;

int lineThick;
int windowHandle;

int drawMode = 0;

int recordMode = 1;

int maxCP  = 0;
int currPointCount = 0;

#define MAX_DRAW_MODE 20
#define MAX_CONTROL_POINTS 100

int cpX[MAX_CONTROL_POINTS];
int cpY[MAX_CONTROL_POINTS];

int maxPointTable[MAX_DRAW_MODE+1] = { 0,
					2, // circle
					2, //parabola
					4, //cubic Bezier
					3, // circular arc
					3, //Ellipse
					2, //Poly
					6, //Quintic Bezier
					MAX_CONTROL_POINTS, //Cardinal Spline
					MAX_CONTROL_POINTS, //Cubic B-spline
					2, //Midpoint Parabola
};


char modeTag[MAX_DRAW_MODE+1][256] = { "None",
					"Draw Circle with center and on point on it",
					"Draw Parabola with it's tip and one point on it",
					"Draw cubic Bezier curve with given 4 control points", //cubic Bezier
					"Draw circular arc passing through 3 given points", 
					"Draw ellipse with it's center and given two points lying on it", //Ellipse
					"Draw infinite polynomial with two (start and end) points on it", //Poly
					"Draw fifth order Bezier curve with given six control points", //Quintic Bezier
					"Draw cardinal cubic spline interpolating all but the first and the last control points", //Cardinal Spline
					"Draw cubic B-spline interpolating all given control points", //Cubic B-spline
					"Draw parabola using midpoint algorithm", //Midpoint Parabola
};




/***************************************************************************/
// Forward declarations

void drawPixel(int x, int y);
void drawDot(int x, int y, int width);

void drawCircle(int centerX, int centerY, int pointOnCricleX, int pointOnCricleY);
void drawEllipse(int centerX, int centerY, int ptX1, int ptY1, int ptX2, int ptY2);
void drawParabola(int vertexX, int vertexY, int pointOnParabolaX, int pointOnParabolaY);
void drawCubicBezier(int* ptX, int* ptY);
void drawArc(int ptX1, int ptY1, int ptX2, int ptY2, int ptX3, int ptY3);
void drawPoly(int ptX1, int ptY1, int ptX2, int ptY2);
void drawQuinticBezier(int* ptX, int* ptY);
void drawCardinalSpline(int* ptX, int* ptY, int controlPointCount);
void drawCubicBSpline(int* ptX, int* ptY, int controlPointCount);
void drawMidpointParabola(int vertexX, int vertexY, int pointOnParabolaX, int pointOnParabolaY);

void callDrawCricle();			//01
void callDrawParabola();		//02
void callDrawCubicBezier();		//03
void callDrawArc();				//04
void callDrawEllipse();			//05
void callDrawPoly();			//06
void callDrawQuinticBezier();	//07
void callDrawCardinalSpline();	//08
void callDrawBSpline();			//09
void callDrawMidpointParabola();//10


/***************************************************************************/
void callDrawCricle() {
	drawCircle(cpX[0], cpY[0], cpX[1], cpY[1]);
}

void callDrawParabola() {
	drawParabola(cpX[0], cpY[0], cpX[1], cpY[1]);
}

void callDrawCubicBezier() {
	drawCubicBezier(cpX, cpY);
}

void callDrawQuinticBezier() {
	drawQuinticBezier(cpX, cpY);
}

void callDrawArc() {
	drawArc(cpX[0], cpY[0], cpX[1], cpY[1], cpX[2], cpY[2]);
}

void callDrawEllipse() {
	drawEllipse(cpX[0], cpY[0], cpX[1], cpY[1], cpX[2], cpY[2]);
}

void callDrawPoly() {
	drawPoly(cpX[0], cpY[0], cpX[1], cpY[1]);
}

void callDrawCardinalSpline() {
	if(currPointCount >= 4)
	drawCardinalSpline(cpX, cpY, currPointCount);
}

void callDrawBSpline() {
	if(currPointCount >= 4)
		drawCubicBSpline(cpX, cpY, currPointCount);
}

void callDrawMidpointParabola() {
	drawMidpointParabola(cpX[0], cpY[0], cpX[1], cpY[1]);
}
/***************************************************************************/


void(*callDrawMode[MAX_DRAW_MODE+1])(void) = {
	NULL,
	callDrawCricle,				//01
	callDrawParabola,			//02
	callDrawCubicBezier,		//03
	callDrawArc,				//04
	callDrawEllipse,			//05
	callDrawPoly,				//06
	callDrawQuinticBezier,		//07
	callDrawCardinalSpline,		//08
	callDrawBSpline,			//09
	callDrawMidpointParabola,	//10
};

/***************************************************************************/
void initWindow()
/* Clear the image area, and set up the coordinate system */
{
    glClearColor(0.0,0.0,0.0,0.0);
	glShadeModel(GL_SMOOTH);
    glOrtho(0,WIDTH,0,HEIGHT,-1.0,1.0);
}

/***************************************************************************/
// draws one single pixel
void drawPixel(int x, int y)
/* Turn on the pixel found at x,y */
{
        glColor3f (1.0, 1.0, 1.0);                 
        glBegin(GL_POINTS);
           glVertex3i( x, y, 0);
        glEnd();	
}


/***************************************************************************/
// draws one single (square) pixel of given width
void drawDot(int x, int y, int width)
/* Turn on the pixel found at x,y */
{
	glPointSize(width);
	glBegin(GL_POINTS);
	glVertex3i(x, y, 0);
	glEnd();
	glPointSize(1);
}



/***************************************************************************/
void display(void)   
{
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);	      // Clear Screen 

	glColor3f(1.0,1.0,1.0);	
	for (int ii = 0; ii < currPointCount;++ii)
	{
		drawDot(cpX[ii],cpY[ii],CP_WIDTH);
	}

	glColor3f(0.0,1.0,0.0);
	if (drawMode > 0 && drawMode <= MAX_DRAW_MODE)
	{
		if(recordMode == 0 || (maxPointTable[drawMode]== MAX_CONTROL_POINTS && currPointCount > 3))
			callDrawMode[drawMode]();
	}

	glutSwapBuffers();                                      // Draw Frame Buffer 
}

int mouseButton = GLUT_MIDDLE_BUTTON;
int mouseState = GLUT_UP;

int candidatePointIndex = -1;

#define MIN_PT_DIST_SQR (CP_WIDTH*CP_WIDTH/4)

/***************************************************************************/
// Callback function for mouse click events
void mouse(int button, int state, int x, int y)
{
	float distCurr;
	float refX;
	float refY;

	if(state == GLUT_UP) {
		mouseButton = GLUT_MIDDLE_BUTTON;
		mouseState = GLUT_UP;
		candidatePointIndex = -1;
		return;
	}

	mouseButton = button;
	mouseState = state;

	if (button != GLUT_LEFT_BUTTON)
		return;

	y = HEIGHT-y;  //flip Y-axis
	
	if (recordMode == 1)
	{ // record new control points
		int awayCount = 0;

		for (int ii = 0; ii < currPointCount; ++ii)
		{
			refX = cpX[ii];
			refY = cpY[ii];

			distCurr = (refX - x)*(refX - x) + (refY - y)*(refY - y);

			if (distCurr > MIN_PT_DIST_SQR)
				awayCount++;
		}
		if (currPointCount == awayCount) 
		{ // current point is far away from all current points, select it
		
			cpX[currPointCount] = x;
			cpY[currPointCount] = y;

			if (currPointCount < maxCP) // to avoid blind points at the begining
				currPointCount++;

			if (currPointCount == maxCP || currPointCount == MAX_CONTROL_POINTS)
			{ // stop recording any furhter points
				recordMode = 0;
				printf("\nFinished setting all points\n");
			}
		}
	}
	else {
		// all control points are set... move the closest one if it is spotted
		for (int ii = 0; ii < currPointCount; ++ii)
		{
			refX = cpX[ii];
			refY = cpY[ii];

			distCurr = (refX - x)*(refX - x) + (refY - y)*(refY - y);

			if (distCurr < MIN_PT_DIST_SQR && state == GLUT_DOWN)
			{
				cpX[ii] = x;
				cpY[ii] = y;
				break;
			}
		}
	}
}
/***************************************************************************/
// Callback function for mouse motion events while one of it's button is kept pressed
void mouseMotion(int x, int y) {

	int distCurr;
	float refX;
	float refY;

	y = HEIGHT - y;  //flip Y-axis

	if (mouseButton != GLUT_LEFT_BUTTON || mouseState != GLUT_DOWN || recordMode == 1)
		return;

	// left mouse button was pressed and it is down
	// also all control points are set... we may move them around, one at a time :)
	if (candidatePointIndex == -1)
	for (int ii = 0; ii < currPointCount; ++ii)
	{
		refX = cpX[ii];
		refY = cpY[ii];

		distCurr = (refX - x)*(refX - x) + (refY - y)*(refY - y);

		if (distCurr < MIN_PT_DIST_SQR)
		{
			candidatePointIndex = ii;
			break;
		}
	}

	if (candidatePointIndex >=0)
	{
		cpX[candidatePointIndex] = x;
		cpY[candidatePointIndex] = y;

	}
}

/***************************************************************************/
// Callback function for menu option selection
void runMenu(int num) {
	if (num == 0) {
		glutDestroyWindow(windowHandle);
		exit(0);
	}
	else {
		drawMode = num;

		printf("\n%s\n", modeTag[drawMode]);
		recordMode = 1;
		maxCP = maxPointTable[drawMode];
		currPointCount = 0;

		if (maxCP < MAX_CONTROL_POINTS) {
			printf("Click %d points\n", maxCP);
		}
		else {
			printf("Click as many control points as you want (less than 100) and then press ESC key\n");
		}
	}

	glutPostRedisplay();
}

void addContextMenu(void) {
	int subMenu1, subMenu2;
	
	int subSubMenu1, subSubMenu2;
	subSubMenu1 = glutCreateMenu(runMenu);
	glutAddMenuEntry("Midpoint Parabola", 10);
	glutAddMenuEntry("Cardinal Spline", 8);
	glutAddMenuEntry("Ellipse", 5);

	subMenu1 = glutCreateMenu(runMenu);
	glutAddMenuEntry("Circle",				1);
	glutAddMenuEntry("Parabola",			2);
	glutAddMenuEntry("Cubic Bezier",		3);
	glutAddSubMenu("Bonus:", subSubMenu1);

	subSubMenu2 = glutCreateMenu(runMenu);
	glutAddMenuEntry("B Spline",			9);
	glutAddMenuEntry("Cardinal Spline",		8);
	glutAddMenuEntry("Midpoint Parabola",	10);

	subMenu2 = glutCreateMenu(runMenu);
	glutAddMenuEntry("Circular Arc",		4);
	glutAddMenuEntry("Ellipse",				5);
	glutAddMenuEntry("Infinite Polynomial", 6);
	glutAddMenuEntry("Fifth-order Bezier",	7);
	glutAddSubMenu("Bonus:", subSubMenu2);


	//menuID = glutCreateMenu(runMenu);
	glutCreateMenu(runMenu);
	
	glutAddSubMenu("4050 - Draw:", subMenu1);
	glutAddSubMenu("6050 - Draw:", subMenu2);
	glutAddMenuEntry("Exit", 0);
	glutAttachMenu(GLUT_RIGHT_BUTTON);
}

/***************************************************************************/
// Callback function for key click events
void keyboard(unsigned char key, int x, int y)  
{

	switch (key) {
	case 27:              // Escape Key
		if (maxCP == MAX_CONTROL_POINTS) {
			maxCP = currPointCount;
			recordMode = 0; // stop taking more control points
			printf("\nFinished setting all points\n");
		}

		break;
	default:
		break;
	}
}

int main (int argc, char *argv[])
{
/* This main function sets up the main loop of the program and continues the
   loop until the end of the data is reached.  Then the window can be closed
   using the escape key.						  */
	
	//while (currExample != 0)
	{
		//intakeChoice();
		
		glutInit(&argc, argv); 
		glutInitDisplayMode(GLUT_RGB | GLUT_DOUBLE | GLUT_DEPTH); 
		glutInitWindowSize(WIDTH,HEIGHT); 
		windowHandle = glutCreateWindow("CG4050/6050 A#02: Draw Curves" );
		addContextMenu();
		glutDisplayFunc(display);  
		glutIdleFunc(display);
		glutMouseFunc(mouse);
		glutMotionFunc(mouseMotion);
		glutKeyboardFunc(keyboard);
		initWindow();				             //create_window
		
		glutMainLoop();                 // Initialize The Main Loop
	}
}


