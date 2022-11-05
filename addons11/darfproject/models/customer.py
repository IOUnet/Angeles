from openerp import models, fields, api




class UserInvestment(models.Model):
    
    _inherit = 'res.users'
    
    @api.model
    def create(self,values):
        test_of_project = False
        if 'project' in values.keys():
            if values['project']:
                project_creation_dict = {
                    'name':values['project_name'],
                    'market_size':values['market_size'],
                    'cagr':values['cagr'],
                    'planned_share_market':values['planned_share_market'],
                    'market':values['market'],
                    'technology':values['technology'],
                    'total_investment':values['total_investment'],
                    'finance_description':values['finance_description'],
                    }
                print(project_creation_dict)
                #del values['areas']
                del values['project_name']
                del values['market_size']
                del values['cagr']      
                del values['planned_share_market']
                del values['market']
                del values['technology']
                del values['total_investment']
                del values['finance_description']
                print('test of values user create')
                print(values)
                test_of_project = True
            else:
                pass
        else:
            pass
                
        res = super(UserInvestment,self).create(values)
        if 'investor' in values.keys() and test_of_project is False:
            if values['investor']:
                pass
#                 group_project = self.env['res.groups'].search([('category_id.name','=','Project')])
#                 for item_group in group_project:
#                     try:
#                         item_group.write({'users':[(3,res.id)]}) 
#                     except:
#                         pass
        if 'project' in values.keys():
            if values['project']:
                project_creation_dict.update({'user_id':res.id,
                                              'partner_id':res.partner_id.id,
                                              'privacy_visibility':'portal'})
                project_res = self.env['project.project'].create(project_creation_dict)
        return res 
            
class CustomerInvestment(models.Model):
    
    _inherit = 'res.partner'
    
    investment_list = fields.One2many('customer.investment.list', 'customer_id', string="Customer's investment")
    ethereum_address = fields.Char(string="Ethereum address")
    use_ethereum_address_for_login = fields.Boolean(string="Use ethereum address for login")
    bitcoin_address = fields.Char(string="Bitcoin address")
    investor = fields.Boolean(string="Is investor")
    project = fields.Boolean(string="Is project")
    area_of_investment = fields.Many2many('area.of.investment',string="Areas of investment")
    stage_investing = fields.Many2many('stage.of.investing',string="Stage of investment")
    date_birth = fields.date(string="Day of Birth")
    state =  fields.Char(string="State of birth")
    citizenship = fields.Char(string="Citizenship")
    personal_inn = fields.Char(string="Personal tax ID")
    living_address =  fields.Char(string="Address of living")
    gender = fields.Char(string="Gender")
    phone_number = fields.Char(string="Phone Number")
    education_school = fields.Char(string="Finished school or college or univercity ") #TODO make import from dictionary
    education_year = fields.Number(string="Year of completing") 
    education_speciality = fields.Char(string="Graduated speciality") #TODO make import from dictionary
    occupation = fields.Selection(                                
                                  [('business', 'Business'),
                                   ('entrepreneurship', 'Entrepreneurship'),
                                 ('self-employing', 'Self-employing'), 
                                 ('employing', 'Employing'),  
                                 ('student', 'Student') ], string="Occupation " ) 
    work_experience = fields.Number(string="Years of experience") 
    skills = fields.Text(string="Professional skills")
    achievements = fields.Text(string="Professional achievements")
    resume_portfolio = fields.Text(string="Link(s) to CV, portfolio, Github, etc")
    have_team = fields.Boolean(string="Have a team?")
    team_role = fields.Char(string="Role in team")
    have_intellectual_property = fields.Boolean(string="Have a patents or over IP?")
    patents =  fields.Char(string="Refs to patents, other IP ")
    have_company = fields.Boolean(string="Have a company?")
    company_inn = fields.Char(string="Company tax ID")
    
    #todo add KYC fields here and in views
    # document_type
    # document_number
    # document_date_issue
    # document_authority_issue
    # postal_address
    # DFS_type
    # DFS_address_document
    # DFS_address_selfy_with_doc
    # DFS_address_bank_receipt
    # DFS_address_selfy_with_bank_rec

    
    @api.model
    def create(self,values):
        res = super(CustomerInvestment,self).create(values)
        return res
    

class CustomerInvestmentList(models.Model):
    
    _name = 'customer.investment.list'
    
    project_of_invest = fields.Many2one('project.project')
    customer_id = fields.Many2one('res.partner')
    project_customer_token_amount = fields.Float(string="Amount of tokens")
    