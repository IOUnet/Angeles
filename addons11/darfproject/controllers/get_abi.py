#from web3 import Web3
import sys
from solc import compile_source
#from web3.contract import ConciseContract

contract_name = sys.argv[1]
contract_path = sys.argv[2]
print(contract_name, contract_path )

with open(contract_path)  as contr:
    contract_source_code = contr.read()
    compiled_sol = compile_source(contract_source_code)  # Compiled source code
    contract_interface = compiled_sol['<stdin>:' + contract_name]
    print (contract_interface)






