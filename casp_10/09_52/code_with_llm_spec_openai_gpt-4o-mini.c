/*@
  requires m != \null && v != \null && o != \null;
  requires \valid(m + (0..3)) && \valid(v + (0..1)) && \valid(o + (0..1));
  ensures o[0] == m[0]*v[0] + m[1]*v[1];
  ensures o[1] == m[2]*v[0] + m[3]*v[1];
  assigns o[0], o[1];
*/
void mv_mult2(int *m, int *v, int *o) {
  o[0] = m[0]*v[0]+m[1]*v[1];
  o[1] = m[2]*v[0]+m[3]*v[1];
}