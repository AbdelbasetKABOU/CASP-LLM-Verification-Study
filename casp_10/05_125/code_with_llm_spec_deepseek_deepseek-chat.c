/*@
  assigns \nothing;
  ensures \result.valid == false;
  ensures \result.value == false;
*/
struct maybeBool noneBool () {
    struct maybeBool result = { false, false };
    return result;
}