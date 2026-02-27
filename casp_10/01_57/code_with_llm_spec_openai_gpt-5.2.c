/*@ 
  requires b != 0;
  assigns \nothing;
  ensures \result == a;
*/
int divmult(int a, int b)
{
	return (a / b) * b + (a % b);
}