##############################################################################
# Copyright (c) 2024 braintec AG (https://braintec.com)
# All Rights Reserved
#
# Licensed under the AGPL-3.0 (http://www.gnu.org/licenses/agpl.html).
# See LICENSE file for full licensing details.
##############################################################################
from odoo import models, fields


class ResPartnerRelationType(models.Model):
    _inherit = 'res.partner.relation.type'

    cla_imputed_ok = fields.Boolean(
        'Use for CLA Imputed?',
        default=False,
    )
