import sounddevice
n=sounddevice.query_devices()
print(*n,sep="\n")