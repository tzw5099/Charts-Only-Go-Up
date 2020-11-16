import sys
import os

print("ABC ", os.path.join(os.path.dirname(__file__)))
print("ABC ", os.path.join(os.path.dirname(__file__), ".."))
print("ABC ", os.path.join(os.path.dirname(__file__), "..", ".."))
