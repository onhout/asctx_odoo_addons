# -*- coding: utf-8 -*-

from odoo import models, fields, api
import os, sys, requests, re
# from Bio.Seq import Seq

class ASC_Plasmid(models.Model):
    _name = 'asc_rdtd.asc_plasmid'

    name = fields.Char(required="True")
    other_name = fields.Char()
    plasmid_id = fields.Char()
    project = fields.Many2one("project.project", string="Related Project", required="True")
    attachment_ids = fields.Many2many('ir.attachment', string='Attachments')
    application = fields.Char()
    components = fields.Char()
    antibiotics = fields.Selection([ ('ampicillin', 'Ampicillin'),('kanamycin', 'Kanamycin'),],'Antibiotics', default='ampicillin')
    source = fields.Char()
    backbone = fields.Char()
    box = fields.Char()
    concentration = fields.Float(string="Concentration(ng/ul)")
    description = fields.Text()
    notes = fields.Text()


class ASC_Virus(models.Model):
    _name = 'asc_rdtd.asc_virus'

    name = fields.Char()
    lot = fields.Char()
    project = fields.Many2one("project.project", string="Related Project", required="True")
    manufacturer = fields.Char()
    manufacture_date = fields.Datetime()
    received_by = fields.Many2one("hr.employee", string="Received By", required="True")
    received_date = fields.Datetime()
    original_titer = fields.Char()
    volume = fields.Char()
    vials = fields.Integer()
    notes = fields.Text()
    attachment_ids = fields.Many2many('ir.attachment', string='Attachments')

