/*@
  requires \valid_read(m + (0..3));
  requires \valid_read(v + (0..1));
  requires \valid(o + (0..1));
  requires \separated(m + (0..3), v + (0..1), o + (0..1));
  assigns o[0], o[1];
  ensures o[0] == \old(m[0]*v[0]+m[1]*v[1]);
  ensures o[1] == \old(m[2]*v[0]+m[3]*v[1]);
*/
void mv_mult2(int *m, int *v, int *o) {
  o[0] = m[0]*v[0]+m[1]*v[1];
  o[1] = m[2]*v[0]+m[3]*v[1];
}