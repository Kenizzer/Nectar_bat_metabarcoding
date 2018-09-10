# Metabarcoding analysis of nectar bat pollen and fecal samples.

### Abridged abstract

In this study, we evaluated the efficacy of sample collection approaches and DNA metabarcoding to identify plants utilized by nectivorous bats, *Leptonycteris yerbabuenae* and *Choeronycteris mexicana*. Samples included guano collected from beneath bat roosts and pollen-swabs from bat fur, both of which were subjected to DNA metabarcoding and visual identification of pollen (light microscopy) to measure plant diversity. Our objectives were to determine whether DNA metabarcoding could detect likely food plants of nectivorous bats, whether sample types would produce different estimates of plant diversity, and to compare results of DNA metabarcoding to visual identification.

**The sequencing in this study was conducted using a Roche 454 with titanium**

Table of markers used within the study.

| Marker   | F Primer| F Primer Sequence     | R Primer| R Primer Sequence    | Size (bp) | Citation                                    |
|:--------:|:-------:|:---------------------:|:-------:|:--------------------:|:---------:|:-------------------------------------------:|
| psbA-trnH | psbAF   | GTTATGCATGAACGTAATGCTC | Trn-HR2 | CGCGCATGGTGGATTCACAAT | 185-887   | Sang *et al.* 1997 and Kress *et al.* 2005  |
| trnL     | C       | CGAAATCGGTAGACGCTACG  | D       | CGGGATAGAGGGACTTGAAC | 254-653   | Taberlet *et al.* 2007                      |
| rbcL     | 1F      | ATGTCACCACAAACAGAAAC  | 724R    | TCGCATGTACCTGCAGTAGC | 724       | Fay *et al.* 1997                           |

### Demultiplexing

Sequences were demultiplexed using by MID and quality filtered using **split_libraries.py** (QIIME V1.91; Caporaso *et al.* 2010) using the mapping files provided for each marker (see mapping_files folder). The following settings were used; minimum sequence length of 170 nucleotides, maximum homopolymer size of 8, mean quality score above 25 and allowing for up to 2 primer mismatches. This was done for each primer separately.

```bash
split_libraries.py -m psbA_mapfile.txt -f 454_seq_ampPipe.fasta -q 454_qual_ampPipe.qual -l 170 -H 8 -b 10 -M 2
```

### Chimera filtering

Chimeric sequence filtering was performed on each primer separately using **identify_chimeric_seqs.py** and **filter_fasta.py** (QIIME V1.91) with the implemented USEARCH *de novo* algorithm using default settings (Edgar 2010).

```bash
#identify chimeric sequences
identify_chimeric_seqs.py -m usearch61 -i seqs.fna --suppress_usearch61_ref -o output

#filter file of detected chimeric sequences
filter_fasta.py -f seqs.fna -o seq_chimera_filter.fna -s output/chimeras.txt -n
```
### Splitting to individual sample

A custom bash script (see scripts folder) was used to extract sequences from the now chimera free FILENAME.fna file. Basically the script preforms a grep search and places the sequences into separate files based off the header line (e.g. >GO1...).

```bash
./split_to_samples.sh
```

### Taxonomic assignment

Taxonomic assignment of sequences was conducted using **BLASTN** (blastn-2.2.31+; Camacho *et al.* 2009), with local alignments of query sequences to the NCBI nt database (downloaded 08/25/2017). BLAST searches were run in parallel using **GNU parallel** (Tange 2011) with a word size of 11 and an E-value cutoff of 1E-10 on the high performance computing cluster at Saint Louis University.

```bash
#!/usr/bin/env bash

#SBATCH --job-name=blastN
#SBATCH --output=metabarcoding_BLASTN.out
#SBATCH --partition=PARTITION_NAME
#SBATCH --ntasks=20

find . -type f -iname "*.fasta" | ~/bin/parallel /PATH/TO/PROGRAM/blastn -word_size 11 -evalue 0.0000000005 -db /PATH/TO/DATABASE/nt -query {} -out {.}.out


```
*note this script is setup for a computer cluster using SLURM as the job scheduler*

