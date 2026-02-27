/*@
  requires x0 != \null;
  requires \valid_read(x0+(0..strlen(x0)));
  ensures \result == 0 || \result == 1;
  ensures \result == 1 <==> (strlen(x0) > 0 && x0[0] == 'a');
  assigns \nothing;
*/
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