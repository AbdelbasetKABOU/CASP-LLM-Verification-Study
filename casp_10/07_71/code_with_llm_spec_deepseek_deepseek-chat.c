/*@
  requires x15 >= 0;
  ensures \result == (x15 == 0 ? 26 : x15 - 1);
  assigns \nothing;
*/
int decypher(int  x15) {
  int x17 = x15 == 0;
  int x19;
  if (x17) {
    x19 = 26;
  } else {
    int x18 = x15 - 1;
    x19 = x18;
  }
  return x19;
}