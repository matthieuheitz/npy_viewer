#!/usr/bin/env python

import os
import anndata
import sys

adata = anndata.read_h5ad(sys.argv[1])
print("##############################")
print(adata)
print("\n##############################\n")
print("adata.X:\n",adata.X)
if not adata.obs.empty:
    print("\n##############################\n")
    print("adata.obs:\n",adata.obs)
if not adata.var.empty:
    print("\n##############################\n")
    print("adata.var:\n",adata.var)
