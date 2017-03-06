import os, csv, json

# input:
# 1: lineage data - [101: GENERATIONS][100: Object: Design]
# 2: unique design data - [N: Unique design]
#
# output:
# 1: [101: Gen][100: Sort position (by PCA1)]
#

#EXTRACT BASE DIRECTORY FOR RELATIVE PATH CONSTRUCTION
base_dir = os.path.dirname(__file__)
base = base_dir.split("\\")


#DESIGN DATA SOURCE
des_fp = "\\".join(base[:-1]) + "\\data\\designs-pca.json"
des_data = open(des_fp, mode='r')
des = json.load(des_data)

for d in des:
    d["instances-sort"] = []

#LINEAGE DATA SOURCE
lin_fp = "\\".join(base[:-1]) + "\\data\\lineage.json"
lin_data = open(lin_fp, mode='r')
lin = json.load(lin_data)

for g, gen in enumerate(lin):
    print "GEN" + str(g)
    ids = [s["design_id"] for s in gen]
    pca = [des[s]["pca-1"] for s in ids]
    sort_id = [ i[0] for i in sorted(enumerate(pca), key=lambda x : x[1], reverse=False)]

    for i,idx in enumerate(ids):
        if idx == -1:
            continue
        des[idx]["instances-sort"].append( [ g, sort_id[i] ] )

out_fp = "C:\\Users\\james\\Documents\\GitHub\\gda-explorer\\data\\designs-pca_sort.json"
with open(out_fp, mode='w') as outfile:
    json.dump(des, outfile, sort_keys=True, indent=4, separators=(',', ': '))
outfile.close()
