/*@
  requires x != \min_int;
  requires y != \min_int;
  assigns \nothing;
  ensures \result == \max(\abs(\old(x)), \abs(\old(y)));
*/
int max_abs(int x, int y) {
  x = abs(x);
  y = abs(y);
  return max(x, y);
}