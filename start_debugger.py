import ptvsd
print("Imported")
ptvsd.enable_attach(address=('localhost', 5678), redirect_output=True)
print("Enabled debugger")
