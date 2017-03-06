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

#EXTRACT PCA DATA
# des_fp = "C:\\Users\\james\\Desktop\\Box Sync\\THE_LIVING\\1610_AU_GenDesign\\03_WORK\\161108_DataViz\\fin_data_norm\\pop_data_v2.json"
# des_data = open(des_fp, mode='r')
# des = json.load(des_data)
# des_data.close()

#DESIGN DATA SOURCE
des_fp = "\\".join(base[:-1]) + "\\data\\designs.json"
des_data = open(des_fp, mode='r')
des = json.load(des_data)

#PCA DATA SOURCE
score_fp = "C:\\Users\\james\\Desktop\\Box Sync\\THE_LIVING\\1610_AU_GenDesign\\03_WORK\\161108_DataViz\\fin_data_norm\\data_final_v2.csv"
score_data = open(score_fp, mode='r')
score = list(csv.DictReader(score_data))

#print type(score.next()["Gen."])

for d in des:
    #get initial occurance positions
    g = int(d["instances"][0][0])
    s = int(d["instances"][0][1])
    #print g,s
    #iterate through score data to find matched PCA
    for line in score:
        if int(line["Gen."]) == g and int(line["Sol."]) == s:
            #print "MATCH!", line["PCA1"]
            d["pca-1"] = float(line["PCA1"])

out_fp = "C:\\Users\\james\\Documents\\GitHub\\gda-explorer\\data\\designs-pca.json"
with open(out_fp, mode='w') as outfile:
    json.dump(des, outfile, sort_keys=True, indent=4, separators=(',', ': '))
outfile.close()

#
# pca1 = []
# presort = []
#
# for g in range(101):
#     sol = []
#     pre = []
#     for s in range(100):
#         try:
#             sol.append( des[str(g)][str(s)]["pca1"] )
#             pre.append( des[str(g)][str(s)]["pca-sort"] )
#         except:
#             pass
#     pca1.append(sol)
#     presort.append(pre)
#
# print pca1[0]
# print [i[0] for i in sorted(enumerate(pca1[0]), key=lambda x:x[1], reverse=True)]
# print [i[1] for i in sorted(enumerate(pca1[0]), key=lambda x:x[1], reverse=True)]
# #
# sort = [ [ i[0] for i in sorted(enumerate(g), key=lambda x:x[1]) ] for g in pca1 ]
#
# for i,g in enumerate(sort):
#     print g
#     print presort[i]
#     for j,s in enumerate(g):
#         if s != presort[i][j]:
#             print "%d : %d" %(s, presort[i][j])
#             print "not a match"
#
# out_fp = "C:\\Users\\james\\Desktop\\BOX MANUAL RESYNC\\GDA\\design_explorer\\data\\sort_order.json"
# with open(out_fp, mode='w') as outfile:
#     json.dump(sort, outfile, indent=4, separators=(',', ': '))
# outfile.close()
