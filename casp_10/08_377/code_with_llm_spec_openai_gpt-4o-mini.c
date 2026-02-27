/*@
    requires a != \null && b != \null; // a and b must not be null
    requires n >= 0; // n must be non-negative
    ensures \result == 1 <==> \forall integer k; 0 <= k < n ==> a[k] == b[k]; // result is 1 if all elements are equal
    assigns \nothing; // function does not modify any memory
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