class ASC_Analysis(models.Model):
    _name = 'asc_rdtd.asc_analysis'

    name = fields.Char(required="True")
    project = fields.Many2one("project.project", string="Related Project", required="True")
    grnas = fields.One2many('asc_rdtd.asc_analysis.asc_grnas', 'analysis', string="gRNAs")
    primers = fields.One2many('asc_rdtd.asc_analysis.asc_primers', 'analysis', string="Primers")
    species = fields.Selection([ ('human', 'Human'),('mouse', 'Mouse'),('rat', 'Rat'),('hamster', 'Hamster'),('monkey', 'Monkey'),],'Species', default='human')
    notes = fields.Text()

    def parse_results(self, path):
        prefix = "n_"
        seq_name = ''
        results = {}
        with open(path, "r") as f:
            for line in f:
                seq_re = re.search(r'SEQUENCE_ID=(\S+)', line)
                seq_tmp = re.search(r'SEQUENCE_TEMPLATE=(\S+)', line)
                pl = re.search(r'PRIMER_LEFT_(\d+)_SEQUENCE=(\S+)', line)
                pr = re.search(r'PRIMER_RIGHT_(\d+)_SEQUENCE=(\S+)', line)
                tml = re.search(r'PRIMER_LEFT_(\d+)_TM=(\S+)', line)
                tmr = re.search(r'PRIMER_RIGHT_(\d+)_TM=(\S+)', line)
                start = re.search(r'PRIMER_LEFT_(\d+)=(\S+),', line)
                end = re.search(r'PRIMER_RIGHT_(\d+)=(\S+),', line)
                if seq_re:
                    seq_name = prefix + seq_re.group(1)
                    results['name'] = seq_name
                    
                if seq_tmp:
                    results['seq'] = seq_tmp.group(1)
                if pl:
                    results[int(pl.group(1))] = {'seq5': pl.group(2)}
                if pr:
                    results[int(pr.group(1))]['seq3'] = pr.group(2)
                if tml:
                    results[int(tml.group(1))]['tm5'] = tml.group(2)
                if tmr:
                    results[int(tmr.group(1))]['tm3'] = tmr.group(2)
                if start:
                    results[int(start.group(1))]['start'] = start.group(2)
                if end:
                    results[int(end.group(1))]['end'] = end.group(2)
                    # end_seq = end.group(2)
                    # if start_seq and end_seq:
                        # results[seq_name][int(end.group(1))]['ref_seq'] = results[seq_name]['seq'][start_seq:end_seq]
                    # results[seq_name][int(end.group(1))]['expected_band_size'] = len(results['ref_seq'])
        for i in range(0, 10):
            start = results[i]['start']
            end = results[i]['end']
            results[i]['ref_seq'] = results['seq'][int(start):int(end)]
            results[i]['expected_band_size'] = len(results[i]['ref_seq'])

        return results

    @api.multi
    def run_analysis(self):
        tmp_folder = '/tmp'
        bioinfo_script_folder = '/bioinfo_scripts'
        blast_db = '/blast_databases'
        grna_in = '/home/administrator/Desktop/all_ref.fasta'
        grna_blast = '{}/grna_blast_python'.format(tmp_folder)
        ngs_in_path = '{}/ngs_in'.format(tmp_folder)
        ngs_out_path = '{}/ngs_out'.format(tmp_folder)

        ensembl_path = 'https://rest.ensembl.org/sequence/region/'
        for g in self.grnas:
            start = g.cut_site
            end = g.cut_site
            ext = (600 - (int(end)-int(start))/2)
            g_start = int(int(start) - ext)
            g_end = int(int(end) + ext)
            ensembl_complete = ensembl_path + '{}/{}:{}..{}:1?content-type=application/json'.format(self.species, g.chromosome, g_start, g_end)
            response = requests.get(ensembl_complete)
            json = response.json()

            ngs_in = 'PRIMER_TASK=generic\nSEQUENCE_ID=id1\nSEQUENCE_TEMPLATE={}\nPRIMER_NUM_RETURN=10\nPRIMER_PICK_LEFT_PRIMER=1\nPRIMER_PICK_INTERNAL_OLIGO=0\nPRIMER_PICK_RIGHT_PRIMER=1\nPRIMER_OPT_SIZE=20\nPRIMER_MIN_SIZE=18\nPRIMER_MAX_SIZE=22\nPRIMER_PRODUCT_SIZE_RANGE=140-280\nPRIMER_EXPLAIN_FLAG=1\nPRIMER_MAX_NS_ACCEPTED=0\nSEQUENCE_PRIMER_PAIR_OK_REGION_LIST=0,{},{},{}\n=\n'.format(json['seq'], int(ext - 25), int(len(json['seq']) - ext + 25), int(ext - 25))

            with open(ngs_in_path, "w") as ngs:
                ngs.write(ngs_in)

            os.system('/usr/bin/primer3_core --output={} {}'.format(ngs_out_path, ngs_in_path))
            results = self.parse_results(ngs_out_path)
            print(results)
            for i in range(0, 10):
                self.env['asc_rdtd.asc_analysis.asc_primers'].create({
                    'analysis': self.id,
                    'grna_sequence': g.sequence,
                    'name': results['name'] + "_primer_" + str(i),
                    'primer5_seq': results[i]['seq5'],
                    'primer3_seq': results[i]['seq3'],
                    'tm5': results[i]['tm5'],
                    'tm3': results[i]['tm3'],
                    'expected_band_size': results[i]['expected_band_size'],
                    'ref_sequence': results[i]['ref_seq'],
                })
            # self.env['asc_rdtd.asc_analysis.asc_grnas'].create(
            #     {'analysis': self.id, 'chromosome': 'X', 'sequence': "ACTG"})
        return
    
   


class ASC_Grna(models.Model):
    _name = 'asc_rdtd.asc_analysis.asc_grnas'

    analysis = fields.Many2one('asc_rdtd.asc_analysis', string="Analysis")
    chromosome = fields.Char(required="True", string="Chr")
    sequence = fields.Char(required="True")
    cut_site = fields.Integer(required="True")

class ASC_Primers(models.Model):
    _name = 'asc_rdtd.asc_analysis.asc_primers'
    analysis = fields.Many2one('asc_rdtd.asc_analysis', string="Analysis")
    grna_sequence = fields.Char()
    name = fields.Char()
    primer5_seq = fields.Char()
    primer3_seq = fields.Char()
    tm5 = fields.Char()
    tm3 = fields.Char()
    expected_band_size = fields.Char()
    ref_sequence = fields.Text()