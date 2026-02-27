/*@
  @ requires \true; // No preconditions
  @ ensures \result.isSome == false; // The result indicates it is not a valid value
  @ ensures \result.value == false; // The value is false
  @ assigns \result; // The function assigns to the result variable
*/
struct maybeBool noneBool () {
    struct maybeBool result = { false, false };
    return result;
}