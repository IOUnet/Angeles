# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import logging
import base64
import datetime
from pprint import pprint

from odoo import http, _
from odoo.exceptions import AccessError
from odoo.http import request
from odoo.tools import consteq
from odoo.addons.portal.controllers.mail import _message_post_helper
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager, get_records_pager
from ast import literal_eval
from odoo.addons.auth_signup.controllers.main import AuthSignupHome
from odoo.addons.website.controllers.main import Website
import werkzeug
from odoo.addons.auth_signup.models.res_users import SignupError
from odoo.exceptions import UserError
# odoo.addons.darfproject.
#from controllers.web3_controller import Invoke_smart_contract
#from web3 import Web3

_logger = logging.getLogger(__name__)


class Website(Website):
    @http.route(auth='public')
    def index(self, data={}, **kw):
        super(Website, self).index(**kw)
        projects_list = request.env['project.project'].sudo().search([], order="create_date desc")
        project_list = []
        project_item_dict = {}
        # if request.env.user.partner_id:
        #    partner = request.env.user.partner_id
        for project_item in projects_list:
            # projects_customer = request.env['customer.investment.list'].search([('customer_id','=',partner.id),
            # 'project_token_amount':projects_customer.project_customer_token_amount,
            # ('project_of_invest','=',project_item.id)])
            project_item_dict.update({'project_name': project_item.name,
                                      'project_token_name': project_item.project_token_name,
                                      'token_amount': project_item.token_amount,
                                      'id': project_item.id,
                                      'project': project_item,
                                      'publish_on_web': project_item.publish_on_web,
                                      })
            project_list.append(project_item_dict)
            project_item_dict = {}
            data.update({'projects': project_list})
        return http.request.render('darfproject.homepage_projects', data)


class AuthSignupHome(AuthSignupHome):

    def _signup_with_values(self, token, values):
        print(values)
        qcontext = request.params.copy()
        print(qcontext)
        if qcontext.get('investor', False):
            values.update(investor=True)
            values.update(ethereum_address=qcontext.get('investor_address', False))
            list_of_areas = []
            list_of_stage = []
            for item_of_qcontext in qcontext.keys():
                if item_of_qcontext.split('-')[0] == 'treeselect':
                    if qcontext[item_of_qcontext].split('_')[0] == 'area':
                        list_of_areas.append(int(qcontext[item_of_qcontext].split('_')[1]))
                    if qcontext[item_of_qcontext].split('_')[0] == 'stage':
                        list_of_stage.append(int(qcontext[item_of_qcontext].split('_')[1]))
            values.update(area_of_investment=[(6, 0, list_of_areas)])
            values.update(stage_investing=[(6, 0, list_of_stage)])
        if qcontext.get('project', False):
            values.update(project=True)
            project_name = qcontext.get('project_name', False)
            # insert in values parameters for project creationg
            values.update(project_name=project_name)
            values.update(market_size=qcontext.get('market_size'))
            values.update(cagr=qcontext.get('cagr'))
            values.update(planned_share_market=qcontext.get('planned_share_market'))
            values.update(market=qcontext.get('market'))
            values.update(technology=qcontext.get('technology'))
            values.update(total_investment=qcontext.get('total_investment'))
            values.update(finance_description=qcontext.get('finance_description'))
        return super(AuthSignupHome, self)._signup_with_values(token, values)

    @http.route('/web/signup', type='http', auth='public', website=True, sitemap=False)
    def web_auth_signup(self, *args, **kw):
        qcontext = self.get_auth_signup_qcontext()

        if not qcontext.get('token') and not qcontext.get('signup_enabled'):
            raise werkzeug.exceptions.NotFound()

        if 'error' not in qcontext and request.httprequest.method == 'POST':
            try:
                self.do_signup(qcontext)
                # Send an account creation confirmation email
                if qcontext.get('token'):
                    user_sudo = request.env['res.users'].sudo().search([('login', '=', qcontext.get('login'))])
                    template = request.env.ref('auth_signup.mail_template_user_signup_account_created',
                                               raise_if_not_found=False)
                    if user_sudo and template:
                        template.sudo().with_context(
                            lang=user_sudo.lang,
                            auth_login=werkzeug.url_encode({'auth_login': user_sudo.email}),
                            password=request.params.get('password')
                        ).send_mail(user_sudo.id, force_send=True)
                return super(AuthSignupHome, self).web_login(*args, **kw)
            except UserError as e:
                qcontext['error'] = e.name or e.value
            except (SignupError, AssertionError) as e:
                if request.env["res.users"].sudo().search([("login", "=", qcontext.get("login"))]):
                    qcontext["error"] = _("Another user is already registered using this email address.")
                else:
                    _logger.error("%s", e)
                    qcontext['error'] = _("Could not create a new account.")
        get_area_of_investing = request.env['area.of.investment'].sudo().search([])
        get_area_of_investing_category = request.env['area.of.investment.category'].sudo().search([])
        get_stage_investing = request.env['stage.of.investing'].sudo().search([])

        qcontext.update({'areas': get_area_of_investing,
                         'categories': get_area_of_investing_category,
                         'stage_invest': get_stage_investing})

        response = request.render('auth_signup.signup', qcontext)
        response.headers['X-Frame-Options'] = 'DENY'
        return response


