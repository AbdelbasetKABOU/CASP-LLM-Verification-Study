/*@
  requires n >= 0;
  requires \valid_read(a + (0 .. n-1));
  requires \valid_read(b + (0 .. n-1));
  assigns \nothing;
  ensures \result == 1 <==> (\forall integer i; 0 <= i < n ==> a[i] == b[i]);
  ensures \result == 0 <==> (\exists integer i; 0 <= i < n && a[i] != b[i]);
*/
int check(int *a, int *b, int n) {
    /*@
        loop invariant 0 <= i <= n;
        loop invariant \forall integer k; 0 <= k < i ==> a[k] == b[k];
        loop assigns i;
        loop variant n - i;
    */
    for (int i = 0; i < n; i++) {
        if (a[i] != b[i]) {
            return 0;
        }
    }
    return 1;
}