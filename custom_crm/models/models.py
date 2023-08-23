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
    products = fields.Many2many('product.product', string='Products')
    sale_order_template_id = fields.Many2one(
        comodel_name='sale.order.template',
        string="Quotation Template",
        check_company=True,
        domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]")

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
        ('100', '100%'),
        ('condition', 'Conditions chantiers')
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

    dossier_de_pose = fields.Boolean(string='Dossier de pose')
    mesure_par = fields.Selection([
        ('PROFENO', 'PROFENO'),
        ('CLIENT', 'CLIENT')
    ], string='Mesure par')
    mesureur = fields.Selection([
        ('JOBL', 'JOBL'),
        ('JB', 'JB'),
        ('RK', 'RK'),
        ('BA', 'BA'),
        ('SP', 'SP'),
        ('LD', 'LD'),
        ('FH', 'FH'),
        ('JK', 'JK')
    ], string='Mesureur')
    aide_pose_heure_fin = fields.Selection([
        ('00:00', '00:00'), ('00:30', '00:30'), ('01:00', '01:00'), ('01:30', '01:30'),
        ('02:00', '02:00'), ('02:30', '02:30'), ('03:00', '03:00'), ('03:30', '03:30'),
        ('04:00', '04:00'), ('04:30', '04:30'), ('05:00', '05:00'), ('05:30', '05:30'),
        ('06:00', '06:00'), ('06:30', '06:30'), ('07:00', '07:00'), ('07:30', '07:30'),
        ('08:00', '08:00'), ('08:30', '08:30'), ('09:00', '09:00'), ('09:30', '09:30'),
        ('10:00', '10:00'), ('10:30', '10:30'), ('11:00', '11:00'), ('11:30', '11:30'),
        ('12:00', '12:00'), ('12:30', '12:30'), ('13:00', '13:00'), ('13:30', '13:30'),
        ('14:00', '14:00'), ('14:30', '14:30'), ('15:00', '15:00'), ('15:30', '15:30'),
        ('16:00', '16:00'), ('16:30', '16:30'), ('17:00', '17:00'), ('17:30', '17:30'),
        ('18:00', '18:00'), ('18:30', '18:30'), ('19:00', '19:00'), ('19:30', '19:30'),
        ('20:00', '20:00'), ('20:30', '20:30'), ('21:00', '21:00'), ('21:30', '21:30'),
        ('22:00', '22:00'), ('22:30', '22:30'), ('23:00', '23:00'), ('23:30', '23:30')
    ], string='Aide pose Heure Fin')
    remarques_chantier = fields.Text(string='Remarques chantier')
    remarques_mesurage = fields.Text(string='Remarques mesurage')
    mesure_le = fields.Date(string='Mesuré le')
    aide_pose_heure_debut = fields.Selection([
        ('00:00', '00:00'), ('00:30', '00:30'), ('01:00', '01:00'), ('01:30', '01:30'),
        ('02:00', '02:00'), ('02:30', '02:30'), ('03:00', '03:00'), ('03:30', '03:30'),
        ('04:00', '04:00'), ('04:30', '04:30'), ('05:00', '05:00'), ('05:30', '05:30'),
        ('06:00', '06:00'), ('06:30', '06:30'), ('07:00', '07:00'), ('07:30', '07:30'),
        ('08:00', '08:00'), ('08:30', '08:30'), ('09:00', '09:00'), ('09:30', '09:30'),
        ('10:00', '10:00'), ('10:30', '10:30'), ('11:00', '11:00'), ('11:30', '11:30'),
        ('12:00', '12:00'), ('12:30', '12:30'), ('13:00', '13:00'), ('13:30', '13:30'),
        ('14:00', '14:00'), ('14:30', '14:30'), ('15:00', '15:00'), ('15:30', '15:30'),
        ('16:00', '16:00'), ('16:30', '16:30'), ('17:00', '17:00'), ('17:30', '17:30'),
        ('18:00', '18:00'), ('18:30', '18:30'), ('19:00', '19:00'), ('19:30', '19:30'),
        ('20:00', '20:00'), ('20:30', '20:30'), ('21:00', '21:00'), ('21:30', '21:30'),
        ('22:00', '22:00'), ('22:30', '22:30'), ('23:00', '23:00'), ('23:30', '23:30')
    ], string='Aide pose Heure Début')
    attachment = fields.Binary(string='Attachement')
    attachment_filename = fields.Char(string='Attachment Filename')

    @api.model
    def create(self, values):
        lead = super(Lead, self).create(values)
        lead.update_sale_order_template()
        return lead

    def write(self, values):
        res = super(Lead, self).write(values)
        if 'partner_id' in values or 'products' in values:
            self.update_sale_order_template()
        return res

    def update_sale_order_template(self):
        for lead in self:
            if lead.partner_id and lead.products:
                if not lead.sale_order_template_id:
                    sale_order_template = self.env['sale.order.template'].create({
                        'name': f"Template for {lead.name}",
                        'sale_order_template_line_ids': [(0, 0, {'product_id': product.id}) for product in
                                                         lead.products],
                    })
                    lead.sale_order_template_id = sale_order_template.id
                else:
                    template_products = lead.sale_order_template_id.sale_order_template_line_ids.mapped('product_id')
                    new_products = lead.products - template_products
                    deleted_products = template_products - lead.products

                    for product in new_products:
                        lead.sale_order_template_id.sale_order_template_line_ids = [(0, 0, {'product_id': product.id})]

                    for product in deleted_products:
                        line_to_delete = lead.sale_order_template_id.sale_order_template_line_ids.filtered(
                            lambda line: line.product_id == product)
                        line_to_delete.unlink()


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.model
    def default_get(self, fields):
        res = super(SaleOrder, self).default_get(fields)
        if self.env.context.get('active_model') and self.env.context.get('active_model') == 'crm.lead':
            lead = self.env['crm.lead'].browse(self.env.context.get('active_id'))
            res['sale_order_template_id'] = lead.sale_order_template_id.id

        return res


class Obligation(models.Model):
    _name = 'obligation.model'
    _description = 'Obligations related to contracts'
    _rec_name = 'name'

    name = fields.Char(string='Name', required=True)
    description = fields.Text(string='Description')
