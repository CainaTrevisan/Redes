from subprocess import Popen, PIPE
import sys

# Modo de Uso
if len(sys.argv) != 2:
    print("python diff.py file_to_be_patched")

FILE = sys.argv[1]

# Create string with the new content of FILE
l = 'asd\nqwe\nzxc\n'

print("The future content of file %s:\n%s" % (FILE, l))

# Call diff 
args = ['diff', FILE, '-'] 
p = Popen(args, stdin=PIPE, stdout=PIPE)

# Put diff output into variable diff
diff, err = p.communicate(l.encode())

# Print diff output
print("Diff output:")
print(diff.decode())

# Call patch
args = ['patch', FILE] 
p = Popen(args, stdin=PIPE)

# Send result of diff as input to patch
p.communicate(diff)
