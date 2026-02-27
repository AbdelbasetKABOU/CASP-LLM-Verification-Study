/*@ 
  assigns \nothing;
  ensures \result.value == \false;
  ensures \result.valid == \false;
*/
struct maybeBool noneBool () {
    struct maybeBool result = { false, false };
    return result;
}