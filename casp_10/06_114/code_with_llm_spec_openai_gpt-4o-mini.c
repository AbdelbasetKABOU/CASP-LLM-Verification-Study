/*@
  @ requires true; // No preconditions
  @ ensures \result == (x >= 0 ? (y >= 0 ? (x > y ? x : y) : x) : (y >= 0 ? y : (x > -y ? x : -y))); // Ensures the result is the maximum of the absolute values
  @ assigns \nothing; // The function does not modify any global state
  @*/
int max_abs(int x, int y) {
  x = abs(x);
  y = abs(y);
  return max(x, y);
}