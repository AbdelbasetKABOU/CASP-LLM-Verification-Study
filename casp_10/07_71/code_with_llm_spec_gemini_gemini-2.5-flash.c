/*@
  @ requires x15 != INT_MIN;
  @ assigns \nothing;
  @ ensures (x15 == 0 ==> \result == 26);
  @ ensures (x15 != 0 ==> \result == x15 - 1);
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