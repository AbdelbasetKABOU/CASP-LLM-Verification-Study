/*@
  requires b != 0;
  // The C standard specifies that `INT_MIN / -1` is undefined behavior.
  // This precondition ensures that this specific case is avoided.
  requires a != INT_MIN || b != -1;
  assigns \nothing;
  // For integers a and b (with b != 0), the mathematical identity
  // a = (a / b) * b + (a % b) holds.
  // C's integer division and modulo operators conform to this identity
  // when b is not zero and the division does not result in overflow
  // (e.g., INT_MIN / -1).
  ensures \result == a;
*/
int divmult(int a, int b)
{
	return (a / b) * b + (a % b);
}