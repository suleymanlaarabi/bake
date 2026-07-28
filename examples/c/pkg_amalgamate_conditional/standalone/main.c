#include "amalgamate_conditional.h"

int main(void) {
    int expected = 0;
#ifdef AMALGAMATE_WITH_PUBLIC
    expected += 40;
#endif
#ifdef AMALGAMATE_WITH_PRIVATE
    expected += 2;
#endif
    return amalgamate_conditional_value() == expected ? 0 : 1;
}
