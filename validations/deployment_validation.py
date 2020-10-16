#
# Copyright (c) 2020 Seagate Technology LLC and/or its Affiliates
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.
# For any questions about this software or licensing,
# please email opensource@seagate.com or cortx-questions@seagate.com.
#

# This is the Main Class or 
# Registry file which will make a call to 
# All the other validate functions


from scripts.utils.network_checks import NetworkValidations
from scripts.utils.pillar_get import PillarGet
from scripts.factory.server_check import ServerValidations
from scripts.factory.network_check import NetworkChecks
 
class FactoryDeploymentValidations():
    ''' Validations for before and after of \
        Factory/Manufacturing Deployment
    '''

    def __init__(self):
        ''' Pre- and Post-flight Validations
        '''
        pass

    #list_of_functions_to_be_validated
    #checks_to_validate = [func_1(), func_2()]
    #res = NetworkChecks.verify_mgmt_vip()
    #print(res)
    res = NetworkChecks.verify_private_data_ip()
    print(res)
    #res = PillarGet.get_pillar("cluster:node_list")
    #print(type(res['response']))
