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

import config
from scripts.utils.network_checks import NetworkValidations
from scripts.utils.pillar_get import PillarGet
from scripts.factory.server_check import ServerValidations
from scripts.factory.network_check import NetworkChecks
from scripts.factory.storage_check import StorageValidations
 

class_mapper = {
    'server_validation': ServerValidations,
    'netowrk_validation': NetworkChecks,
    'storage_validation': StorageValidations
}

class FactoryDeploymentValidations():
    ''' Validations for before and after of \
        Factory/Manufacturing Deployment
    '''

    def __init__(self):
        ''' Pre- and Post-flight Validations
        '''
        pass

    @staticmethod
    def factory_checks():
        check_list = config.FACTORY_POST_CHECK
        for check, cls in check_list.items():
            res = getattr(class_mapper[cls], check)()
            if res:
               if res['ret_code']:
                   print(f"{check}: Failed : {res['message']}")
                   #print(f"Response: {res}")
               else:
                   print(f"{check}: Success : {res['message']}")
                   

FactoryDeploymentValidations.factory_checks()
