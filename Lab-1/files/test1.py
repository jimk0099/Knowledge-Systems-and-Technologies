# -*- coding: utf-8 -*-
"""
Created on Sat May 14 19:13:12 2022

@author: Admin
"""

from rdflib import Graph, Literal, URIRef, Namespace

ns1 = Namespace('http://example.org/ns/')


## Αρχικοποίηση ενός κενού γράφου
g = Graph()

## Διάβασμα του αρχείου και προσθήκη στο γράφο
g.parse('Admin\Desktop\Gnwsi_Graphs\\final233.nt', format='nt')


def recommender1(graph, song):
  
  results = []
  #song = song.replace(' ','_')

  ans=g.query(
      """
        PREFIX exp: <http://example.org/props/>
        PREFIX ex: <http://example.org/ns/>


        SELECT DISTINCT ?song2 (COUNT(distinct ?song2) AS ?count)
          WHERE {
              ex:"""+song+""" exp:has_composer ?comp ;
                              exp:has_publisher ?publisher ;
                              exp:has_emotions ?emotion ;
                              exp:has_genres ?genre ;
                              exp:has_instruments ?ins .
              {?song2 exp:has_composer ?comp .} UNION {?song2 exp:has_publisher ?publisher .} .
              #{?song2 exp:has_emotions ?emotion .} .#UNION {?song2 exp:has_genres ?genre .} .#UNION {exp:has_instruments ?ins} .
          }
          GROUP BY ?song2
        """)

    #for a in ans:
    #print(str(a.asdict()['song2'].toPython()).replace(ns1,''))
    #results.append(str(a.asdict()['song2'].toPython()).replace(ns1,''))
  ans = [a['song2'].toPython().replace(ns1,'') for a in ans]
  return ans



# read file and make a line for each user
# make user_line

user_line = []
user_line_len = []
f = open("\\Users\Admin\Desktop\Gnwsi_Graphs\\new_users.txt", "r")
Lines = f.readlines()
for line in Lines:
  line = line.split()
  user_line.append(line)
  user_line_len.append(len(line))
  
  
  
  
# find recommended songs based on user_line
# make rec_list

def recommend_me(rec):
  rec_list = []
  rec_list_len = []
  for i in range (len(user_line)):
    rec_list.append(rec(g, user_line[i][0]))
    rec_list_len.append(len(rec(g, user_line[i][0])))
  return [rec_list, rec_list_len]



# calculate precision and recall

temp_l = recommend_me(recommender1)
rec_list = temp_l[0]
rec_list_len = temp_l[1]

tp = [0 for i in range(10)]
tpfp = rec_list_len
tpfn = user_line_len

for l in range(10):                                     # for all lines
  for i in range(len(rec_list[l])):                        # for all the songs the recommender finds
    for j in range(1, len(user_line[l])):               # find which are the same with the songs that the user actually likes
      if(rec_list[l][i] == user_line[l][j]):
        tp[l] = tp[l] + 1


precision = []
recall = []
for i in range(10):
  if(tpfp[i] != 0):
    precision.append(tp[i]/tpfp[i])
  else:
    precision.append(0)
  recall.append(tp[i]/tpfn[i])

meanP = 0
meanR = 0

for i in range(10):
  meanP = meanP + precision[i]
  meanR = meanR + recall[i]
  print("user%d precision:%.3f recall:%.3f" %(i, precision[i], recall[i]))

print("\nIn total precision:%.3f recall:%.3f" %(meanP/10, meanR/10))