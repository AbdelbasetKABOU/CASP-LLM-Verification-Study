/*@
  requires b != 0;
  ensures \result == a;
  assigns \nothing;
*/
int divmult(int a, int b)
{
	return (a / b) * b + (a % b);
}