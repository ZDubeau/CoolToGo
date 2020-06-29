class category():
    """ Merge all category """

    def __init__(self, request_json):
        self.__request_json = request_json
        self.__dict_id = {}

    # def __category_equip(self):
    #     self.__dict_id['Catégories_prestation_equipement'] = None
    #     if 'informationsEquipement' in self.__request_json:
    #         if 'activites' in self.__request_json['informationsEquipement']:
    #             category_equip = ''
    #             first = True
    #             for value in self.__request_json['informationsEquipement']['activitess']:
    #                 if 'libelleFr' in value:
    #                     if first:
    #                         category_equip += value['libelleFr']
    #                         first = False
    #                     else:
    #                         category_equip += ', ' + value['libelleFr']
    #             self.__dict_id['Catégories_prestation_equipement'] = category_equip

    def __category_resto(self):
        self.__dict_id['Catégories_restauration'] = None
        if 'informationsRestauration' in self.__request_json:
            if 'categories' in self.__request_json['informationsRestauration']:
                category_resto = ''
                first = True
                for value in self.__request_json['informationsRestauration']['categories']:
                    if 'libelleFr' in value:
                        if first:
                            category_resto += value['libelleFr']
                            first = False
                        else:
                            category_resto += ', ' + value['libelleFr']
                self.__dict_id['Catégories_restauration'] = category_resto

    def __category_commerce(self):
        self.__dict_id['Catégories_commerce'] = None
        if 'informationsCommerceEtService' in self.__request_json:
            if 'typesDetailles' in self.__request_json['informationsCommerceEtService']:
                category_commerce = ''
                first = True
                for value in self.__request_json['informationsCommerceEtService']['typesDetailles']:
                    if 'libelleFr' in value:
                        if first:
                            category_commerce += value['libelleFr']
                            first = False
                        else:
                            category_commerce += ', ' + value['libelleFr']
                self.__dict_id['Catégories_commerce'] = category_commerce

    def __category_manif(self):
        self.__dict_id['Catégories_fete_manifestation'] = None
        if 'informationsFeteEtManifestation' in self.__request_json:
            if 'categories' in self.__request_json['informationsFeteEtManifestation']:
                category_manif = ''
                first = True
                for value in self.__request_json['informationsFeteEtManifestation']['categories']:
                    if 'libelleFr' in value:
                        if first:
                            category_manif += value['libelleFr']
                            first = False
                        else:
                            category_manif += ', ' + value['libelleFr']
                self.__dict_id['Catégories_fete_manifestation'] = category_manif

    def __category_patriCtrl(delf):
        self.__dict_id['Catégories_patrimoine_culturel'] = None
        if 'informationsPatrimoineCulturel' in self.__request_json:
            if 'categories' in self.__request_json['informationsPatrimoineCulturel']:
                category_patri = ''
                first = True
                for value in self.__request_json['informationsPatrimoineCulturel']['categories']:
                    if 'libelleFr' in value:
                        if first:
                            category_patri += value['libelleFr']
                            first = False
                        else:
                            category_patri += ', ' + value['libelleFr']
                self.__dict_id['Catégories_patrimoine_culturel'] = category_patri

    def __category_patriNtrl(self):
        self.__dict_id['Catégories_patrimoine_naturel'] = None
        if 'informationsPatrimoineNaturel' in self.__request_json:
            if 'categories' in self.__request_json['informationsPatrimoineNaturel']:
                category_nature = ''
                first = True
                for value in self.__request_json['informationsPatrimoineNaturel']['categories']:
                    if 'libelleFr' in value:
                        if first:
                            category_nature += value['libelleFr']
                            first = False
                        else:
                            category_nature += ', ' + value['libelleFr']
                self.__dict_id['Catégories_patrimoine_naturel'] = category_nature

    def __category_activity(self):  # Prestations + Activités
        self.__dict_id['category_activity'] = None
        if 'informationsActivite' in self.__request_json:
            if 'categories' in self.__request_json['informationsActivite']:
                category_nature = ''
                first = True
                for value in self.__request_json['informationsActivite']['categories']:
                    if 'libelleFr' in value:
                        if first:
                            category_nature += value['libelleFr']
                            first = False
                        else:
                            category_nature += ', ' + value['libelleFr']

            if 'activitesSportives' in self.__request_json['informationsActivite']:
                sportif_activity = ''
                first = True
                for value in self.__request_json['informationsActivite']['activitesSportives']:
                    if 'libelleFr' in value:
                        if first:
                            sportif_activity += value['libelleFr']
                            first = False
                        else:
                            sportif_activity += ', ' + value['libelleFr']
                self.__dict_id['category_activity'] = category_nature + \
                    ', ' + sportif_activity