class CustomerPortal(CustomerPortal):

    def _prepare_portal_layout_values(self):
        values = super(CustomerPortal, self)._prepare_portal_layout_values()
        partner = request.env.user.partner_id
        projects = request.env['customer.investment.list'].search([('customer_id', '=', partner.id)])
        projects_list = request.env['project.project'].sudo().search([])
        projects_customer_list = []
        if projects:
            for project_item in projects:
                project_item_dic = {}
                project_item_dic.update({'project_name': project_item.project_of_invest.name,
                                         'project_token_name': project_item.project_of_invest.project_token_name,
                                         'token_amount': project_item.project_of_invest.token_amount,
                                         'project_token_amount': project_item.project_customer_token_amount,
                                         'id': project_item.project_of_invest.id,
                                         'publish_on_web': project_item.publish_on_web,
                                         })
                projects_customer_list.append(project_item_dic)
        else:
            project_item_dic = {}
        values.update({
            'projects': projects_customer_list,
        })
        project_list = []
        project_item_dict = {}
        for project_item in projects_list:
            projects_customer = request.env['customer.investment.list'].search([('customer_id', '=', partner.id),
                                                                                ('project_of_invest', '=',
                                                                                 project_item.id)])
            project_item_dict.update({'project_name': project_item.name,
                                      'project_token_name': project_item.project_token_name,
                                      'token_amount': project_item.token_amount,
                                      'project_token_amount': projects_customer.project_customer_token_amount,
                                      'id': project_item.id,
                                      'project': project_item,
                                      'publish_on_web': project_item.publish_on_web,
                                      })
            project_list.append(project_item_dict)
            project_item_dict = {}

        values.update({'projects_list': project_list})
        return values

    @http.route(['/my/home/project/<int:project>'], type='http', auth="public", website=True)
    def project_page(self, project, **kw):
        project = request.env['project.project'].browse([project])
        project_sudo = project.sudo()
        partner = request.env.user.partner_id
        return request.render("darfproject.project_page", {
            'project': project_sudo,
        })

    @http.route(['/my/home/projectsboard'], type='http', auth="user", website=True)
    def project_board(self, **kw):
        project = request.env['project.project'].sudo().search([])
        project_sudo = project.sudo()
        partner = request.env.user.partner_id
        project_list = []
        project_item_dict = {}
        for project_item in project:
            projects_customer = request.env['customer.investment.list'].search([('customer_id', '=', partner.id),
                                                                                ('project_of_invest', '=',
                                                                                 project_item.id)])
            project_item_dict.update({'project_name': project_item.name,
                                      'project_token_name': project_item.project_token_name,
                                      'token_amount': project_item.token_amount,
                                      'project_token_amount': projects_customer.project_customer_token_amount,
                                      'id': project_item.id,
                                      'project': project_item,
                                      'publish_on_web': project_item.publish_on_web,
                                      })
            project_list.append(project_item_dict)
            project_item_dict = {}

        return request.render("darfproject.projects_board", {
            'projects': project_list,
        })

    @http.route(['/my/home/invest/<int:project>'], type='http', auth="user", website=True)
    def project_invest(self, project, **kw):
        project = request.env['project.project'].browse([project])
        project_sudo = project.sudo()
        partner = request.env.user.partner_id
        return request.render("darfproject.project_invest", {
            'project': project_sudo,
        })

    @http.route(['/my/home/setting'], type='http', auth="user", website=True)
    def customer_setting(self, **kw):
        partner = request.env.user.partner_id
        return request.render("darfproject.customer_setting", {
            'customer': partner,
        })

    @http.route(['/web/condition'], type='json', auth="user", website=True)
    def buy_condition(self, project_id, token_value, **kw):
        partner = request.env.user.partner_id
        return True

    @http.route(['/web/buytoken'], type='json', auth="user", website=True)
    def buy_tokens(self, project_id, accept, token_value, **kw):
        partner = request.env.user.partner_id
        project_id = int(project_id)
        get_list = request.env['customer.investment.list'].search(
            [('customer_id', '=', partner.id), ('project_of_invest', '=', project_id)])
        if get_list:
            token_value = get_list.project_customer_token_amount + int(token_value)
            get_list.write({'project_customer_token_amount': token_value})
        else:
            dict_for_write = {'project_of_invest': project_id,
                              'project_customer_token_amount': token_value}
            partner.write({'investment_list': [(0, 0, dict_for_write)]})
        return True

    @http.route(['/my/home/condition/<int:project_id>/<int:token_value>'], type='http', auth="user", website=True)
    def buy_condition_page(self, project_id, token_value, **kw):
        partner = request.env.user.partner_id
        project = request.env['project.project'].browse([project_id])
        return request.render("darfproject.term_and_condition", {
            'project': project,
            'token_value': token_value,
        })

    #    @http.route(['/my/home/mint_token/<int:project>'], type='http', auth="public", website=True) #todo auth = user
    @http.route(['/my/home/mint/<int:project>'], type='http', auth="user", website=True)
    def project_mint_token(self, project, **kw):
        project = request.env['project.project'].browse(project)
        project_sudo = project.sudo()
        return request.render("darfproject.mint_token", project_sudo
                              # { 'project': project_sudo}
                              )

    @http.route(['/my/home/start_minting/<int:project>'], type='http', auth="user", website=True)
    def project_start_mint_token(self, project, **kw):
        project = request.env['project.project'].browse([project])
        project_sudo = project.sudo()
        return request.render("darfproject.mint_token", project_sudo
                              # { 'project': project_sudo}
                              )

    @http.route(['/my/home/buy_ANG'], type='http', auth="user", website=True)
    def buy_ang(self, **kw):
        project = request.env.project #['project.project'].sudo().search([])
        #_ir = request.env['ir.default']

        #sellANGETH_addr = Web3.toChecksumAddress(_ir['ANG_sale_addr'])  #
        #
        # from project
        #beneficiar_addr = Web3.toChecksumAddress(request.env.user.partner_id.ethereum_address)  # from profile
       # _req = request.params.copy()
       # summ_buy = Web3.toInt(_req.get('amount', False))
       # discount_password = _req.get('discount_password', False)  # from request

