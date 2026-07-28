#include "amalgamate_conditional.h"

#if (AMALGAMATE_WITH_PRIVATE) || (AMALGAMATE_WITH_PUBLIC)

int amalgamate_leaf_value(void) {
    return 40;
}

#endif /* (AMALGAMATE_WITH_PRIVATE) || (AMALGAMATE_WITH_PUBLIC) */

#if AMALGAMATE_WITH_PUBLIC

int amalgamate_dependency_value(void) {
    return amalgamate_leaf_value();
}

#endif /* AMALGAMATE_WITH_PUBLIC */

#if AMALGAMATE_WITH_PRIVATE

int amalgamate_private_value(void) {
    return 2;
}

#endif /* AMALGAMATE_WITH_PRIVATE */
#ifdef AMALGAMATE_WITH_PRIVATE
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

