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