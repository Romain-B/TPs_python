#! /usr/bin/env python
#-*- coding:utf-8 -*-
import plotly.offline as py
import plotly.graph_objs as go
import math

py.init_notebook_mode()

def weight_matrix(possibilities, data_str):
  matrix = [[0]*len(possibilities) for _ in range(len(possibilities))]
  last_c = 0
  for c in data_str:
    if last_c != 0:
      matrix[possibilities.index(c)][possibilities.index(last_c)] +=1.0/len(data_str)
    last_c = c

  return matrix
  

def make_heatmap(matrix,axis_labels,filename):
  data = [go.Heatmap(z=matrix,x=axis_labels,y=axis_labels)]
  py.plot(data, filename=filename)

def get_string_from_fasta_file(fasta_name):
  ret_str = ""
  with open(fasta_name,"r") as feb:
    next(feb)
    for line in feb:
      ret_str+= line
  ret_str = ret_str.replace('\n','')

  return ret_str

def compute_log_likelihood(m,possibilities,data_str):
  last_c = 0
  log_sum = 0
  for c in data_str:
    if last_c != 0:
      log_sum += math.log(m[possibilities.index(c)][possibilities.index(last_c)]) 
    last_c = c
  return log_sum

if __name__ == '__main__':
  a = 0

  poss = ['A','T','C','G']
  
  ebola = get_string_from_fasta_file("ebola.fasta")
  narna = get_string_from_fasta_file("narna.fasta")
  unknown = get_string_from_fasta_file("unknown.fasta")

  #print narna
  m_eb = weight_matrix(poss, ebola)
  #make_heatmap(m_eb,poss,"ebola")
  m_na = weight_matrix(poss,narna)
  #make_heatmap(m_na,poss,"narna")

  print "Ebola likelihood :  ",compute_log_likelihood(m_eb, poss, unknown)
  print "Narna likelihood :  ",compute_log_likelihood(m_na, poss, unknown)