Taxonomic binning was performed on output files using mostly default settings, except a percent identity cutoff of 95%, in **Megan6 CE** (V6.11.4; Huson *et al.* 2016) with the naive lowest common ancestor (LCA) algorithm. In Megan each blast file was imported and analyzed using the LCA, all leaves and nodes below Eukaryota corresponding to plants are selected, and finally the results are exported to a .csv file using the default output options. With all of the FILE_all-ex.txt files you run the bash one liner to extract a .csv file of the taxonomic nodes.

```bash
#extract taxonomic node list
egrep -o '\".*\"' G*_all-ex.txt | egrep -o '\".*\"' | sort | uniq | sed -e 's/^"//' -e 's/"$/,/'| tr -d '\n' > taxa_list.csv

#Create a matrix from the FILE_all-ex.txt files and the file created above

python matrix_maker_nbat.py

```

After which the matrix is imported into Excel for the creation of figures. Individual figures were assembled, aligned, and touched up using GNU image manipulation program (GIMP).

**Citations**

  * Camacho, C., Coulouris, G., Avagyan, V., Ma, N., Papadopoulos, J., Bealer, K., and Madden, T.L. 2009. BLAST+: architecture and applications. BMC Bioinformatics 10: 421. doi:10.1186/1471-2105-10-421.
  * Caporaso, J.G., Kuczynski, J., Stombaugh, J., Bittinger, K., Bushman, F.D., Costello, E.K., Fierer, N., Peña, A.G., Goodrich, J.K., Gordon, J.I., Huttley, G.A., Kelley, S.T., Knights, D., Koenig, J.E., Ley, R.E., Lozupone, C.A., Mcdonald, D., Muegge, B.D., Pirrung, M., Reeder, J., Sevinsky, J.R., Turnbaugh, P.J., Walters, W.A., Widmann, J., Yatsunenko, T., Zaneveld, J., and Knight, R. 2010. QIIME allows analysis of high- throughput community sequencing data Intensity normalization improves color calling in SOLiD sequencing. Nat. Publ. Gr. 7(5): 335–336. Nature Publishing Group. doi:10.1038/nmeth0510-335.
  * Edgar, R.C. 2010. Search and clustering orders of magnitude faster than BLAST. Bioinformatics 26(19): 2460–2461. doi:10.1093/bioinformatics/btq461.
  * Fay, M.F., Swensen, S.M., and Chase, M.W. 1997. Taxonomic affinities of Medusagyne oppositifolia (Medusagynaceae). Kew Bull. 52: 111. doi:10.2307/4117844.
  * Huson, D.H., Beier, S., Flade, I., Gorska, A., El-Hadidi, M., Mitra, S., Ruscheweyh, H.J., and Tappu, R. 2016. MEGAN Community Edition - Interactive Exploration and Analysis of Large-Scale Microbiome Sequencing Data. PLoS Comput. Biol. 12: 1–12. doi:10.1371/journal.pcbi.1004957.
  * Kress, W.J., Wurdack, K.J., Zimmer, E.A., Weigt, L.A., and Janzen, D.H. 2005. Use of DNA barcodes to identify flowering plants. Proc. Natl. Acad. Sci. U. S. A. 102: 8369–74. doi:10.1073/pnas.0503123102.
  * Sang, T., Crawford, D.J., and Stuessy, T.F. 1997. Chloroplast DNA phylogeny, reticulate evolution, and biogeography of Paeonia (Paeoniaceae). Am. J. Bot. 84: 1120–1136. doi:10.2307/2446155.
  * Taberlet, P., Coissac, E., Pompanon, F., Gielly, L., Miquel, C., Valentini, A., Vermat, T., Corthier, G., Brochmann, C., and Willerslev, E. 2007. Power and limitations of the chloroplast trnL (UAA) intron for plant DNA barcoding. Nucleic Acids Res. 35: e14. doi:10.1093/nar/gkl938.
  * Tange, O. 2011. GNU Parallel: the command-line power tool. ;login USENIX Mag. 36: 42–47. doi:10.5281/zenodo.16303.