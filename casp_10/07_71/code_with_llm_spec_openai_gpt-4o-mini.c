/*@
  @ requires x15 >= 0 && x15 <= 26; // x15 must be in the range of valid inputs
  @ ensures \result >= 0 && \result <= 26; // the result must also be in the range of valid outputs
  @ assigns \result; // the function assigns a value to the result
  @*/
int decypher(int x15) {
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