#ifndef Py_UFUNCOBJECT_H
#define Py_UFUNCOBJECT_H

#include <numpy/npy_math.h>
#include <numpy/npy_common.h>

#ifdef __cplusplus
extern "C" {
#endif

/*
 * The legacy generic inner loop for a standard element-wise or
 * generalized ufunc.
 */
typedef void (*PyUFuncGenericFunction)
            (char **args,
             npy_intp *dimensions,
             npy_intp *strides,
             void *innerloopdata);

/*
 * The most generic one-dimensional inner loop for
 * a standard element-wise ufunc. This typedef is also
 * more consistent with the other NumPy function pointer typedefs
 * than PyUFuncGenericFunction.
 */
typedef void (PyUFunc_StridedInnerLoopFunc)(
                char **dataptrs, npy_intp *strides,
                npy_intp count,
                NpyAuxData *innerloopdata);

/*
 * The most generic one-dimensional inner loop for
 * a masked standard element-wise ufunc. "Masked" here means that it skips
 * doing calculations on any items for which the maskptr array has a true
 * value.
 */
typedef void (PyUFunc_MaskedStridedInnerLoopFunc)(
                char **dataptrs, npy_intp *strides,
                char *maskptr, npy_intp mask_stride,
                npy_intp count,
                NpyAuxData *innerloopdata);

/* Forward declaration for the type resolver and loop selector typedefs */
struct _tagPyUFuncObject;

/*
 * Given the operands for calling a ufunc, should determine the
 * calculation input and output data types and return an inner loop function.
 * This function should validate that the casting rule is being followed,
 * and fail if it is not.
 *
 * For backwards compatibility, the regular type resolution function does not
 * support auxiliary data with object semantics. The type resolution call
 * which returns a masked generic function returns a standard NpyAuxData
 * object, for which the NPY_AUXDATA_FREE and NPY_AUXDATA_CLONE macros
 * work.
 *
 * ufunc:             The ufunc object.
 * casting:           The 'casting' parameter provided to the ufunc.
 * operands:          An array of length (ufunc->nin + ufunc->nout),
 *                    with the output parameters possibly NULL.
 * type_tup:          Either NULL, or the type_tup passed to the ufunc.
 * out_dtypes:        An array which should be populated with new
 *                    references to (ufunc->nin + ufunc->nout) new
 *                    dtypes, one for each input and output. These
 *                    dtypes should all be in native-endian format.
 *
 * Should return 0 on success, -1 on failure (with exception set),
 * or -2 if Py_NotImplemented should be returned.
 */
typedef int (PyUFunc_TypeResolutionFunc)(
                                struct _tagPyUFuncObject *ufunc,
                                NPY_CASTING casting,
                                PyArrayObject **operands,
                                PyObject *type_tup,
                                PyArray_Descr **out_dtypes);

/*
 * Given an array of DTypes as returned by the PyUFunc_TypeResolutionFunc,
 * and an array of fixed strides (the array will contain NPY_MAX_INTP for
 * strides which are not necessarily fixed), returns an inner loop
 * with associated auxiliary data.
 *
 * For backwards compatibility, there is a variant of the inner loop
 * selection which returns an inner loop irrespective of the strides,
 * and with a void* static auxiliary data instead of an NpyAuxData *
 * dynamically allocatable auxiliary data.
 *
 * ufunc:             The ufunc object.
 * dtypes:            An array which has been populated with dtypes,
 *                    in most cases by the type resolution funciton
 *                    for the same ufunc.
 * fixed_strides:     For each input/output, either the stride that
 *                    will be used every time the function is called
 *                    or NPY_MAX_INTP if the stride might change or
 *                    is not known ahead of time. The loop selection
 *                    function may use this stride to pick inner loops
 *                    which are optimized for contiguous or 0-stride
 *                    cases.
 * out_innerloop:     Should be populated with the correct ufunc inner
 *                    loop for the given type.
 * out_innerloopdata: Should be populated with the void* data to
 *                    be passed into the out_innerloop function.
 * out_needs_api:     If the inner loop needs to use the Python API,
 *                    should set the to 1, otherwise should leave
 *                    this untouched.
 */
typedef int (PyUFunc_LegacyInnerLoopSelectionFunc)(
                            struct _tagPyUFuncObject *ufunc,
                            PyArray_Descr **dtypes,
                            PyUFuncGenericFunction *out_innerloop,
                            void **out_innerloopdata,
                            int *out_needs_api);
typedef int (PyUFunc_InnerLoopSelectionFunc)(
                            struct _tagPyUFuncObject *ufunc,
                            PyArray_Descr **dtypes,
                            npy_intp *fixed_strides,
                            PyUFunc_StridedInnerLoopFunc **out_innerloop,
                            NpyAuxData **out_innerloopdata,
                            int *out_needs_api);
typedef int (PyUFunc_MaskedInnerLoopSelectionFunc)(
                            struct _tagPyUFuncObject *ufunc,
                            PyArray_Descr **dtypes,
                            PyArray_Descr *mask_dtype,
                            npy_intp *fixed_strides,
                            npy_intp fixed_mask_stride,
                            PyUFunc_MaskedStridedInnerLoopFunc **out_innerloop,
                            NpyAuxData **out_innerloopdata,
                            int *out_needs_api);

typedef struct _tagPyUFuncObject {
        PyObject_HEAD
        /*
         * nin: Number of inputs
         * nout: Number of outputs
         * nargs: Always nin + nout (Why is it stored?)
         */
        int nin, nout, nargs;

        /* Identity for reduction, either PyUFunc_One or PyUFunc_Zero */
        int identity;

        /* Array of one-dimensional core loops */
        PyUFuncGenericFunction *functions;
        /* Array of funcdata that gets passed into the functions */
        void **data;
        /* The number of elements in 'functions' and 'data' */
        int ntypes;

        /* Does not appear to be used */
        int check_return;

        /* The name of the ufunc */
        char *name;

        /* Array of type numbers, of size ('nargs' * 'ntypes') */
        char *types;

        /* Documentation string */
        char *doc;

        void *ptr;
        PyObject *obj;
        PyObject *userloops;

        /* generalized ufunc parameters */

        /* 0 for scalar ufunc; 1 for generalized ufunc */
        int core_enabled;
        /* number of distinct dimension names in signature */
        int core_num_dim_ix;

        /*
         * dimension indices of input/output argument k are stored in
         * core_dim_ixs[core_offsets[k]..core_offsets[k]+core_num_dims[k]-1]
         */

        /* numbers of core dimensions of each argument */
        int *core_num_dims;
        /*
         * dimension indices in a flatted form; indices
         * are in the range of [0,core_num_dim_ix)
         */
        int *core_dim_ixs;
        /*
         * positions of 1st core dimensions of each
         * argument in core_dim_ixs
         */
        int *core_offsets;
        /* signature string for printing purpose */
        char *core_signature;

        /*
         * A function which resolves the types and fills an array
         * with the dtypes for the inputs and outputs.
         */
        PyUFunc_TypeResolutionFunc *type_resolver;
        /*
         * A function which returns an inner loop written for
         * NumPy 1.6 and earlier ufuncs. This is for backwards
         * compatibility, and may be NULL if inner_loop_selector
         * is specified.
         */
        PyUFunc_LegacyInnerLoopSelectionFunc *legacy_inner_loop_selector;
        /*
         * A function which returns an inner loop for the new mechanism
         * in NumPy 1.7 and later. If provided, this is used, otherwise
         * if NULL the legacy_inner_loop_selector is used instead.
         */
        PyUFunc_InnerLoopSelectionFunc *inner_loop_selector;
        /*
         * A function which returns a masked inner loop for the ufunc.
         */
        PyUFunc_MaskedInnerLoopSelectionFunc *masked_inner_loop_selector;

        /*
         * List of flags for each operand when ufunc is called by nditer object.
         * These flags will be used in addition to the default flags for each
         * operand set by nditer object.
         */
        npy_uint32 *op_flags;

        /*
         * List of global flags used when ufunc is called by nditer object.
         * These flags will be used in addition to the default global flags
         * set by nditer object.
         */
        npy_uint32 iter_flags;
} PyUFuncObject;

#include "arrayobject.h"

#define UFUNC_ERR_IGNORE 0
#define UFUNC_ERR_WARN   1
#define UFUNC_ERR_RAISE  2
#define UFUNC_ERR_CALL   3
#define UFUNC_ERR_PRINT  4
#define UFUNC_ERR_LOG    5

        /* Python side integer mask */

#define UFUNC_MASK_DIVIDEBYZERO 0x07
#define UFUNC_MASK_OVERFLOW 0x3f
#define UFUNC_MASK_UNDERFLOW 0x1ff
#define UFUNC_MASK_INVALID 0xfff

#define UFUNC_SHIFT_DIVIDEBYZERO 0
#define UFUNC_SHIFT_OVERFLOW     3
#define UFUNC_SHIFT_UNDERFLOW    6
#define UFUNC_SHIFT_INVALID      9


#define UFUNC_OBJ_ISOBJECT      1
#define UFUNC_OBJ_NEEDS_API     2

   /* Default user error mode */
#define UFUNC_ERR_DEFAULT                               \
        (UFUNC_ERR_WARN << UFUNC_SHIFT_DIVIDEBYZERO) +  \
        (UFUNC_ERR_WARN << UFUNC_SHIFT_OVERFLOW) +      \
        (UFUNC_ERR_WARN << UFUNC_SHIFT_INVALID)

#if NPY_ALLOW_THREADS
#define NPY_LOOP_BEGIN_THREADS do {if (!(loop->obj & UFUNC_OBJ_NEEDS_API)) _save = PyEval_SaveThread();} while (0);
#define NPY_LOOP_END_THREADS   do {if (!(loop->obj & UFUNC_OBJ_NEEDS_API)) PyEval_RestoreThread(_save);} while (0);
#else
#define NPY_LOOP_BEGIN_THREADS
#define NPY_LOOP_END_THREADS
#endif

/*
 * UFunc has unit of 1, and the order of operations can be reordered
 * This case allows reduction with multiple axes at once.
 */
#define PyUFunc_One 1
/*
 * UFunc has unit of 0, and the order of operations can be reordered
 * This case allows reduction with multiple axes at once.
 */
#define PyUFunc_Zero 0
/*
 * UFunc has no unit, and the order of operations cannot be reordered.
 * This case does not allow reduction with multiple axes at once.
 */
#define PyUFunc_None -1
/*
 * UFunc has no unit, and the order of operations can be reordered
 * This case allows reduction with multiple axes at once.
 */
#define PyUFunc_ReorderableNone -2

#define UFUNC_REDUCE 0
#define UFUNC_ACCUMULATE 1
#define UFUNC_REDUCEAT 2
#define UFUNC_OUTER 3


typedef struct {
        int nin;
        int nout;
        PyObject *callable;
} PyUFunc_PyFuncData;

/* A linked-list of function information for
   user-defined 1-d loops.
 */
typedef struct _loop1d_info {
        PyUFuncGenericFunction func;
        void *data;
        int *arg_types;
        struct _loop1d_info *next;
        int nargs;
        PyArray_Descr **arg_dtypes;
} PyUFunc_Loop1d;


#include "__ufunc_api.h"

#define UFUNC_PYVALS_NAME "UFUNC_PYVALS"

#define UFUNC_CHECK_ERROR(arg) \
        do {if ((((arg)->obj & UFUNC_OBJ_NEEDS_API) && PyErr_Occurred()) || \
            ((arg)->errormask && \
             PyUFunc_checkfperr((arg)->errormask, \
                                (arg)->errobj, \
                                &(arg)->first))) \
                goto fail;} while (0)


/* keep in sync with ieee754.c.src */
#if defined(sun) || defined(__BSD__) || defined(__OpenBSD__) || \
      (defined(__FreeBSD__) && (__FreeBSD_version < 502114)) || \
      defined(__NetBSD__) || \
      defined(__GLIBC__) || defined(__APPLE__) || \
      defined(__CYGWIN__) || defined(__MINGW32__) || \
      (defined(__FreeBSD__) && (__FreeBSD_version >= 502114)) || \
      defined(_AIX) || \
      defined(_MSC_VER) || \
      defined(__osf__) && defined(__alpha)
#else
#define NO_FLOATING_POINT_SUPPORT
#endif


/*
 * THESE MACROS ARE DEPRECATED.
 * Use npy_set_floatstatus_* in the npymath library.
 */
#define UFUNC_FPE_DIVIDEBYZERO  NPY_FPE_DIVIDEBYZERO
#define UFUNC_FPE_OVERFLOW      NPY_FPE_OVERFLOW
#define UFUNC_FPE_UNDERFLOW     NPY_FPE_UNDERFLOW
#define UFUNC_FPE_INVALID       NPY_FPE_INVALID

#define UFUNC_CHECK_STATUS(ret) \
    { \
       ret = npy_clear_floatstatus(); \
    }
#define generate_divbyzero_error() npy_set_floatstatus_divbyzero()
#define generate_overflow_error() npy_set_floatstatus_overflow()

  /* Make sure it gets defined if it isn't already */
#ifndef UFUNC_NOFPE
/* Clear the floating point exception default of Borland C++ */
#if defined(__BORLANDC__)
#define UFUNC_NOFPE _control87(MCW_EM, MCW_EM);
#else
#define UFUNC_NOFPE
#endif
#endif


#ifdef __cplusplus
}
#endif
#endif /* !Py_UFUNCOBJECT_H */