#        sellANGETH_ABI = _ir['ANG_sale_ABI']

        #        _buy_ang_smart_contract = web3.contract(address=sellANGETH_addr,  abi=sellANGETH_ABI)
  #      if (discount_password):
            #return #Invoke_smart_contract(sellANGETH_addr, sellANGETH_ABI).functions.sell_discount(beneficiar_addr, summ_buy,     discount_password).transact()
        #else:
        #    return #Invoke_smart_contract(sellANGETH_addr, sellANGETH_ABI).functions.sellANGETH(beneficiar_addr, summ_buy).transact()

            # call({'beneficiar': beneficiar_addr, 'summa':summ_buy})

    #
    @http.route(['/admin/ETH_chain_system'], type='http', auth="user", website=True)  # todo: auth="admin"
    def configs_ETH_chain(self, **kw):
        return request.render("darfproject.admin_ETH_chain_system",
                      {"DARF_system_address": request.registry.models["darfsystem.config"]["DARF_system_address"],
                       "DLT_node_address_port": request.registry.models["darfsystem.config"]["DLT_node_address_port"]
                       } )

    @http.route(['/admin/save_eth_conf'], type='http', auth="user", website=True)  # todo: auth="admin"
    def save_configs_ETH_chain(self, **kw):
        _req = request.params.copy()
        request.registry.models["darfsystem.config"] = _req
        print("data saved")
        return request.render("darfproject.admin_ETH_chain_system",
                              request.registry.models["darfsystem.config"]
                              )
