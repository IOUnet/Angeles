from odoo import models, fields, api, SUPERUSER_ID
#from odoo.addons.test_impex.models import compute_fn
#from odoo import SUPERUSER_ID


class ProjectInvestingInformation(models.Model):
    
    _inherit = 'project.project'
   # _name = 'project.DARFproject'
    
    project_token = fields.Char(string="Project token address")  # +
    project_token_name = fields.Char(string="Token name")
    project_token_symbol = fields.Char(string="Token symbol")  # todo - real term instead code?
    project_owner_address = fields.Char(string="Project owner address")  # +
    project_address = fields.Char(string="Address for token selling")
    #addr_CN_argeement = fields.Char(string="Project convertible note agreement address")
    DARF_system_address =  fields.Char(string="DARF system address")  # +
    DFS_Project_describe = fields.Char(string="Project description address in DFS")
    DFS_type = fields.Char(string="Type of DFS used")  # todo, now just IPFS
    buy_back_address = fields.Char(string="Buy back address")
    abi_buy_back = fields.Char(string="ABI smart contract")
    crowd_sale_addr = fields.Char(string="Address of crowd sale contract")
    crowd_sale_abi = fields.Char(string="ABI crowd sale contract")

    smart_contracts = fields.One2many('project.smartcontracts', 'project_id', string="Project smart contracts addresses", index = True)

    # addition fields for project card

    token_amount = fields.Float(string="Token Amount")
    exchange_rate = fields.Float(string="Exchange Rate")
    exchange_price = fields.Float(string="Exchange price")
    tokens_price = fields.Float(string="Token's Price")
    

    #
    #passport of project
    description = fields.Text(string="Descriprion")
    image = fields.Binary(string="Image ICO")
    image_medium = fields.Binary()
    image_small = fields.Binary()

    #market
    market_size = fields.Float(string="Market size")
    cagr = fields.Float(string="Compound Annual Growth Rate (CAGR)")
    planned_share_market = fields.Float(string="Planned share of the market")
    market = fields.Text(string="Market")
    presentation = fields.Char(string = "Link to presentation")

    #Technology
    technology = fields.Text(string="Technology")
    patents = fields.Text(string = "Link(s) to scans of patents, other IP")
    review = fields.Text(string = "Links to expert's reviews")
    other_level_proofs = fields.Text (string = "Links to proofs of project's level")

    #finance
    total_investment = fields.Float(string="Total investment")
    finance_description = fields.Text(string="Description")
    open_close_for_investment = fields.Boolean()
    forms_of_investment = fields.Selection([('bootstraping', 'bootstraping'), 
                                            ('Angels', 'Angels investments'), 
                                            ('vc', 'Venture Funds'), 
                                            ('crowdinvesting', 'Crowd Investing'), 
                                            ('DAICO', 'daico')],
    string="Forms of investment")  # todo add VC, angels forms
    investment_condition = fields.Text(string="Investment conditions")
    term_and_condition = fields.Text(string="Finance terms & Conditions")
    round_of_investment = fields.One2many('round.investment', 'project_id', string="Rounds of investment")
    areas_of_investment = fields.Many2many('area.of.investment', string="Select area of project")
    annual_revenue = fields.Float(string = "Annual revenue")
    business_plan = fields.Char(string = "Link to business plan")
    

    #Legal issues
    legal_issues = fields.Text(string="Legal Issues")
    moderator_check = fields.Boolean(string="test",compute = "_moderator_check")
    publish_on_web = fields.Boolean(string="Publish on WEB")

    website_url = fields.Char(string="Website of project")
    #  Team
    project_team = fields.One2many('project.team','project_id',string="Project Team")

    #
    #states

    project_states = fields.One2many('project.states', 'project_id', string="Project states ")

    def _moderator_check(self):
        if SUPERUSER_ID == self._uid:
            self.moderator_check = True
        else:
            self.moderator_check = False
         
    


class ProjectTeam(models.Model):
    
    _name='project.team'
    
    project_id = fields.Many2one('project.project')
    team_mamber = fields.Many2one('res.partner',string="Team member")


class RoundInvestment(models.Model):
    
    _name = 'round.investment'
    
    project_id = fields.Many2one('project.project')
    name_of_round = fields.Many2one('round.of.investment',string="Name of round")
    start_date = fields.Date(string="Start round of investing") 
    end_date = fields.Date(string="End round of investing")
    min_amount = fields.Float(string="Minimal amount")
    max_amount = fields.Float(string="Max amount")
    
#Area of investment class    
class AreaOfInvestment(models.Model):
    
    _name = 'area.of.investment'
    
    name = fields.Char(string="Name of area")
    description = fields.Text(string="Description")
    category = fields.Many2one('area.of.investment.category', require = True)


#Category of area of investment   
class AreaOfInvestmentCategory(models.Model):
    
    _name = 'area.of.investment.category'
    
    name = fields.Char(string="Name of category")
    
    
class RaundOfInvestment(models.Model):
    
    _name = 'round.of.investment'
    
    name = fields.Char(string="Name of Round")
    description = fields.Text(string="Description")
      
class ProjectStates(models.Model):

    _name = 'project.states'
    project_id = fields.Many2one('project.project')

    DFS_changes_addr  = fields.Char(string="Address of changes in DFS")
    DFS_changes_hash =  fields.Char(string="Address of hash of changes in DLT")
    # DFS_type = fields.Char(string="Type of DFS used") #todo, now just IPFS
    PoA_addr =  fields.Char(string="Address of Proof of Accounting in DFS")
    timestamp = fields.Datetime(string = "Timestamp od state")

class SmartContractsAdresses (models.Model): #adresses in
    _name = 'project.smartcontracts'
    project_id = fields.Many2one('project.project')
    smart_contract_name =  fields.Char(string="Name of smart contract")
    smart_contract_address = fields.Char(string="Address of smart contract")
    smart_contract_ABI = fields.Char(string="ABI of smart contract")


class DarfConfig (models.Model):

    _inherit = "res.config.settings"
    _name = "darfsystem.config"

    DARF_system_address =  fields.Char(string="DARF system address") # +
    DLT_type = fields.Char(string="Type of DLT used") #todo, now just ETH
    DLT_node_address_port = fields.Char(string="Distributed ledgeg (DLT) node address:port")
    withdraw_address = fields.Char(string="Withdraw contract address")
    withdraw_ABI = fields.Char(string="ABI Withdraw  contract")
    ANG_sale_addr = fields.Char(string="Address of crowd sale contract")
    ANG_sale_ABI = fields.Char(string="ABI crowd sale contract")
    external_storage_addr = fields.Char(string="External storage address")
    external_storage_ABI = fields.Char(string="ABI of external storage ")

# docker exec odooweb /usr/bin/python3 /usr/bin/odoo --db_host 172.17.0.2 --db_port 5432 --db_user odoo --db_password odoo -d darfchain -u darfproject --xmlrpc-port=9999