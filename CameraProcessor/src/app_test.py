import pytest
from app import Hello

def test_hello_init():
    msg = "Hello World"
    h = Hello(msg)
    assert h._msg == "Hello World"
 
def test_hello_properties():
    h = Hello("Random msg")
    assert h.msg == "Random msg"
    
    h.msg = "Hello"
    assert h.msg == "Hello"