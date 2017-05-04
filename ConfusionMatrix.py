out_arr=[]
out_num = [0,0,0,0,0,0,0]
cat_num = [0,0,0,0,0,0,0]
fp = [0,0,0,0,0,0,0]
fn = [0,0,0,0,0,0,0]
result = [[0for col in range(8)] for row in range(8)]

f = open("output.txt", "r")
lines = f.readlines()
for line in lines:
    out_arr.append(line)
f.close()

fr = open("testfile.txt", "r")
f = open("output.txt", "r")
out = f.readlines()
lines = fr.readlines()

n=0
for line in lines:
    cat = line.split()[0]
    result[int(cat)-1][int(out_arr[n])-1] = result[int(cat)-1][int(out_arr[n])-1] + 1
    n=n+1

for row in result:
    print row

fr.close()
f.close()