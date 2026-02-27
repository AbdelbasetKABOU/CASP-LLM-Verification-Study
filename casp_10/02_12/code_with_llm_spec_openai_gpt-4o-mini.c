/*@
  @ requires x0 != \null; // x0 must be a non-null pointer
  @ requires \valid_string(x0); // x0 must point to a valid null-terminated string
  @ ensures \result == (x0[0] == 'a'); // result is true if the first character is 'a', false otherwise
  @ assigns \result; // only the result is assigned
  @*/
int matcher(char  * x0) {
  int x2 = strlen(x0);
  int x3 = 0 < x2;
  int x6;
  if (x3) {
    char x4 = x0[0];
    int x5 = 'a' == x4;
    x6 = x5;
  } else {
    x6 = 0/*false*/;
  }
  int x7;
  if (x6) {
    x7 = 1/*true*/;
  } else {
    x7 = 0/*false*/;
  }
  return x7;
}