/*@
  @ requires b > 0; // b must be positive to avoid division by zero
  @ ensures \result == a; // the result is equal to a
  @ assigns \nothing; // the function does not modify any state
*/
int divmult(int a, int b)
{
	return (a / b) * b + (a % b);
}