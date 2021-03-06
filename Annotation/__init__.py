import os


class Probe:
    """
    This class holds probe info.

    USAGE:

.. code:: python

    my_probe = Annotation.Probe()

    """

    def __init__(self):
        self.id = None
        self.seq = None
        self.name = None
        self.chr = None
        self.cord = None
        self.strand = None
        self.gene = None
        self.refseq = None
        self.beta = None
        self.tour = None
        self.loc = None


class SNP:
    """

    This class defines the SNPs in probes. Can be used to filter probes.


    """

    def __init__(self):
        self.probeid = None
        self.snpid = None


class ChrLoc:
    """

    defines a chromosomal interval.

    USAGE:

.. code:: python

    my_probe = Annotation.ChrLoc("X", 122333232, 123334444)

    """

    def __init__(self, chromosome, start, end):
        self.chr = chromosome
        self.start = start
        self.end = end


class Location:
    """
    Probe location is defined here.
    """

    BODY = "Body"
    TSS200 = "TSS200"
    TSS1500 = "TSS1500"
    UTR5 = "5'UTR"
    UTR3 = "3'UTR"
    EXON = "Exon"


class CpG_location:
    """
    CpG location is defined here.
    """

    ISLAND = "Island"
    NSHORE = "N_Shore"
    SSHORE = "S_Shore"
    NSHELF = "N_Shelf"
    SSHELF = "S_Shelf"


class Feature:
    """

    This class parse features associated with probes.


    """

    def __init__(self, feature):
        self.feature_title = None
        self.feature = None
        if feature in ["Body", "TSS200", "TSS1500", "5'UTR", "3'UTR", "Exon"]:
            self.feature_title = "Location"
            self.feature = feature
        elif feature in ["Island", "N_Shore", "S_Shore", "N_Shelf", "S_Shelf"]:
            self.feature_title = "cpg_loc"
            self.feature = feature
        else:
            self.feature_title = "gene"
            self.feature = feature


