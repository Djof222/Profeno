# -*- coding: utf-8 -*-
import re
from odoo import models, fields, api, _


class Lead(models.Model):
    _inherit = 'crm.lead'

    ref_projet = fields.Char(string='Ref projet')
    ref_projet = fields.Char(string='Ref projet')
    token_jopps = fields.Char(string='Token JoPPS')
    date_creation = fields.Date(string='Date de création')
    adresse_chantier = fields.Boolean(string='Adresse du chantier')
    soumission_ferme = fields.Selection([
        ('soumission', 'Soumission'),
        ('ferme', 'Ferme')
    ], string='Soumission/Ferme')
    statut_covid = fields.Selection([
        ('covid_fab', 'COVID FAB'),
        ('covid_mea', 'COVID MEA')
    ], string='Statut COVID')
    type_offre = fields.Selection([
        ('menuiserie_ext', 'Menuiserie Extérieure'),
        ('pergolas', 'Pergolas'),
        ('menuiserie_int', 'Menuiserie Intérieure')
    ], string='Type Offre')
    phase_vente = fields.Selection([
        ('offre_en_cours', 'Offre en cours'),
        ('offre_signee', 'Offre Signée'),
        ('fabrication_en_cours', 'Fabrication en cours'),
        ('a_planifier', 'A planifier'),
        ('gagnee', 'Gagnée'),
        ('perdue', 'Perdue'),
        ('a_commander', 'A commander'),
        ('commande_en_cours', 'Commande en cours'),
        ('a_mesurer', 'A mesurer'),
        ('place', 'Placé'),
        ('livre_facturer', 'Livré-à-facturer'),
        ('cloture', 'Clôturé'),
        ('offre_non_suivie', 'Offre non suivie')
    ], string='Phase de vente')
    no_jorpa = fields.Char(string='N°JoRPA')
    date_modification = fields.Datetime(string='Date de modification')
    emplacement_cle = fields.Integer(string='Emplacement clé (boite)')
