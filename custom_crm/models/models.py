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
        ('menuiserie_int', 'Menuiserie Intérieure'),
        ('condition', 'Conditions chantiers')
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

    phase_offre = fields.Selection([
        ('offre_en_cours', 'Offre en cours'),
        ('offre_acceptee', 'Offre Acceptée'),
        ('offre_refusee', 'Offre refusée'),
        ('offre_refusee_plus_tard', 'Offre refusée - Pour plus tard'),
        ('offre_refusee_trop_cher', 'Offre refusée - Trop cher'),
        ('offre_refusee_trouve_ailleurs', 'Offre refusée - Trouvé ailleurs'),
        ('offre_refusee_rupture_contrat', 'Offre refusée - Rupture de contrat'),
        ('offre_acceptee_sous_reserve', 'Offre Acceptée sous réserve'),
        ('offre_refusee_autre_raison', 'Offre refusée - Autre raison'),
        ('offre_non_suivie', 'Offre non suivie')
    ], string='Phase offre')

    no_offre_jopps = fields.Char(string='N° Offre JoPPS')
    date_signature_probable = fields.Date(string='Date signature probable')
    date_signature = fields.Date(string='Date Signature')
    date_dernier_contact = fields.Date(string='Date dernier contact')
    date_echeance = fields.Date(string='Date échéance')

    obligation_contrat = fields.Many2many('obligation.model', string='Obligation contrat')
    promo = fields.Selection([
        ('pose_1_euro', 'Pose 1 Euro'),
        ('promo_prime_2021', 'Promo Prime 2021'),
        ('tablette_2019', 'Tablette 2019'),
        ('tablette_2018', 'Tablette 2018'),
        ('cheque_cadeau', 'Cheque Cadeau'),
        ('a_cs20_250', 'A_CS20_250'),
        ('a_cs20_550', 'A_CS20_550'),
        ('a_cs20_1150', 'A_CS20_1150'),
        ('b_cs20_50', 'B_CS20_50'),
        ('b_cs20_100', 'B_CS20_100'),
        ('b_cs20_150', 'B_CS20_150')
    ], string='Promo')

    date_prochain_contact = fields.Date(string='Date prochain contact')
    moins_value_plus_value = fields.Selection([
        ('oui', 'Oui'),
        ('non', 'Non')
    ], string='moins value plus value')

    semaine_livraison_estimee = fields.Char(string='Semaine livraison estimée')
    montant_offre_jopps = fields.Float(string='Montant Offre JoPPS')
    type_contrat = fields.Selection([
        ('enlevement', 'Enlevement'),
        ('pose_marche_prive_sans_architecte', 'Pose marché privé : travaux sans architecte'),
        ('livraison', 'Livraison'),
        ('pose_marche_prive_avec_architecte', 'Pose marché privé : travaux avec architecte'),
        ('pose_marche_public', 'Pose marché public'),
        ('pose_sous-traitance', 'Pose sous-traitance')
    ], string='Type contrat')

    type_facturation = fields.Selection([
        ('40_50_10', '40% - 50% - 10%'),
        ('40_60', '40% - 60%'),
        ('100', '100%')
    ], string='Type de facturation')

    conditions_chantiers = fields.Selection([
        ('cautionnement_5', '5%'),
        ('cautionnement_10', '10% (5%RP-5%RD)'),
    ], string='Cautionnement')

    tva = fields.Selection([
        ('tva_0', 'TVA 0'),
        ('tva_6_renovation_10', '6% Travaux de rénovation pour logements privés plus de 10 ans'),
        ('tva_6_renovation_15', '6% Travaux de rénovation pour logements privés plus de 15 ans'),
        ('tva_6_logements_handicapes', '6% Logements pour personnes handicapés'),
        ('tva_6_institutions_handicapes', '6% Institutions pour handicapés'),
        ('tva_21', '21'),
        ('tva_6', '6')
    ], string='TVA')

    garantie_decennale = fields.Selection([
        ('oui', 'Oui'),
        ('non', 'Non'),
    ], string='Garantie décennale')

    etat_avancement = fields.Boolean(string="Etat d'avancement")

    escompte = fields.Selection([
        ('pas_descompte', "pas d'escompte"),
        ('2', '2%'),
        ('3', '3%'),
        ('5', '5%')
    ], string='Escompte')

    conditions_paiement = fields.Selection([
        ('60_jours_date_facture', '60 jours date facture'),
        ('30_jour_date_facture', '30 jour date facture'),
        ('60_jour_fin_de_mois', '60 jour fin de mois'),
        ('30_jour_fin_de_mois', '30 jour fin de mois'),
        ('40_acompte_solde_15_jours', '40 % Acompte - Solde 15 jours')
    ], string='Conditions de paiement')


class Obligation(models.Model):
    _name = 'obligation.model'
    _description = 'Obligations related to contracts'
    _rec_name = 'name'

    name = fields.Char(string='Name', required=True)
    description = fields.Text(string='Description')
