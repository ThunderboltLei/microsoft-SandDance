# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

import os
import streamlit.components.v1 as components
import pandas as pd
from .py_types.insight import Insight
from .py_types.explorer import ExplorerProps

from typing import Optional

# Create a _RELEASE constant. We'll set this to False while we're developing
# the component, and True when we're ready to package and distribute it.
# (This is, of course, optional - there are innumerable ways to manage your
# release process.)
_RELEASE = False

COMPONENT_NAME = "sanddance"

# Declare a Streamlit component. `declare_component` returns a function
# that is used to create instances of the component. We're naming this
# function "_component_func", with an underscore prefix, because we don't want
# to expose it directly to users. Instead, we will create a custom wrapper
# function, below, that will serve as our component's public API.

# It's worth noting that this call to `declare_component` is the
# *only thing* you need to do to create the binding between Streamlit and
# your component frontend. Everything else we do in this file is simply a
# best practice.

if not _RELEASE:
    _component_func = components.declare_component(
        # We give the component a simple, descriptive name ("sanddance"
        # does not fit this bill, so please choose something better for your
        # own component :)
        COMPONENT_NAME,
        # Pass `url` here to tell Streamlit that the component will be served
        # by the local dev server that you run via `npm run start`.
        # (This is useful while your component is in development.)
        url="http://localhost:3001",
    )
else:
    # When we're distributing a production version of the component, we'll
    # replace the `url` param with `path`, and point it to the component's
    # build directory:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend/build")
    _component_func = components.declare_component(COMPONENT_NAME, path=build_dir)


# Create a wrapper function for the component. This is an optional
# best practice - we could simply expose the component function returned by
# `declare_component` and call it done. The wrapper allows us to customize
# our component's API: we can pre-process its input args, post-process its
# output value, and add a docstring for users.

def sanddance(key: Optional[str] = None, df: pd.DataFrame = None, insight: Optional[Insight] = None, explorerProps: Optional[ExplorerProps] = None) -> int:
    """Create a new instance of "sanddance".

    Parameters
    ----------
    key: str or None
        An optional key that uniquely identifies this component. If this is
        None, and the component's arguments are changed, the component will
        be re-mounted in the Streamlit frontend and lose its current state.
    df: pandas.DataFrame
        A dataframe parameter.

    Returns
    -------
    SandDanceEvent or None
        A dict containing the event data, or None if no event has occurred.
    """

    # Call through to our private component function. Arguments we pass here
    # will be sent to the frontend, where they'll be available in an "args"
    # dictionary.
    component_value = _component_func(records=df.to_dict(orient='records'), key=key, default=None, insight=insight, explorerProps=explorerProps)

    # We could modify the value returned from the component if we wanted.
    # There's no need to do this in our simple example - but it's an option.
    return component_value
