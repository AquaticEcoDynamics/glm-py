#include <Python.h>

static PyModuleDef glmpy_module = {
    PyModuleDef_HEAD_INIT,
    "glmpy",
    NULL,
    -1,
    NULL
};

PyMODINIT_FUNC PyInit_glmpy(void) {
    return PyModule_Create(&glmpy_module);
}