#!/usr/bin/python
import sys
import re



# Generator versinos of split - to avoid memory overheads
#sep = re.compile(r"[A-Za-z']+")
sep = re.compile(r"[A-Za-z_\-']+")

def split_iter(string):
    return (x.group(0) for x in re.finditer(sep, string))

def isplit(source, sep):
    sepsize = len(sep)
    start = 0
    while True:
        idx = source.find(sep, start)
        if idx == -1:
            yield source[start:]
            return
        yield source[start:idx]
        start = idx + sepsize

def main():
	if len(sys.argv) < 2:
		usage()
	ped_base = sys.argv[1]
	out_base = sys.argv[2]
	map_file = ped_base + ".map"
	ped_file = ped_base + ".ped"
	out_meta = out_base + ".meta"
	out_geno = out_base + ".stru.1"
	with open(map_file) as f:
		try:
			snp_id = [ x[1] for x in [ y.split("\t") for y in f.readlines() ] ]
		except IndexError:
			snp_id = [ x[1] for x in [ y.split(" ") for y in f.readlines() ] ]
	#for i in xrange(6):
	#	sys.stderr.write( snp_id[i] + "\n" )
	with open(ped_file) as ped, open(out_meta, "w") as out1, open(out_geno, "w") as out2 :
		# The first line is SNP ids
		out2.write(" ".join(snp_id) +"\n")
		for line in ped:
			#words = split_iter(line) # generator
			words = isplit( line.rstrip(), " ")
			fid = words.next()
			iid = words.next()
			z1 = words.next()
			z2 = words.next()
			z3 = words.next()
			ph = words.next()
			al1 = []
			al2 = []
			try:
				while True:
					al1.append( words.next() )
					al2.append( words.next() )
			except StopIteration:
				pass
			# Write two lines with IID to 'meta' file
			out1.write(iid + "\n"+ iid + "\n") #"%s\n%s\n".format(iid,iid))
			
			# Write allele 1 line and then allele2 line to the "genotype" file
			out2.write(" ".join(al1) + "\n")
			out2.write(" ".join(al2) + "\n")


if __name__ == "__main__":
	main()

