#include "amalgamate_dependee.h"
#include "amalgamate_private.h"

int amalgamate_dependee_value(void) {
    return amalgamate_dependency_value() + amalgamate_private_value();
}
