/*@
  @ requires \true;
  @ assigns \nothing;
  @ ensures \result.hasValue == \false && \result.value == \false;
  @*/
struct maybeBool noneBool () {
    struct maybeBool result = { false, false };
    return result;
}