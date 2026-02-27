/*@
  requires n > 0;
  requires \valid(a + (0 .. n-1));
  assigns a[0 .. n-1];
  ensures \exists integer k; 0 <= k < n && a[n-1] == \old(a[k]);
  ensures \forall integer i; 0 <= i < n ==> a[n-1] >= a[i];
  ensures \forall integer v;
            (\numof integer i; 0 <= i < n && a[i] == v) ==
            (\numof integer i; 0 <= i < n && \old(a[i]) == v);
*/
void selectioninnerloop(int a[], int n)
{
    int max_idx = 0;

    /*@
      loop invariant 0 <= j <= n;
      loop invariant 0 <= max_idx < n;
      loop invariant \forall integer i; 0 <= i < j ==> a[max_idx] >= a[i];
      loop assigns max_idx, j;
      loop variant n - j;
    */
    for (int j = 0; j < n; j++)
    {
        if (a[j] > a[max_idx])
        {
            max_idx = j;
        }
    }
    int temp = a[n - 1];
    a[n - 1] = a[max_idx];
    a[max_idx] = temp;
}