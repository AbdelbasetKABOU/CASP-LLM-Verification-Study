/*@
  requires \true;
  ensures (y > 0 ==> \result == 50) && (y <= 0 ==> \result == -150);
  assigns \nothing;
*/
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