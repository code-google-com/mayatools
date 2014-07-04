# coding: utf-8
"""zmq Context class"""

#-----------------------------------------------------------------------------
#  Copyright (C) 2013 Felipe Cruz
#
#  This file is part of pyzmq
#
#  Distributed under the terms of the New BSD License.  The full license is in
#  the file COPYING.BSD, distributed as part of this software.
#-----------------------------------------------------------------------------

import weakref

from ._cffi import C, ffi

from .socket import *
from .constants import *

from zmq.error import ZMQError, _check_rc

class Context(object):
    _zmq_ctx = None
    _iothreads = None
    _closed = None
    _sockets = None
    _shadow = False

    def __init__(self, io_threads=1, shadow=None):
        
        if shadow:
            self._zmq_ctx = ffi.cast("void *", shadow)
            self._shadow = True
        else:
            self._shadow = False
            if not io_threads >= 0:
                raise ZMQError(EINVAL)
        
            self._zmq_ctx = C.zmq_ctx_new()
        if self._zmq_ctx == ffi.NULL:
            raise ZMQError(C.zmq_errno())
        if not shadow:
            C.zmq_ctx_set(self._zmq_ctx, IO_THREADS, io_threads)
        self._closed = False
        self._sockets = set()
    
    def __del__(self):
        if self._zmq_ctx and not self._closed and not self._shadow:
            C.zmq_ctx_destroy(self._zmq_ctx)
            self._zmq_ctx = None
            self._closed = True
    
    @property
    def underlying(self):
        """The address of the underlying libzmq context"""
        return int(ffi.cast('size_t', self._zmq_ctx))
    
    @property
    def closed(self):
        return self._closed

    def _add_socket(self, socket):
        ref = weakref.ref(socket)
        self._sockets.add(ref)
        return ref

    def _rm_socket(self, ref):
        if ref in self._sockets:
            self._sockets.remove(ref)

    def set(self, option, value):
        """set a context option
        
        see zmq_ctx_set
        """
        rc = C.zmq_ctx_set(self._zmq_ctx, option, value)
        _check_rc(rc)

    def get(self, option):
        """get context option
        
        see zmq_ctx_get
        """
        rc = C.zmq_ctx_get(self._zmq_ctx, option)
        _check_rc(rc)
        return rc

    def term(self, linger=None):
        if self.closed:
            return

        sockets = self._sockets
        self._sockets = set()
        for s in sockets:
            s = s()
            if s and not s.closed:
                if linger:
                    s.setsockopt(LINGER, linger)

        C.zmq_ctx_destroy(self._zmq_ctx)

        self._zmq_ctx = None
        self._closed = True

    def destroy(self, linger=None):
        if self.closed:
            return

        sockets = self._sockets
        self._sockets = set()
        for s in sockets:
            s = s()
            if s and not s.closed:
                if linger:
                    s.setsockopt(LINGER, linger)
                s.close()
        
        self.term()

__all__ = ['Context']
