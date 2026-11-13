"""
Pages package
=============
Each sub-module exposes a ``render()`` function and calls it at module
level behind an ``if __name__ == "__main__":`` guard, since Streamlit
runs each page file as a script rather than importing it.
"""
