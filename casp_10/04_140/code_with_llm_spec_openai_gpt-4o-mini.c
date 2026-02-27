/*@
  @ requires y >= -150; // Precondition: y must be greater than or equal to -150
  @ ensures \result == -150; // Postcondition: the result will be -150 for y <= 0
  @ ensures \result == 50;   // Postcondition: the result will be 50 for y > 0
  @ assigns \result;        // The function modifies the return value only
  @*/
int g(int y){
	int x=0;
	
	if(y>0){
		x=100;
		x=x+50;
		x=x-100;
	}else{
		x = x - 150;
		x=x-100;
		x=x+100;
	}
	return x;
}