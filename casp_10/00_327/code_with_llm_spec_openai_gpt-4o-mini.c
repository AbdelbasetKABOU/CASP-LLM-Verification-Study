/*@
  requires a != \null; // a must not be null
  requires n >= 0; // n must be non-negative
  ensures \forall integer k; 0 <= k < n ==> a[k] == 0; // all elements in the array are set to 0
  assigns a[0..n-1]; // the function modifies the first n elements of the array
*/
void array_zero(int* a, int n){
 /*@ loop invariant 0 <= i <= n && (\forall integer k; 0 <= k < i ==> a[k] == 0);
     loop assigns a[0..n-1], i;
     loop variant n-i;
 */
 for(int i = 0;i< n;i++){
  a[i]=0;
 }
}