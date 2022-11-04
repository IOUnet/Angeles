# Web3 controller
# for Web3:
# apt-get update && apt install gcc python3.5-dev
#
#pip3 install web3
#workflow   https://www.draw.io/#G1yXU5Wpk7tX8-46XPNUB-CUb27HRQmbiy

#import openERP as odoo


import json
from odoo import http, _
from odoo.http import request

#from web3 import Web3, HTTPProvider, TestRPCProvider
#from solc import compile_source
#from web3.contract import ConciseContract
#import  web3
#from web3.eth import contract
#from web3.auto.infura import w3
#from web3.contract import ContractFunction
from web3 import Web3

from solc import compile_source
#from web3.contract import ConciseContract


# PROJECTSMARTCONTRACTNAME = 'scruminvest/project'

def _Invoke_smart_contract_func(smart_contract_function_addr, smart_contract_ABI, smart_contract_function_name):
    # todo: adopt to  SmartContractsAdresses ledger
    w3 = Web3(Web3.HTTPProvider("http://172.17.0.1:8545/"))
    w3.eth.defaultAccount = w3.eth.accounts[0]

    # https://web3py.readthedocs.io/en/stable/contracts.html#web3.contract.ContractFunction
    smart_contract = w3.eth.contract(address=smart_contract_function_addr,
                                     abi=smart_contract_ABI)  # globals()['web3.eth.contract']()

    return smart_contract.functions[smart_contract_function_name]
    # getattr(smart_contract, smart_contract_function_name ) #returns function in smartcontract

def Invoke_smart_contract(smart_contract_function_addr, smart_contract_ABI):

    # todo: adopt to  SmartContractsAdresses ledger
    w3 = Web3(Web3.HTTPProvider(request.env['ir.default']['DLT_node_address_port'], request_kwargs={'timeout': 60}))
    w3.eth.defaultAccount = w3.eth.accounts[0]

    # https://web3py.readthedocs.io/en/stable/contracts.html#web3.contract.ContractFunction
    smart_contract = w3.eth.contract(address=smart_contract_function_addr, \
                                     abi=smart_contract_ABI)  # globals()['web3.eth.contract']()

    return smart_contract
    # getattr(smart_contract, smart_contract_function_name ) #returns function in smartcontract


def Get_smart_contract_data (self, smartcontractname, project_id):
    project = request.env['project.project'].browse([project_id])

    return (project.smart_contracts[('smart_contract_name','=',\
                                     smartcontractname).smart_contract_address],\
                                     project.smart_contracts[('smart_contract_name','=',\
                                     smartcontractname).smart_contract_ABI] )



def Get_info_external_storage(self, variablename, variablefunction): #needs name of get* function in https://github.com/DARFChainTeam/Angeles.VC-token-scrum-investing/contracts/admin/implementation/externalstorage.sol
    (external_storage_addr, external_storage_ABI) = self.Get_smart_contract_data(
        'admin/implementation/externalstorage')

    return self._invoke_smart_contract(self, external_storage_addr, external_storage_ABI, variablefunction).call({'record': variablename})



def Set_info_external_storage(self, variablevalue, variablename, variablefunction): #needs name of set* function in https://github.com/DARFChainTeam/Angeles.VC-token-scrum-investing/contracts/admin/implementation/externalstorage.sol

    (external_storage_addr, external_storage_ABI) = \
            self.Get_smart_contract_data('admin/implementation/externalstorage')
    return self._invoke_smart_contract(self, external_storage_addr, external_storage_ABI,\
                                       variablefunction).call({'record': variablename,\
                                                               'value': variablevalue}) #todo need to control types!


def Create_project(self, project_id): #address Projecttokenaddr, bytes32 DFSProjectdescribe, bytes4 DFStype)
    project = request.env['project.project'].browse([project_id])
     # 0. why need checkrights? self.checkrights (project.project_token)

     # 1.transfer tokens to system

     # make page in DFS
    self.DFS_save (self, project.project_token)
    (smart_contract_function_addr, smart_contract_ABI ) = \
            self.Get_smart_contract_data ('scruminvest/project')
     # invoke create_project
    return self._Invoke_smart_contract(self, smart_contract_function_addr,\
                                smart_contract_ABI, 'create_project').\
                                call({'Projecttokenaddr': project.project_token,\
                                      'DFSProjectdescribe': project.DFS_Project_describe,\
                                      'DFStype':project.DFS_type    })


def Change_project_info(self):
    return
def  Finish_project  (self):
    return
def Project_add_state(self):
    return

def Project_get_state(self,project_token):
    return

def Set_rights(self):
    return

def Check_rights(self, token_address):


    return

def DFS_save(self, token_address):

    DFS_addr = 0x0 #mockup
    return DFS_addr
# token management
#todo add token management to menu, views


def Set_external_storage(smart_contract_addr, smart_contract_abi,external_storage_addr):
    Invoke_smart_contract(Web3.toChecksumAddress(smart_contract_addr),                      smart_contract_abi).functions._setExternalstorageaddr(
        Web3.toChecksumAddress(external_storage_addr)).transact()
#_setExternalstorageaddr(address Externalstorageaddr )
    return

def Init_smart_contract (smart_contract_addr, smart_contract_abi, external_storage_addr):
    # init procedure for smart contract

    #_initExternalStorage(address    Externalstorageaddr) public     onlyAdmins(msg.sender)
    Invoke_smart_contract(Web3.toChecksumAddress(smart_contract_addr), smart_contract_abi).functions._initExternalStorage(Web3.toChecksumAddress(external_storage_addr)).transact()

    # load_conditions_ES () ,- from function

    return