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
    investor = fields.Boolean(string="Инвестор")
    project = fields.Boolean(string="Участник")
    area_of_investment = fields.Many2many('area.of.investment',string="Область инвестирования")
    stage_investing = fields.Many2many('stage.of.investing',string="Раунды инвестирования")
    full_name =  fields.Char(string="Фамилия, имя, отчество ")
    date_birth = fields.Date(string="Дата рождения")
    state =  fields.Char(string="Страна проживания")
    citizenship = fields.Char(string="Гражданство ")
    living_address =  fields.Char(string="Адрес проживания")
    personal_inn = fields.Char(string="Персональный ИНН")
    gender = fields.Char(string="Пол")
    phone_number = fields.Char(string="Контактный номер телефона")
    education_school = fields.Char(string="Что заканчивали? ") #TODO make import from dictionary
    education_year = fields.Integer(string="Когда заканчивали") 
    education_speciality = fields.Char(string="Специальность по диплому") #TODO make import from dictionary
    occupation = fields.Selection(                                
                                  [('business', 'Собственный бизнес'),
                                   ('entrepreneurship', 'Предприниматель'),
                                 ('self-employing', 'Самозанятый'), 
                                 ('employing', 'Работа по найму'),  
                                 ('student', 'Обучение') ], string="Род занятий " ) 
    work_experience = fields.Integer(string="Опыт работы") 
    skills = fields.Text(string="авыки (например, технологии - SQL,Data Science, коптеры)")
    achievements = fields.Text(string="Достижения / Профессиональный опыт")
    resume_portfolio = fields.Text(string="Резюме / Портфолио  - файл / ссылка / Профиль Github / Профиль LinkedIn")
    have_team = fields.Char(string="Название команды")
    team_role = fields.Char(string="Роль в команде")
    have_intellectual_property = fields.Boolean(string="Являетесь ли автором объектов интеллектуальной собственности (есть ли патент)?")
    patents =  fields.Text(string="Ссылки на патенты, свидетельства, и т.д.")
    have_company = fields.Boolean(string="Есть ли юр.лицо")
    company_inn = fields.Char(string="ИНН юр.лица")
    
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
    