# ----------------------------------

    # def classement_patriNtrl(self):
    #     dict_for_id['classement_patri'] = None
    #     if 'informationsPatrimoineNaturel' in req:
    #         if 'classements' in req['informationsPatrimoineNaturel']:
    #             classment_pn = ""
    #             first = True
    #             for value in req['informationsPatrimoineNaturel']['classements']:
    #                 if 'libelleFr' in value:
    #                     if first:
    #                         classment_pn += value['libelleFr']
    #                         first = False
    #                     else:
    #                         classment_pn += ", " + value['libelleFr']
    #             dict_for_id['classement_patri'] = classment_pn

    def type_resto(self):
        dict_for_id['type_resto'] = None
        if 'informationsRestauration' in req:
            if 'restaurationType' in req['informationsRestauration']:
                if 'libelleFr' in req['informationsRestauration']['restaurationType']:
                    dict_for_id['type_resto'] = req['informationsRestauration']['restaurationType']['libelleFr']

    # def classement_equip(self):
    #     dict_for_id['Classement_equip'] = None
    #     if 'informationsEquipement' in req:
    #         if 'restaurationType' in req['informationsEquipement']:
    #             if 'libelleFr' in req['informationsRestauration']['restaurationType']:
    #                 dict_for_id['Classement_equip'] = req['informationsRestauration']['restaurationType']['libelleFr']

    def speciality_resto(self):
        dict_for_id['speciality'] = None
        if 'informationsRestauration' in req:
            if 'specialites' in req['informationsRestauration']:
                Specialité = ""
                first = True
                for value in req['informationsRestauration']['specialites']:
                    if 'libelleFr' in value:
                        if first:
                            Specialité += value['libelleFr']
                            first = False
                        else:
                            Specialité += ", " + value['libelleFr']
                dict_for_id['speciality'] = Specialité

    def type_manif(self):
        dict_for_id['type_manif'] = None
        if 'informationsFeteEtManifestation' in req:
            if 'typesManifestation' in req['informationsFeteEtManifestation']:
                type_manif = ''
                first = True
                for value in req['informationsFeteEtManifestation']['typesManifestation']:
                    if 'libelleFr' in value:
                        if first:
                            type_manif += value['libelleFr']
                            first = False
                        else:
                            type_manif += ', ' + value['libelleFr']
                dict_for_id['type_manif'] = type_manif

    def type_patriCtrl(self):
        dict_for_id['type_patriC'] = None
        if 'informationsPatrimoineCulturel' in req:
            if 'patrimoineCulturelType' in req['informationsPatrimoineCulturel']:
                if 'libelleFr' in req['informationsPatrimoineCulturel']['patrimoineCulturelType']:
                    dict_for_id['type_patriC'] = req['informationsPatrimoineCulturel']['patrimoineCulturelType']['libelleFr']

    def type_commerce(self):
        dict_for_id['type_commerce'] = None
        if 'informationsCommerceEtService' in req:
            if 'commerceEtServiceType' in req['informationsCommerceEtService']:
                if 'libelleFr' in req['informationsCommerceEtService']['commerceEtServiceType']:
                    dict_for_id['type_commerce'] = req['informationsCommerceEtService']['commerceEtServiceType']['libelleFr']

    def type_activity(self):
        dict_for_id['type_activity'] = None
        if 'informationsActivite' in req:
            if 'activiteType' in req['informationsActivite']:
                if 'libelleFr' in req['informationsActivite']['activiteType']:
                    dict_for_id['type_activity'] = req['informationsActivite']['activiteType']['libelleFr']

    def them_manif(self):
        dict_for_id['theme_manif'] = None
        if 'informationsFeteEtManifestation' in req:
            if 'themes' in req['informationsFeteEtManifestation']:
                Theme_manif = ''
                first = True
                for value in req['informationsFeteEtManifestation']['themes']:
                    if 'libelleFr' in value:
                        if first:
                            Theme_manif += value['libelleFr']
                            first = False
                        else:
                            Theme_manif += ', ' + value['libelleFr']
                dict_for_id['theme_manif'] = Theme_manif

    def them_patriCtrl(self):
        dict_for_id['Theme_ctrl'] = None
        if 'informationsPatrimoineCulturel' in req:
            if 'themes' in req['informationsPatrimoineCulturel']:
                theme_patriCtrl = ''
                first = True
                for value in req['informationsPatrimoineCulturel']['themes']:
                    if 'libelleFr' in value:
                        if first:
                            theme_patriCtrl += value['libelleFr']
                            first = False
                        else:
                            theme_patriCtrl += ', ' + value['libelleFr']
                dict_for_id['Theme_ctrl'] = theme_patriCtrl

    def activityCtrl(self):
        dict_for_id['activity_ctrl'] = None
        if 'informationsActivite' in req:
            if 'activitesCulturelles' in req['informationsActivite']:
                activityCtrl = ''
                first = True
                for value in req['informationsActivite']['activitesCulturelles']:
                    if 'libelleFr' in value:
                        if first:
                            activityCtrl += value['libelleFr']
                            first = False
                        else:
                            activityCtrl += ', ' + value['libelleFr']
                dict_for_id['activity_ctrl'] = activityCtrl

    def prestataire_activity(self):
        dict_for_id['prestataire'] = None
        if 'informationsActivite' in req:
            if 'prestataireActivites' in req['informationsActivite']:
                if 'nom' in req['informationsActivite']['prestataireActivites']:
                    if 'libelleFr' in req['informationsActivite']['prestataireActivites']['nom']:
                        dict_for_id['prestataire'] = req['informationsActivite']['prestataireActivites']['nom']['libelleFr']
            if 'prestataireActivites' is None:
                if 'commerceEtServicePrestataire' in req['informationsActivite']:
                    if 'nom' in req['informationsActivite']['commerceEtServicePrestataire']:
                        if 'libelleFr' in req['informationsActivite']['commerceEtServicePrestataire']['nom']:
                            dict_for_id['prestataire'] = req['informationsActivite']['commerceEtServicePrestataire']['nom']['libelleFr']

    def categorys(self):
        # self.__category_equip()
        self.__category_resto()
        self.__category_commerce()
        self.__category_manif()
        self.__category_patri_culturel()
        self.__category_patri_naturel()
        self.__category_activity()

    def dict_id(self):
        return self.__dict_id
