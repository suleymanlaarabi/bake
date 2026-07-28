#include "amalgamate_conditional.h"
#ifdef AMALGAMATE_WITH_PRIVATE
#include "amalgamate_private.h"
#endif

int amalgamate_conditional_value(void) {
    int result = 0;
#ifdef AMALGAMATE_WITH_PUBLIC
    result += amalgamate_dependency_value();
#endif
#ifdef AMALGAMATE_WITH_PRIVATE
    result += amalgamate_private_value();
#endif
    return result;
}
