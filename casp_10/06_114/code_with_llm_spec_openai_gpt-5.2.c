/*@
  requires x != INT_MIN;
  requires y != INT_MIN;
  assigns \nothing;
  ensures \result >= 0;
  ensures \result == ( (x < 0 ? -x : x) >= (y < 0 ? -y : y)
                     ? (x < 0 ? -x : x)
                     : (y < 0 ? -y : y) );
*/
int max_abs(int x, int y) {
  x = abs(x);
  y = abs(y);
  return max(x, y);
}