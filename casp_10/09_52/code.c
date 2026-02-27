void mv_mult2(int *m, int *v, int *o) {
  o[0] = m[0]*v[0]+m[1]*v[1];
  o[1] = m[2]*v[0]+m[3]*v[1];
}