class Annotator:
    """

    This class parse all information about Illumina probes.

    USAGE:

.. code:: python

    annotations = Annotation.Annotator()

    """

    def __init__(self):
        ann_file = os.path.abspath("Data/config.ini")
        for i in open(ann_file, mode="r"):
            self.ann = os.path.join("Data/", i.strip("\n").strip("\r"))

        self.probe = {}
        self.__run__()

    def __run__(self):
        """

        Run the annotation initial setup.

        :return: nothing. A static function.

        """
        for i in open(self.ann, mode="r"):
            if i.startswith("cg"):
                data = i.split(",")
                # Assigning probe information.
                new_probe = Probe()
                new_probe.id = data[0]
                new_probe.name = data[1]
                new_probe.seq = data[13]
                new_probe.chr = str(data[11])
                new_probe.cord = int(data[12])
                new_probe.strand = data[16]
                new_probe.gene = data[21].split(";")
                new_probe.refseq = data[22]
                locs = data[23].split(";")
                list_locs = []
                for i in locs:
                    if i not in list_locs:
                        list_locs.append(i)

                new_probe.loc = list_locs

                new_probe.tour = data[25]
                newcpg = {new_probe.id: new_probe}
                self.probe.update(newcpg)

    def remove_snp_probes(self):
        """

        This function will removes all SNPs associated with probes.

        :return: returns a new probe listing.

        """
        snp_list = []
        snp_file = open("Data/humanmethylation450_dbsnp137.snpupdate.table.v2.sorted.txt", "r")
        for line in snp_file:
            if line.startswith("cg"):
                line = line.strip("\n").strip("\r").split("\t")
                new_snp = SNP()
                new_snp.probeid = line[0]
                new_snp.snpid = line[1]
                snp_list.append(new_snp)

        for snp in snp_list:
            self.probe.pop(snp.probeid)

    def get_all_probe_ids(self):
        """

        Get all probe ids.

        :return: a list of probe ids.

        """
        return self.probe

    def get_probes_id_from_gene(self, gene_name):
        """

        Get all probes ids associated with a gene.

        :param gene_name:
        :return: a lst of probe ids.

        """
        probes = {k: self.probe[k] for k in self.probe if gene_name in self.probe[k].gene}
        return self.get_keys(probes.keys())

    def get_probes_id_from_loc(self, probe_loc):
        """

        Get all probes ids associated with genomic locations.

        :param probe_loc:
        :return: a list of probe ids.

        """
        probes = {k: self.probe[k] for k in self.probe if probe_loc in self.probe[k].loc}
        return self.get_keys(probes.keys())

    def get_probes_id_from_cpg(self, cpg_loc):
        """

        Get all probes ids associated with CpG sites.

        :param cpg_loc:
        :return: a list of probe ids.

        """
        probes = {k: self.probe[k] for k in self.probe if cpg_loc in self.probe[k].tour}
        return self.get_keys(probes.keys())

    def get_probes_id_from_probe(self, probe_list):
        """

        Get all probes ids from a list of probe objects.

        :param probe_list: A list of probe ids.
        :return: a list of probe ids.

        """
        return self.get_keys(probe_list.keys())

    def get_keys(self, dic_keys):
        """

        Get Probe id from probe dictionaries

        :param dic_keys: Probe dict.
        :return: returns a list of probe id.

        """
        l = []
        for i in dic_keys:
            l.append(i)
        return l

    def get_probe(self, probe_id):
        """

        This function returns the info associated with an id.

        :param probe_id: ILLUMINA ID
        :return: all info

        """

        try:
            probe = self.probe[probe_id]
        except Exception as ex:
            probe = None
            print("WARNING: No probe with id of %s found." % probe_id)
        return probe

    def get_probes(self, list_of_ids):
        """

        This function returns a list of probe object from a list of ids.

        :param list_of_ids:
        :return: A list of probe objects.

        """
        out_list = []
        for probe_id in list_of_ids:
            out_list.append(self.get_probe(probe_id))

        return out_list

    def get_all_probes(self):
        """

        Get a list of all probes.

        :return: A list of all probes in the Annotation object.

        """

        probe_list = []
        for probe in self.probe.iterkeys():
            probe_list.append(self.get_probe(probe))
        return probe_list



    def get_probes_from_gene(self, gene_name):
        """

        Get a list probe objects from an associated gene name.

        :param gene_name: Gene name in string format
        :return: A probe.

        """
        return self.get_probes(self.get_probes_id_from_gene(gene_name))

    def get_probes_from_loc(self, loc):
        """

        Get a list probe objects from genomic location.

        :param loc: from Location object.
        :return: probes.

        """
        return self.get_probes(self.get_probes_id_from_loc(loc))

    def get_probes_from_cpg(self, cpg_loc):
        """

        Get a list probe objects from cpg location.

        :param cpg_loc: from CpG object
        :return: probes.

        """
        return self.get_probes(self.get_probes_from_cpg(cpg_loc))

    def get_probes_from_chr_loc(self, chr_loc):
        """

        Get a list of probes that are within a genomic region

        :param chr_loc: Genomic location interval
        :return: A list of probes.

        """
        chrom = chr_loc.chr
        start = int(chr_loc.start)
        end = int(chr_loc.end)

        probes = {k: self.probe[k] for k in self.probe if
                  self.probe[k].chr == chrom and start < self.probe[k].cord < end}
        return probes

    def get_probes_id_from_chr_loc(self, chr_loc):
        """

        Get a list of probe ids that are witihn a genomic region

        :param chr_loc: Genomic location interval
        :return: A list of probe ids.

        """
        probes = self.get_probes_from_chr_loc(chr_loc)
        return self.get_keys(probes)

    def get_number(self):
        """

        Get numbers of probes

        :return: An integer representing the number of probes.

        """
        number = 0
        for probe_id in self.probe.iterkeys():
            number += 1

        return number

    def get_coord(self, probe):
        """

        Get genomic coordinate of a probe.

        :param probe: A probe object
        :return: An integer indicator of probe numbers

        """
        return probe.cord

    def sort_coord_probe(self, probes):
        """

        This function sorts probes based on the probe genomic location. Best used in combination with plotting module.

        :param probes: Input probe list.
        :return: A sorted probe list.

        """
        soreted_probes = sorted(probes, key=self.get_coord)
        return soreted_probes


def get_probes(annotations, probes_ids):
    """

    Get a list of probes from probe ids

    :param annotations: Annotation object that has been initiated properly.
    :param probes_ids: A list of probe ids.
    :return: A list of probes.

    """
    return annotations.get_probes(probes_ids)


def get_probes_from_feature(probes_ids, filter_val):
    """

    This function returns filters probes based on a feature.

    :param probes_ids: The probe ids that you would like to filter.
    :param filter_val: Feature to be filtered.
    :return: Returns a list of probes.

    """
    probes = probes_ids
    out_probes = []
    if filter_val.feature_title == "Location":
        out_probes = [probe for probe in probes if filter_val.feature in probe.loc]
        print("Location")
        return out_probes
    elif filter_val.feature_title == "cpg_loc":
        print("CPG")
        out_probes = [probe for probe in probes if filter_val.feature in probe.tour]
        return out_probes
    elif filter_val.feature_title == "gene":
        out_probes = [probe for probe in probes if filter_val.feature in probe.gene]
        return out_probes
    elif filter_val is None:
        return None
