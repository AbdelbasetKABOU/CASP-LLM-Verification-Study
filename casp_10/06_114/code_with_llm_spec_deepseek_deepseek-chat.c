/*@
  requires \valid_read(&x) && \valid_read(&y);
  assigns \nothing;
  ensures \result >= 0;
  ensures \result == \max(\abs(x), \abs(y));
*/
int max_abs(int x, int y) {
  x = abs(x);
  y = abs(y);
  return max(x, y);
}