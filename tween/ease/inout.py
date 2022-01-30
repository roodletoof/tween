'''
A collection of ease_in-out functions.
All functions use the ease.helper.clamp_decorator.
'''

from ease import inn, out
from ease.helper import make_inout_function

sine    = make_inout_function(  inn.sine,       out.sine    )
quad    = make_inout_function(  inn.quad,       out.quad    )
cubic   = make_inout_function(  inn.cubic,      out.cubic   )
quart   = make_inout_function(  inn.quart,      out.quart   )
quint   = make_inout_function(  inn.quint,      out.quint   )
expo    = make_inout_function(  inn.expo,       out.expo    )
circ    = make_inout_function(  inn.circ,       out.circ    )
back    = make_inout_function(  inn.back,       out.back    )
elastic = make_inout_function(  inn.elastic,    out.elastic )
bounce  = make_inout_function(  inn.bounce,     out.bounce  )