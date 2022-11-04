from openerp import models, fields, api




class UserStory(models.Model):
    
    _name = 'user.story'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'portal.mixin']
    
    name = fields.Char(string="Name of story")
    project = fields.Many2one('project.project',string="Project")
    description = fields.Text(string="Description of story")
    partner_id = fields.Many2one('res.partner',string="Investor",require=True)
    stage_id = fields.Many2one('project.task.type',string="Stage")
    image = fields.Binary(string="Image",related="project.image")
    image_medium = fields.Binary(related="project.image_medium")
    image_small = fields.Binary(related="project.image_small")
    stage_id = fields.Many2one('user.story.stage',string='Stage')
    kanban_state = fields.Selection([
        ('normal', 'Grey'),
        ('done', 'Green'),
        ('blocked', 'Red')], string='Kanban State',
        copy=False, default='normal', required=True,
        help="A task's kanban state indicates special situations affecting it:\n"
             " * Grey is the default situation\n"
             " * Red indicates something is preventing the progress of this task\n"
             " * Green indicates the task is ready to be pulled to the next stage")
    
    
    
    @api.one
    def write(self,values):
        if 'uid' in self._context.keys():
            values.update({'partner_id':self.env['res.users'].sudo().search([('id','=',self._context['uid'])]).partner_id.id})
        res = super(UserStory,self).write(values)
        return res
        
    @api.model
    def create(self,values):
        values.update({'partner_id':self.env['res.users'].sudo().search([('id','=',self._context['uid'])]).partner_id.id})
        project_object = self.env['project.project'].search([('id','=',values['project'])])
        res = super(UserStory,self).create(values)
        res.message_subscribe([project_object.user_id.partner_id.id],subtype_ids=[])
        return res
    
class UserStoryStage(models.Model):
    
    _name = 'user.story.stage'
    
    name = fields.Char(string="Name of stage")
    description = fields.Char('Description')
    
    